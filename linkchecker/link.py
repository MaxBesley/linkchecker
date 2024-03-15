from socket import gaierror, timeout
from http.client import HTTPConnection
from urllib.parse import urlparse
from pprint import pprint
import requests

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

            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'Content-Type': '*', # 'text/plain;charset=UTF-8'
                'Referer': 'https://www.google.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
                }

            # api_key = ''
            # response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + api_key)
            # headers = response.json().get('result', [])[0]
            # pprint(headers)


            conn = HTTPConnection(host=self.hostname, port=80, timeout=10)
            conn.request('HEAD', '/', headers=headers)
            res = conn.getresponse()
            self.is_alive = 199 < res.status < 400
            self.status = res.status
        except (gaierror, timeout) as e:
            self.is_alive = False
            match e:
                case gaierror():
                    self.status = 'Connection error'
                case timeout():
                    self.status = 'Timed out'
        except Exception as e:
            print('Some other exception...')
            print(e)
        finally:
            conn.close()

    def parse_hostname(self, url):
        parser = urlparse(url)
        host = parser.netloc or parser.path.split('/')[0]

        # WIP
        new_host = parser.hostname  # or this instead???
        if host != new_host:
            print(host, new_host)
            exit("Host mismatch")

        return host

    def __str__(self):
        return f"url = {self.url}"
