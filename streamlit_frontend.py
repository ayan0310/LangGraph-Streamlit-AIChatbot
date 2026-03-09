import streamlit as st
from langgraph_backend import chatbot_workflow
from langchain_core.runnables import RunnableConfig

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
    #add chatbot output into the message history
    chatbot_output = chatbot_workflow.invoke({'question': user_input, 'answer': ''},config=config)
    ai_message = chatbot_output['answer']
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)