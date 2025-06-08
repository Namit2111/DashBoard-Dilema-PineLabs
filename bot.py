import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config.config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
from main import run_nl_to_sql_pipeline

# Load your credentials
SLACK_BOT_TOKEN = SLACK_BOT_TOKEN  # starts with xoxb-
SLACK_APP_TOKEN = SLACK_APP_TOKEN  # starts with xapp-

# Initialize your app in Socket Mode
app = App(token=SLACK_BOT_TOKEN)

# Respond when the bot is mentioned
@app.event("app_mention")
def handle_mention(event, say):
    user = event["user"]
    text = event.get("text", "")
    result = run_nl_to_sql_pipeline(text,debug=True)
    # say(f"<@{user}> you said: `{text}`")
    say(f"<@{user}> The result is: \n\n{result}")

# Optional: respond to messages in channels the bot is in
@app.message("hi")
def handle_hi(message, say):
    user = message['user']
    say(f"Hello <@{user}>! 👋")

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
