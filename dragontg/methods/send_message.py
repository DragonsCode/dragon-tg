import logging
from .parent import Request, Response

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    level=logging.DEBUG
)

async def send_message(token: str, chat_id: int, text: str, reply_to_message_id: int = None):
    reply_parameters = None
    if reply_to_message_id is not None:
        reply_parameters = {"message_id": reply_to_message_id, "chat_id": chat_id}
        data = dict(chat_id=chat_id, text=text, reply_parameters=reply_parameters)
    else:
        data = dict(chat_id=chat_id, text=text)

    request = Request('/sendMessage', token, data=data)
    response = await request.post_response()

    if response.ok:
        logging.debug(f'Message sent to chat {chat_id}: {text}')
        return response.result
    else:
        logging.error(f'Failed to send message: {response.error_code} - {response.description}')
        return False
