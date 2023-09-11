curl --proxy 127.0.0.1:8080 --cacert ~/.mitmproxy/mitmproxy-ca-cert.pem \
  'https://my-site.com' \
  --data-raw '{"hello":"world"}' \
  --compressed