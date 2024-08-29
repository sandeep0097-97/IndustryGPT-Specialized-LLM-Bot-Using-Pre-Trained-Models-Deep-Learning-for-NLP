import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(page_title="💬 Finance Chatbot")

# Sidebar content
with st.sidebar:
    st.title('💬 Finance Chatbot')
    st.write('This chatbot uses a fine-tuned Llama-2-7b model for finance-related queries.')
    ngrok_url = st.text_input('Enter ngrok URL:', value="http://localhost:5000")

if not ngrok_url:
    st.warning('Please enter the ngrok URL!', icon='⚠️')

# Function to generate response
def generate_response(prompt_input):
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": prompt_input}
    response = requests.post(f"{ngrok_url}/generate", headers=headers, data=json.dumps(payload))
    try:
        response_json = response.json()
        return response_json['generated_text']
    except json.JSONDecodeError:
        st.error("Error decoding JSON response")
        st.write("Response text:", response.text)
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error making request: {str(e)}")
        return None

# Initialize chat messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat history function
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Sidebar button to clear chat history
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Input field for the prompt
if prompt := st.chat_input("Enter your message:", disabled=not ngrok_url):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate response if the last message is from the user
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            if response:
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
