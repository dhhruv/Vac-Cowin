import datetime
import os
import sys
from hashlib import sha256

import requests

BOOKING_URL = "https://cdn-api.co-vin.in/api/v2/appointment/schedule"
BENEFICIARIES_URL = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
CALENDAR_URL_DISTRICT = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={0}&date={1}"
CALENDAR_URL_PINCODE = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode={0}&date={1}"
CAPTCHA_URL = "https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha"
OTP_PUBLIC_URL = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"
OTP_PRO_URL = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"

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
        print("Mobile Number cannot be empty. Please Try Again...")
        os.system("pause")
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
                print(
                    f"Successfully Requested OTP for the Mobile Number {mobile} at {datetime.datetime.today()}.."
                )
                txnId = txnId.json()["txnId"]

                OTP = input(
                    "Enter OTP (If you don't recieve OTP in 2 minutes, Press Enter to Retry): "
                )
                if OTP:
                    data = {
                        "otp": sha256(str(OTP).encode("utf-8")).hexdigest(),
                        "txnId": txnId,
                    }
                    print(f"Validating OTP. Please Wait...")

                    token = requests.post(
                        url="https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp",
                        json=data,
                        headers=request_header,
                    )
                    if token.status_code == 200:
                        token = token.json()["token"]
                        print(f"Token Generated: {token}")
                        valid_token = True
                        return token

                    else:
                        print("Unable to Validate OTP...")
                        print(f"Response: {token.text}")

                        retry = input(
                            f"Want to Retry with the {mobile} ? (y/n Default y): "
                        )
                        retry = retry if retry else "y"
                        if retry == "y":
                            pass
                        else:
                            sys.exit()

            else:
                print("Unable to Generate OTP...")
                print(txnId.status_code, txnId.text)

                retry = input(f"Want to Retry with the {mobile} ? (y/n Default y): ")
                retry = retry if retry else "y"
                if retry == "y":
                    pass
                else:
                    sys.exit()

        except Exception as e:
            print(str(e))
