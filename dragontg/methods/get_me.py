from .parent import Request, Response
from dragontg.models.user import User

async def get_me(token: str) -> tuple[bool, User | tuple[int, str]]:
    request = Request('/getMe', token)
    response = await request.get_response()
    if response.ok:
        return True, response.result
    else:
        return False, (response.error_code, response.description)