# start server changed
mitmproxy -s delay_response.py

# curl 'https://mc-api.europe-west1.gcp.escemo.com/proxy/connect/32a0e125-fd74-4145-969e-b1662521a8c0/connectors-staged?integrationTypes=tax&limit=0&offset=20&sort=createdAt+desc' \
# -x http://127.0.0.1:8080 \
# -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0' \
# -H 'Accept: application/json' \
# -H 'Accept-Language: en-US,en;q=0.5' \
# -H 'Accept-Encoding: gzip, deflate, br' \
# -H 'x-application-id: __local:account' \
# -H 'x-correlation-id: mc/67a57ae0-f899-42f9-899c-d28825bd983c/d4b97ab0-2c54-44a6-80e7-15f30f472c33' \
# -H 'x-user-agent: unknown-http-client Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0 Application account' \
# -H 'Origin: http://localhost:3001' \
# -H 'Alt-Used: mc-api.europe-west1.gcp.escemo.com' \
# -H 'Connection: keep-alive' \
# -H 'Sec-Fetch-Dest: empty' \
# -H 'Sec-Fetch-Mode: cors' \
# -H 'Sec-Fetch-Site: cross-site' \
# -H 'TE: trailers'
