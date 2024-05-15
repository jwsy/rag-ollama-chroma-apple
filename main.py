import gradio as gr
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
# from langchain.output_parsers import PydanticOutputParser
from langchain_text_splitters.character import CharacterTextSplitter

# Run Ollama locally before
#   OLLAMA_HOST=0.0.0.0 ollama serve


local_ollama = 'http://192.168.86.33:11434'
# Be sure to `ollama pull nomic-embed-text' and the model you desire below. This was also tested with mistral:7b
local_model = 'llama3:8b'

# Adapted from https://mer.vin/2024/02/ollama-embedding/

def process_input(urls, question):
    model_local = ChatOllama(
        base_url=local_ollama,
        model=local_model
    )
    
    # Convert string of URLs to list
    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]
    
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)
    # local_embedding = embeddings.ollama.OllamaEmbeddings(
    local_embedding = embeddings.OllamaEmbeddings(
        model='nomic-embed-text',
        base_url=local_ollama
    )
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=local_embedding
    )
    retriever = vectorstore.as_retriever()

    after_rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )
    return after_rag_chain.invoke(question)

# Define Gradio interface
iface = gr.Interface(fn=process_input,
                     inputs=[gr.Textbox(label="Enter URLs separated by new lines"), gr.Textbox(label="Question")],
                     outputs="text",
                     title="Document Query with Ollama",
                     description="Enter URLs and a question to query the documents.")
iface.launch()
