# Summarizer LLM

This project is a monorepo containing a React frontend and a Flask backend for a document summarization application.

## Prerequisites

Before you begin, ensure you have the following installed:
- Node.js and npm (for React frontend)
- Python 3.x and pip (for Flask backend)
- Git

## Clone the Repository

1. Open a terminal or command prompt.
2. Clone the repository:

```git clone https://github.com/jayantsinghjhala/Summarizer_LLM.git```
```cd Summarizer_LLM```

## Frontend Setup

1. Navigate to the React frontend directory:

```cd react_frontend```

2. Install dependencies:

```npm install```

3. Start the development server:

```npm start```

The frontend should now be running on `http://localhost:3000`.

## Backend Setup

1. Navigate to the Flask backend directory:

```cd ../flask_backend```

2. Create a virtual environment:

```python -m venv venv```

3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install dependencies:

```pip install -r requirements.txt```

5. Start the Flask server:

```flask run```

The backend should now be running on `http://localhost:5000`.

## Usage

With both the frontend and backend running, you can now use the application by opening a web browser and navigating to `http://localhost:3000`.


