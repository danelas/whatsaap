# WhatsApp OpenAI Bot

A WhatsApp bot that uses OpenAI's API to respond to messages. This bot integrates with the WhatsApp Business API via the Graph API.

## Prerequisites

1. Python 3.8 or higher
2. A Facebook Developer Account with WhatsApp Business API access
3. An OpenAI API key
4. Ngrok or a similar service for local development (to expose your local server to the internet)

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual credentials.

## Configuration

Update the following environment variables in the `.env` file:

- `WHATSAPP_TOKEN`: Your WhatsApp Business API token
- `WHATSAPP_PHONE_NUMBER_ID`: Your WhatsApp Business phone number ID
- `VERIFY_TOKEN`: A secret token for webhook verification
- `OPENAI_API_KEY`: Your OpenAI API key

## Running the Bot

1. Start the Flask server:
   ```
   python app.py
   ```

2. Expose your local server to the internet using ngrok:
   ```
   ngrok http 5000
   ```

3. Set up your webhook in the Facebook Developer Console:
   - Go to your WhatsApp app settings
   - Under "Webhook," enter your ngrok URL followed by `/webhook`
   - Set the Verify Token to match your `VERIFY_TOKEN` in the `.env` file
   - Subscribe to the messages webhook

## Usage

1. Send a message to your WhatsApp Business number
2. The bot will respond using OpenAI's API

## Security Notes

- Never commit your `.env` file to version control
- Use environment variables for all sensitive information
- Implement proper error handling and logging in production
- Consider adding rate limiting and authentication for the webhook endpoint

## License

MIT
