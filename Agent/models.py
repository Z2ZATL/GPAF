from enum import Enum
import os
from typing import Any
from pydantic import SecretStr
from langchain_openai import (
    ChatOpenAI,
    OpenAI,
    OpenAIEmbeddings,
    AzureChatOpenAI,
    AzureOpenAIEmbeddings,
    AzureOpenAI,
)
from langchain_community.llms.ollama import Ollama
from langchain_ollama import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_huggingface import (
    HuggingFaceEmbeddings,
    ChatHuggingFace,
    HuggingFaceEndpoint,
)
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
    embeddings as google_embeddings,
)
from langchain_mistralai import ChatMistralAI

from python.helpers import dotenv, runtime
from python.helpers.dotenv import load_dotenv
from python.helpers.rate_limiter import RateLimiter

# environment variables
load_dotenv()


class ModelType(Enum):
    CHAT = "Chat"
    EMBEDDING = "Embedding"


class ModelProvider(Enum):
    AUTOMATIC = "Automatic"
    ANTHROPIC = "Anthropic"
    CHUTES = "Chutes"
    DEEPSEEK = "DeepSeek"
    GOOGLE = "Google"
    GROQ = "Groq"
    HUGGINGFACE = "HuggingFace"
    LMSTUDIO = "LM Studio"
    MISTRALAI = "Mistral AI"
    OLLAMA = "Ollama"
    OPENAI = "OpenAI"
    OPENAI_AZURE = "OpenAI Azure"
    OPENROUTER = "OpenRouter"
    SAMBANOVA = "Sambanova"
    TYPHOON = "Typhoon"
    OTHER = "Other"


rate_limiters: dict[str, RateLimiter] = {}


# Utility function to get API keys from environment variables
def get_api_key(service):
    return (
        dotenv.get_dotenv_value(f"API_KEY_{service.upper()}")
        or dotenv.get_dotenv_value(f"{service.upper()}_API_KEY")
        or dotenv.get_dotenv_value(
            f"{service.upper()}_API_TOKEN"
        )  # Added for CHUTES_API_TOKEN
        or "None"
    )


def get_model(type: ModelType, provider: ModelProvider, name: str, **kwargs):
    fnc_name = f"get_{provider.name.lower()}_{type.name.lower()}"  # function name of model getter
    model = globals()[fnc_name](name, **kwargs)  # call function by name
    return model


def get_rate_limiter(
    provider: ModelProvider, name: str, requests: int, input: int, output: int
) -> RateLimiter:
    # get or create
    key = f"{provider.name}\\{name}"
    rate_limiters[key] = limiter = rate_limiters.get(key, RateLimiter(seconds=60))
    # always update
    limiter.limits["requests"] = requests or 0
    limiter.limits["input"] = input or 0
    limiter.limits["output"] = output or 0
    return limiter


def parse_chunk(chunk: Any):
    if isinstance(chunk, str):
        content = chunk
    elif hasattr(chunk, "content"):
        content = str(chunk.content)
    else:
        content = str(chunk)
    return content


# Ollama models
def get_ollama_base_url():
    return (
        dotenv.get_dotenv_value("OLLAMA_BASE_URL")
        or f"http://{runtime.get_local_url()}:11434"
    )


def get_ollama_chat(
    model_name: str,
    base_url=None,
    num_ctx=8192,
    **kwargs,
):
    if not base_url:
        base_url = get_ollama_base_url()
    return ChatOllama(
        model=model_name,
        base_url=base_url,
        num_ctx=num_ctx,
        **kwargs,
    )


def get_ollama_embedding(
    model_name: str,
    base_url=None,
    num_ctx=8192,
    **kwargs,
):
    if not base_url:
        base_url = get_ollama_base_url()
    return OllamaEmbeddings(
        model=model_name, base_url=base_url, num_ctx=num_ctx, **kwargs
    )


# HuggingFace models
def get_huggingface_chat(
    model_name: str,
    api_key=None,
    **kwargs,
):
    # different naming convention here
    if not api_key:
        api_key = get_api_key("huggingface") or os.environ["HUGGINGFACEHUB_API_TOKEN"]

    # Initialize the HuggingFaceEndpoint with the specified model and parameters
    llm = HuggingFaceEndpoint(
        repo_id=model_name,
        task="text-generation",
        do_sample=True,
        **kwargs,
    )

    # Initialize the ChatHuggingFace with the configured llm
    return ChatHuggingFace(llm=llm)


def get_huggingface_embedding(model_name: str, **kwargs):
    return HuggingFaceEmbeddings(model_name=model_name, **kwargs)


