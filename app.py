import feedparser
import time
import requests
import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

slack_token = os.getenv('SLACK_OAUTH_TOKEN')
slack_channel = os.getenv('SLACK_CHANNEL')

client = WebClient(token=slack_token)

timer_interval = int(os.getenv('TIMER_INTERVAL', 60))  # Default to 60 seconds if not set

rss_feed_url = os.getenv('RSS_FEED_URL')

last_entry_published  = None

def initialize_memory():
    global last_entry_published
    feed = feedparser.parse(rss_feed_url)
    if feed.entries:
        last_entry_published = feed.entries[0].published_parsed

def check_rss_and_post():
    global last_entry_published
    logger.info("Checking RSS feed for updates...")
    feed = feedparser.parse(rss_feed_url)
    if feed.entries:
        new_entries = []
        for entry in feed.entries:
            if entry.published_parsed > last_entry_published:
                new_entries.append(entry)
        
        if new_entries:
            last_entry_published = new_entries[0].published_parsed
            logger.info(f"Found {len(new_entries)} new entries")
        
        for entry in reversed(new_entries):
            post_to_slack(entry)

def post_to_slack(entry):
    try:
        response = client.chat_postMessage(
            channel=slack_channel,
            text=f"{entry.title}\n{entry.link}"
        )
        logger.info(f"Posted new entry to Slack: {entry.title}")
    except SlackApiError as e:
        logger.error(f"Error posting to Slack: {e.response['error']}")

if __name__ == "__main__":
    logger.info("Starting RSS Feed Checker")
    initialize_memory()
    while True:
        check_rss_and_post()
        time.sleep(timer_interval)
