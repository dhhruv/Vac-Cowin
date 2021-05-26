import copy
import datetime
import os
import random
import sys
import time

import requests
from colorama import Fore, Style, init
from inputimeout import TimeoutOccurred, inputimeout

from utils.captcha import captchaBuilder
from utils.checkCalender import checkCalenderByDistrict, checkCalenderByPincode
from utils.displayData import displayTable
from utils.getData import getMinAge
from utils.urls import *

WARNING_BEEP_DURATION = (1000, 2000)

init(convert=True)

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


def generateCaptcha(request_header):
    print(f"{Fore.RESET}", end="")
    print(
        "================================= RECIEVING CAPTCHA =================================================="
    )
    resp = requests.post(CAPTCHA_URL, headers=request_header)
    print(f"{Fore.CYAN}", end="")
    print(f"Captcha Response Code: {resp.status_code}")
    print(f"{Fore.RESET}", end="")

    if resp.status_code == 200:
        # captchaBuilder(resp.json())
        return captchaBuilder(resp.json())


def bookAppointment(request_header, details):
    """
    This function
        1. Takes details in json format
        2. Attempts to book an appointment using the details
        3. Returns True or False depending on Token Validity
    """
    try:
        valid_captcha = True
        while valid_captcha:
            captcha = generateCaptcha(request_header)
            details["captcha"] = captcha

            print(f"{Fore.RESET}", end="")
            print(
                "================================= ATTEMPTING TO BOOK =================================================="
            )

            resp = requests.post(BOOKING_URL, headers=request_header, json=details)
            print(f"{Fore.CYAN}", end="")
            print(f"Booking Response Code: {resp.status_code}")
            print(f"Booking Response : {resp.text}")
            print(f"{Fore.RESET}", end="")

            if resp.status_code == 401:
                print(f"{Fore.RED}", end="")
                print("TOKEN is INVALID!")
                print(f"{Fore.RESET}", end="")
                return False

            elif resp.status_code == 200:
                beep(WARNING_BEEP_DURATION[0], WARNING_BEEP_DURATION[1])
                print(f"{Fore.GREEN}", end="")
                print(
                    "\n\n##############    BOOKED!  ############################    BOOKED!  ##############"
                )
                print(
                    "                Congratulations! You've Successfully Booked a Slot!                       \n"
                )

                print("\nPress any key thrice to Exit the Program.")
                os.system("pause")
                os.system("pause")
                os.system("pause")
                print(f"{Fore.RESET}", end="")
                sys.exit()

            elif resp.status_code == 400:
                print(f"{Fore.RED}", end="")
                print(f"Response: {resp.status_code} : {resp.text}")
                print(f"{Fore.RESET}", end="")
                pass

            else:
                print(f"{Fore.RED}", end="")
                print(f"Response: {resp.status_code} : {resp.text}")
                print(f"{Fore.RESET}", end="")
                return True

    except Exception as e:
        print(f"{Fore.RED}", end="")
        print(str(e))
        print(f"{Fore.RESET}", end="")
        print("\n\n")
        beep(WARNING_BEEP_DURATION[0], WARNING_BEEP_DURATION[1])


