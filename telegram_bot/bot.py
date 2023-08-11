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

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": text,
        }
        response = requests.post(url, data=data)
        return Return_Object(response.json())

    def send_photo(self, photo, caption=None):
        response = []
        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        data = {
            "chat_id": self.chat_id,
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

    def send_sticker(self, sticker):
        response = []
        url = f"https://api.telegram.org/bot{self.token}/sendSticker"
        data = {
            "chat_id": self.chat_id,
        }
        file_path = os.path.dirname(os.path.abspath(__file__))
        sticker_folder = file_path +'/../stickers/'
        sticker = sticker_folder + sticker + '.webp'
        with open(sticker, 'rb') as f:
            files = {'sticker': f}
            response = requests.post(url, data=data, files=files)
        return Return_Object(response.json())

    def edit_message_text(self, message_id, text):
        url = f"https://api.telegram.org/bot{self.token}/editMessageText"
        data = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "text": text,
        }
        response = requests.post(url, data=data)
        return Return_Object(response.json())

        
    def edit_message_photo(self, message_id, photo, caption=None):

        url = f"https://api.telegram.org/bot{self.token}/editMessageMedia"
        data = {
            "chat_id": self.chat_id,
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

    def delete_message(self, message_id):
        url = f"https://api.telegram.org/bot{self.token}/deleteMessage"
        data = {
            "chat_id": self.chat_id,
            "message_id": message_id,
        }
        response = requests.post(url, data=data)
        return Return_Object(response.json())
