from .chatLLM import run_chat

def run_llm_chat(
    llm_chat_rjurl="http://cloud.rj-info.com/ai/chat/completion?_timeout=111111111",
    # llm_chat_rjurl="http://cloud.rj-info.com/ai/plugin/chat/completion?_timeout=111111111",
    llm_name = "coze-gpt", #修改使用的大模型，可以改成qwen,kimi,c-renlab,gpt-text,gemini,qwen-long
    # llm_name = "qwen-long", #修改使用的大模型，可以改成qwen,kimi,c-renlab,gpt-text,gemini,qwen-long
    input_approach = "File",#输入文章信息的方式，可以是Str或者File(json文件)
    prompt_json_path = r"D:\SYSU\RenLab\Lab\LLM\scicat\payload_Job_ptmDrag.json",
    template_prompt_json_path = r"D:\SYSU\RenLab\Lab\LLM\scicat\payload_Job_ptmDrag.json",
    custom_data_json_path = r"D:\SYSU\RenLab\Lab\LLM\scicat\custom_data.json"):
    return run_chat(llm_chat_rjurl, llm_name, input_approach, prompt_json_path, template_prompt_json_path, custom_data_json_path)

def run_llm_chat_with_file(
    llm_chat_rjurl="http://cloud.rj-info.com/ai/chat/completion?_timeout=111111111",
    # llm_chat_rjurl="http://cloud.rj-info.com/ai/plugin/chat/completion?_timeout=111111111",
    llm_name = "coze-gpt", #修改使用的大模型，可以改成qwen,kimi,c-renlab,gpt-text,gemini,qwen-long
    input_approach = "File",#输入文章信息的方式，可以是Str或者File(json文件)
    prompt_json_path = r"D:\SYSU\RenLab\Lab\LLM\scicat\payload_Job_ptmDrag.json",
    template_prompt_json_path = r"D:\SYSU\RenLab\Lab\LLM\scicat\payload_Job_ptmDrag.json",
    custom_data_json_path = r"D:\SYSU\RenLab\Lab\LLM\scicat\custom_data.json"):
    return run_llm_chat_with_file(llm_chat_rjurl, llm_name, input_approach, prompt_json_path, template_prompt_json_path, custom_data_json_path)