def checkAndBook(
    request_header, beneficiary_dtls, location_dtls, search_option, **kwargs
):
    """
    This function
        1. Checks the vaccination calendar for available slots,
        2. Lists all viable options,
        3. Takes user's choice of vaccination center and slot,
        4. Calls function to book appointment, and
        5. Returns True or False depending on Token Validity
    """
    try:
        min_age_booking = getMinAge(beneficiary_dtls)

        minimum_slots = kwargs["min_slots"]
        refresh_freq = kwargs["ref_freq"]
        auto_book = kwargs["auto_book"]
        start_date = kwargs["start_date"]
        vaccine_type = kwargs["vaccine_type"]
        fee_type = kwargs["fee_type"]

        """ dose = (
            2
            if [beneficiary["status"] for beneficiary in beneficiary_dtls][0]
            == "Partially Vaccinated"
            else 1
        ) """

        dose = (
            2 if any(beneficiary["vaccine"] for beneficiary in beneficiary_dtls) else 1
        )

        # dose = (2 if any(detail['vaccine'] for detail in collected_details["beneficiary_dtls"]) else 1)

        if isinstance(start_date, int) and start_date == 2:
            start_date = datetime.datetime.today() + datetime.timedelta(days=1)
        elif isinstance(start_date, int) and start_date == 1:
            start_date = datetime.datetime.today()
        else:
            pass

        num_days = 7
        list_format = [start_date + datetime.timedelta(days=i) for i in range(num_days)]
        actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

        if search_option == 2:
            options = checkCalenderByDistrict(
                request_header,
                vaccine_type,
                location_dtls,
                actual_dates,
                minimum_slots,
                min_age_booking,
                fee_type,
                dose,
            )
        else:
            options = checkCalenderByPincode(
                request_header,
                vaccine_type,
                location_dtls,
                actual_dates,
                minimum_slots,
                min_age_booking,
                fee_type,
                dose,
            )

        if isinstance(options, bool):
            return False

        options = sorted(
            options,
            key=lambda k: (
                k["district"].lower(),
                k["pincode"],
                k["name"].lower(),
                datetime.datetime.strptime(k["date"], "%d-%m-%Y"),
            ),
        )

        tmp_options = copy.deepcopy(options)
        if len(tmp_options) > 0:
            cleaned_options_for_display = []
            for item in tmp_options:
                item.pop("session_id", None)
                item.pop("center_id", None)
                cleaned_options_for_display.append(item)

            displayTable(cleaned_options_for_display)
            if auto_book == "yes-please":
                print(f"{Fore.GREEN}", end="")
                print(
                    "AUTO-BOOKING IS ENABLED. PROCEEDING WITH FIRST CENTRE, DATE, and RANDOM SLOT."
                )
                print(f"{Fore.RESET}", end="")
                option = options[0]
                random_slot = random.randint(1, len(option["slots"]))
                choice = f"1.{random_slot}"
            else:
                print(f"{Fore.YELLOW}", end="")
                choice = inputimeout(
                    prompt="----------> Wait 20 seconds for Updated Options OR \n----------> Enter a choice e.g: 1.4 for (1st Centre & 4th Slot): ",
                    timeout=20,
                )
                print(f"{Fore.RESET}", end="")

        else:
            for i in range(refresh_freq, 0, -1):
                print(f"{Fore.YELLOW}", end="")
                msg = f"No Options Available right now. Next Update in {i} seconds.."
                print(msg, end="\r", flush=True)
                print(f"{Fore.RESET}", end="")
                sys.stdout.flush()
                time.sleep(1)
            choice = "."

    except TimeoutOccurred:
        time.sleep(1)
        return True

    else:
        if choice == ".":
            return True
        else:
            try:
                choice = choice.split(".")
                choice = [int(item) for item in choice]
                print(f"{Fore.GREEN}", end="")
                print(
                    f"============> Got a Choice: Center #{choice[0]}, Slot #{choice[1]}\n"
                )
                print(f"{Fore.RESET}", end="")

                new_req = {
                    "beneficiaries": [
                        beneficiary["bref_id"] for beneficiary in beneficiary_dtls
                    ],
                    "dose": 2
                    if any(beneficiary["vaccine"] for beneficiary in beneficiary_dtls)
                    else 1,
                    "center_id": options[choice[0] - 1]["center_id"],
                    "session_id": options[choice[0] - 1]["session_id"],
                    "slot": options[choice[0] - 1]["slots"][choice[1] - 1],
                }

                print(f"{Fore.GREEN}", end="")
                print(f"Booking with Information: {new_req}")
                print(f"{Fore.RESET}", end="")
                return bookAppointment(request_header, new_req)

            except IndexError:
                print(f"{Fore.RED}", end="")
                print("============> Invalid Option Entered!")
                print(f"{Fore.RESET}", end="")
                os.system("pause")
                pass
