from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
# from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import time
import logging


logger = logging.getLogger(__name__)
load_dotenv()

MEMORY_DICT = {}


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error occurred while invoking AOAI Client Models: {e}")
            return ""
    return wrapper

def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable {key} not set")
    return value

def load_env_vars(llm_name: str) -> dict:
    return {
        'api_key': get_env_var(f'AZURE_{llm_name.upper()}_API_KEY'),
        'api_version': get_env_var('AZURE_API_VERSION'),
        'azure_endpoint': get_env_var(f'AZURE_{llm_name.upper()}_API_ENDPOINT'),
    }


def get_client(llm_name: str) -> AzureOpenAI:
    env_vars = load_env_vars(llm_name)
    return AzureOpenAI(
        api_key=env_vars['api_key'],
        api_version=env_vars['api_version'],
        azure_endpoint=env_vars['azure_endpoint']
    )

@handle_exceptions
def get_client_answer(client: AzureOpenAI, llm_name: str, lore: str, question: str, temperature: float, img_url: str = None) -> str:
    if img_url is None:
        messages=[
            {"role": "system", "content": lore},
            {"role": "user", "content": question}
        ]
    else:
        messages=[
            {"role": "system", "content": lore},
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": question
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": img_url
                    }
                }
            ] } 
        ]
    response = client.chat.completions.create(
        model=llm_name, 
        messages=messages,
        temperature=temperature
        
    )
    return response.choices[0].message.content


def get_chat_model(llm_name: str, temperature: float) -> AzureChatOpenAI:
    env_vars = load_env_vars(llm_name)
    return AzureChatOpenAI(
        api_key=env_vars['api_key'],
        api_version=env_vars['api_version'],
        azure_endpoint=env_vars['azure_endpoint'],
        azure_deployment=llm_name,
        temperature=temperature
    )

@handle_exceptions
def invoke_chat_model(llm: AzureChatOpenAI, lore: str, question: str, example_conversation: BaseMessage = None) -> str:
    messages = [    
        SystemMessage(content=lore),
        HumanMessage(content=question)
    ]
    if example_conversation:
    # 將 example_conversation 列表中的每一個訊息都插入到 messages 列表中
        messages[1:1] = example_conversation
    return (llm.invoke(messages)).content


@handle_exceptions
def assemble_img_url(conversation: list, img_url: str, question: str) -> dict:
    conversation[-1]["content"] = [
        { 
            "type": "text", 
            "text": question
        },
        { 
            "type": "image_url",
            "image_url": {
                "url": img_url
            }
        }
    ]
    return conversation

@handle_exceptions
def invoke_chat_model_by_whole_message(llm: AzureChatOpenAI,messages: list[BaseMessage]) -> str:
    return (llm.invoke(messages)).content


if __name__ == "__main__":
    path = os.getcwd()
    path += "/src/text/lore_Ina_eng.txt"
    with open(path, 'r', encoding='utf-8') as file:
        lore = file.read()
    llm = get_client("gpt-4o")
    start_time = time.time()
    response = get_client_answer(llm,"gpt-4o", lore, "tell me a joke", 0.7)
    print(response)
    print(f"Time: {time.time()-start_time}")