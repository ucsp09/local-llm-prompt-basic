import aiohttp
import asyncio
import constants
import json

async def make_single_non_streaming_prompt(session: aiohttp.ClientSession, model: str, prompt: str, *args, **kwargs):
    try:
        url = f"{constants.OLLAMA_HOST}:{constants.OLLAMA_PORT}/api/generate"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "model": model,
            "prompt": prompt,
            "options": {
                "num_predict": constants.OLLAMA_MAX_RESPONSE_TOKENS,
                "num_ctx": constants.OLLAMA_CONTEXT_SIZE,
                "temperature": constants.OLLAMA_DEFAULT_TEMPERATURE
            },
            "stream": False
        }
        print(f"Making non-streaming call curl -X POST {url} -d '{payload}' -H 'Content-Type: application/json'")
        async with session.post(url=url, headers=headers, json=payload) as response:
            response_text = await response.text()
            print(f"Response: {response_text}")
            print(f"Status: {response.status}")
            if response.status == 200:
                print("Non-streaming prompt request successful with status 200")            
                response_json = json.loads(response_text)
                return response_json, None
            else:
                print(f"Non-streaming prompt request failed with status: {response.status}")
                return None, Exception(f"Non-streaming prompt request failed with status code: {response.status}")
    except Exception as e:
        print(f"Error occurred while making non-streaming prompt request: {e}")
        return None, e


async def main():
    try:
        tcp_connector = aiohttp.TCPConnector(limit=constants.AIOHTTP_TCP_CONNECTOR_DEFAULT_LIMIT)
        client_timeout = aiohttp.ClientTimeout(total=constants.AIOHTTP_CLIENT_SESSION_DEFAULT_TIMEOUT)
        print("Initializing aiohttp ClientSession...")
        session = aiohttp.ClientSession(
            connector=tcp_connector, 
            timeout=client_timeout)
        print("Initialized aiohttp ClientSession successfully!!!")
        model = constants.DEFAULT_MODEL
        prompt = """
        Analyze the following stacktrace and provide possible root cause
        Stacktrace: 
        Traceback (most recent call last):
        File "example.py", line 10, in <module>
            main()
        File "example.py", line 6, in main
            result = 10 / 0
        The response format should be like this:
        Possible Root Cause: <root cause> (in max 30 words)
        """
        print("Starting Non-Streaming Prompt Request...")
        response, err = await make_single_non_streaming_prompt(
            session=session,
            model=model,
            prompt=prompt
        )
        if err:
            print(f"Error in non-streaming prompt request: {err}")
        else:
            print(f"Non-Streaming Prompt Request Completed with response:{response}")
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        print("Closing aiohttp ClientSession...")
        await session.close()
        print("Closed aiohttp ClientSession successfully!!!")


if __name__ == "__main__":
    asyncio.run(main())