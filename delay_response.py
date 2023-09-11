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
        if '88888888FetchMyProjectsReferencesQuery' in json.dumps(request_body):
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
    if re.match(r"https://mc-api\.europe-west1\.gcp\.escemo\.com/proxy/connect/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/", flow.request.pretty_url):
        ctx.log.info(f"Request URL: {flow.request.pretty_url}")
        # if flow.request.method == "DELETE":
        #     ctx.log.info("DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE")
        #     create_response(flow, {"json":b'{noJson,"statusCode": 404,"message":"hello world"}',"status": 404})
        #     return
        if flow.request.method == "GET" and re.match(r".*/deployments/0ea4981b-edea-454c-be27-bf6dd252f225.*$", flow.request.pretty_url):
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
        if re.match(r".*/connectors/1d412b0a-f2ee-4fae-9726-7eba04fea817.*$", flow.request.pretty_url):
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

        if re.match(r".*/connectors-staged/f354d04a-9c82-43a3-8001-4c6bfbdfd65a.*$", flow.request.pretty_url):
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

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "OPTIONS":
        return
    if flow.request.pretty_url.startswith("http://localhost:3000/"):
        flow.response.headers["access-control-allow-origin"] = flow.request.headers.get('Origin', 'http://localhost:3001')
        flow.response.headers["access-control-allow-credentials"] = "true"
        flow.response.headers["access-control-expose-headers"] = "x-refreshed-session-token"