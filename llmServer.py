from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the following question only based on the data I will provide below, in Greek.
If you do not know the answer based on this data, say 'I don't know' and do not try to guess.

{context}

---

Answer the user question: {question}
"""

def get_embedding_function():
    embeddings = OllamaEmbeddings(model = "nomic-embed-text")
    return embeddings

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=10)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = Ollama(model="llama3.2:latest", temperature=0.2)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

app = Flask(__name__)
CORS(app)

@app.route("/response", methods=["POST"])
def generateAnswer():
    try:
        message = request.get_json(force=True)
        print("Received JSON Data:", message)
        final_query = query_rag(message["text"])
        #Request to Ollama and llama 3.2:latest and response
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2:latest",
            "prompt": final_query,
            "stream": False
        })
        return jsonify(response.json())

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
