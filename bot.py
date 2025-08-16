from dotenv import load_dotenv
import os
import gradio as gr

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
system_prompt = (
    "You are buddy and supposed to behave like a study partner assistant and"
    " assist in study with a little humor added. You are supposed to assist with all the subjects asked to"
    " teach from multiple domains. Also answer in 2-6 sentences for now"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key,
    temperature=0.5,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user", "{input}")
])
chain = prompt | llm | StrOutputParser()

print("Hi, I am Buddy, how can I help you today")

# Chat function
def chat(user_input, hist):
    if not user_input.strip():
        return "", hist

    langchain_history = []
    for item in hist:
        if item['role'] == 'user':
            langchain_history.append(HumanMessage(content=item['content']))
        elif item['role'] == 'assistant':
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({"input": user_input, "history": langchain_history})

    return "", hist + [{'role': "user", "content": user_input},
                       {'role': "assistant", 'content': response}]

def clear_chat():
    return "", []

# Custom CSS
custom_css = """
html, body, .gradio-container {
    height: 100%;
    margin: 0;
    background: linear-gradient(135deg, #fdfcfb, #e6eaf3);
    font-family: 'Fira Sans', sans-serif;
}

/* Remove white background from chatbot box */
#chatbot {
    background: transparent !important;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    padding: 8px;
}

/* Input row styling */
#input-row {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 12px;
    padding: 5px;
}

/* Send button styling */
#send-btn {
    width: 45px !important;
    height: 45px !important;
    min-width: 45px !important;
    border-radius: 50% !important;
    background-color: #4a90e2 !important;
    color: white !important;
    font-size: 20px !important;
    display: flex !important;
    justify-content: center;
    align-items: center;
    padding: 0 !important;
    border: none !important;
}
"""


# UI
page = gr.Blocks(
    title="Chat with Buddy",
    theme=gr.themes.Soft(),
    css=custom_css
)

with page:
    gr.Markdown(
        """
        <h1 style='text-align:center;'>🤖 Chat with Buddy</h1>
        <p style='text-align:center;'>Welcome to your personal Study Buddy</p>
        """
    )
    chatbot = gr.Chatbot(type="messages",
                         avatar_images=[None, 'buddy.png'],
                         elem_id="chatbot")

    with gr.Row(elem_id="input-row"):
        with gr.Column(scale=20):
            msg = gr.Textbox(show_label=False, placeholder="Ask your Buddy anything...")
        with gr.Column(scale=1,min_width=60):
            send_btn = gr.Button("➤", elem_id="send-btn")

    clear = gr.Button("Clear Chat", variant="secondary")

    # Actions
    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    send_btn.click(chat, [msg, chatbot], [msg, chatbot])
    clear.click(clear_chat, outputs=[msg, chatbot])

page.launch(share=True)
