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


# Custom Pastel CSS
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, .gradio-container {
    height: 100%;
    margin: 0;
    background: linear-gradient(135deg, #fce4ec 0%, #e8f5e8 25%, #e1f5fe 50%, #fff3e0 75%, #f3e5f5 100%);
    font-family: 'Poppins', sans-serif;
}

.gradio-container {
    background-attachment: fixed;
    min-height: 100vh;
}

/* Main container styling */
.contain {
    background: rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(10px);
    border-radius: 25px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 8px 32px rgba(255, 192, 203, 0.2) !important;
    margin: 10px !important;
    max-height: 95vh !important;
    overflow: hidden !important;
}

/* Header styling */
h1 {
    background: linear-gradient(45deg, #ff9a9e, #fecfef, #fecfef) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}

/* Chatbot container */
#chatbot {
    background: rgba(255, 255, 255, 0.4) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 182, 193, 0.3) !important;
    box-shadow: inset 0 2px 10px rgba(255, 192, 203, 0.1) !important;
    padding: 15px !important;
    backdrop-filter: blur(5px) !important;
}

/* Message bubbles */
.message-wrap {
    margin: 8px 0 !important;
}

.user {
    background: linear-gradient(135deg, #fbb6ce, #f8bbd9) !important;
    border: 1px solid rgba(251, 182, 206, 0.5) !important;
    color: #6d4c7d !important;
    border-radius: 18px 18px 5px 18px !important;
}

.bot {
    background: linear-gradient(135deg, #c8e6c9, #a5d6a7) !important;
    border: 1px solid rgba(200, 230, 201, 0.5) !important;
    color: #2e7d32 !important;
    border-radius: 18px 18px 18px 5px !important;
}

/* Input row styling */
#input-row {
    background: rgba(255, 255, 255, 0.6) !important;
    border-radius: 25px !important;
    padding: 8px !important;
    border: 1px solid rgba(255, 182, 193, 0.3) !important;
    box-shadow: 0 4px 15px rgba(255, 192, 203, 0.1) !important;
    backdrop-filter: blur(10px) !important;
}

/* Input textbox */
.gr-textbox input {
    background: transparent !important;
    border: none !important;
    color: #6d4c7d !important;
    font-size: 16px !important;
    padding: 15px 20px !important;
}

.gr-textbox input::placeholder {
    color: #b39ddb !important;
    opacity: 0.7 !important;
}

#send-btn {
    width: 50px !important;
    height: 50px !important;
    min-width: 50px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #ff9a9e, #fecfef) !important;
    color: white !important;
    font-size: 22px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 0 !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(255, 154, 158, 0.3) !important;
    transition: all 0.3s ease !important;
}

#send-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4) !important;
}

/* Clear button styling */
.gr-button[variant="secondary"] {
    background: linear-gradient(135deg, #e1bee7, #f8bbd9) !important;
    color: #6d4c7d !important;
    border: 1px solid rgba(225, 190, 231, 0.5) !important;
    border-radius: 20px !important;
    padding: 12px 25px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(225, 190, 231, 0.2) !important;
}

.gr-button[variant="secondary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(225, 190, 231, 0.3) !important;
    background: linear-gradient(135deg, #d1c4e9, #f48fb1) !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #ff9a9e, #fecfef);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #f48fb1, #e1bee7);
}

/* Loading animation */
@keyframes pastel-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(255, 154, 158, 0.3); }
    50% { box-shadow: 0 0 30px rgba(225, 190, 231, 0.5); }
}

.generating {
    animation: pastel-glow 2s infinite;
}
"""

# UI with pastel theme
page = gr.Blocks(
    title="Chat with Buddy - Pastel Edition",
    theme=gr.themes.Soft(
        primary_hue="pink",
        secondary_hue="purple",
        neutral_hue="slate",
    ),
    css=custom_css
)

with page:
    gr.Markdown(
        """
        <h1 style='text-align:center; font-size: 2.5rem; margin-bottom: 0.3rem;'>🌸 Chat with Buddy</h1>
        <p style='text-align:center; color: #8e24aa; font-size: 1rem; font-weight: 400; margin-bottom: 1rem;'>
            ✨ Your Personal Study Companion in Pastel Paradise ✨
        </p>
        """
    )

    chatbot = gr.Chatbot(
        type="messages",
        avatar_images=[None, 'buddy.png'],
        elem_id="chatbot",
        height=400,
        show_label=False
    )

    with gr.Row(elem_id="input-row"):
        with gr.Column(scale=20):
            msg = gr.Textbox(
                show_label=False,
                placeholder="Ask your Buddy anything... 💭",
                container=False
            )
        with gr.Column(scale=1, min_width=70):
            send_btn = gr.Button("✨", elem_id="send-btn")

    with gr.Row():
        clear = gr.Button("🧹 Clear Chat", variant="secondary")

    # Actions
    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    send_btn.click(chat, [msg, chatbot], [msg, chatbot])
    clear.click(clear_chat, outputs=[msg, chatbot])

page.launch(share=True)