# LM Studio and other OpenAI compatible interfaces
def get_lmstudio_base_url():
    return (
        dotenv.get_dotenv_value("LM_STUDIO_BASE_URL")
        or f"http://{runtime.get_local_url()}:1234/v1"
    )


def get_lmstudio_chat(
    model_name: str,
    base_url=None,
    **kwargs,
):
    if not base_url:
        base_url = get_lmstudio_base_url()
    return ChatOpenAI(model_name=model_name, base_url=base_url, api_key="none", **kwargs)  # type: ignore


def get_lmstudio_embedding(
    model_name: str,
    base_url=None,
    **kwargs,
):
    if not base_url:
        base_url = get_lmstudio_base_url()
    return OpenAIEmbeddings(model=model_name, api_key="none", base_url=base_url, check_embedding_ctx_length=False, **kwargs)  # type: ignore


# Anthropic models
def get_anthropic_chat(
    model_name: str,  # ใช้ model_name ตามที่ API ต้องการ
    api_key: str | None = None,
    base_url: str | None = None,
    **kwargs,
) -> ChatAnthropic:
    if not api_key:
        api_key = get_api_key("anthropic")
    if not base_url:
        base_url = dotenv.get_dotenv_value("ANTHROPIC_BASE_URL")
    secret_key = SecretStr(api_key) if api_key else SecretStr("")
    return ChatAnthropic(
        model_name=model_name,
        api_key=secret_key,
        **kwargs
    )


