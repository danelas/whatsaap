import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# WhatsApp API configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

# Webhook verification endpoint
@app.get('/webhook')
def verify_webhook():
    """
    Webhook verification endpoint that Facebook will hit to verify your webhook.
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK_VERIFIED')
            return challenge, 200
        else:
            return 'Verification token mismatch', 403
    return 'Bad Request', 400

# Webhook endpoint for receiving messages
@app.post('/webhook')
def webhook():
    """
    Endpoint for receiving WhatsApp messages.
    """
    data = request.get_json()
    
    # Check if this is a WhatsApp message
    if 'object' in data and 'entry' in data:
        try:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    value = change.get('value')
                    if 'messages' in value:
                        for message in value['messages']:
                            if message['type'] == 'text':
                                handle_message(message)
            return jsonify({'status': 'ok'}), 200
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

def handle_message(message):
    """
    Process incoming message and generate a response using OpenAI.
    """
    sender_phone = message['from']
    message_body = message['text']['body']
    
    try:
        # Generate response using OpenAI
        system_prompt = (
            "You are a friendly and helpful assistant for Gold Touch Mobile Massage. "
            "Always respond in a warm, professional, and helpful manner. Use emojis occasionally to sound friendly.\n\n"
            "Here are specific responses to use for common questions:\n\n"
            "Greeting (when someone says hi/hello):\n"
            "'Hi there! 😊 How can I help?'\n\n"
            "Availability:\n"
            "'Hi! Yes, I am available. The quickest and easiest way to book is at goldtouchmobile.com/providers 😊'\n\n"
            "Pricing:\n"
            "'🚗 Mobile (we come to you):\n"
            "60 min - $150\n"
            "90 min - $200\n\n"
            "🏡 In-Studio:\n"
            "60 min - $120\n"
            "90 min - $170'\n\n"
            "Services Offered:\n"
            "'We offer Swedish, Deep tissue, Reflexology, Sports Massage, and more. What type are you interested in?'\n\n"
            "Location:\n"
            "'Hi, I do mobile service. Other massage providers I work with offer in-studio appointments, but not all. "
            "You can check who offers studio sessions at goldtouchmobile.com/providers.'\n\n"
            "For any other questions, respond helpfully while maintaining our friendly and professional tone. "
            "Always try to guide users to goldtouchmobile.com/providers for booking."
        )
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_body}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        # Get the generated response
        ai_response = response.choices[0].message['content'].strip()
        
        # Send the response back to the user
        send_whatsapp_message(sender_phone, ai_response)
        
    except Exception as e:
        print(f"Error generating response: {e}")
        send_whatsapp_message(sender_phone, "Sorry, I encountered an error processing your message.")

def send_whatsapp_message(recipient_phone, message_text):
    """
    Send a WhatsApp message using the Graph API.
    """
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'messaging_product': 'whatsapp',
        'to': recipient_phone,
        'text': {'body': message_text}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending WhatsApp message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)
