from .parent import Request, Response


async def send_message(token: str, chat_id: int, text: str, reply_to_message_id: int = None):
    reply_parameters = None
    if reply_to_message_id is not None:
        reply_parameters = {"chat_id": chat_id, "message_id": reply_to_message_id}
    request = Request('/sendMessage', token, data=dict(chat_id=chat_id, text=text, reply_parameters=reply_parameters))
    response = await request.post_response()
    if response.ok:
        return response.result
    else:
        return False