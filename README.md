# AI Agent with Rasa, Data Ingestion, and Dashboard

This project helps you create an AI agent for customer support. It includes:
- **Rasa Chatbot:** With Telegram integration (see instructions in `rasa/credentials.yml`).
- **Data Ingestion Module:** Processes uploaded files (e.g., PDFs, text files) to extract text and keywords.
- **Dashboard:** A web interface for:
  - Uploading files (with a file description field),
  - Manually triggering file processing (via a "Process Files" button),
  - Reviewing processed files,
  - Viewing integration instructions (for embedding the agent into a website or linking it to social media).
- **Prometheus Integration:** Exposes a basic metric (number of files processed) for future analytics.

## Getting Started

### Prerequisites
- Docker & Docker Compose  
- Python 3.7+ (for running the ingestion module and dashboard)

### Steps

1. **Start Docker Services:**  
   From the project root, run:
   ```bash
   docker-compose up
