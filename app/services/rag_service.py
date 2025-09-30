from typing import List, Dict, Any
import pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from ..core.config import settings

class RAGService:
    def __init__(self):
        # Initialize embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Initialize Pinecone
        pinecone.init(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENVIRONMENT
        )
        
        # Get or create index
        if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
            pinecone.create_index(
                name=settings.PINECONE_INDEX_NAME,
                dimension=768,  # matches the embedding dimension
                metric="cosine"
            )
        
        self.index = pinecone.Index(settings.PINECONE_INDEX_NAME)
        self.vectorstore = Pinecone(
            self.index, self.embeddings.embed_query, "text"
        )
        
        # Initialize LLM
        self.llm = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )
        
        # Initialize QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    async def process_document(self, file_path: str, metadata: Dict[str, Any]) -> bool:
        """Process and index a document"""
        try:
            # Load document based on file type
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith('.txt'):
                loader = TextLoader(file_path)
            elif file_path.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
            else:
                raise ValueError("Unsupported file type")
            
            documents = loader.load()
            
            # Split documents
            texts = self.text_splitter.split_documents(documents)
            
            # Add metadata
            for text in texts:
                text.metadata.update(metadata)
            
            # Add to vector store
            self.vectorstore.add_documents(texts)
            
            return True
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            return False
    
    async def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system"""
        try:
            # Get answer from QA chain
            result = self.qa_chain({"query": question})
            
            # Get source documents
            docs = self.vectorstore.similarity_search(question, k=3)
            sources = [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
            
            return {
                "answer": result["result"],
                "sources": sources
            }
        except Exception as e:
            print(f"Error querying RAG system: {str(e)}")
            return {
                "answer": "Sorry, I couldn't process your question.",
                "sources": []
            }