# FastAPI Q&A Bot using Langchain

This is a FastAPI application that utilizes Langchain to answer questions based on documents stored in the "app/experiences" folder. Each document is stored as a `.py` file containing JSON strings to be processed by Langchain.

## Project Structure

The project structure is organized as follows:

- `app/`: The main application folder.
  - `experiences/`: Contains documents in `.py` files as JSON strings to be processed.
  - `main.py`: The entry point for the FastAPI application.
  - `qa_bot.py`: Contains the code for answering questions using Langchain.

- `tests/`: Contains JSON files used for running tests against the API.

## Local Setup

To run the FastAPI application locally, follow these steps inside the repository root:

1. Create a virtual environment using `virtualenv`:

    ```bash
    virtualenv venv
    ```

2. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

3. Install the required dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4. Navigate to the `app` folder:

    ```bash
    cd app
    ```

5. Start the FastAPI application using `uvicorn`:

    ```bash
    uvicorn main:app
    ```

The API will be available at `http://localhost:8000`.

## Using the API

To get answers to questions, make a POST request to `http://localhost:8000/get_answer` with a JSON payload containing the "question" attribute. The API will respond with answers based on the provided question and documents in the "app/experiences" folder.

## API Validation

This project utilizes Pydantic to validate API calls, ensuring that the data sent to the API is in the expected format.

## Testing

You can run tests against the API using the JSON files in the `tests` folder. These test files contain sample input data for various questions to verify the functionality of your Q&A bot.

## Deployment

For deployment instructions, refer to the `deploy.md` file in the repository.

Feel free to customize this README with more specific information about your project and any additional details you'd like to provide.
