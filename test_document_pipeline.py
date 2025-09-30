import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import textwrap

load_dotenv()

def test_document_pipeline():
    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
        
        # Initialize embedding model
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Create a sample document
        sample_text = """
        Retrieval Augmented Generation (RAG) is a technique that combines retrieval-based and generation-based approaches 
        for natural language processing tasks. In RAG systems, relevant information is first retrieved from a knowledge base, 
        and then used to augment the input to a language model for generating more accurate and contextually relevant responses.
        
        Key components of a RAG system include:
        1. Document Processing Pipeline
        2. Vector Database for Semantic Search
        3. Embedding Model for Text Vectorization
        4. Large Language Model for Generation
        5. Retrieval Strategy for Context Selection
        """
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
        )
        chunks = text_splitter.split_text(sample_text)
        
        print(f"Created {len(chunks)} chunks from the sample text:")
        for i, chunk in enumerate(chunks):
            print(f"\nChunk {i+1}:")
            print(textwrap.fill(chunk, width=100))
        
        # Create embeddings for chunks
        print("\nGenerating embeddings...")
        embeddings_list = embeddings.embed_documents(chunks)
        print(f"Generated {len(embeddings_list)} embeddings of dimension {len(embeddings_list[0])}")
        
        # Upload to Pinecone
        print("\nUploading vectors to Pinecone...")
        vectors = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings_list)):
            vectors.append({
                "id": f"chunk_{i}",
                "values": emb,
                "metadata": {
                    "text": chunk,
                }
            })
        
        index.upsert(vectors=vectors)
        print(f"Successfully uploaded {len(vectors)} vectors to Pinecone")
        
        # Test retrieval
        print("\nTesting retrieval...")
        query = "What are the main components of a RAG system?"
        query_embedding = embeddings.embed_query(query)
        
        results = index.query(
            vector=query_embedding,
            top_k=2,
            include_metadata=True
        )
        
        print("\nQuery Results:")
        for match in results.matches:
            print(f"\nScore: {match.score:.4f}")
            print(textwrap.fill(match.metadata["text"], width=100))
        
        return True
        
    except Exception as e:
        print(f"Error in document pipeline: {e}")
        return False

if __name__ == "__main__":
    test_document_pipeline()