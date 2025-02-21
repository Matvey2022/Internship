from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

from transformers import pipeline

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"status": "OK"}


class SummaryRequest(BaseModel):
    text: str

    @validator("text")
    def clean_text(cls, value):
        return value.replace("\r", "").replace("\n", " ").strip()


@app.post("/summarize")
async def summarize(request: SummaryRequest):
    if request.text.strip() == "":
        return {"summary": "No text provided"}
    summary = summarizer(request.text, max_length=130, min_length=30, do_sample=False)
    if not summary:
        raise HTTPException(status_code=400, detail="Summarization failed")
    return {"summary": summary[0]["summary_text"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
