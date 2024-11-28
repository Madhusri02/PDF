from dotenv import load_dotenv
import os
import difflib
import requests
from bs4 import BeautifulSoup
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

def questionAndAnswer(url , question):
    

    chat = ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="mixtral-8x7b-32768"
    )

    system = (
        "You are a helpful assistant trained to provide information strictly based on a predefined knowledge base provided by the website. "
        "Do not generate any answers beyond what is available in the knowledge base. "
        "If the user's question closely matches any part of the knowledge base, you should return the relevant information from it. "
        "If the question does not match anything in the knowledge base, you must reply with: 'Sorry, I could not help you with that.' "
        "Do not make assumptions or provide general knowledge outside the given data. "
        "Only answer questions that are related to the content available on the website."
    )

    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | chat

    def fetch_website_data(url):
        response = requests.get(url)
        if response.status_code != 200:
            return "Sorry, I couldn't fetch data from this URL."

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        website_text = ' '.join([para.get_text() for para in paragraphs])
        return website_text

    def load_knowledge_base(url):
        website_data = fetch_website_data(url)
        knowledge_base = website_data.split("\n")
        return knowledge_base

    def process_query(user_input, url):
        knowledge_base = load_knowledge_base(url)
        user_query = user_input
        best_match = difflib.get_close_matches(user_query, knowledge_base, n=1, cutoff=0.3)
        if best_match:
            return best_match[0]

        response = chain.invoke({"text": user_input})
        return response.content


    result = process_query(question, url)
    print(result)

    return result
