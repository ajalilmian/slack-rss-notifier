FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# ENV TIMER_INTERVAL=120
# ENV SLACK_OAUTH_TOKEN=
# ENV SLACK_CHANNEL=
# ENV RSS_FEED_URL=

CMD ["python", "app.py"]
