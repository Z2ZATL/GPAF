import models
from agent import AgentConfig, ModelConfig
from python.helpers import runtime, settings, defer
from python.helpers.print_style import PrintStyle


def get_automatic_provider(model_type: str, current_settings: settings.Settings) -> models.ModelProvider:
    """เลือก provider อัตโนมัติตาม API keys ที่มี"""
    api_keys = current_settings.get("api_keys", {})
    
    # ลำดับความสำคัญของ providers
    if model_type == "chat":
        priority = [
            models.ModelProvider.OPENAI,
            models.ModelProvider.ANTHROPIC,
            models.ModelProvider.GOOGLE,
            models.ModelProvider.MISTRALAI,
            models.ModelProvider.GROQ,
            models.ModelProvider.OLLAMA,
        ]
    elif model_type == "util":
        priority = [
            models.ModelProvider.OPENAI,
            models.ModelProvider.ANTHROPIC,
            models.ModelProvider.GROQ,
            models.ModelProvider.OLLAMA,
        ]
    elif model_type == "embed":
        priority = [
            models.ModelProvider.HUGGINGFACE,
            models.ModelProvider.OPENAI,
            models.ModelProvider.OLLAMA,
        ]
    elif model_type == "browser":
        priority = [
            models.ModelProvider.OPENAI,
            models.ModelProvider.ANTHROPIC,
            models.ModelProvider.GOOGLE,
            models.ModelProvider.OLLAMA,
        ]
    else:
        priority = [models.ModelProvider.OPENAI]
    
    # ตรวจสอบ API keys และเลือก provider แรกที่มี key
    for provider in priority:
        if provider == models.ModelProvider.HUGGINGFACE:
            # HuggingFace ไม่จำเป็นต้องมี API key สำหรับ embedding models
            return provider
        elif provider == models.ModelProvider.OLLAMA:
            # Ollama ใช้ local ไม่ต้องมี API key
            return provider
        elif f"api_key_{provider.name.lower()}" in api_keys and api_keys[f"api_key_{provider.name.lower()}"]:
            return provider
    
    # ถ้าไม่พบ provider ที่มี API key ให้ใช้ค่า default
    return priority[0] if priority else models.ModelProvider.OPENAI


def get_automatic_model_name(provider: models.ModelProvider, model_type: str) -> str:
    """เลือกชื่อ model อัตโนมัติตาม provider และประเภท"""
    if model_type == "chat":
        defaults = {
            models.ModelProvider.OPENAI: "gpt-4-turbo-preview",
            models.ModelProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
            models.ModelProvider.GOOGLE: "gemini-1.5-pro",
            models.ModelProvider.MISTRALAI: "mistral-large-latest",
            models.ModelProvider.GROQ: "llama-3.1-70b-versatile",
            models.ModelProvider.OLLAMA: "llama3.2",
        }
    elif model_type == "util":
        defaults = {
            models.ModelProvider.OPENAI: "gpt-4o-mini",
            models.ModelProvider.ANTHROPIC: "claude-3-haiku-20240307",
            models.ModelProvider.GROQ: "llama3-8b-8192",
            models.ModelProvider.OLLAMA: "llama3.2",
        }
    elif model_type == "embed":
        defaults = {
            models.ModelProvider.HUGGINGFACE: "sentence-transformers/all-MiniLM-L6-v2",
            models.ModelProvider.OPENAI: "text-embedding-3-small",
            models.ModelProvider.OLLAMA: "nomic-embed-text",
        }
    elif model_type == "browser":
        defaults = {
            models.ModelProvider.OPENAI: "gpt-4-turbo-preview",
            models.ModelProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
            models.ModelProvider.GOOGLE: "gemini-1.5-pro",
            models.ModelProvider.OLLAMA: "llama3.2",
        }
    else:
        return "gpt-4-turbo-preview"
    
    return defaults.get(provider, "gpt-4-turbo-preview")


