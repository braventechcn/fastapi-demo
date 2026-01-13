from fastapi import FastAPI

# 1. 创建应用实例
app = FastAPI()

# 2. 定义一个 GET 接口
#   - 当用户访问网站根路径 "/" 时，执行下面这个函数
@app.get("/")
def read_root():
    return {"message": "你好，这里是 FastAPI！"}

@app.get("/hello/{name}")
def greet(name: str):
    return {"greeting": f"你好，{name}！"}

from pydantic import BaseModel

# 定义请求体模型
class Item(BaseModel):
    text: str

@app.post("/echo")
def echo_text(item: Item):
    return {"received": item.text}

@app.get("/users/{user_id}/logs")
def get_logs(user_id: int, limit: int = 10):
    return {"user_id": user_id, "limit": limit}


import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Please set DEEPSEEK_API_KEY or OPENAI_API_KEY in your environment")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
    )

# 定义一个用于大模型调用的 Pydantic 数据模型
class ChatRequest(BaseModel):
    prompt: str                 # prompt 是用户输入
    max_tokens: int = 120       # max_tokens 控制回复长度（默认 120）
    temperature: float = 0.7    # temperature 控制创造性（默认 0.7）

@app.post("/chat")
async def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": req.prompt},
        ],
        stream=False,
        max_tokens=req.max_tokens,
        temperature=req.temperature
    )   
    # result = response.choices[0].message["content"]
    result = response.choices[0].message.content
    
    return {"answer": result}