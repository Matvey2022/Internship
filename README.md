# FastAPI Text Summarization Service
## Features

* Summarization Endpoint: `/summarize`
* Health Check Endpoint: `/ping`
* Input Validation
* Comprehensive Test Suite
* Dockerized Deployment

## API Endpoints

### `/ping`

* Method: `GET`
* Description: Checks service status.
* Response: `{"status": "OK"}`

### `/summarize`

* Method: `POST`
* Request Body:
```json
{
  "text": "Text to be summarized"
}
```
- ReDoc: `http://localhost:8000/redoc`

* **`tests/test_endpoints.py`:**  Includes tests for the `/ping` and `/summarize` endpoints using `pytest` and `fastapi.testclient`.

## Dependencies

See `requirements.txt` for a complete list of dependencies.  Key dependencies include:

* `fastapi`
* `uvicorn`
* `pydantic`
* `transformers`
* `pytest`


## Future Enhancements

* **Customizable Summary Length:** Allow users to specify the desired length of the summary.
* **Different Summarization Models:**  Support other summarization models from the Transformers library.
* **Batch Summarization:**  Enable summarizing multiple texts in a single request.

