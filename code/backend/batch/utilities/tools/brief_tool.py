from typing import List
from ..helpers.llm_helper import LLMHelper
from .answering_tool_base import AnsweringToolBase
from ..common.answer import Answer


class BriefTool(AnsweringToolBase):
    def __init__(self) -> None:
        self.name = "BriefProcessing"

    def answer_question(self, question: str, chat_history: List[dict] = [], **kwargs):
        llm_helper = LLMHelper()
        campaign = kwargs.get("campaign")
        user_content = (
            f"This is the campaign: {campaign}"
            if (campaign)
            else question
        )

        system_message = """You are an AI assistant helping an advertisment company to create a brief for a new campaign.
                            Given the brief, you should create a bullet point list with the following information: name of the brand,
                            campaign description, campaign style, main industry (choose between: banking, health, toys, baby, sports)
                            and secondary industry (banking, health, toys, baby, sports).
                            If any information is missing or not clear, please ask for additional information."""

        result = llm_helper.get_chat_completion(
            [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_content},
            ]
        )

        answer = Answer(
            question=question,
            answer=result.choices[0].message.content,
            source_documents=[],
            prompt_tokens=result.usage.prompt_tokens,
            completion_tokens=result.usage.completion_tokens,
        )
        return answer
