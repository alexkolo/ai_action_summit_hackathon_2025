# API Documentation

A FastAPI service designed to generate refined summaries of user documents by integrating PostgreSQL, an object store, and sequential LLM processing using Mistral.

---

## Overview

This project provides an API endpoint that accepts a user social_security_number and processes the associated documents through a multi-step workflow:

1. **User 'social security number' Input**: The API receives a user social_security_number.
2. **Database Query**: It fetches document links related to the user from a PostgreSQL database.
3. **Document Retrieval**: The service retrieves the actual documents from an object store (e.g., S3, MinIO) using the obtained links.
4. **LLM Processing Stage 1**: All document content is combined with a custom prompt and sent to a Mistral LLM to generate a **COMPREHENSIVE SUMMARY**.
5. **LLM Processing Stage 2**: The comprehensive summary is then passed to another Mistral LLM call with an additional prompt to produce the **FINAL SUMMARY**.
6. **Response**: The API returns the FINAL SUMMARY as the final output to the client.

---

## Project Workflow

1. **API Request Handling**  
   - **Input**: Accept a JSON payload containing the user social_security_number.
   - **Validation**: Use Pydantic models to validate incoming data.

2. **Database Interaction**  
   - **Query**: Connect to a PostgreSQL database to retrieve user document links.
   - **Tables**:
     - **User Table**: Stores user informations.
     - **Document Table**: Stores document links associated with the user.

3. **Object Store Integration**  
   - **Fetch Documents**: Use the retrieved document links to pull the corresponding documents from an object store.

4. **First LLM Call**  
   - **Data Aggregation**: Combine the fetched documents with a predefined prompt.
   - **LLM Processing**: Send this combined payload to the Mistral LLM to generate a **COMPREHENSIVE SUMMARY**.

5. **Second LLM Call**  
   - **Refinement**: Submit the comprehensive summary with another tailored prompt to a second Mistral LLM call.
   - **Output**: Receive the **FINAL SUMMARY**.

6. **API Response**  
   - Return the FINAL SUMMARY as the response to the API request.

---

## Project Structure

The project follows a modular architecture for scalability and maintainability:

```
 
├── app/  
│   ├── __init__.py  
│   ├── main.py  # FastAPI application entry point.  
│   ├── config.py  # Loads and manages configuration from environment variables.  
│   ├── db.py  # Database connection and session management.  
│   ├── models/  
│   │   ├── __init__.py  
│   │   ├── user.py  # ORM model for users (includes social_security_number field).  
│   │   └── documents.py  # ORM model for document links associated with users.  
│   ├── schemas/  
│   │   ├── __init__.py  
│   │   ├── user_schema.py  # Pydantic schemas for validating user input.  
│   │   └── documents_schema.py  # Schemas for document link data.  
│   ├── services/  
│   │   ├── __init__.py  
│   │   ├── object_store.py  # Handles fetching documents from the object store.  
│   │   ├── llm_client.py  # Manages interaction with the Mistral LLM service.  
│   │   └── data_processor.py  # Orchestrates the overall data processing workflow.  
│   └── api/  
│       ├── __init__.py  
│       └── endpoints.py  # Defines API endpoints and request/response logic.  
├── .env  # Environment configuration file (DB credentials, object store keys, LLM API keys, etc.).  
├── requirements.txt  # List of Python dependencies.  
└── README.md  # This documentation file. 
```

---

## Features

- **User Input Handling**:  
  Securely receives and validates user social_security_number via FastAPI endpoints.

- **Database Integration**:  
  Utilizes PostgreSQL to store and retrieve user social_security_number and document links efficiently.

- **Object Store Connectivity**:  
  Fetches document content from an external object store based on stored document links.

- **Two-Stage LLM Processing**:  
  - **Stage 1 (Comprehensive Summary)**: Aggregates document data with a prompt to generate an initial summary using the Mistral LLM.
  - **Stage 2 (Final Summary)**: Refines the comprehensive summary with an additional prompt to produce a final, polished summary.
  
- **Modular Architecture**:  
  The separation into models, schemas, services, and API endpoints ensures that the project is easy to maintain, scale, and extend.

- **Configuration Management**:  
  Environment variables are managed via a `.env` file, ensuring sensitive data like DB credentials, object store keys, and LLM API keys are kept secure and configurable.

---

## Environment Configuration

The `.env` file includes all necessary configuration parameters. Key variables include:

- **Database Settings**:
  - `DB_HOST`: Hostname for the PostgreSQL server.
  - `DB_PORT`: Port for the PostgreSQL server.
  - `DB_USER`: Database username.
  - `DB_PASSWORD`: Database password.
  - `DB_NAME`: Name of the PostgreSQL database.

- **Object Store Settings**:
  - `OBJECT_STORE_URL`: Base URL for the object store.
  - `OBJECT_STORE_KEY`: API key or access token for accessing the object store.

- **LLM Settings**:
  - `LLM_API_KEY`: API key for the Mistral LLM service.
  - `LLM_ENDPOINT`: Endpoint URL for the Mistral LLM.
  - *(Additional prompt-related configuration variables can be added as required.)*

---

## Getting Started

1. **Install Dependencies**  
   Install the required packages using:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**  
   - Create a `.env` file in the root directory.
   - Populate it with the necessary configuration as outlined above.

3. **Run the Application**  
   Start the FastAPI application using:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access API Documentation**  
   Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to interact with the API through the automatically generated Swagger UI.

---

## Future Enhancements

- **Enhanced Error Handling**: Implement robust error handling and logging for improved debugging and reliability.
- **Caching Strategies**: Integrate caching mechanisms to optimize repeated document retrieval and LLM calls.
- **Security Improvements**: Strengthen authentication and authorization, especially for API endpoints and external service integrations.
- **Monitoring & Analytics**: Add tools to monitor API performance and track usage metrics.
- **Asynchronous Processing**: Leverage asynchronous I/O for database and object store interactions to improve performance under load.

---

This README provides a structured overview of the project, ensuring clarity and ease of use for developers and stakeholders.

