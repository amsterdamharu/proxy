# create token with local-test:token script in apis
# use token here to set header in request (line 140)
# set CONNECT_ENV=local-test in apis .env file
# start this proxy with mitmproxy -s delay_response.py
# start apis
# start mc frontend with pnpm start
from mitmproxy import http
from mitmproxy import ctx
from connector import Connector 
from deployment import Deployment 
import re
import json
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
    try:
        # Decode the request body (assuming it's JSON) to a Python object
        request_body = '' if flow.request.text == None else json.loads(flow.request.text)
        if 'QQQQQQFetchMyProjectsReferencesQuery' in json.dumps(request_body):
            ctx.log.info("Replace graphql query")
            create_response(flow, {"json":b'''
{
  "data": {
    "myProjects": {
      "total": 3,
      "results": [
        {
          "id": "5aa199be-a295-4650-9285-2e386fadd974",
          "key": "harm-sandbox-1",
          "name": "harm-sandbox-1",
          "__typename": "Project"
        },
        {
          "id": "5aa199be-a295-4650-9285-2e386fadd975",
          "key": "harm-sandbox-2",
          "name": "harm-sandbox-2",
          "__typename": "Project"
        },
        {
          "id": "5aa199be-a295-4650-9285-2e386fadd976",
          "key": "harm-sandbox-3",
          "name": "harm-sandbox-3",
          "__typename": "Project"
        }
      ],
      "__typename": "ProjectQueryResult"
    }
  }
}
            ''',"status": 200})
            return
    except ValueError:
      pass
    if re.match(r"[ configure url ]", flow.request.pretty_url):
        ctx.log.info(f"Request URL: {flow.request.pretty_url}")
        # if flow.request.method == "DELETE":
        #     ctx.log.info("DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE")
        #     create_response(flow, {"json":b'{noJson,"statusCode": 404,"message":"hello world"}',"status": 404})
        #     return
        if flow.request.method == "GET" and re.match(r".*/qqdeployments/ed54a36c-5191-44ab-abee-35379d7fd413.*$", flow.request.pretty_url):
            ctx.log.info("OVERRIDE DEPLOYMENT GET")
            create_response(flow, {"json":Deployment()
              .setApps([
                  {
                      "standardConfig": 20,
                      "securedConfig": 20,
                      "applicationType": "service",
                      "applicationName": "app1"
                  },
                  {
                      "standardConfig": 0,
                      "securedConfig": 0,
                      "applicationType": "assets",
                      "applicationName": "app2"
                  }
              ])
              .setGlobalConfig({"standardConfig": 2, "securedConfig": 1})                                   
              .build(),"status": 200})
            return
        if re.match(r".*/qqconnectors/f6c77ff0-b82b-48cb-baa9-3c353e2ff4af.*$", flow.request.pretty_url):
            ctx.log.info("OVERRIDE CONNECTOR GET")
            create_response(flow, {"json":Connector()
              .setApps([
                  {
                      "standardConfig": 3,
                      "securedConfig": 2,
                      "applicationType": "service",
                      "applicationName": "app1"
                  },
                  {
                      "standardConfig": 0,
                      "securedConfig": 0,
                      "applicationType": "assets",
                      "applicationName": "app2"
                  }
              ])
              .setGlobalConfig({"standardConfig": 2, "securedConfig": 1})                                   
              .build(),"status": 200})
            return

        if re.match(r".*/qqconnectors-staged/a3028357-6b25-4cf6-8815-ad743437d2bf.*$", flow.request.pretty_url):
            ctx.log.info("OVERRIDE CONNECTOR STAGED GET")
            create_response(flow, {"json":Connector()
              .setApps([
                  {
                      "standardConfig": 30,
                      "securedConfig": 2,
                      "applicationType": "service",
                      "applicationName": "app1"
                  },
                  {
                      "standardConfig": 0,
                      "securedConfig": 0,
                      "applicationType": "assets",
                      "applicationName": "app2"
                  }
              ])
              .setGlobalConfig({"standardConfig": 30, "securedConfig": 1})                                   
              .build(),"status": 200})
            return
        ctx.log.info("PASS THROUGH LOCALHOST (REMOVE AND IT'LL PASS TRHOUGH STAGED)")
        flow.request.host = "localhost"
        flow.request.port = 3000
        flow.request.scheme = "http"
        flow.request.path = re.sub(r"/proxy/connect/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/", "/", flow.request.path)
        flow.request.headers["Authorization"] = "Bearer your-token" 

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    if flow.request.pretty_url.startswith("http://localhost:3000/"):
        flow.response.headers["access-control-allow-origin"] = flow.request.headers.get('Origin', 'http://localhost:3001')
        flow.response.headers["access-control-allow-credentials"] = "true"
        flow.response.headers["access-control-expose-headers"] = "x-refreshed-session-token"