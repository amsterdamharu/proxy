from time import sleep
from mitmproxy import http
import json
import logging
import asyncio

async def request(flow: http.HTTPFlow) -> None:
    try:
        # Decode the request body (assuming it's JSON) to a Python object
        request_body = '' if flow.request.text == None else json.loads(flow.request.text)
        if 'skirt' in json.dumps(request_body):
            await asyncio.sleep(0.2)
    except ValueError:
        logging.info("Error: ValueError")
        pass  # Handle JSON parsing errors here
async def response(flow: http.HTTPFlow) -> None:
    try:
        request_body = '' if flow.request.text == None else json.loads(flow.request.text)
        if 'skirt' in json.dumps(request_body):
            # Delay the response by adding an artificial delay (e.g., 5 seconds)
            # flow.response.delay = 5.0
            await asyncio.sleep(0.2)
    except ValueError:
        logging.info("Error: ValueError")
        pass  # Handle JSON parsing errors here
