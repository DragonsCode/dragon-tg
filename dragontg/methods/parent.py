import aiohttp
import asyncio
import logging

# Logging setup
# logging.basicConfig(
#     format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
#     level=logging.DEBUG
# )

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
    def __init__(self, method: str, token: str, headers: dict = None, timeout: int = 60, data: dict = None, json: dict = None):
        self.data = data
        self.json = json
        self.headers = headers
        self.method = method
        self.timeout = timeout
        self.url = 'https://api.telegram.org/bot' + token
    
    async def get_response(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(
                        self.url + self.method,
                        data=self.data,
                        json=self.json,
                        headers=self.headers,
                        timeout=self.timeout
                    ) as response:
                        j = await response.json()
                        logging.debug(f'GET {self.url + self.method} - Status: {response.status}')
                        return Response(response, j)
                except asyncio.TimeoutError:
                    logging.warning("Timeout error, retrying in 3 seconds...")
                    await asyncio.sleep(3)
    
    async def post_response(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.post(
                        self.url + self.method,
                        data=self.data,
                        json=self.json,
                        headers=self.headers,
                        timeout=self.timeout
                    ) as response:
                        j = await response.json()
                        logging.debug(f'POST {self.url + self.method} - Status: {response.status}')
                        return Response(response, j)
                except asyncio.TimeoutError:
                    logging.warning("Timeout error, retrying in 3 seconds...")
                    await asyncio.sleep(3)