def get_anthropic_embedding(
    model_name: str,
    api_key=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("anthropic")
    secret_key = SecretStr(api_key) if api_key else None
    return OpenAIEmbeddings(
        model=model_name,
        api_key=secret_key,
        **kwargs
    )


# OpenAI models
def get_openai_chat(
    model_name: str,
    api_key=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("openai")
    secret_key = SecretStr(api_key) if api_key else None
    return ChatOpenAI(
        model=model_name,
        api_key=secret_key,
        **kwargs
    )


def get_openai_embedding(
    model_name: str,
    api_key=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("openai")
    secret_key = SecretStr(api_key) if api_key else None
    return OpenAIEmbeddings(
        model=model_name,
        api_key=secret_key,
        **kwargs
    )


def get_openai_azure_chat(
    azure_deployment: str,
    api_key: str | None = None,
    azure_endpoint: str | None = None,
    api_version: str | None = None,
    **kwargs,
) -> AzureChatOpenAI:
    if not api_key:
        api_key = get_api_key("openai_azure")
    if not azure_endpoint:
        azure_endpoint = dotenv.get_dotenv_value("AZURE_OPENAI_ENDPOINT")
    if not api_version:
        api_version = dotenv.get_dotenv_value("OPENAI_API_VERSION")
    
    if not api_version:
        raise ValueError("OPENAI_API_VERSION is required for Azure OpenAI, but it's not set.")

    secret_key = SecretStr(api_key) if api_key else None
    
    return AzureChatOpenAI(
        azure_deployment=azure_deployment,
        api_key=secret_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
        **kwargs
    )


def get_openai_azure_embedding(
    azure_deployment: str,
    api_key: str | None = None,
    azure_endpoint: str | None = None,
    api_version: str | None = None,
    **kwargs,
) -> AzureOpenAIEmbeddings:
    if not api_key:
        api_key = get_api_key("openai_azure")
    if not azure_endpoint:
        azure_endpoint = dotenv.get_dotenv_value("AZURE_OPENAI_ENDPOINT")
    if not api_version:
        api_version = dotenv.get_dotenv_value("OPENAI_API_VERSION")
    
    if not api_version:
        raise ValueError("OPENAI_API_VERSION is required for Azure OpenAI, but it's not set.")

    secret_key = SecretStr(api_key) if api_key else None
    
    return AzureOpenAIEmbeddings(
        azure_deployment=azure_deployment,
        api_key=secret_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
        **kwargs
    )


# Google models
def get_google_chat(
    model_name: str,
    api_key=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("google")
    secret_key = SecretStr(api_key) if api_key else None
    return ChatGoogleGenerativeAI(
        model=model_name,
        api_key=secret_key,
        safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE},
        **kwargs
    )


def get_google_embedding(
    model_name: str,
    api_key=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("google")
    secret_key = SecretStr(api_key) if api_key else None
    return google_embeddings.GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=secret_key,
        **kwargs
    )


# Mistral models
def get_mistralai_chat(
    model_name: str,
    api_key=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("mistral")
    secret_key = SecretStr(api_key) if api_key else None
    return ChatMistralAI(
        model_name=model_name,
        api_key=secret_key,
        **kwargs
    )


# Groq models
def get_groq_chat(
    model_name: str,
    api_key=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("groq")
    secret_key = SecretStr(api_key) if api_key else None
    return ChatGroq(
        model=model_name,
        api_key=secret_key,
        **kwargs
    )


# DeepSeek models
def get_deepseek_chat(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("deepseek")
    if not base_url:
        base_url = dotenv.get_dotenv_value("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"
    secret_key = SecretStr(api_key) if api_key else None
    return ChatOpenAI(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        **kwargs
    )


# OpenRouter models
def get_openrouter_chat(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("openrouter")
    if not base_url:
        base_url = dotenv.get_dotenv_value("OPEN_ROUTER_BASE_URL") or "https://openrouter.ai/api/v1"
    secret_key = SecretStr(api_key) if api_key else None
    return ChatOpenAI(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        stream_usage=True,
        model_kwargs={
            "extra_headers": {
                "HTTP-Referer": "https://gpaf.ai",
                "X-Title": "GPAF",
            }
        },
        **kwargs
    )


def get_openrouter_embedding(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("openrouter")
    if not base_url:
        base_url = dotenv.get_dotenv_value("OPEN_ROUTER_BASE_URL") or "https://openrouter.ai/api/v1"
    secret_key = SecretStr(api_key) if api_key else None
    return OpenAIEmbeddings(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        **kwargs
    )


# Sambanova models
def get_sambanova_chat(
    model_name: str,
    api_key=None,
    base_url=None,
    max_tokens=1024,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("sambanova")
    if not base_url:
        base_url = dotenv.get_dotenv_value("SAMBANOVA_BASE_URL") or "https://fast-api.snova.ai/v1"
    secret_key = SecretStr(api_key) if api_key else None
    return ChatOpenAI(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        model_kwargs={"max_tokens": max_tokens},
        **kwargs
    )


def get_sambanova_embedding(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("sambanova")
    if not base_url:
        base_url = dotenv.get_dotenv_value("SAMBANOVA_BASE_URL") or "https://fast-api.snova.ai/v1"
    secret_key = SecretStr(api_key) if api_key else None
    return OpenAIEmbeddings(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        **kwargs
    )


# Other OpenAI compatible models
def get_other_chat(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    secret_key = SecretStr(api_key) if api_key else None
    return ChatOpenAI(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        **kwargs
    )


def get_other_embedding(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    secret_key = SecretStr(api_key) if api_key else None
    return OpenAIEmbeddings(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        **kwargs
    )


# Chutes models
def get_chutes_chat(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("chutes")
    if not base_url:
        base_url = dotenv.get_dotenv_value("CHUTES_BASE_URL") or "https://api.chutes.ai/v1"
    secret_key = SecretStr(api_key) if api_key else None
    return ChatOpenAI(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        model_kwargs={
            "extra_headers": {
                "HTTP-Referer": "https://gpaf.ai",
                "X-Title": "GPAF",
            }
        },
        **kwargs
    )


# Typhoon models
def get_typhoon_base_url():
    return (
        dotenv.get_dotenv_value("TYPHOON_BASE_URL")
        or "https://api.opentyphoon.ai/v1"
    )


def get_typhoon_chat(
    model_name: str,
    api_key=None,
    base_url=None,
    num_ctx=8192,
    api_version=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("typhoon")
    if not base_url:
        base_url = get_typhoon_base_url()
    if not api_version:
        api_version = dotenv.get_dotenv_value("TYPHOON_API_VERSION") or "2024-02-15"
    
    if not api_key or api_key == "None":
        raise ValueError("TYPHOON_API_KEY is required but not set")
    
    secret_key = SecretStr(api_key)
    
    rate_limiter = None
    if "rate_limiter" in kwargs:
        rate_limiter = kwargs.pop("rate_limiter")
    
    model = ChatOpenAI(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        model_kwargs={
            "extra_headers": {
                "HTTP-Referer": "https://gpaf.ai",
                "X-Title": "GPAF",
            },
            "max_tokens": num_ctx,
        },
        **kwargs
    )
    
    if rate_limiter:
        model.rate_limiter = rate_limiter
    
    return model


def get_typhoon_embedding(
    model_name: str,
    api_key=None,
    base_url=None,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("typhoon")
    if not base_url:
        base_url = get_typhoon_base_url()
    
    secret_key = SecretStr(api_key) if api_key else None
    
    return OpenAIEmbeddings(
        model=model_name,
        api_key=secret_key,
        base_url=base_url,
        **kwargs
    )
