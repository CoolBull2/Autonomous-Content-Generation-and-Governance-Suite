import os
from dotenv import load_dotenv
# Still use OpenAIEmbeddings, but configure its base_url
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


perplexity_api_key = "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"

# Perplexity's base URL for OpenAI-compatible embedding calls
perplexity_base_url = "https://api.perplexity.ai"

# Choose a Perplexity model suitable for embeddings (check their documentation for the latest names)
# Example, check Perplexity's documentation for current embedding model names
perplexity_embedding_model = "pplx-7b-online"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)
print("OpenAIEmbeddings configured for OpenRouter successfully initialized.")





try:
            # For demo purposes, we'll create a simple knowledge base
            # In production, this would be loaded from your company's document
            sample_docs = [
                "Content should be engaging and informative.",
                "Always fact-check claims before publishing.",
                "Use clear, concise language appropriate for the target audience.",
                "Include relevant examples and case studies when possible."
            ]

            # Create temporary text files
            docs = []
            for i, doc in enumerate(sample_docs):
                with open(f"temp_doc_{i}.txt", "w") as f:
                    f.write(doc)
                docs.append(f"temp_doc_{i}.txt")

            # Load and split documents
            documents = []
            for doc_path in docs:
                loader = TextLoader(doc_path)
                documents.extend(loader.load())

            text_splitter =RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=0)
            splits = text_splitter.split_documents(documents)
            # list_of_strings = [doc.page_content for doc in splits]
            print(type(splits)) 
           
            # Create vector store
            knowledge_base = FAISS.from_documents(splits, embeddings)
            print("✅ Knowledge base initialized with sample documents.")
            # Clean up temporary files
            for doc_path in docs:
                if os.path.exists(doc_path):
                    os.remove(doc_path)

except Exception as e:
    print("Error setting up knowledge base", {"error": str(e)})