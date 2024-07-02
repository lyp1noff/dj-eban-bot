FROM python:3.9-alpine

WORKDIR /app
COPY . /app/

# RUN apk add --no-cache ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]