def initialize_agent():
    current_settings = settings.get_settings()

    # จัดการกับ AUTOMATIC provider สำหรับ chat model
    chat_provider = current_settings["chat_model_provider"]
    if chat_provider == models.ModelProvider.AUTOMATIC.name:
        chat_provider = get_automatic_provider("chat", current_settings).name
        chat_model_name = get_automatic_model_name(models.ModelProvider[chat_provider], "chat")
    else:
        chat_model_name = current_settings["chat_model_name"]

    # chat model from user settings
    chat_llm = ModelConfig(
        provider=models.ModelProvider[chat_provider],
        name=chat_model_name,
        ctx_length=current_settings["chat_model_ctx_length"],
        vision=current_settings["chat_model_vision"],
        limit_requests=current_settings["chat_model_rl_requests"],
        limit_input=current_settings["chat_model_rl_input"],
        limit_output=current_settings["chat_model_rl_output"],
        kwargs=current_settings["chat_model_kwargs"],
    )

    # จัดการกับ AUTOMATIC provider สำหรับ utility model
    util_provider = current_settings["util_model_provider"]
    if util_provider == models.ModelProvider.AUTOMATIC.name:
        util_provider = get_automatic_provider("util", current_settings).name
        util_model_name = get_automatic_model_name(models.ModelProvider[util_provider], "util")
    else:
        util_model_name = current_settings["util_model_name"]

    # utility model from user settings
    utility_llm = ModelConfig(
        provider=models.ModelProvider[util_provider],
        name=util_model_name,
        ctx_length=current_settings["util_model_ctx_length"],
        limit_requests=current_settings["util_model_rl_requests"],
        limit_input=current_settings["util_model_rl_input"],
        limit_output=current_settings["util_model_rl_output"],
        kwargs=current_settings["util_model_kwargs"],
    )

    # จัดการกับ AUTOMATIC provider สำหรับ embedding model
    embed_provider = current_settings["embed_model_provider"]
    if embed_provider == models.ModelProvider.AUTOMATIC.name:
        embed_provider = get_automatic_provider("embed", current_settings).name
        embed_model_name = get_automatic_model_name(models.ModelProvider[embed_provider], "embed")
    else:
        embed_model_name = current_settings["embed_model_name"]

    # embedding model from user settings
    embedding_llm = ModelConfig(
        provider=models.ModelProvider[embed_provider],
        name=embed_model_name,
        limit_requests=current_settings["embed_model_rl_requests"],
        kwargs=current_settings["embed_model_kwargs"],
    )

    # จัดการกับ AUTOMATIC provider สำหรับ browser model
    browser_provider = current_settings["browser_model_provider"]
    if browser_provider == models.ModelProvider.AUTOMATIC.name:
        browser_provider = get_automatic_provider("browser", current_settings).name
        browser_model_name = get_automatic_model_name(models.ModelProvider[browser_provider], "browser")
    else:
        browser_model_name = current_settings["browser_model_name"]

    # browser model from user settings
    browser_llm = ModelConfig(
        provider=models.ModelProvider[browser_provider],
        name=browser_model_name,
        vision=current_settings["browser_model_vision"],
        kwargs=current_settings["browser_model_kwargs"],
    )

    # จัดการกับ automatic subdirectories
    prompts_subdir = current_settings["agent_prompts_subdir"]
    if prompts_subdir == "automatic":
        prompts_subdir = "default"
    
    knowledge_subdir = current_settings["agent_knowledge_subdir"]
    if knowledge_subdir == "automatic":
        knowledge_subdir = "custom"

    # agent configuration
    config = AgentConfig(
        chat_model=chat_llm,
        utility_model=utility_llm,
        embeddings_model=embedding_llm,
        browser_model=browser_llm,
        prompts_subdir=prompts_subdir,
        memory_subdir=current_settings["agent_memory_subdir"],
        knowledge_subdirs=["default", knowledge_subdir],
        mcp_servers=current_settings["mcp_servers"],
        code_exec_docker_enabled=False,
        # code_exec_docker_name = "A0-dev",
        code_exec_docker_image = "frdel/gpaf-run:development",
        # code_exec_docker_ports = { "22/tcp": 55022, "80/tcp": 55080 }
        # code_exec_docker_volumes = {
        # files.get_base_dir(): {"bind": "/a0", "mode": "rw"},
        # files.get_abs_path("work_dir"): {"bind": "/root", "mode": "rw"},
        # },
        # code_exec_ssh_enabled = True,
        # code_exec_ssh_addr = "localhost",
        # code_exec_ssh_port = 55022,
        # code_exec_ssh_user = "root",
        # code_exec_ssh_pass = "",
        # additional = {},
    )

    # update SSH and docker settings
    _set_runtime_config(config, current_settings)

    # update config with runtime args
    _args_override(config)

    # initialize MCP in deferred task to prevent blocking the main thread
    # async def initialize_mcp_async(mcp_servers_config: str):
    #     return initialize_mcp(mcp_servers_config)
    # defer.DeferredTask(thread_name="mcp-initializer").start_task(initialize_mcp_async, config.mcp_servers)
    # initialize_mcp(config.mcp_servers)

    # import python.helpers.mcp_handler as mcp_helper
    # import agent as agent_helper
    # import python.helpers.print_style as print_style_helper
    # if not mcp_helper.MCPConfig.get_instance().is_initialized():
    #     try:
    #         mcp_helper.MCPConfig.update(config.mcp_servers)
    #     except Exception as e:
    #         first_context = agent_helper.AgentContext.first()
    #         if first_context:
    #             (
    #                 first_context.log
    #                 .log(type="warning", content=f"Failed to update MCP settings: {e}", temp=False)
    #             )
    #         (
    #             print_style_helper.PrintStyle(background_color="black", font_color="red", padding=True)
    #             .print(f"Failed to update MCP settings: {e}")
    #         )

    # return config object
    return config

