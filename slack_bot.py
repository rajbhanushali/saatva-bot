import os
from slack_bolt import App
from langchain.vectorstores import Pinecone
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import pinecone
import requests
import json

# Initialize environment variables
load_dotenv()

# Initialize the Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),  # Use your "Bot User OAuth Access Token" here
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),  # Your Slack app's signing secret
)

# Authenticate with Pinecone DB
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV"),
)
INDEX_NAME = "saatva-bot"

# Create header object to interact with HF Inference Endpoint
HF_ENDPOINT_HEADERS = {
    'Authorization': f"Bearer {os.environ.get('HUGGINGFACE_TOKEN')}",
    'Content-Type': 'application/json',
}

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
docsearch = Pinecone.from_existing_index(INDEX_NAME, embeddings)

"""
Generates a prompt with the user's query and relevant info, and sends a request to the HuggingFace Inference Endpoint.
:param info: the documents returned by Pinecone similarity search
:param query: the user's search query
:param response: any previous response the LLM has started to generate
"""
def query_hf_llm(info, query, response):

    # Select the top 3 most relevant documents and provide them as context.
    context = ' '.join([doc.page_content for doc in info[:3]])

    prompt=PromptTemplate(
        template = 
"""You are a helpful assistant working for an online mattress company called Saatva. Your role is to answer any questions the customer may have. Be as concise as possible. Limit your answers to a few sentences. Use the context below, and if the question cannot be answered with the provided information, respond with "I don't know. Answer in the style of these examples:
===
User: What sizes and colors does the Saatva Dog Bed come in?
AI: The Saatva Dog Bed comes in Small, Medium, and Large sizes. It is available in Natural Linen, Taupe Boucle, and Slate Boucle.
===
User: Does the Saatva Classic mattress provide good support?
AI: Yes, it provides extra support where you need it most with our patented Lumbar Zone® Technology. You can enjoy healthy spinal alignment in any sleep position!
===
User: What is white glove delivery?
AI: White glove delivery is the Saatva service standard and comes free with every mattress, bedroom furniture, and rug order. While our teams don't actually wear white gloves, we do all the work for you. We hand-deliver your mattress and set it up in the room of your choice.
===
Context: {context}
===
User: {query}
AI: {response}""",
        input_variables=["context", "query", "response"],
    )
    final_prompt = prompt.format(context=context, query=query, response=response)

    json_data = {
        "inputs": final_prompt,
    }

    response = requests.post(os.environ.get('HUGGINGFACE_ENDPOINT'), headers=HF_ENDPOINT_HEADERS, json=json_data)
    if response.status_code == 200:
        print('RESPONSE', response.json()[0]['generated_text'])
        return response.json()[0]['generated_text']
    else:
        print(response.status_code)
        print(json_data)
        return 'Failed to reach model.'

# Define the message event listener
@app.event("message")
def handle_message(event, say):

    message = event["text"]
    docs = docsearch.similarity_search(message)

    final_text =  ""
    while "===" not in final_text:
        response = query_hf_llm(docs, message, final_text)
        final_text = final_text + response
        if "===" in final_text:
            final_text = final_text.split("==")[0]
            break
        elif response.strip() == "":
            break
        elif "Failed to reach" in final_text:
            final_text = "Failed to reach model."
            break

    say(final_text)

if __name__ == "__main__":
    # Start the app
    app.start(port=int(os.environ.get("PORT", 3000)))


