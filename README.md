# PydanticAI-Koyeb

A FastAPI web application that uses PydanticAI with Ollama to process CSV files containing product data.

The application can read CSV files, query a PostgreSQL database for regional data, and apply currency exchange rates to provide comprehensive product analysis.

## Features

- **CSV File Upload**: Upload CSV files through a web interface
- **AI-Powered Processing**: Uses PydanticAI with Ollama for intelligent data processing
- **Database Integration**: Queries PostgreSQL database for regional product data
- **Currency Conversion**: Applies real-time exchange rates (USD to EUR)
- **Real-time Logging**: View processing logs in real-time
- **Background Processing**: Handles file processing asynchronously

## Prerequisites

- Python 3.8+
- Ollama installed and running
- PostgreSQL database
- Free Currency API key

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd example-pydanticai
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:

   ```env
   OLLAMA_MODEL=mistral-small:24b
   OLLAMA_BASE_URL=http://localhost:11434
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   FREE_CURRENCY_API_URL=https://api.freecurrencyapi.com
   FREE_CURRENCY_API_KEY=your_api_key_here
   ```

4. **Set up the database**
   Ensure your PostgreSQL database has a table named `regional_data` with the following schema:

   ```sql
   CREATE TABLE regional_data (
       region VARCHAR(255),
       product VARCHAR(255),
       sales INTEGER,
       amount DECIMAL(10,2)
   );
   ```

## Usage

1. **Start the application**

   ```bash
   uvicorn app:app --host 0.0.0.0
   ```

2. **Access the web interface**
   Open your browser and navigate to `http://localhost:8000`

3. **Upload and process CSV files**
   - Upload a CSV file containing product data
   - Click "Process File" to start AI-powered analysis
   - View real-time processing logs
   - The system will:
     - Read the CSV file
     - Extract product names
     - Query regional data from the database
     - Apply USD to EUR exchange rates
     - Display results in a formatted table

## Project Structure

```
PydanticAI-Koyeb/
├── app.py              # FastAPI application with web routes
├── agent.py            # PydanticAI agent implementation
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   └── upload.html    # Upload page template
└── uploads/           # Uploaded files directory (created automatically)
```

## API Endpoints

- `GET /` - Home page with file upload form
- `POST /upload` - Upload CSV file
- `POST /process` - Process uploaded file with AI agent
- `GET /log/{filename}` - Get processing logs for a file

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **PydanticAI**: AI agent framework for intelligent data processing
- **Ollama**: Local LLM inference server
- **PostgreSQL**: Database for regional data storage
- **Jinja2**: Template engine for HTML rendering
- **Pandas**: Data manipulation and CSV processing
- **HTMX**: Dynamic UI updates without JavaScript

## Environment Variables

| Variable                | Description                     | Required |
| ----------------------- | ------------------------------- | -------- |
| `OLLAMA_MODEL`          | Name of the Ollama model to use | Yes      |
| `OLLAMA_BASE_URL`       | Ollama server URL               | Yes      |
| `DATABASE_URL`          | PostgreSQL connection string    | Yes      |
| `FREE_CURRENCY_API_URL` | Free Currency API base URL      | Yes      |
| `FREE_CURRENCY_API_KEY` | Free Currency API key           | Yes      |

## CSV Format

The application expects CSV files with product data. The CSV should contain columns that can be used to identify products. Example format:

```csv
product,sales,amount
Product A,100,1500.00
Product B,75,1200.00
Product C,200,3000.00
```

## Deployment

This application is designed to be deployed on Koyeb. The FastAPI application runs on port 8000 and can be easily containerized or deployed as a serverless function.

## License

This project is licensed under the MIT License.
