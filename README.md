# numbrute
A versatile web app brute-force tool written in pure Python, capable of running attacks in multiple threads (user-definable) and attempting combinations randomly rather than sequentially.

## How to use it

To use this tool, you have to save requests to a file from burp-suit, why'd do that? you might ask. Well, because this tool has randomized brute-forcing and there's no throattling unlike burp-suit, specially the community version.
in the request file, replace the part where the payload is bing sent with {{num}}

> NOTE: This tool uses jinja templates underneath

*example:*

From:

```http
POST https://www.example.com/api/users HTTP/1.1
Host: www.example.com
Content-Type: application/json

{ "userid": "7793", "email": "johndoe@example.com", "password": "securepassword123" }
```
To:

```http
POST https://www.example.com/api/users HTTP/1.1
Host: www.example.com
Content-Type: application/json

{ "userid": "{{num}}", "email": "johndoe@example.com", "password": "securepassword123" }
```


### Flags

- `-f <request filepath>` use this flag to specify the path of the request file 
- `-e <error message>` the error message shown on incorrect attempt
- `-c <status code of error response>` the status code came with the error message in response
- `-t <number of threads>` (optional) use this to add the number of threads you wanna run duruing the attack, default is 3
- `-l <lenght of the number>` add the lenght of combinations to try
- `-H` (optional) add this flag to disable HTTPS

example:

```bash
python main.py -f post_req.http -e "invalid attempt" -c 401 -t 5 -l 4 
```

numberute will keep attacking long as it finds either the `error message` given or the `error status code` in the response. But, once it sees anything different, for example if the response status code changes or the if the server doesn't send the error in the response, numbrute stops there.

