import os
import requests

class Return_Object:
    def __init__(self, json):
        self.json = json
        self.ok = json.get('ok')
        result = json.get('result')
        if type(result) == dict:
            self.message_id = result.get('message_id')
            self.date = result.get('date')
            self.text = result.get('text')
            from_ = result.get('from')
            if from_ is not None:
                self.from_id = from_.get('id')
                self.from_is_bot = from_.get('is_bot')
                self.from_first_name = from_.get('first_name')
                self.from_username = from_.get('username')
            chat_ = json['result'].get('chat')
            if chat_ is not None: 
                self.chat_id = chat_.get('id')
                self.chat_first_name = chat_.get('first_name')
                self.chat_username = chat_.get('username')
                self.chat_type = chat_.get('type')
        elif type(result) == bool:
            pass
            # print(json)
        else:
            self.error_code = json.get('error_code')
            self.description = json.get('description')

            
    def __str__(self):
        string = ""
        if self.ok:
            string += f"message_id: {self.message_id}, date: {self.date}, text: {self.text}"
        else:
            string = f"error_code: {self.error_code}, description: {self.description}"
        return string

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, text, chat_id=None):
        chat_id = chat_id or self.chat_id
        url = f"{self.url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, data=data)
        return Return_Object(response.json())


    def send_photo(self, photo, caption=None, chat_id=None):
        chat_id = chat_id or self.chat_id
        response = []
        url = f"{self.url}/sendPhoto"
        data = {
            "chat_id": chat_id, 
        }
        if caption:
            data["caption"] = caption
        if type(photo) == str:
            with open(photo, 'rb') as f:
                files = {'photo': f}
                response = requests.post(url, data=data, files=files)
        else:
            files = {'photo': ('photo.jpg', photo, 'image/jpeg')}
            response = requests.post(url, data=data, files=files)
        response = Return_Object(response.json())
        if not response.ok:
            print(response)
        return response

    def send_sticker(self, sticker_relative_path, chat_id=None):
        chat_id = chat_id or self.chat_id
        url = f"{self.url}/sendSticker"
        data = {"chat_id": chat_id}

        # Den Stickerpfad relativ zur aufrufenden Datei auflösen
        caller_dir = os.path.dirname(os.path.abspath(__file__))
        sticker_path = os.path.abspath(os.path.join(caller_dir, sticker_relative_path))

        # Prüfen, ob der Sticker existiert
        if not os.path.isfile(sticker_path):
            raise FileNotFoundError(f"Sticker not found at path: {sticker_path}")

        # Sticker senden
        with open(sticker_path, 'rb') as f:
            files = {'sticker': f}
            response = requests.post(url, data=data, files=files)

        return Return_Object(response.json())

    def edit_message_text(self, message_id, text, chat_id=None):
        chat_id = chat_id or self.chat_id
        url = f"{self.url}/editMessageText"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
        }
        response = requests.post(url, data=data)
        return Return_Object(response.json())

        
    def edit_message_photo(self, message_id, photo, caption=None, chat_id=None):
        chat_id = chat_id or self.chat_id

        url = f"{self.url}/editMessageMedia"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        
        data['media'] = f'{{"type":"photo", "media":"attach://photo"}}'
        if caption:
            data['media'] = data['media'][:-1] + f', "caption":"{caption}"}}'

        if type(photo) == str:
            with open(photo, 'rb') as f:
                files = {'photo': f}
                response = requests.post(url, data=data, files=files)
        else:
            files = {'photo': ('photo.jpg', photo, 'image/jpeg')}
            response = requests.post(url, data=data, files=files)

        response = Return_Object(response.json())
        if not response.ok:
            print(response)
        return response

    def delete_message(self, message_id, chat_id=None):
        chat_id = chat_id or self.chat_id
        url = f"{self.url}/deleteMessage"
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        response = requests.post(url, data=data)
        return Return_Object(response.json())
    
    def get_updates(self, offset=None):
        params = {"offset": offset} if offset else {}
        response = requests.get(f"{self.url}/getUpdates", params=params)
        if response.status_code == 200:
            return Return_Object(response.json())
        return None
    
    def add_webhook(self, url):
        '''
        Set webhook to receive updates via POST requests.

        Args:
            url (str): The URL to send the POST requests to. Must be HTTPS.

        Returns:
            Return_Object: The response from the Telegram API as a structured object.

        ## Documentation:
            This method configures a webhook for the Telegram bot. When the webhook
            is set, Telegram will send all updates (e.g., messages, callbacks) to the
            provided URL via POST requests. The URL must be accessible via HTTPS.

            If the webhook is successfully set, the bot will no longer rely on polling 
            (`getUpdates`) to receive updates. The webhook must be handled server-side, 
            with an endpoint capable of processing Telegram updates.

        ### Example Usage:
            bot = TelegramBot(token="YOUR_TOKEN")
            response = bot.add_webhook("https://your-server.com/webhook")
            print(response)

        ### Notes:
            - Ensure your server is properly configured with an HTTPS certificate.
            - To remove the webhook and revert to polling, use `deleteWebhook`.

        ### API Reference:
            - https://core.telegram.org/bots/api#setwebhook
        '''
        response = requests.get(f"{self.url}/setWebhook?url={url}")
        return Return_Object(response.json())

    def remove_webhook(self):
        '''Remove webhook to stop receiving updates via POST requests'''
        response = requests.post(f"{self.url}/deleteWebhook")
        return Return_Object(response.json())