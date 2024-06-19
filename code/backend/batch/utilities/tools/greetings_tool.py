from typing import List
from ..helpers.llm_helper import LLMHelper
from .answering_tool_base import AnsweringToolBase
from ..common.answer import Answer


class GreetingsProcessingTool(AnsweringToolBase):
    def __init__(self) -> None:
        self.name = "GreetingsProcessing"

    def answer_question(self, question: str, chat_history: List[dict] = [], **kwargs):
        llm_helper = LLMHelper()
        user_content = question

        system_message = """You are an AI assistant for the user. Your task is to say hello and always explain your key functionalities:
            1. Elaborate customer's requests and transform in a structured campaign brief
            2. Based on s campaign brief, retrieve similar campaigns
            3. Recommend the best influencers for the campaign
        """

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
