# from dotenv import load_dotenv
# import os
# import difflib
# import requests
# from bs4 import BeautifulSoup
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_groq import ChatGroq

# def questionAndAnswer(url , question):
    

#     chat = ChatGroq(
#         temperature=0,
#         groq_api_key=os.getenv("GROQ_API_KEY"),
#         model_name="mixtral-8x7b-32768"
#     )

#     system = (
#         "You are a helpful assistant trained to provide information strictly based on a predefined knowledge base provided by the website. "
#         "Do not generate any answers beyond what is available in the knowledge base. "
#         "If the user's question closely matches any part of the knowledge base, you should return the relevant information from it. "
#         "If the question does not match anything in the knowledge base, you must reply with: 'Sorry, I could not help you with that.' "
#         "Do not make assumptions or provide general knowledge outside the given data. "
#         "Only answer questions that are related to the content available on the website."
#     )

#     human = "{text}"
#     prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
#     chain = prompt | chat

#     def fetch_website_data(url):
#         response = requests.get(url)
#         if response.status_code != 200:
#             return "Sorry, I couldn't fetch data from this URL."

#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = soup.find_all('p')
#         website_text = ' '.join([para.get_text() for para in paragraphs])
#         return website_text

#     def load_knowledge_base(url):
#         website_data = fetch_website_data(url)
#         knowledge_base = website_data.split("\n")
#         return knowledge_base

#     def process_query(user_input, url):
#         knowledge_base = load_knowledge_base(url)
#         user_query = user_input
#         best_match = difflib.get_close_matches(user_query, knowledge_base, n=1, cutoff=0.9)
#         if best_match:
#             return best_match[0]

#         response = chain.invoke({"text": user_input})
#         return response.content


#     result = process_query(question, url)
#     print(result)

#     return result


import requests
from bs4 import BeautifulSoup
from clarifai.client.model import Model

def fetch_content_from_website(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the main text content (customize this based on the website structure)
        content = soup.get_text(separator="\n", strip=True)
        return content
    except Exception as e:
        return f"Error fetching content from the website: {e}"

def ask_question_from_knowledge_base(content, question):
    # Define the prompt
    knowledge_base_prompt = f"""[INST] I have the following knowledge base:- [KNOWLEDGE_BASE]{content}[END_KNOWLEDGE_BASE]
Based on this knowledge base, please answer the following question concisely:
[QUESTION]{question}[/QUESTION]
Only return the answer without any extra information or explanation. Do not prepend anything like "The answer is".[/INST]"""
    
    # Model details
    model_url = "https://clarifai.com/openai/chat-completion/models/gpt-4-turbo"
    model = Model(url=model_url, pat="de242f3fc61f4e5b9388c9dc7fe7b0a9")
    
    # Make prediction
    try:
        model_prediction = model.predict_by_bytes(knowledge_base_prompt.encode(), input_type="text")
        return model_prediction.outputs[0].data.text.raw
    except Exception as e:
        return f"Error occurred: {e}"

# # Example usage
# website_url = "https://example.com"  # Replace with the actual URL
# question = "What is the main purpose of this website?"

# # Fetch content from the website

def questionAndAnswer(url , question):
    knowledge_base = fetch_content_from_website(url)

    print(knowledge_base)
    answer = ask_question_from_knowledge_base(knowledge_base, question)
    print("answer is" , answer)
    return answer

# # Ask the question
# if "Error" not in knowledge_base:  # Proceed only if content was fetched successfully
#     answer = ask_question_from_knowledge_base(knowledge_base, question)
#     print(answer)
# else:
#     print(knowledge_base)
