from langgraph.graph import StateGraph, START, END
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"


load_dotenv()

# Define state for LLM with messages for streaming support
class LLMState(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize LLM
llm = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.environ["HUGGINGFACE_ACCESS_TOKEN"]
)

model = ChatHuggingFace(llm=llm)

# Define function for LLM to answer question
def llm_qa(state: LLMState) -> LLMState:
    messages = state['messages']
    response = model.invoke(messages)
    return {'messages': [response]}

# Initialize graph
graph = StateGraph(LLMState)

graph.add_node("llm_qa", llm_qa)
graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)

config = {'configurable': {'thread_id': '1'}}

conn=sqlite3.connect('chatbot_conversations.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

chatbot_workflow = graph.compile(checkpointer=checkpointer)



def retrieve_all_threads(): 
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        configurable = checkpoint.config.get('configurable', {})
        if 'thread_id' in configurable:
            all_threads.add(configurable['thread_id'])

    return list(all_threads)





