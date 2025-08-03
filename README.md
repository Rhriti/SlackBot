# Slack Message Classifier Bot

This project is a Slack bot that automatically classifies messages from a source channel into categories using OpenAI's GPT models, and forwards them to the appropriate Slack channels. It also includes tools for evaluating and visualizing the classifier's performance.

## Features
- Listens to messages in a specified Slack channel
- Classifies messages into categories (e.g., founder-sourcing, candidate-sourcing, marketing-ideas-finding, marketing-pitch)
- Forwards messages to the correct Slack channel based on classification
- Uses OpenAI GPT (configurable model)
- Includes a test suite and visualization for misclassifications

## Setup

### 1. Clone the repository
```
git clone <your-repo-url>
cd slackbot
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the project root with the following variables:
```
SLACK_BOT_TOKEN=your-slack-bot-token
SLACK_SIGNING_SECRET=your-slack-signing-secret
OPENAI_API_KEY=your-openai-api-key
SOURCE_CHANNEL_ID=your-source-channel-id
FOUNDER_CHANNEL_ID=channel-id-for-founder-sourcing
CANDIDATE_CHANNEL_ID=channel-id-for-candidate-sourcing
MARKETING_FINDING_IDEAS_CHANNEL_ID=channel-id-for-marketing-ideas-finding
MARKETING_PITCH_CHANNEL_ID=channel-id-for-marketing-pitch
```

### 4. Run the Bot
```
python app.py
```

The bot will start a Flask server and listen for Slack events.

## Testing & Evaluation
- Place your test data in `test.jsonl` (see sample format in the repo)
- Run the test suite:
```
python test.py
```
- Misclassifications will be saved to `misclassifications.jsonl` and visualized as a bar chart.

## Files
- `app.py` — Main bot logic and Flask server
- `test.py` — Test runner and visualization
- `test.jsonl` — Test dataset (JSONL format)
- `misclassifications.jsonl` — Output of misclassified predictions
- `requirements.txt` — Python dependencies
- `.env` — Environment variables (not committed)

## Notes
- Make sure your bot is invited to all target Slack channels.
- You can change the OpenAI model in `app.py` (e.g., to `gpt-4` or another available model).

## License
MIT
