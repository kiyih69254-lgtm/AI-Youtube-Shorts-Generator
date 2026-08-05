FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator.git . && rm -rf .git

COPY requirements-hf.txt .
RUN pip install --no-cache-dir -r requirements-hf.txt

COPY app.py .
COPY .env .

RUN mkdir -p output

EXPOSE 7860

CMD ["python", "app.py"]
