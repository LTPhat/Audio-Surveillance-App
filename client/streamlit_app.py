import streamlit as st
import json
from prompts.sample_prompt import SYSTEM_PROMPT
from groq import Groq
from dotenv import load_dotenv
import os
import time
from utils import generate_system_prompt, response_generator
import yaml
import requests
import base64

load_dotenv()
# Load YAML llm config
with open("./configs/llm_config.yaml", "r") as file:
    llm_config = yaml.safe_load(file)
#------------------Define API -----------------
client = Groq(
    api_key=os.getenv('GROQ_API_KEY'))

FASTAPI_URL = "http://localhost:8000/process_audio/"

#--------------------------------------------------------------------------------------
# Streamlit Page Configuration
st.set_page_config(
    page_title="An Intelligent Audio Analyzer",
    page_icon="./img/chatbot.jpg",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        
    }
)

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Error converting image to base64: {str(e)}")
        return None

def decorate():
        #-------------------------- START APP--------------------------------------
    title_style = """
        <style>
        .title {
            text-align: center;
            font-size: 45px;
        }
        </style>
        """
    st.markdown(
    title_style,
    unsafe_allow_html=True
    )
    title  = """
    <h1 class = "title" >SurveilAI: An Audio Analyzer for Surveillance Application</h1>
    </div>
    """
    st.markdown(title,
                unsafe_allow_html=True)
    # Insert custom CSS for glowing effect
    st.markdown(
        """
        <style>
        .cover-glow {
            width: 100%;
            height: auto;
            padding: 3px;
            box-shadow: 
                0 0 5px #819ccc,
                0 0 10px #6b89bf,
                0 0 15px #5b7dba,
                0 0 20px #496fb3,
                0 0 25px #365b9c,
                0 0 30px #295096,
                0 0 35px #174391;
            position: relative;
            z-index: -1;
            border-radius: 45px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load and display sidebar image
    img_path = "./img/chatbot.jpg"
    img_base64 = img_to_base64(img_path)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("---")
    st.sidebar.write("**SurveilAI:** An Audio Analyzer for Surveillance Application")
    st.sidebar.markdown("---")
    
    # Display basic interactions
    show_basic_info = st.sidebar.checkbox("Show Basic Interactions", value=True)
    if show_basic_info:
        st.sidebar.markdown("""
        ### Basic Interactions
        - **Upload your audio file**: Click the "Browze Files" button to upload your audio file.   
        - **Extract information**: Click "Extract information" button and wait for the information to be extracted.                         
        - **Ask anything about the audio**: Enter your question in the text box.
        """)


def main():
    decorate()

    # ============ GET INPUT AUDIO ==========================
    uploaded_file = st.file_uploader("Upload your WAV file:", type=["wav"])

    # Display the result
    st.write("Your uploaded wav file: ")
    st.audio(uploaded_file, format = 'audio/wav')

    # ============ PROCESS FILE ========================
    if "json_label" not in st.session_state:
        st.session_state.json_label = None
    if st.button("Extract information") and uploaded_file:
        with st.spinner('Extracting information from input file...'):
            st.session_state.messages = []
            start_time = time.time()
            # Get FastAPI response
            files = {"file": (uploaded_file.name, uploaded_file, "audio/wav")}
            response = requests.post(FASTAPI_URL, files=files)
            end_time = time.time()
            if response.status_code == 200:
                json_data = response.json()
                st.session_state.json_label = json_data
                st.success(f"Processing completed! Processing time: {end_time - start_time:.2f}s")
            else:
                st.error(f"Error: {response.json()}")


    # ============ PROCESS CONVERSATION ==========================
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app 
    for message in st.session_state.messages:
        if message["role"] == "user":
            # Display user message without avatar
            with st.chat_message("user", avatar="./img/person.jpg"):
                st.markdown(message["content"])
        else:
            # Display assistant message with avatar
            with st.chat_message("assistant", avatar="./img/chatbot.jpg"):
                st.markdown(message["content"])


    # Accept user input
    if prompt := st.chat_input("Enter your question here?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare conversation history for LLM
        messages_history = [{"role": "system", "content": SYSTEM_PROMPT[-1]["Intro"] + str(st.session_state.json_label) + SYSTEM_PROMPT[-1]["Outro"]}]  
        messages_history.extend(st.session_state.messages)  # Append previous messages 
        messages_history.append({"role": "user", "content": prompt})  # Add current question
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar="./img/chatbot.jpg"):
            chat_completion = client.chat.completions.create(
        messages = messages_history,
        model=llm_config['LLM_MODEL'],
        temperature=llm_config['TEMPERATURE'],
        max_tokens=llm_config['MAX_TOKENS'],
        top_p=llm_config['TOP_P'],
        stop=llm_config['STOP'],
        stream=llm_config['STREAM'],
    )
            with st.spinner('Thinking...'):
                
                llm_output_text = chat_completion.choices[0].message.content
            response = st.write_stream(response_generator(llm_output_text))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
if __name__ == "__main__":
    main()

