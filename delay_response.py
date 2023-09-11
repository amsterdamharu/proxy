# create token with local-test:token script in apis
# use token here to set header in request (line 18)
# set CONNECT_ENV=local-test in apis .env file
# start this proxy with mitmproxy -s delay_response.py
# start apis
# start mc frontend with pnpm start
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    # if browser tries to connect to mc api, redirect to localhost
    if flow.request.pretty_url.startswith("https://url_to_mc_api/proxy/connect/organization_id_selected/"):
        flow.request.host = "localhost"
        flow.request.port = 3000
        flow.request.scheme = "http"
        flow.request.path = flow.request.path.replace("/proxy/connect/organization_id_selected/", "/")
        flow.request.headers["Authorization"] = "Bearer YOUR_TOKEN_CREATED_WITH_LOCAL_TEST:TOKEN_SCRIPT"
        

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    if flow.request.pretty_url.startswith("http://localhost:3000/"):
        flow.response.headers["access-control-allow-origin"] = flow.request.headers.get('Origin', 'http://localhost:3001')
        flow.response.headers["access-control-allow-credentials"] = "true"
        flow.response.headers["access-control-expose-headers"] = "x-refreshed-session-token"