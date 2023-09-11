from mitmproxy import http
from mitmproxy import ctx
import re
from config import token, host

def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
        # normal production url forwared to dev or staged
    if re.match(r"[ configure url ]", flow.request.pretty_url):
        ctx.log.info("Monster xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        flow.request.host = host
        flow.request.path = re.sub(r"/proxy/connect/", "/system/", flow.request.path)
        flow.request.headers["authorization"] = "Bearer " + token
    # if this is swagger
    if flow.request.pretty_url.startswith(f"https://{host}"):
        ctx.log.info("Swagger xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        flow.request.headers["authorization"] = "Bearer " + token # add the auth token to the request
        

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    if flow.request.pretty_url.startswith("http://localhost:3000/"):
        flow.response.headers["access-control-allow-origin"] = flow.request.headers.get('Origin', 'http://localhost:3001')
        flow.response.headers["access-control-allow-credentials"] = "true"
        flow.response.headers["access-control-expose-headers"] = "x-refreshed-session-token"