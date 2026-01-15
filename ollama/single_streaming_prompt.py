import aiohttp
import asyncio
import constants
import json

async def make_single_streaming_prompt(session: aiohttp.ClientSession, model: str, prompt: str, *args, **kwargs):
    try:
        url = f"{constants.OLLAMA_HOST}:{constants.OLLAMA_PORT}/api/generate"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'model': model,
            'prompt': prompt,
            'max_tokens': constants.OLLAMA_MAX_RESPONSE_TOKENS,
            'stream': True
        }
        print(f"Making streaming call curl -X POST {url} -d '{payload}' -H \'Content-Type: application/json\' ")
        async with session.post(url=url, headers=headers, json=payload) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                print("Streaming request successful")
                response_text = ""
                async for line in response.content:
                    decoded = line.decode('utf-8')
                    decoded_json = json.loads(decoded)
                    response_text += decoded_json.get('response', '')
                return response_text, None
            else:
                print(f"Streaming request failed with status:{response.status}")
                return None, Exception(f"Streaming request failed with status:{response.status}")
    except Exception as e:
        print(f"Error while making single streaming prompt:{e}")
        return None, e

async def main():
    try:
        tcp_connector = aiohttp.TCPConnector(limit=constants.AIOHTTP_TCP_CONNECTOR_DEFAULT_LIMIT)
        client_timeout = aiohttp.ClientTimeout(total=constants.AIOHTTP_CLIENT_SESSION_DEFAULT_TIMEOUT)
        print("Initializing aiohttp client session ...")
        session = aiohttp.ClientSession(connector=tcp_connector, timeout=client_timeout)
        print("aiohttp client session initialized successfully !!!")
        model = constants.DEFAULT_MODEL
        prompt = """
        Analyze the following stacktrace and provide possible root cause and solutions
        Stacktrace: 
        Traceback (most recent call last):
        File "example.py", line 10, in <module>
            main()
        File "example.py", line 6, in main
            result = 10 / 0
        The response format should be like this:
        Possible Root Cause: <root cause> (in max 100 words)
        Possible Solutions: <solution> (in max 100 words)
        """
        response, err = await make_single_streaming_prompt(
            session=session,
            model=model,
            prompt=prompt
        )
        if err:
            print(f"streaming request failed with error:{err}")
        else:
            print(f"Streaming request successful with response:{response}")
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        print("Closing the aiohttp client session ...")
        await session.close()
        print("Closed the aiohttp client session successfully")

if __name__ == "__main__":
    asyncio.run(main())