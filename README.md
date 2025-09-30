# RAG Q&A System

This project implements a Retrieval Augmented Generation (RAG) system for enterprise document question-answering. The system leverages modern cloud technologies and machine learning to provide accurate, context-aware responses to user queries about organizational documents.

## Features

- **Document Processing**: Efficient processing and vectorization of documents
- **Vector Search**: Fast similarity search using Pinecone
- **Document Storage**: MongoDB for storing and managing document metadata
- **RESTful API**: FastAPI-based endpoints for easy integration
- **Secure Authentication**: Built-in security features
- **Docker Support**: Containerized deployment ready

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Vector Database**: Pinecone
- **Document Store**: MongoDB
- **LLM Integration**: OpenAI API
- **Containerization**: Docker

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- MongoDB
- Pinecone Account
- OpenAI API Key

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/ankiphr09/rag_qa_system.git
cd rag_qa_system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
MONGODB_CONNECTION_STRING=your_mongodb_connection_string
```

## Project Structure

```
rag_qa_system/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── services/
│   │   └── rag_service.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── setup_pinecone.py
├── test_connections.py
└── test_document_pipeline.py
```

## Getting Started

1. Test your connections:
```bash
python test_connections.py
```

2. Initialize Pinecone:
```bash
python setup_pinecone.py
```

3. Run the test pipeline:
```bash
python test_document_pipeline.py
```

## Docker Deployment

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

2. Access the API at `http://localhost:8000`

## API Endpoints

- `POST /api/v1/query`: Submit a question to the RAG system
- `POST /api/v1/documents`: Upload new documents for processing
- `GET /api/v1/documents`: List processed documents
- Additional endpoints documented in the API documentation

## API Documentation

Once the service is running, view the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - ankiphr09@gmail.com
Project Link: https://github.com/ankiphr09/rag_qa_system
