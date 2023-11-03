from aiohttp import ClientSession
import asyncio

class RequestError(RuntimeError):
    def __init__(self, message, code, url, response_headers: dict = None):
        self.message = message
        self.code = code
        self.url = url
        self.response_headers = response_headers

class ClientObject:
    async def get(self, url: str):
        async with ClientSession() as session:
            result = await asyncio.gather(self._get(session, url))
        
            return result[0]
    
    async def get_many(self, urls: list[str]):
        async with ClientSession() as session:
            results = await asyncio.gather(*[self._get(session, url) for url in urls])

            return results
    
    async def _get(self, session: ClientSession, url: str):
        async with session.get(url) as res:

            if res.status==429:
                print(429, url)
                await asyncio.sleep(10)
                return await self._get(session, url)
            elif res.status>=400:
                raise RequestError(res.reason, url, res.status, res.headers)
        
            content_type = res.headers.get("Content-Type", "application/octet-stream")
        
            if "APPLICATION/JSON" in content_type:
                data = await res.json()
            else:
                data = await res.text("utf-8")
            
            return data