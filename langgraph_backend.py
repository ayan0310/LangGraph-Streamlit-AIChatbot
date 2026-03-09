from langgraph.graph import StateGraph,START,END
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from typing import TypedDict, Annotated
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"

from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

#define state for LLM
class LLMState(TypedDict):
    messages: Annotated[list, add_messages]

#initialize llm 
llm = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.environ["HUGGINGFACE_ACCESS_TOKEN"]
)

model=ChatHuggingFace(llm=llm)

#define function for llm to answer question
def llm_qa(state: LLMState) -> LLMState:
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': [response]}

#initialize graph
graph=StateGraph(LLMState)

graph.add_node("llm_qa",llm_qa)
graph.add_edge(START,"llm_qa")
graph.add_edge("llm_qa",END)

config={'configurable': {'thread_id': '1'}}
checkpointer=InMemorySaver()

chatbot_workflow=graph.compile(checkpointer=checkpointer)



