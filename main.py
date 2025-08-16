from dotenv import load_dotenv
import os
import gradio as gr

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

gemini_key= os.getenv("GEMINI_API_KEY")
system_prompt = ("You are buddy and supposed to behave like a study partner assistant and"
                 " assist in study with a little humor added . You are supposed to assist with all the subjects asked to"
                 " teach from multiple domains . Also answer in 2-6 sentences for now")
llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key,
    temperature=0.5,
)

prompt= ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user", "{input}")]
)
chain = prompt | llm | StrOutputParser()

print("Hi, I am Buddy, how can I help you today")

history=[]
def chat(user_input,hist):
    print(user_input, hist)



    langchain_history = []
    for item in hist:
        if item['role'] == 'user':
            langchain_history.append(HumanMessage(content =item['content']))
        elif item['role'] == 'assistant':
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({"input": user_input, "history": langchain_history} )

    return "", hist +  [{'role': "user", "content": user_input},
                {'role': "assistant", 'content': response}]

def clear_chat():
    return  "",[]

page = gr.Blocks(
    title = "Chat with Buddy",
    theme = gr.themes.Soft()

)
with page:
    gr.Markdown(
        """
       Chat with Buddy
        \nWelcome to your personal Study Buddy
        """
    )
    chatbot= gr.Chatbot(type="messages",
                        avatar_images=[None, 'buddy.png'])
    msg=gr.Textbox(show_label=False, placeholder="Ask your Buddy anything...")
    msg.submit(chat, [msg, chatbot], [msg,chatbot ])
    clear = gr.Button("Clear Chat",variant = "Secondary")
    clear.click(clear_chat,outputs=[msg, chatbot])

page.launch(share=True)