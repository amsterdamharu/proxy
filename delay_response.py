from mitmproxy import http
from mitmproxy import ctx
import time

LOCAL_TARGET_HOST = "localhost"
LOCAL_TARGET_PORT = 4000
TOKEN="your valid manage token"


def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    operation_name = flow.request.headers.get("x-graphql-operation-name", "")
    if "Agentic" in operation_name and operation_name != "FetchStoresForAgenticChannels":
        # if operation_name == "UpdateAgenticChannel":
        #     time.sleep(5)
        flow.request.host = LOCAL_TARGET_HOST
        flow.request.port = LOCAL_TARGET_PORT
        flow.request.scheme = "http"
        flow.request.path = "/graphql"
        flow.request.headers["authorization"] = f'Bearer {TOKEN}'
    else:
        ctx.log.info("NOT ROUTING TO LOCALHOST")
        ctx.log.info(flow.request.pretty_url)

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    if flow.request.pretty_url.startswith(f"http://{LOCAL_TARGET_HOST}:{LOCAL_TARGET_PORT}/"):
        flow.response.headers["access-control-allow-origin"] = flow.request.headers.get('Origin', f'http://{LOCAL_TARGET_HOST}:{LOCAL_TARGET_PORT}')
        flow.response.headers["access-control-allow-credentials"] = "true"
        flow.response.headers["access-control-allow-headers"] = "authorization, content-type"
        flow.response.headers["access-control-expose-headers"] = "x-refreshed-session-token"