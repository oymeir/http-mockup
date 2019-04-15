
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


DATA = {
    "aba": {"foo": [1, 2, 3], "bar": "vaz"},
    "bac": {"bar": "vaz", "lorem": {"impsum": 3.14}}
}


class Server(BaseHTTPRequestHandler):

    sessions = {}

    def _set_headers(self, type="text/html"):

        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()

    def do_GET(self):

        # implement the landing page
        if self.path in ["/start", "/"]:

            # let's prepare html for listing the keys
            html = []
            for k in DATA.keys():
                html.append("<a href=/value/{}>{}</a></br>".format(k, k))
            html = "\n".join(html)

            self._set_headers()
            self.wfile.write(html.encode())

        # implement value lookup and print
        elif re.match('/value/[0-9A-Za-z]+', self.path) is not None:

            # get the key, which is embedded in the url
            key = re.search('/value/([0-9A-Za-z]+)', self.path).group(1)
            s = json.dumps(DATA[key], indent=2)

            self._set_headers(type="application/json")
            self.wfile.write(s.encode())


if __name__ == "__main__":

    httpd = HTTPServer(("0.0.0.0", 8080), Server)
    print("Go to: http://localhost:{}/start".format(8080))
    httpd.serve_forever()