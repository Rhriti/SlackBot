import os
from flask import Flask, request , make_response

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Slack app and OpenAI client
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
handler = SlackRequestHandler(app)
flask_app = Flask(__name__)

# Define categories and their Slack channel IDs (replace with real IDs)
CHANNELS = {
    "founder-sourcing": os.environ.get("FOUNDER_CHANNEL_ID"),
    "candidate-sourcing": os.environ.get("CANDIDATE_CHANNEL_ID"),
    "marketing-ideas-finding": os.environ.get("MARKETING_FINDING_IDEAS_CHANNEL_ID"),
    "marketing-pitch": os.environ.get("MARKETING_PITCH_CHANNEL_ID"),
}

FEW_SHOT_PROMPT = """
<your_job>
Classify the following message into one of these categories: founder-sourcing, candidate-sourcing, marketing-ideas-finding, marketing-pitch.
</your_job>


Make decision based on the content of the message and the categories, here's a little guide that can assist you in decision making
<logic>
1. If the message is about finding co-founders, high-level company strategy, internal operations, leadership, or investor relations, classify it as "founder-sourcing".
2. If the message is about a job candidate, hiring processes, or recruitment, classify it as "candidate-sourcing".
3. If the message is about marketing research, competitive insights, user feedback for marketing, or brainstorming new marketing campaigns and ideas, classify it as "marketing-ideas-finding".
4. If the message is about creating or executing specific promotional content, planning a marketing campaign, or launching an A/B test, classify it as "marketing-pitch"
</logic>

<Example>
----------------founder-sourcing----------------

Text: "Let’s revisit our 12-month runway plan."
Label: "founder-sourcing"

Text: "Should we go solo to this accelerator or apply as a team?"
Label: "founder-sourcing"

Text: "What’s our default decision rule when we disagree?"
Label: "founder-sourcing"

-----------------candidate-sourcing----------------

Text: "Found a cool DevRel on Twitter who knows our stack inside out."
Label: "candidate-sourcing"

Text: "Next round — can we do “build a tiny feature” live?"
Label: "candidate-sourcing"

Text: "Had to drop a great candidate because we were too slow 😞"
Label: "candidate-sourcing"

----------------marketing-ideas-finding-----------

Text: "Users seem to love using us for side projects — lean into that?"
Label: "marketing-ideas-finding"

Text: "Should we make a “Switching from X” guide like Notion did?"
Label: "marketing-ideas-finding"

Text: "Landing page needs better above-the-fold copy."
Label: "marketing-ideas-finding"

----------------marketing-pitch----------------

Text: "Just repurposed that blog post into a Twitter carousel."
Label: "marketing-pitch"

Text: "Working on a case study titled “From Notion Doc to $10K MRR.”"
Label: "marketing-pitch"

Text: "We should test plain-text emails vs HTML ones."
Label: "marketing-pitch"

-----------------end of example----------------

</Example>

Message: {message}

<important>
Output only the category name.
</important>
"""

def classify_message(message):

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": FEW_SHOT_PROMPT.format(message=message)}],
            max_tokens=10,
        )
        category = response.choices[0].message.content.strip().lower()
        return category
    except Exception as e:
        print(f"Error classifying message: {e}")
        return None


# Slack message event handler
@app.event("message")
def handle_message(event, say, client):
    if "channel" in event and event["channel"] == os.environ["SOURCE_CHANNEL_ID"] and "bot_id" not in event:
        text = event.get("text", "")
        if not text:
            return

      
        category= classify_message(text)
        if not category:
            print("No category returned from classification.")
            return
        print(f"Classified category: {category}")

        try:
            target_channel = CHANNELS.get(category)
        except:
            return 
        client.chat_postMessage(channel=target_channel, text=f"*[Auto-sorted from #general]*\n{text}")
        say(text=f"Message sorted to #{category}", channel=event["channel"])

# Flask route to receive Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # URL Verification: Echo back the challenge
    if request.headers.get("Content-Type") == "application/json":
        data = request.get_json()
        if "challenge" in data:
            return make_response(data["challenge"], 200, {"content_type": "text/plain"})
    
    # Pass everything else to the Slack handler
    return handler.handle(request)

# Flask health check
@flask_app.route("/", methods=["GET"])
def home():
    return "Slack Bot is running!"

# Run Flask app
if __name__ == "__main__":
    flask_app.run(port=int(os.environ.get("PORT", 3000)))
