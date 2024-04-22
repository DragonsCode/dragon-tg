from .parent import Request, Response


async def send_message(token: str, chat_id: int, text: str, reply_to_message_id: int = None):
    reply_parameters = None
    if reply_to_message_id is not None:
        reply_parameters = {"message_id": reply_to_message_id, "chat_id": chat_id}
        data = dict(chat_id=chat_id, text=text, reply_parameters=reply_parameters)
    data = dict(chat_id=chat_id, text=text)
    request = Request('/sendMessage', token, data=data)
    response = await request.post_response()
    if response.ok:
        return response.result
    else:
        print(response.error_code, response.description)
        return False