import os
from dotenv import load_dotenv
from typing import List, Literal, Optional
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler
import uvicorn

load_dotenv()


class Message(BaseModel):
    role: Literal["system", "assistant", "human"]
    content: str


class Parameters(BaseModel):
    model: Optional[str] = "gpt-4o-mini"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = None
    timeout: Optional[float] = None
    max_retries: Optional[int] = 2


class ModelRequest(BaseModel):
    messages: List[Message]
    parameters: Optional[Parameters] = Parameters()


app = FastAPI()


def to_lc_messages(messages: List[Message]):
    result = []
    for m in messages:
        if m.role == "system":
            result.append(SystemMessage(content=m.content))
        elif m.role == "assistant":
            result.append(AIMessage(content=m.content))
        elif m.role == "human":
            result.append(HumanMessage(content=m.content))
    return result


@app.post("/chat")
async def chat_endpoint(
    request: ModelRequest, mandator_id: Optional[str] = Header(None)
):
    if not mandator_id:
        raise HTTPException(status_code=403, detail="Mandator ID is required")

    langfuse_handler = CallbackHandler(user_id=mandator_id)

    lc_messages = to_lc_messages(request.messages)
    llm = ChatOpenAI(
        model=request.parameters.model,
        temperature=request.parameters.temperature,
        max_tokens=request.parameters.max_tokens,
        timeout=request.parameters.timeout,
        max_retries=request.parameters.max_retries,
    )

    response = llm.invoke(
        lc_messages,
        config={
            "callbacks": [langfuse_handler],
        },
    )

    return {"role": "assistant", "content": response.content}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
