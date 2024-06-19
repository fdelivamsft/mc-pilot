import logging
from typing import List
import json

from .orchestrator_base import OrchestratorBase
from ..helpers.llm_helper import LLMHelper
from ..tools.post_prompt_tool import PostPromptTool
from ..tools.campaign_influencer_tool import CampaignInfluencerTool
from ..tools.text_processing_tool import TextProcessingTool
from ..tools.greetings_tool import GreetingsProcessingTool
from ..tools.brief_tool import BriefTool
from ..common.answer import Answer

logger = logging.getLogger(__name__)


class InstagramFunctionsOrchestrator(OrchestratorBase):
    def __init__(self) -> None:
        super().__init__()
        self.functions = [
            {
                "name": "greetings",
                "description": "How to answer when the user is saying hello or asking more info on how this product works",
                "parameters": {}
            },
            {
                "name": "search_documents",
                "description": "Search for similar campaigns or influencer performance in the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "A standalone question, converted from the chat history",
                        },
                        "campaignKeywords": {
                            "type": "string",
                            "description": "a list of relevant keywords describing the campaign the user is searching",
                        },
                        "industry": {
                            "type": "string",
                            "description": "The campaign industry, it can be one between: banking, health, toys, baby, sports. Please keep it lowercase.",
                        },
                        "instagram": {
                            "type": "string",
                            "description": "The instagram handler of the influencer mentioned",
                        },
                        "searchType": {
                            "type": "string",
                            "enum":["influencer","campaign"],
                            "description": "Select influencer if the user is searching an influencer or camapign if the user is looking for similar campaign",
                        },
                    },
                    "required": ["question","campaignKeywords","industry","instagram","searchType"],
                },
            },
            {
                "name": "text_processing",
                "description": "Useful when you want to apply a transformation on the text, like translate, summarize, rephrase and so on.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to be processed",
                        },
                        "operation": {
                            "type": "string",
                            "description": "The operation to be performed on the text. Like Translate to Italian, Summarize, Paraphrase, etc. If a language is specified, return that as part of the operation. Preserve the operation name in the user language.",
                        },
                    },
                    "required": ["text", "operation"],
                },
            },
            {
                "name": "brief",
                "description": "Useful when you need to analyze an advertisment brief for a campaign",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "campaign": {
                            "type": "string",
                            "description": "campaign info",
                        }
                    },
                    "required": ["campaign"],
                },
            },
        ]

    async def orchestrate(
        self, user_message: str, chat_history: List[dict], **kwargs: dict
    ) -> list[dict]:
        # Call Content Safety tool
        if self.config.prompts.enable_content_safety:
            if response := self.call_content_safety_input(user_message):
                return response

        # Call function to determine route
        llm_helper = LLMHelper()

        system_message = """You help employees to navigate only private information sources.
        You must prioritize the function call over your general knowledge for any question by calling the search_documents function.
        Call the text_processing function when the user request an operation on the current context, such as translate, summarize, or paraphrase. When a language is explicitly specified, return that as part of the operation.
        Call the brief function when the user provide a campaign brief.
        When directly replying to the user, always reply in the language the user is speaking.
        """
        # Create conversation history
        messages = [{"role": "system", "content": system_message}]
        for message in chat_history:
            messages.append({"role": message["role"], "content": message["content"]})
        messages.append({"role": "user", "content": user_message})

        result = llm_helper.get_chat_completion_with_functions(
            messages, self.functions, function_call="auto"
        )
        self.log_tokens(
            prompt_tokens=result.usage.prompt_tokens,
            completion_tokens=result.usage.completion_tokens,
        )

        # TODO: call content safety if needed

        if result.choices[0].finish_reason == "function_call":
            logger.info("Function call detected")
            if result.choices[0].message.function_call.name == "search_documents":
                logger.info("search_documents function detected")
                question = json.loads(
                    result.choices[0].message.function_call.arguments
                )["question"]


                try:
                    campaignKeywords = json.loads(result.choices[0].message.function_call.arguments)[
                        "campaignKeywords"
                    ]
                except:
                    logger.info("Failed to retrieve campaignKeywords from response")
                    campaignKeywords = ""
                try:
                    searchType = json.loads(result.choices[0].message.function_call.arguments)[
                        "searchType"
                    ]
                except:
                    logger.info("Failed to retrieve SEARCHTYPE from response")
                    searchType = "campaign"
                try:
                    instagram = json.loads(result.choices[0].message.function_call.arguments)[
                        "instagram"
                    ]
                except:
                    logger.info("Failed to retrieve INSTAGRAM from response")
                    instagram = ""

                try:
                    industry = json.loads(result.choices[0].message.function_call.arguments)[
                        "industry"
                    ]
                except:
                    logger.info("Failed to retrieve INDUSTRY from response")
                    industry = ""
                # run answering chain
                answering_tool = CampaignInfluencerTool()
                logger.info(f"Search initiated for {searchType} with industry {industry} and instagram {instagram}, question: {question} and keywords {campaignKeywords}")
                answer = answering_tool.answer_question(question, campaignKeywords, chat_history, searchType, instagram, industry)

                self.log_tokens(
                    prompt_tokens=answer.prompt_tokens,
                    completion_tokens=answer.completion_tokens,
                )

                # Run post prompt if needed
                if self.config.prompts.enable_post_answering_prompt:
                    logger.debug("Running post answering prompt")
                    post_prompt_tool = PostPromptTool()
                    answer = post_prompt_tool.validate_answer(answer)
                    self.log_tokens(
                        prompt_tokens=answer.prompt_tokens,
                        completion_tokens=answer.completion_tokens,
                    )
            elif result.choices[0].message.function_call.name == "text_processing":
                logger.info("text_processing function detected")
                text = json.loads(result.choices[0].message.function_call.arguments)[
                    "text"
                ]
                operation = json.loads(
                    result.choices[0].message.function_call.arguments
                )["operation"]
                text_processing_tool = TextProcessingTool()
                answer = text_processing_tool.answer_question(
                    user_message, chat_history, text=text, operation=operation
                )
                self.log_tokens(
                    prompt_tokens=answer.prompt_tokens,
                    completion_tokens=answer.completion_tokens,
                )
            elif result.choices[0].message.function_call.name == "greetings":
                logger.info("greetings function detected")
                greetings_tool = GreetingsProcessingTool()
                answer = greetings_tool.answer_question(
                    user_message, chat_history
                )
                self.log_tokens(
                    prompt_tokens=answer.prompt_tokens,
                    completion_tokens=answer.completion_tokens,
                )
            elif result.choices[0].message.function_call.name == "brief":
                logger.info("brief function detected")
                campaign = json.loads(result.choices[0].message.function_call.arguments)[
                    "campaign"
                ]
                brief_tool = BriefTool()
                answer = brief_tool.answer_question(
                    user_message, chat_history, campaign=campaign
                )
                self.log_tokens(
                    prompt_tokens=answer.prompt_tokens,
                    completion_tokens=answer.completion_tokens,
                )
        else:
            logger.info("No function call detected")
            text = result.choices[0].message.content
            answer = Answer(question=user_message, answer=text)

        # Call Content Safety tool
        if self.config.prompts.enable_content_safety:
            if response := self.call_content_safety_output(user_message, answer.answer):
                return response

        # Format the output for the UI
        messages = self.output_parser.parse(
            question=answer.question,
            answer=answer.answer,
            source_documents=answer.source_documents,
        )
        return messages
