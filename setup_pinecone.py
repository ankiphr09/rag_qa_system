import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def setup_pinecone_index():
    try:
        # Initialize Pinecone client
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        # List existing indexes
        existing_indexes = pc.list_indexes()
        print(f"Available Pinecone indexes: {existing_indexes.names()}")
        
        # Get index details
        index_name = os.getenv("PINECONE_INDEX_NAME", "document-qa")
        if index_name in existing_indexes.names():
            index = pc.describe_index(index_name)
            print(f"\nIndex details:")
            print(f"Name: {index.name}")
            print(f"Dimension: {index.dimension}")
            print(f"Metric: {index.metric}")
            print(f"Status: {index.status}")
        return True
        
    except Exception as e:
        print(f"Error setting up Pinecone index: {e}")
        return False
        
        return True
    
    except Exception as e:
        print(f"Error setting up Pinecone index: {e}")
        return False

if __name__ == "__main__":
    setup_pinecone_index()