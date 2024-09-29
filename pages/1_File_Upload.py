import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import os
import tempfile

st.header("File Upload")

def setup():

    # Select OpenAI model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    # Initialise chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [{"role": "assistant", "content": "Hi! What are we discussing today?"}]
    
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = ""

    if "files_uploaded" not in st.session_state:
        st.session_state["files_uploaded"] = False
    
    Settings.llm = OpenAI(model=st.session_state["openai_model"], temperature=0.5, system_prompt=st.session_state["system_prompt"])

setup()


if st.session_state["files_uploaded"]:
    st.write("Please proceed to the chat window.")
    exit()


### FILE UPLOAD LOGIC ###
st.write("""Upload files here for the chatbot to use as context. Compatible filetypes include PDF, TXT. Upload your file(s) and press 'Done' to process them.""")

# Streamlit file uploader
uploaded_files = st.file_uploader("Upload a file", accept_multiple_files=True)

def files_uploaded():
    ### BUILD INDEX LOGIC ###
    temp_dir = tempfile.TemporaryDirectory()

    # Write the uploaded file(s) to a temporary directory.
    for up_file in uploaded_files:
        if up_file is not None:
            with open(os.path.join(temp_dir.name, up_file.name), "wb") as f:
                f.write(up_file.getbuffer())

    # Loads data from the temporary directory
    def load_data(): 
        with st.spinner(text="Loading knowledge base, please do not leave this page"):
            reader = SimpleDirectoryReader(input_dir=temp_dir.name, recursive=True)
            docs = reader.load_data()
            index = VectorStoreIndex.from_documents(docs)
            return index

    index = load_data()

    # Initialize the chat engine
    if "chat_engine" not in st.session_state.keys():
        # st.write("New chat engine created.")
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    temp_dir.cleanup()

    st.session_state["files_uploaded"] = True

if uploaded_files:
    st.button("Done", on_click=files_uploaded)





