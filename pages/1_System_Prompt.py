import streamlit as st


st.title("System Prompt")


def setdefaultprompt():
    with open("defaultprompt.txt", "r") as file:
        defaultprompt = file.read()

    if "default_prompt" not in st.session_state:
        st.session_state["default_prompt"] = defaultprompt

    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = defaultprompt

setdefaultprompt()


defaultprompt = st.session_state["default_prompt"]


def clearhistory(): 
    st.session_state["chat_history"] = []


sysprompt = st.text_area(
    "Change the system prompt below:",
    st.session_state["system_prompt"],
    height = 400,
    key = "sysprompt",
    on_change = clearhistory
)


def save():
    st.session_state["system_prompt"] = sysprompt

save()


def resetsysprompt():
    st.session_state["system_prompt"] = defaultprompt
    clearhistory()

st.button("Reset prompt", on_click=resetsysprompt)