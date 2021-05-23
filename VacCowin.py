#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import copy
import os
import sys
from types import SimpleNamespace

import requests
from colorama import Fore, Style, init

from utils.appointment import checkAndBook
from utils.displayData import displayInfoDict
from utils.generateOTP import generateTokenOTP
from utils.urls import *
from utils.userInfo import (
    collectUserDetails,
    confirmAndProceed,
    getSavedUserInfo,
    saveUserInfo,
)

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Passing the token directly")
    args = parser.parse_args()

    filename = "vaccine-booking-details.json"
    mobile = None

    print()
    print(f"{Fore.CYAN}", end="")
    print("Running VacCowin...")
    print(f"{Fore.RESET}", end="")
    beep(500, 150)

    try:
        base_request_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        }

        if args.token:
            token = args.token
        else:
            print(f"{Fore.YELLOW}", end="")
            mobile = input("Enter the Registered Mobile Number: ")
            print(f"{Fore.RESET}", end="")
            token = generateTokenOTP(mobile, base_request_header)

        request_header = copy.deepcopy(base_request_header)
        request_header["Authorization"] = f"Bearer {token}"

        if os.path.exists(filename):
            print(f"{Fore.RESET}", end="")
            print(
                "\n=================================== Note ===================================\n"
            )
            print(f"{Fore.GREEN}", end="")
            print(
                f"Information from a Previous Session already exists in {filename} in this directory."
            )
            print(f"{Fore.CYAN}", end="")
            print(
                f"IMPORTANT: If you're running this application for the first time then we recommend NOT To USE THE FILE!\n"
            )
            print(f"{Fore.YELLOW}", end="")
            try_file = input(
                "Would you like to see the details from that file and confirm to proceed? (y/n Default y): "
            )
            print(f"{Fore.RESET}", end="")
            try_file = try_file if try_file else "y"

            if try_file == "y":
                print(f"{Fore.RESET}", end="")
                collected_details = getSavedUserInfo(filename)
                print(
                    "\n================================= Info =================================\n"
                )
                displayInfoDict(collected_details)

                print(f"{Fore.YELLOW}", end="")
                file_acceptable = input(
                    "\nProceed with the above Information? (y/n Default n): "
                )
                print(f"{Fore.RESET}", end="")
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
                print(f"{Fore.RED}", end="")
                print("Token is INVALID!")
                print(f"{Fore.RESET}", end="")
                token_valid = False

                print(f"{Fore.YELLOW}", end="")
                tryOTP = input("Do you want to try for a new Token? (y/n Default y): ")
                if tryOTP.lower() == "y" or not tryOTP:
                    if not mobile:
                        print(f"{Fore.YELLOW}", end="")
                        mobile = input("Enter the Registered Mobile Number: ")
                    token = generateTokenOTP(mobile, base_request_header)
                    token_valid = True
                else:
                    print(f"{Fore.RED}", end="")
                    print("Exiting the Script...")
                    os.system("pause")
                    print(f"{Fore.RESET}", end="")

    except Exception as e:
        print(f"{Fore.RED}", end="")
        print(str(e))
        print("Exiting the Script...")
        os.system("pause")
        print(f"{Fore.RESET}", end="")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}User Aborted the Program.\nExiting, Please Wait...")
        sys.exit()
