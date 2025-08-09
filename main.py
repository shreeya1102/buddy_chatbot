from dotenv import load_dotenv
import os
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



print("Hi, I am Buddy, how can I help you today")

while True:
    user_input=input("You: ")
    if user_input == "exit":
        break

    response = llm.invoke([{"role": "system", "content": system_prompt},
                           {"role": "user", "content": user_input}])
    print(f"Buddy: {response.content}")
    #print(f"Cool, thanks for sharing that {user_input}")
