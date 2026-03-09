import streamlit as st
from langgraph_backend_streaming import chatbot_workflow
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessageChunk

#define a config for the workflow
config: RunnableConfig = {'configurable': {'thread_id': '1'}}

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

#print the message history
for message in st.session_state["message_history"]:
      with st.chat_message(message["role"]):
            st.text(message["content"])

#get user input and add it into the message history, then invoke the workflow to get chatbot output and add it into the message history
user_input = st.chat_input("Ask a question: ")
if user_input:
    #add the user input into the message history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
    #show chatbot output in streaming way and add it into the message history
    with st.chat_message("assistant"):
        def stream_response():
            for message_chunk, metadata in chatbot_workflow.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=config,
                stream_mode='messages'
            ):
                if isinstance(message_chunk, AIMessageChunk) and message_chunk.content:
                    yield message_chunk.content
        
        ai_message = st.write_stream(stream_response())

    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
        