import os
from dotenv import load_dotenv
from pinecone import Pinecone
from pymongo import MongoClient
import redis
from openai import OpenAI

load_dotenv()

def test_pinecone():
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        indexes = pc.list_indexes()
        print(f"Pinecone connection successful. Indexes: {indexes}")
    except Exception as e:
        print(f"Pinecone connection failed: {e}")

def test_mongodb():
    try:
        client = MongoClient(os.getenv("MONGODB_URL"))
        dbs = client.list_database_names()
        print(f"MongoDB connection successful. Databases: {dbs}")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

def test_redis():
    try:
        r = redis.from_url(os.getenv("REDIS_URL"))
        pong = r.ping()
        print(f"Redis connection successful. Ping: {pong}")
    except Exception as e:
        print(f"Redis connection failed: {e}")

def test_openai():
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        models = client.models.list()
        print(f"OpenAI connection successful. Models: {[model.id for model in models.data[:3]]}")
    except Exception as e:
        print(f"OpenAI connection failed: {e}")

if __name__ == "__main__":
    print("Testing Pinecone...")
    test_pinecone()
    print("\nTesting MongoDB...")
    test_mongodb()
    print("\nTesting Redis...")
    test_redis()
    print("\nTesting OpenAI...")