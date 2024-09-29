import streamlit as st

st.header("Chat")

if "prompt_saved" not in st.session_state:
    st.session_state["prompt_saved"] = False

if "files_uploaded" not in st.session_state:
    st.session_state["files_uploaded"] = False

if not st.session_state["prompt_saved"] or not st.session_state["files_uploaded"]:
    st.write("Please set your system prompt and upload files before chatting.")
    exit()

# Initialise chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "Hi! What are we discussing today?"}]

# Chat logic
if prompt := st.chat_input("Ask questions here"):
    st.session_state["chat_history"].append({"role": "user", "content": prompt})


# Display the prior chat messages
for message in st.session_state.chat_history:
     with st.chat_message(message["role"]):
        st.markdown(message["content"])


# If last message is not from assistant, generate a new response
if st.session_state.chat_history[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Use the chat engine to generate a response
            response = st.session_state.chat_engine.chat(prompt)
            st.markdown(response.response)

            # Add the response to the chat history
            message = {"role": "assistant", "content": response.response}
            st.session_state.chat_history.append(message)