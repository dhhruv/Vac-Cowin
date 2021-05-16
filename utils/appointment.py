import copy
import datetime
import os
import random
import sys
import time

import requests
from inputimeout import TimeoutOccurred, inputimeout

from utils.captcha import captchaBuilder
from utils.checkCalender import check_calendar_by_district, check_calendar_by_pincode
from utils.displayData import display_table
from utils.getData import get_min_age

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


def generate_captcha(request_header):
    print(
        "================================= GETTING CAPTCHA =================================================="
    )
    resp = requests.post(CAPTCHA_URL, headers=request_header)
    print(f"Booking Response Code: {resp.status_code}")

    if resp.status_code == 200:
        # captchaBuilder(resp.json())
        captcha = captchaBuilder(resp.json())
        return captcha


def book_appointment(request_header, details):
    """
    This function
        1. Takes details in json format
        2. Attempts to book an appointment using the details
        3. Returns True or False depending on Token Validity
    """
    try:
        valid_captcha = True
        while valid_captcha:
            captcha = generate_captcha(request_header)
            details["captcha"] = captcha

            print(
                "================================= ATTEMPTING BOOKING =================================================="
            )

            resp = requests.post(BOOKING_URL, headers=request_header, json=details)
            print(f"Booking Response Code: {resp.status_code}")
            print(f"Booking Response : {resp.text}")

            if resp.status_code == 401:
                print("TOKEN INVALID")
                return False

            elif resp.status_code == 200:
                beep(WARNING_BEEP_DURATION[0], WARNING_BEEP_DURATION[1])
                print(
                    "##############    BOOKED!  ############################    BOOKED!  ##############"
                )
                print(
                    "                        Hey, Hey, Hey! It's your lucky day!                       "
                )
                print("\nPress any key thrice to exit program.")
                os.system("pause")
                os.system("pause")
                os.system("pause")
                sys.exit()

            elif resp.status_code == 400:
                print(f"Response: {resp.status_code} : {resp.text}")
                pass

            else:
                print(f"Response: {resp.status_code} : {resp.text}")
                return True

    except Exception as e:
        print(str(e))
        beep(WARNING_BEEP_DURATION[0], WARNING_BEEP_DURATION[1])


def check_and_book(
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
        min_age_booking = get_min_age(beneficiary_dtls)

        minimum_slots = kwargs["min_slots"]
        refresh_freq = kwargs["ref_freq"]
        auto_book = kwargs["auto_book"]
        start_date = kwargs["start_date"]
        vaccine_type = kwargs["vaccine_type"]
        fee_type = kwargs["fee_type"]

        if isinstance(start_date, int) and start_date == 2:
            start_date = (
                datetime.datetime.today() + datetime.timedelta(days=1)
            ).strftime("%d-%m-%Y")
        elif isinstance(start_date, int) and start_date == 1:
            start_date = datetime.datetime.today().strftime("%d-%m-%Y")
        else:
            pass

        if search_option == 2:
            options = check_calendar_by_district(
                request_header,
                vaccine_type,
                location_dtls,
                start_date,
                minimum_slots,
                min_age_booking,
                fee_type,
            )
        else:
            options = check_calendar_by_pincode(
                request_header,
                vaccine_type,
                location_dtls,
                start_date,
                minimum_slots,
                min_age_booking,
                fee_type,
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

            display_table(cleaned_options_for_display)
            if auto_book == "yes-please":
                print(
                    "AUTO-BOOKING IS ENABLED. PROCEEDING WITH FIRST CENTRE, DATE, and RANDOM SLOT."
                )
                option = options[0]
                random_slot = random.randint(1, len(option["slots"]))
                choice = f"1.{random_slot}"
            else:
                choice = inputimeout(
                    prompt="----------> Wait 20 seconds for updated options OR \n----------> Enter a choice e.g: 1.4 for (1st center 4th slot): ",
                    timeout=20,
                )

        else:
            for i in range(refresh_freq, 0, -1):
                msg = f"No viable options. Next update in {i} seconds.."
                print(msg, end="\r", flush=True)
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
                print(
                    f"============> Got Choice: Center #{choice[0]}, Slot #{choice[1]}"
                )

                new_req = {
                    "beneficiaries": [
                        beneficiary["bref_id"] for beneficiary in beneficiary_dtls
                    ],
                    "dose": 2
                    if [beneficiary["status"] for beneficiary in beneficiary_dtls][0]
                    == "Partially Vaccinated"
                    else 1,
                    "center_id": options[choice[0] - 1]["center_id"],
                    "session_id": options[choice[0] - 1]["session_id"],
                    "slot": options[choice[0] - 1]["slots"][choice[1] - 1],
                }

                print(f"Booking with info: {new_req}")
                return book_appointment(request_header, new_req)

            except IndexError:
                print("============> Invalid Option!")
                os.system("pause")
                pass
