# Debug with proxy

- Install mitmproxy using pip install mitmproxy or your systems package manager like:
  - Ubuntu: sudo apt install mitmproxy
  - MacOs: brew install mitmproxy
  - Windows: download binary from mitmproxy.org

- Run `mitmproxy` in the terminal (`bash ./start.sh`) and it'll start a proxy on `localhost:8080` on your machine.
- Install Oxylabs proxy extension for chrome and set up the proxy (http 127.0.0.1 port 8080, no user name or password)
- Open http://mitm.it in the browser while using the proxy with oxylabs and download the certificate for your system (other platforms mitmproxy-ca-cert.pem).
- Install the certificate to your Chrome or Chromium browser:
  - Open chrome://certificate-manager/ in the browser.
  - Custom -> Installed by you -> Trusted Certificates -> Import
