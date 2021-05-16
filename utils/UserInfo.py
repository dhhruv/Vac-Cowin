import datetime
import json
import os
import sys
from collections import Counter

from utils.displayData import displayInfoDict
from utils.getData import getBeneficiaries, getDistricts, getPincodes
from utils.preferences import getFeeTypePreference, getVaccinePreference

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


def confirmAndProceed(collected_details):
    print(
        "\n================================= Confirm Info =================================\n"
    )
    displayInfoDict(collected_details)

    confirm = input("\nProceed with above info (y/n Default y) : ")
    confirm = confirm if confirm else "y"
    if confirm != "y":
        print("Details not confirmed. Exiting process.")
        os.system("pause")
        sys.exit()


def saveUserInfo(filename, details):
    print(
        "\n================================= Save Info =================================\n"
    )
    save_info = input(
        "Would you like to save this as a JSON file for easy use next time?: (y/n Default y): "
    )
    save_info = save_info if save_info else "y"
    if save_info == "y":
        with open(filename, "w") as f:
            json.dump(details, f)

        print(f"Info saved to {filename} in {os.getcwd()}")


def getSavedUserInfo(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    return data


def collectUserDetails(request_header):
    # Get Beneficiaries
    print("Fetching registered beneficiaries.. ")
    beneficiary_dtls = getBeneficiaries(request_header)

    if len(beneficiary_dtls) == 0:
        print("There should be at least one beneficiary. Exiting.")
        os.system("pause")
        sys.exit(1)

    # Make sure all beneficiaries have the same type of vaccine
    vaccine_types = [beneficiary["vaccine"] for beneficiary in beneficiary_dtls]
    vaccines = Counter(vaccine_types)

    if len(vaccines.keys()) != 1:
        print(
            f"All beneficiaries in one attempt should have the same vaccine type. Found {len(vaccines.keys())}"
        )
        os.system("pause")
        sys.exit(1)

    # if all([beneficiary['status'] == 'Partially Vaccinated' for beneficiary in beneficiary_dtls]) else None
    vaccine_type = vaccine_types[0]
    if not vaccine_type:
        print(
            "\n================================= Vaccine Info =================================\n"
        )
        vaccine_type = getVaccinePreference()

    print(
        "\n================================= Location Info =================================\n"
    )
    # get search method to use
    search_option = input(
        """Search by Pincode? Or by State/District? \nEnter 1 for Pincode or 2 for State/District. (Default 2) : """
    )

    if not search_option or int(search_option) not in [1, 2]:
        search_option = 2
    else:
        search_option = int(search_option)

    if search_option == 2:
        # Collect vaccination center preferance
        location_dtls = getDistricts(request_header)

    else:
        # Collect vaccination center preferance
        location_dtls = getPincodes()

    print(
        "\n================================= Additional Info =================================\n"
    )

    # Set filter condition
    minimum_slots = input(
        f"Filter out centers with availability less than ? Minimum {len(beneficiary_dtls)} : "
    )
    if minimum_slots:
        minimum_slots = (
            int(minimum_slots)
            if int(minimum_slots) >= len(beneficiary_dtls)
            else len(beneficiary_dtls)
        )
    else:
        minimum_slots = len(beneficiary_dtls)

    # Get refresh frequency
    refresh_freq = input(
        "How often do you want to refresh the calendar (in seconds)? Default 15. Minimum 5. : "
    )
    refresh_freq = int(refresh_freq) if refresh_freq and int(refresh_freq) >= 5 else 15

    # Get search start date
    start_date = input(
        "\nSearch for next seven day starting from when?\nUse 1 for today, 2 for tomorrow, or provide a date in the format yyyy-mm-dd. Default 2: "
    )
    if not start_date:
        start_date = 2
    elif start_date in ["1", "2"]:
        start_date = int(start_date)
    else:
        try:
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            start_date = 2

    # Get preference of Free/Paid option
    fee_type = getFeeTypePreference()

    print(
        "\n=========== CAUTION! =========== CAUTION! CAUTION! =============== CAUTION! =======\n"
    )
    print(
        "===== BE CAREFUL WITH THIS OPTION! AUTO-BOOKING WILL BOOK THE FIRST AVAILABLE CENTRE, DATE, AND A RANDOM SLOT! ====="
    )
    auto_book = input(
        "Do you want to enable auto-booking? (yes-please or no) Default no: "
    )
    auto_book = "no" if not auto_book else auto_book

    collected_details = {
        "beneficiary_dtls": beneficiary_dtls,
        "location_dtls": location_dtls,
        "search_option": search_option,
        "minimum_slots": minimum_slots,
        "refresh_freq": refresh_freq,
        "auto_book": auto_book,
        "start_date": start_date,
        "vaccine_type": vaccine_type,
        "fee_type": fee_type,
    }

    return collected_details
