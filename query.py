import argparse
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings


#ollama pull nomic-embed-text
def get_embedding_function():
    embeddings = OllamaEmbeddings(model = "nomic-embed-text")
    return embeddings

CHROMA_PATH = "wikidb"

PROMPT_TEMPLATE = """
Απαντα την επομενη ερωτηση μονο με δεδομενα που θα σου παραθεσω παρακατω στα Ελληνικα.
Αν δεν γνωριζεις την απαντηση με βαση αυτα τα δεδομενα, πες 'Δεν γνωριζω' και μην προσπαθησεις να μαντεψεις.

{context}

---

Απαντα την επομενη ερωτηση του χρηστη: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = Ollama(model="llama3.2:latest", temperature=0.0)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()