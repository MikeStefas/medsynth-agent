from langchain_openai import ChatOpenAI
import config

local_llm = ChatOpenAI(
    base_url=config.LMSTUDIO_BASE_URL,
    api_key="pipapapaiap",
    model=config.LMSTUDIO_MODEL_NAME,
)
