import pytest
from fastapi.testclient import TestClient
from contextlib import contextmanager
from main import app


class TestService:
    def __init__(self, client):
        self.client = client

    def ping(self):
        return self.client.get("/ping")

    def summary(self, text: str):
        return self.client.post("/summarize", json={"text": text})

    @contextmanager
    def assert_response(self, response, expected_status_code: int):
        try:
            assert response.status_code == expected_status_code
            yield response.json() if response.status_code == 200 else response
        except AssertionError:
            raise AssertionError(
                f"Expected status code {expected_status_code}, but got {response.status_code}. "
                f"Response: {response.text}"
            )


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def service(client):
    return TestService(client)


def test_ping(service):
    with service.assert_response(service.ping(), 200) as response:
        assert response == {"status": "OK"}


def test_summary_valid_input(service):
    test_text = "This is a test text that needs to be summarized. So here u will be able to see how the summarization works. actually it is a test text that needs to be summarized. So here u will be able to see how the summarization works."
    with service.assert_response(service.summary(test_text), 200) as response:
        assert "summary" in response, "Response should contain 'summary' field"
        assert isinstance(response["summary"], str), "Summary should be a string"
        assert len(response["summary"]) <= len(test_text), (
            "Summary should be shorter than or equal to the original text"
        )


def test_summary_empty_input(service):
    with service.assert_response(service.summary(""), 200) as response:
        assert "summary" in response
        assert response["summary"] == "No text provided"


def test_summary_missing_text(service):
    with service.assert_response(service.client.post("/summarize", json={}), 422):
        pass


def test_summary_invalid_json(service):
    with service.assert_response(
        service.client.post("/summarize", data="invalid json"), 422
    ):
        pass
