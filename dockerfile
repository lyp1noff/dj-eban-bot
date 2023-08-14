FROM python:3.9

WORKDIR /app
COPY . /app/

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]