from socket import gaierror, timeout
from http.client import HTTPConnection
from urllib.parse import urlparse


class Link:
    def __init__(self, url, line=0, column=0, is_alive=None, status=None):
        self.url = url
        self.line = line
        self.column = column
        self.is_alive = is_alive
        self.status = status
        self.hostname = self.parse_hostname(url)

    def find_status(self):
        try:
            conn = HTTPConnection(host=self.hostname, port=80, timeout=10)
            conn.request("HEAD", "/")
            res = conn.getresponse()
            self.is_alive = 199 < res.status < 400
            self.status = res.status
        except (gaierror, timeout) as e:
            self.is_alive = False
            match e:
                case gaierror():
                    self.status = "Connection error"
                case timeout():
                    self.status = "Timed out"
        except Exception as e:
            print("Some other exception...")
            print(e)
        finally:
            conn.close()

    def parse_hostname(self, url):
        parser = urlparse(url)
        host = parser.netloc or parser.path.split("/")[0]
        # host = parser.hostname  # or this instead???
        return host

    def __str__(self):
        return f"url = {self.url}"
