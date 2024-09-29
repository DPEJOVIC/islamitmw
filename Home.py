import streamlit as st


st.title("System Prompt")


# If the user has submitted their prompt, then do not execute the rest of the Python file.
if "prompt_saved" not in st.session_state:
    st.session_state["prompt_saved"] = False

if st.session_state["prompt_saved"]:
    st.write("Please upload your context files in the File Upload tab. Reload the webpage to start again.")
    exit()


st.write("Change the system prompt here, and click 'Submit' when ready. Then, upload files for the chatbot to use as context in the File Upload tab.")
st.write("\nOnce submitted, the system prompt cannot be changed. To start again, please reload the webpage.")


# Read default system prompt
with open("systemprompt.txt", "r") as file:
    systemprompt = file.read()

# Edit system prompt
sysprompt = st.text_area(
    "Change the system prompt below:",
    systemprompt,
    height = 200,
    key = "sysprompt",
)

# Activates once the user submits their edited prompt
def submit_sys_prompt():
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = ""

    # Save the updated system prompt to the session state
    st.session_state["system_prompt"] = sysprompt

    # Change the prompt_saved variable in the session state to stop execution of this file on rerun
    st.session_state["prompt_saved"] = True


st.button("Submit", on_click=submit_sys_prompt)