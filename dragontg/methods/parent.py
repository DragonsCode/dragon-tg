import aiohttp
import asyncio

class Response:
    def __init__(self, request, request_json):
        self.request = request
        self.status = request.status
        self.text = request.text
        self.request_json = request_json
        self.headers = request.headers
    
    @property
    def ok(self):
        return self.request_json['ok']
    
    @property
    def result(self):
        if self.status != 200:
            return None
        return self.request_json['result']
    
    @property
    def description(self):
        if self.status == 200:
            return None
        return self.request_json['description']
    
    @property
    def error_code(self):
        if self.status == 200:
            return None
        return self.request_json['error_code']

class Request:
    def __init__(self, method: str, token: str, headers: dict = None, timeout: int = 60, data: dict = None):
        self.data = data
        self.headers = headers
        self.method = method
        self.timeout = timeout
        self.url = 'https://api.telegram.org/bot'+token
    
    async def get_response(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(self.url+self.method, data=self.data, headers=self.headers, timeout=self.timeout) as response:
                        j = await response.json()
                        return Response(response, j)
                except asyncio.TimeoutError:
                    print("Timeout error, retrying in 3 seconds...")
                    await asyncio.sleep(3)
    
    async def post_response(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.post(self.url+self.method, data=self.data, headers=self.headers, timeout=self.timeout) as response:
                        j = await response.json()
                        return Response(response, j)
                except asyncio.TimeoutError:
                    print("Timeout error, retrying in 3 seconds...")
                    await asyncio.sleep(3)
