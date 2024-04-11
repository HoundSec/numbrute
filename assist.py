import requests
from jinja2 import Template

class Response:
    def __init__(self,code,headers,text):
        self.code = code
        self.headers = headers
        self.text = text

class Request:
    method = ''
    path = ''
    headers = {}
    url = ''
    data = ''

    def __init__(self,request_file_path,disable_https=False):
        self.request_file_path = request_file_path
        if disable_https:
            self.url = "http://"
        else:
            self.url = "https://"
    def load_file(self):
        with open(self.request_file_path,"r") as file:
            lines = file.readlines()

        request_line= lines[0].strip()
        self.method= request_line.split()[0]
        self.path = request_line.split()[1]

        # Extract headers
        for line in lines[1:]:
            if not line.strip():
                break  # Stop when encountering an empty line (indicating the end of headers)
            key, value = line.strip().split(': ', 1)
            self.headers[key] = value
        self.url = self.url + self.headers["Host"]  + self.path

        # Extract data (if exists)
        self.data = ''.join(lines[len(self.headers) + 1:]).strip()

    def send(self,num):
        proxies = {
            'http':'127.0.0.1:8080',
            'https':'127.0.0.1:8080'
        }

        headers = {}

        for key in self.headers:
            template = Template(self.headers[key])
            headers[key] = template.render({"num":num})

        template = Template(self.data)
        data = template.render({"num":num})

        response = requests.request(
            method=self.method,
            url=self.url,
            headers=headers,
            data=data
         ,verify=False   ,proxies = proxies
            )
        response_obj = Response(response.status_code, response.headers, response.text,)
        return response_obj



class Attack(Request):
    incorrect_num = True
    def __init__(self,request_file_path,error_message=None,error_code=None,threads=3,disable_https=False):
        super().__init__(request_file_path,disable_https)
        self.error_message = error_message
        self.error_code = error_code
        self.threads = threads
    
    def try_num(self,num):
        response = self.send(num)
        if self.error_message is not None and not self.error_message in response.text:
            self.incorrect_num = False
            return response
        if self.error_code is not None and self.error_code != response.code:
            self.incorrect_num = False
            return response


