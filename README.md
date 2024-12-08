# Integration Layer for OpenAI Service

This repository provides a FastAPI-based proxy service for integrating with OpenAI's API.

## Features

- FastAPI as a Proxy layer for the OpenAI API.
- Rename `.env.example` to `.env` and change the values as needed.
- Use docker-compose up to set up Langfuse and Postgres.

## Getting Started

1. Clone the repository and navigate to the project folder.
2. Rename `.env.example` to `.env` and update the required environment variables.
3. Start the Langfuse and database services using Docker Compose:

   docker-compose up

4. Run the FastAPI application:

   uvicorn app:app --host 0.0.0.0 --port 8000

## Endpoints

### /chat (POST)

Accepts structured requests and forwards them to OpenAI while tracking interactions with Langfuse.
