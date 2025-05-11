# E-Commerce Assistant Chatbot

This repository contains a full-stack chatbot solution for an e-commerce assistant, built with FastAPI microservices and a Streamlit frontend. The chatbot can answer user queries about products and order history, using retrieval-augmented generation (RAG) with product data.

## Project Structure

- **product_service/**: FastAPI service for searching products. Uses a sentence-transformer model to perform semantic search on product descriptions.
- **order_service/**: FastAPI service for retrieving order data. Wraps a mock API around provided order history CSV.
- **chat_service/**: FastAPI service that handles user queries, fetches data from the above services, and uses an LLM (OpenAI GPT-3.5) to generate natural language responses.
- **frontend/**: Streamlit app that provides a chat interface to interact with the assistant.
- `docker-compose.yml`: Orchestrates all services with Docker Compose.

## Setup Instructions

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
- (Optional) An OpenAI API key for GPT-3.5 Turbo. If not available, the chat responses will be placeholders.

### Running with Docker Compose

1. Clone the repository and navigate to its directory.
2. Place the provided CSV datasets (`Product_Information_Dataset.csv` and `Order_Data_Dataset.csv`) into the `product_service/` and `order_service/` directories respectively.
3. In `docker-compose.yml`, replace `YOUR_OPENAI_API_KEY` with your actual OpenAI key, or set it in a `.env` file.
4. Build and start all services:
   ```bash
   docker-compose up --build
