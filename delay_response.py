from time import sleep
from mitmproxy import http
import json
import logging
import asyncio
logger = logging.getLogger(__name__)

async def request(flow: http.HTTPFlow) -> None:
    try:
        # Decode the request body (assuming it's JSON) to a Python object
        request_body = '' if flow.request.text == None else json.loads(flow.request.text)
        if 'query AllFeatures {' in json.dumps(request_body):
            await asyncio.sleep(2)
    except ValueError:
        logging.info("Error: ValueError")
        pass  # Handle JSON parsing errors here
async def response(flow: http.HTTPFlow) -> None:
    try:
        request_body = '' if flow.request.text == None else json.loads(flow.request.text)
        if 'query AllFeatures {' in json.dumps(request_body):
            response_json = {
                "data": {
                    "hello":"world"
                }
            }
            flow.response = http.Response.make(
                200,  # HTTP status code
                json.dumps(response_json),  # JSON response
                {
                    "Content-Type": "application/json",
                    "access-control-allow-origin":"https://mysite.com",
                    "access-control-allow-credentials":"true"
                 }  # Headers
            )
    except ValueError:
        logging.info("Error: ValueError")
        logging.info(ValueError)
        pass  # Handle JSON parsing errors here
