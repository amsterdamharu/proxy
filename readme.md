# Debug with proxy


- Install mitmproxy using pip install mitmproxy or your systems package manager like:
  - Ubuntu: sudo apt install mitmproxy
  - MacOs: brew install mitmproxy
  - Windows: download binary from mitmproxy.org

- Run `mitmproxy` in the terminal and it'll start a proxy on `localhost:8080` on your machine.
- Start Chrome instance with `mitmproxy` proxy attached to it:
  - Linux: `google-chrome --proxy-server="localhost:8080"`
  - MacOs: `open -a "Google Chrome" --args --proxy-server="localhost:8080"`
  - Windows: `chrome.exe --proxy-server="localhost:8080"`
- Open http://mitm.it in the browser and download the certificate for your system.
- Install the certificate to your Chrome or Chromium browser:
  - Open chrome://settings/certificates in the browser.
  - Click on Authorities tab.
  - Click on Import button and select the certificate from the step 4.

In mitmproxy press E to see events that will show the logger.info