def initialize_chats():
    from python.helpers import persist_chat
    async def initialize_chats_async():
        persist_chat.load_tmp_chats()
    return defer.DeferredTask().start_task(initialize_chats_async)

def initialize_mcp():
    set = settings.get_settings()
    async def initialize_mcp_async():
        from python.helpers.mcp_handler import initialize_mcp as _initialize_mcp
        return _initialize_mcp(set["mcp_servers"])
    return defer.DeferredTask().start_task(initialize_mcp_async)

def initialize_job_loop():
    from python.helpers.job_loop import run_loop
    return defer.DeferredTask("JobLoop").start_task(run_loop)


def _args_override(config):
    # update config with runtime args
    for key, value in runtime.args.items():
        if hasattr(config, key):
            # conversion based on type of config[key]
            if isinstance(getattr(config, key), bool):
                value = value.lower().strip() == "true"
            elif isinstance(getattr(config, key), int):
                value = int(value)
            elif isinstance(getattr(config, key), float):
                value = float(value)
            elif isinstance(getattr(config, key), str):
                value = str(value)
            else:
                raise Exception(
                    f"Unsupported argument type of '{key}': {type(getattr(config, key))}"
                )

            setattr(config, key, value)


def _set_runtime_config(config: AgentConfig, set: settings.Settings):
    ssh_conf = settings.get_runtime_config(set)
    for key, value in ssh_conf.items():
        if hasattr(config, key):
            setattr(config, key, value)

    # if config.code_exec_docker_enabled:
    #     config.code_exec_docker_ports["22/tcp"] = ssh_conf["code_exec_ssh_port"]
    #     config.code_exec_docker_ports["80/tcp"] = ssh_conf["code_exec_http_port"]
    #     config.code_exec_docker_name = f"{config.code_exec_docker_name}-{ssh_conf['code_exec_ssh_port']}-{ssh_conf['code_exec_http_port']}"

    #     dman = docker.DockerContainerManager(
    #         logger=log.Log(),
    #         name=config.code_exec_docker_name,
    #         image=config.code_exec_docker_image,
    #         ports=config.code_exec_docker_ports,
    #         volumes=config.code_exec_docker_volumes,
    #     )
    #     dman.start_container()

    # config.code_exec_ssh_pass = asyncio.run(rfc_exchange.get_root_password())
