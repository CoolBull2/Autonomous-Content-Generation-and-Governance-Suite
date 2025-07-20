# agents/generator/content_generator.py

from langchain_perplexity import ChatPerplexity
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from typing import Dict, Any, List
from datetime import datetime
import os
from ..base_agent import BaseAgent
from dotenv import load_dotenv
load_dotenv()


class ContentGeneratorAgent(BaseAgent):
    """Agent responsible for generating original content using Perplexity API"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ContentGenerator", config)

        # Initialize the ChatPerplexity client
        self.llm = ChatPerplexity(
            model="sonar-pro",
            temperature=0.7,
            api_key=os.getenv("PPLX_API_KEY")  # Use api_key parameter
        )

        # Initialize a local, open-source embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.knowledge_base = None
        self._setup_knowledge_base()

    def _setup_knowledge_base(self):
        """Initialize RAG knowledge base"""
        try:
            sample_docs = [
                "Content should be engaging and informative.",
                "Always fact-check claims before publishing.",
                "Use clear, concise language appropriate for the target audience.",
                "Include relevant examples and case studies when possible."
            ]

            docs = []
            for i, doc in enumerate(sample_docs):
                with open(f"temp_doc_{i}.txt", "w") as f:
                    f.write(doc)
                docs.append(f"temp_doc_{i}.txt")

            documents = []
            for doc_path in docs:
                loader = TextLoader(doc_path)
                documents.extend(loader.load())

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(documents)
            
            self.knowledge_base = FAISS.from_documents(splits, self.embeddings)
            
            for doc_path in docs:
                if os.path.exists(doc_path):
                    os.remove(doc_path)

        except Exception as e:
            self.log_activity(
                "Error setting up knowledge base", {"error": str(e)})

    def process(self, content_request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content based on the request"""
        try:
            self.log_activity("Starting content generation", content_request)

            topic = content_request.get("topic", "")

            # Use a RetrievalQA chain for RAG
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.knowledge_base.as_retriever()
            )
            # Invoke the chain with the topic as the query
            response = qa_chain.invoke(topic)
            generated_content = response.get("result", "")

            result = {
                "content": generated_content,
                "metadata": {
                    "content_type": content_request.get("type", "blog_post"),
                    "topic": topic,
                    "agent_id": self.agent_id,
                    "generation_timestamp": datetime.now().isoformat()
                },
                "status": "generated",
                "quality_score": self._calculate_quality_score(generated_content)
            }

            self.log_activity("Content generation completed", {
                              "content_length": len(generated_content)})
            return result

        except Exception as e:
            self.log_activity("Content generation failed", {"error": str(e)})
            return {"content": None, "error": str(e), "status": "failed"}

    def _calculate_quality_score(self, content: str) -> float:
        """Calculate a basic quality score for the generated content"""
        score = 0.0
        if 100 <= len(content) <= 5000:
            score += 0.3
        if content.count('.') > 0:
            score += 0.2
        if '?' in content or 'example' in content.lower():
            score += 0.2
        if len(content.split()) > 50:
            score += 0.3
        return min(score, 1.0)
