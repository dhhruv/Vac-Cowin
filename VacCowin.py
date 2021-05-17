#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import copy
import os
import sys
from types import SimpleNamespace

import requests

from utils.appointment import checkAndBook
from utils.displayData import displayInfoDict
from utils.generateOTP import generateTokenOTP
from utils.userInfo import (
    collectUserDetails,
    confirmAndProceed,
    getSavedUserInfo,
    saveUserInfo,
)

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Passing the token directly")
    args = parser.parse_args()

    filename = "vaccine-booking-details.json"
    mobile = None

    print("Running VacCowin...")
    beep(500, 150)

    try:
        base_request_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        }

        if args.token:
            token = args.token
        else:
            mobile = input("Enter the Registered Mobile Number: ")
            token = generateTokenOTP(mobile, base_request_header)

        request_header = copy.deepcopy(base_request_header)
        request_header["Authorization"] = f"Bearer {token}"

        if os.path.exists(filename):
            print(
                "\n=================================== Note ===================================\n"
            )
            print(
                f"Information from a Previous Session already exists in {filename} in this directory."
            )
            print(
                f"IMPORTANT: If you're running this application for the first time then we recommend NOT To USE THE FILE!"
            )
            try_file = input(
                "Would you like to see the details from that file and confirm to proceed? (y/n Default y): "
            )
            try_file = try_file if try_file else "y"

            if try_file == "y":
                collected_details = getSavedUserInfo(filename)
                print(
                    "\n================================= Info =================================\n"
                )
                displayInfoDict(collected_details)

                file_acceptable = input(
                    "\nProceed with the above Information? (y/n Default n): "
                )
                file_acceptable = file_acceptable if file_acceptable else "n"

                if file_acceptable != "y":
                    collected_details = collectUserDetails(request_header)
                    saveUserInfo(filename, collected_details)

            else:
                collected_details = collectUserDetails(request_header)
                saveUserInfo(filename, collected_details)

        else:
            collected_details = collectUserDetails(request_header)
            saveUserInfo(filename, collected_details)
            confirmAndProceed(collected_details)

        info = SimpleNamespace(**collected_details)

        token_valid = True
        while token_valid:
            request_header = copy.deepcopy(base_request_header)
            request_header["Authorization"] = f"Bearer {token}"

            # call function to check and book slots
            token_valid = checkAndBook(
                request_header,
                info.beneficiary_dtls,
                info.location_dtls,
                info.search_option,
                min_slots=info.minimum_slots,
                ref_freq=info.refresh_freq,
                auto_book=info.auto_book,
                start_date=info.start_date,
                vaccine_type=info.vaccine_type,
                fee_type=info.fee_type,
            )

            # check if token is still valid
            beneficiaries_list = requests.get(BENEFICIARIES_URL, headers=request_header)
            if beneficiaries_list.status_code == 200:
                token_valid = True

            else:
                # if token invalid, regenerate OTP and new token
                beep(WARNING_BEEP_DURATION[0], WARNING_BEEP_DURATION[1])
                print("Token is INVALID!")
                token_valid = False

                tryOTP = input("Do you want to try for a new Token? (y/n Default y): ")
                if tryOTP.lower() == "y" or not tryOTP:
                    if not mobile:
                        mobile = input("Enter the Registered Mobile Number: ")
                    token = generateTokenOTP(mobile, base_request_header)
                    token_valid = True
                else:
                    print("Exiting the Script...")
                    os.system("pause")

    except Exception as e:
        print(str(e))
        print("Exiting the Script...")
        os.system("pause")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUser Aborted the Program.\nExiting, Please Wait...")
        sys.exit()
