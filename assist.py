import requests
from jinja2 import Template

class Response:
    def __init__(self,code,headers,text):
        self.code = code
        self.headers = headers
        self.text = text

class Request:
    def __init__(self,request_file_path,disable_https=False):
        self.request_file_path = request_file_path
        if disable_https:
            self.protocol = "http://"
        else:
            self.protocol = "https://"
        with open(self.request_file_path,"r") as file:
           self.file_content = file.read() 

    def send(self,num):
        template = Template(self.file_content)
        request = template.render({"num":num})
        lines = request.splitlines()

        request_line= lines[0].strip()
        method= request_line.split()[0]
        path = request_line.split()[1]
        headers = {}

        for line in lines[1:]:
            if not line.strip():
                break  # Stop when encountering an empty line (indicating the end of headers)
            key, value = line.strip().split(': ', 1)
            headers[key] = value
        url = self.protocol + headers["Host"]  + path

        # Extract data (if exists)
        data = ''.join(lines[len(headers) + 1:]).strip()

        #proxy for debuging
        # proxies = {
        #     'http':'127.0.0.1:8080',
        #     'https':'127.0.0.1:8080'
        # }

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data
         # ,verify=False   ,proxies = proxies
            )
        response_obj = Response(response.status_code, response.headers, response.text,)
        return response_obj



class Attack(Request):
    incorrect_num = True
    def __init__(self,request_file_path,error_message=None, stop_message=None, error_code=None,threads=3,disable_https=False):
        super().__init__(request_file_path,disable_https)
        self.error_message = error_message
        self.stop_message = stop_message
        self.error_code = error_code
        self.threads = threads
    
    def try_num(self,num):
        response = self.send(num)
        if self.error_message is not None and not self.error_message in response.text:
            self.incorrect_num = False
            return response
        elif self.stop_message is not None and self.stop_message in response.text:
            self.incorrect_num = False
            return response
        elif self.error_code is not None and self.error_code != response.code:
            self.incorrect_num = False
            return response


