import streamlit as st
import asyncio
import aiohttp


async def fetch_response(prompt):
    api_url = "http://lb-1401664878.ap-south-1.elb.amazonaws.com/tradonomy/"
    payload = {"prompt": prompt}
    headers = {"Authorization": "Bearer YOUR_API_KEY"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("result", "No response received.")
                else:
                    return f"Error: {response.status} - {await response.text()}"
    except Exception as e:
        return f"Error fetching response: {e}"

st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Typing...")


        # Fetch assistant response asynchronously
        async def get_response():
            response = await fetch_response(prompt)
            message_placeholder.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})


        asyncio.run(get_response())
