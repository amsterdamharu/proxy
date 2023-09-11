from mitmproxy import http
from mitmproxy import ctx
import re
def create_response(flow, interface):
    headers = {
        "Content-Type": "application/json",
        "access-control-allow-origin": flow.request.headers.get('Origin', 'http://localhost:5173'),
        "access-control-allow-credentials": "true",
        "access-control-expose-headers": "x-refreshed-session-token"
    }
    flow.response = http.Response.make(
        interface["status"],  # status code
        interface["json"],  # response body
        headers  # response headers
    )


def request(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    # if browser tries to connect to mc api
    if re.match(r"https://mc-api\.europe-west1\.gcp\.escemo\.com/proxy/connect/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/", flow.request.pretty_url):
        # example returning faulty json on delete request
        # if flow.request.method == "DELETE":
        #     ctx.log.info("DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE")
        #     create_response(flow, {"json":b'{noJson,"statusCode": 404,"message":"hello world"}',"status": 404})
        #     return
        # example returning faulty json on get connectors request
        # if re.match(r".*/connectors\?.*$", flow.request.pretty_url):
        #     ctx.log.info("RETURN ERROR--RETURN ERROR--RETURN ERROR--RETURN ERROR--RETURN ERROR--RETURN ERROR")
        #     create_response(flow, {"json":b'{nojson, "statusCode": 400,"message":"hello world"}',"status": 200})
        #     return
        # redirect to localhost
        ctx.log.info("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        flow.request.host = "localhost"
        flow.request.port = 3000
        flow.request.scheme = "http"
        flow.request.path = re.sub(r"/proxy/connect/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/", "/", flow.request.path)
        flow.request.headers["Authorization"] = "Bearer YOUR_TOKEN_CREATED_WITH_LOCAL_TEST_TOKEN_SCRIPT"

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    if flow.request.pretty_url.startswith("http://localhost:3000/"):
        flow.response.headers["access-control-allow-origin"] = flow.request.headers.get('Origin', 'http://localhost:3001')
        flow.response.headers["access-control-allow-credentials"] = "true"
        flow.response.headers["access-control-expose-headers"] = "x-refreshed-session-token"