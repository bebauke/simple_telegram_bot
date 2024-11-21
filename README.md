# Simple Telegram Bot API Wrapper

This Python project provides a wrapper for the Telegram Bot API, enabling you to easily interact with Telegram through Python code. The `TelegramBot` class provides functions to send messages, photos, stickers, and edit or delete messages in a Telegram chat. Additionally, a `Return_Object` class is included to handle API responses in a structured way.

## Features
- **Send Messages**: Send text messages to a Telegram chat.
- **Send Photos**: Send photos with optional captions.
- **Send Stickers**: Send `.webp` stickers to the chat.
- **Edit Messages**: Edit text or media of an existing message.
- **Delete Messages**: Delete a specific message in the chat.
- **Structured Responses**: API responses are handled by the `Return_Object` class for easier debugging and handling.

## Todo:
- Implement async recive metodes
---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required Python libraries:
   ```bash
   pip install requests
   ```

3. Set up your Telegram Bot:
   - Create a bot using the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
   - Obtain your bot's **API token**.
   - Retrieve your **chat ID** using a bot like [@getidsbot](https://telegram.me/getidsbot).

---

## Usage

1. **Import the TelegramBot Class**
   ```python
   from telegram_bot import TelegramBot
   ```

2. **Initialize the Bot**
   ```python
   bot = TelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")
   ```

3. **Send a Message**
   ```python
   response = bot.send_message("Hello, world!")
   print(response)
   ```

4. **Send a Photo**
   ```python
   response = bot.send_photo(photo="path/to/photo.jpg", caption="Check this out!")
   print(response)
   ```

5. **Send a Sticker**
   ```python
   response = bot.send_sticker(sticker="sticker_name")
   print(response)
   ```

6. **Edit a Message**
   ```python
   response = bot.edit_message_text(message_id=123456789, text="Updated message text")
   print(response)
   ```

7. **Delete a Message**
   ```python
   response = bot.delete_message(message_id=123456789)
   print(response)
   ```

---

## Code Overview

### `TelegramBot` Class
Handles all interactions with the Telegram Bot API. Key methods include:
- `send_message(text)`: Sends a text message.
- `send_photo(photo, caption)`: Sends a photo with an optional caption.
- `send_sticker(sticker)`: Sends a sticker (requires `.webp` format).
- `edit_message_text(message_id, text)`: Edits the text of an existing message.
- `edit_message_photo(message_id, photo, caption)`: Edits the photo or caption of an existing message.
- `delete_message(message_id)`: Deletes a specific message.

### `Return_Object` Class
Used to parse and structure the API's JSON responses. Key attributes:
- `ok`: Boolean indicating if the API call was successful.
- `message_id`, `date`, `text`: Available if the response contains message details.
- `error_code`, `description`: Available if an error occurs.

---

## Example

```python
from telegram_bot import TelegramBot

# Initialize the bot
bot = TelegramBot(token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")

# Send a text message
response = bot.send_message("Hello, Telegram!")
if response.ok:
    print(f"Message sent successfully: {response.message_id}")
else:
    print(f"Error: {response.description}")

# Send a photo
photo_response = bot.send_photo("path/to/image.jpg", caption="Check out this image!")
print(photo_response)

# Delete the message
bot.delete_message(message_id=response.message_id)
```

---

## Error Handling
- If an API call fails, the `Return_Object` will contain `error_code` and `description`.
- Example:
  ```python
  if not response.ok:
      print(f"Error {response.error_code}: {response.description}")
  ```

---

## Dependencies
- `requests`: For making HTTP requests to the Telegram API.

---

## Notes
- Stickers must be in `.webp` format and stored in a `../stickers/` folder relative to the script.
- For advanced features like inline keyboards, the code can be extended as needed.

---

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute it.
