FROM python:3.10-slim

WORKDIR /app

RUN pip install fastapi uvicorn numpy pydantic

COPY api.py .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
