import datetime
import os
import sys

import requests
from colorama import Fore, Style, init

from utils.displayData import viableOptions
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


def checkCalenderByDistrict(
    request_header,
    vaccine_type,
    location_dtls,
    start_date,
    minimum_slots,
    min_age_booking,
    fee_type,
    dose,
):
    """
    This function
        1. Takes details required to check vaccination calendar
        2. Filters result by minimum number of slots available
        3. Returns False if token is invalid
        4. Returns list of vaccination centers & slots if available
    """
    try:
        print(
            "==================================================================================="
        )
        today = datetime.datetime.today()
        base_url = CALENDAR_URL_DISTRICT

        if vaccine_type:
            base_url += f"&vaccine={vaccine_type}"

        options = []
        for location in location_dtls:
            resp = requests.get(
                base_url.format(location["district_id"], start_date),
                headers=request_header,
            )

            if resp.status_code == 401:
                print(f"{Fore.RED}", end="")
                print("TOKEN is INVALID!")
                print(f"{Fore.RESET}", end="")
                return False

            elif resp.status_code == 200:
                resp = resp.json()
                if "centers" in resp:
                    print(f"{Fore.YELLOW}", end="")
                    print(
                        f"Centres are available in {location['district_name']} from {start_date} as of {today.strftime('%Y-%m-%d %H:%M:%S')}: {len(resp['centers'])}"
                    )
                    print(f"{Fore.RESET}", end="")
                    options += viableOptions(
                        resp, minimum_slots, min_age_booking, fee_type, dose
                    )

            else:
                pass

        for location in location_dtls:
            if location["district_name"] in [option["district"] for option in options]:
                for _ in range(2):
                    beep(location["alert_freq"], 150)
        return options

    except Exception as e:
        print(f"{Fore.RED}", end="")
        print(str(e))
        print(f"{Fore.RESET}", end="")
        beep(WARNING_BEEP_DURATION[0], WARNING_BEEP_DURATION[1])


def checkCalenderByPincode(
    request_header,
    vaccine_type,
    location_dtls,
    start_date,
    minimum_slots,
    min_age_booking,
    fee_type,
    dose,
):
    """
    This function
        1. Takes details required to check vaccination calendar
        2. Filters result by minimum number of slots available
        3. Returns False if token is invalid
        4. Returns list of vaccination centers & slots if available
    """
    try:
        print(
            "==================================================================================="
        )
        today = datetime.datetime.today()
        base_url = CALENDAR_URL_PINCODE

        if vaccine_type:
            base_url += f"&vaccine={vaccine_type}"

        options = []
        for location in location_dtls:
            resp = requests.get(
                base_url.format(location["pincode"], start_date), headers=request_header
            )

            if resp.status_code == 401:
                print(f"{Fore.RED}", end="")
                print("TOKEN is INVALID!")
                print(f"{Fore.RESET}", end="")
                return False

            elif resp.status_code == 200:
                resp = resp.json()
                if "centers" in resp:
                    print(f"{Fore.YELLOW}", end="")
                    print(
                        f"Centres are available in {location['pincode']} from {start_date} as of {today.strftime('%Y-%m-%d %H:%M:%S')}: {len(resp['centers'])}"
                    )
                    print(f"{Fore.RESET}", end="")
                    options += viableOptions(
                        resp, minimum_slots, min_age_booking, fee_type, dose
                    )

            else:
                pass

        for location in location_dtls:
            if int(location["pincode"]) in [option["pincode"] for option in options]:
                for _ in range(2):
                    beep(location["alert_freq"], 150)

        return options

    except Exception as e:
        print(f"{Fore.RED}", end="")
        print(str(e))
        print(f"{Fore.RESET}", end="")
        beep(WARNING_BEEP_DURATION[0], WARNING_BEEP_DURATION[1])
