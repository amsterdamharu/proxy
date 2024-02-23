# create token with local-test:token script in apis
# use token here to set header in request (line 21)
# set CONNECT_ENV=local-test in apis .env file
# start this proxy with mitmproxy -s delay_response.py
# start apis
# start mc frontend with pnpm start
from mitmproxy import http
from mitmproxy import ctx
import re

def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    # if browser tries to connect to mc api, redirect to localhost
    if re.match(r"https://mc-api\.europe-west1\.gcp\.escemo\.com/proxy/connect/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/", flow.request.pretty_url):
        ctx.log.info("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        flow.request.host = "localhost"
        flow.request.port = 3000
        flow.request.scheme = "http"
        flow.request.path = re.sub(r"/proxy/connect/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/", "/", flow.request.path)
        flow.request.headers["Authorization"] = "Bearer YOUR_TOKEN_CREATED_WITH_LOCAL_TEST:TOKEN_SCRIPT"
        

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    if flow.request.pretty_url.startswith("http://localhost:3000/"):
        flow.response.headers["access-control-allow-origin"] = flow.request.headers.get('Origin', 'http://localhost:3001')
        flow.response.headers["access-control-allow-credentials"] = "true"
        flow.response.headers["access-control-expose-headers"] = "x-refreshed-session-token"