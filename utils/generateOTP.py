import datetime
import os
import sys
from hashlib import sha256

import requests
from colorama import Fore, Style, init

from utils.ratelimit import handleRateLimited
from utils.urls import *

init(convert=True)

WARNING_BEEP_DURATION = (1000, 2000)


try:
    import winsound

except ImportError:
    import os

    if sys.platform == "darwin":

        def beep(freq, duration):
            # brew install SoX --> install SOund eXchange universal sound sample translator on mac
            os.system(f"play -n synth {duration/1000} sin {freq} >/dev/null 2>&1")

    else:

        def beep(freq, duration):
            # apt-get install beep  --> install beep package on linux distros before running
            os.system("beep -f %s -l %s" % (freq, duration))


else:

    def beep(freq, duration):
        winsound.Beep(freq, duration)


def generateTokenOTP(mobile, request_header):
    """
    This function generate OTP and returns a new token
    """

    if not mobile:
        print(f"{Fore.RED}", end="")
        print("Mobile Number cannot be empty. Please Try Again...")
        os.system("pause")
        print(f"{Fore.RESET}", end="")
        sys.exit()

    valid_token = False
    while not valid_token:
        try:
            data = {
                "mobile": mobile,
                "secret": "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw==",
            }
            txnId = requests.post(url=OTP_PRO_URL, json=data, headers=request_header)

            if txnId.status_code == 200:
                print(f"{Fore.CYAN}", end="")
                print(
                    f"Successfully Requested OTP for the Mobile Number {mobile} at {datetime.datetime.today()}.."
                )
                print(f"{Fore.RESET}", end="")
                txnId = txnId.json()["txnId"]

                print(f"{Fore.YELLOW}", end="")
                OTP = input(
                    "Enter OTP (If you don't recieve OTP in 2 minutes, Press Enter to Retry): "
                )
                print(f"{Fore.RESET}", end="")
                if OTP:
                    data = {
                        "otp": sha256(str(OTP).encode("utf-8")).hexdigest(),
                        "txnId": txnId,
                    }
                    print(f"{Fore.CYAN}", end="")
                    print(f"Validating OTP. Please Wait...")
                    print(f"{Fore.RESET}", end="")

                    token = requests.post(
                        url="https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp",
                        json=data,
                        headers=request_header,
                    )
                    if token.status_code == 200:
                        token = token.json()["token"]
                        print(f"{Fore.GREEN}", end="")
                        print(f"Token Generated: {token}")
                        print(f"{Fore.RESET}", end="")
                        valid_token = True
                        return token

                    else:
                        print(f"{Fore.RED}", end="")
                        print("Unable to Validate OTP...")
                        print(f"Response: {token.text}")
                        print(f"{Fore.RESET}", end="")

                        print(f"{Fore.YELLOW}", end="")
                        retry = input(
                            f"Want to Retry with the {mobile} ? (y/n Default y): "
                        )
                        print(f"{Fore.RESET}", end="")
                        retry = retry if retry else "y"
                        if retry == "y":
                            pass
                        else:
                            sys.exit()

            else:
                print(f"{Fore.RED}", end="")
                print("Unable to Generate OTP...")
                print(txnId.status_code, txnId.text)
                if txnId.status_code == 403 or txnId.status_code == 429:
                    handleRateLimited()
                print(f"{Fore.RESET}", end="")

                print(f"{Fore.YELLOW}", end="")
                retry = input(f"Want to Retry with the {mobile} ? (y/n Default y): ")
                print(f"{Fore.RESET}", end="")
                retry = retry if retry else "y"
                if retry == "y":
                    pass
                else:
                    sys.exit()

        except Exception as e:
            print(f"{Fore.RED}", end="")
            print(str(e))
            print(f"{Fore.RESET}", end="")
