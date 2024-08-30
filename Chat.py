import streamlit as st
import openai


st.set_page_config(
    page_title="Chat",
    page_icon="👋",
)

st.title("Chat")


def setup():
    # Set up OpenAI API client
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Select GPT model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    # Initialise chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Set up default system prompt
    with open("defaultprompt.txt", "r") as file:
        defaultprompt = file.read()

    if "default_prompt" not in st.session_state:
        st.session_state["default_prompt"] = defaultprompt

    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = defaultprompt

    return client


# Function to write chat history
def write_chat_history():
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


client = setup()


# Temperature setting
def change_temp(temp):
    st.session_state["temp"] = temp

if "temp" not in st.session_state:
    st.session_state["temp"] = 1.0

temperature = st.slider("""Temperature refers to the 'randomness' or 'creativity' of the AI model's output. Lower values result in less random responses. A temperature between 0.0 and 1.0 is recommended. Select a temperature for the output: """, 0.0, 2.0, st.session_state["temp"], 0.1)

change_temp(temperature)


# Write chat history
write_chat_history()


# Chat logic
if prompt := st.chat_input("Write something here"):
    
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages_with_system_prompt = [{"role": "system", "content": st.session_state["system_prompt"]}] + [
            {"role": m["role"], "content": m["content"]}
        for m in st.session_state.chat_history
        ]

        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = messages_with_system_prompt,
            stream = True,
            temperature = st.session_state["temp"]
        )
        response = st.write_stream(stream)

    st.session_state.chat_history.append({"role": "assistant", "content": response})