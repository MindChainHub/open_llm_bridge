FROM python:3.10-slim-buster
LABEL authors="huwentao"

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app
ENV HOST=0.0.0.0
ENV PORT=9000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]