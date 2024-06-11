from enum import Enum


class OrchestrationStrategy(Enum):
    INSTAGRAM_FUNCTION = "instagram_function"
    OPENAI_FUNCTION = "openai_function"
    LANGCHAIN = "langchain"
    SEMANTIC_KERNEL = "semantic_kernel"
