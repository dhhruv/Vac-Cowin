import datetime
import json
import os
import sys
from collections import Counter

from colorama import Fore, Style, init

from utils.displayData import displayInfoDict
from utils.getData import getBeneficiaries, getDistricts, getPincodes
from utils.preferences import getFeeTypePreference, getVaccinePreference
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


def confirmAndProceed(collected_details):
    print(f"{Fore.RESET}", end="")
    print(
        "\n================================= Confirm the Information =================================\n"
    )
    displayInfoDict(collected_details)

    print(f"{Fore.YELLOW}", end="")
    confirm = input("\nProceed with the above Information (y/n Default y) : ")
    print(f"{Fore.RESET}", end="")
    confirm = confirm if confirm else "y"
    if confirm != "y":
        print(f"{Fore.RED}", end="")
        print("Details not Confirmed. Exiting the Process.")
        print("Please Wait...")
        os.system("pause")
        print(f"{Fore.RESET}", end="")
        sys.exit()


def saveUserInfo(filename, details):
    print(f"{Fore.RESET}", end="")
    print(
        "\n================================= Save Information =================================\n"
    )
    print(f"{Fore.YELLOW}", end="")
    save_info = input(
        "Would you like to save this Session's Data as a JSON File for easy use the next time?: (y/n Default y): "
    )
    print(f"{Fore.RESET}", end="")
    save_info = save_info if save_info else "y"
    if save_info == "y":
        with open(filename, "w") as f:
            json.dump(details, f)
        print(f"{Fore.GREEN}", end="")
        print(f"Information saved to {filename} in {os.getcwd()}")
        print(f"{Fore.RESET}", end="")


def getSavedUserInfo(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    return data


def collectUserDetails(request_header):
    # Get Beneficiaries
    print(f"{Fore.CYAN}", end="")
    print("Fetching the Registered Beneficiaries... ")
    print(f"{Fore.RESET}", end="")
    beneficiary_dtls = getBeneficiaries(request_header)

    if len(beneficiary_dtls) == 0:
        print(f"{Fore.RED}", end="")
        print("There should be at least one Beneficiary.")
        print("Please Login to the CoWIN Portal to Add a Beneficiary.")
        print("Exiting")
        os.system("pause")
        print(f"{Fore.RESET}", end="")
        sys.exit(1)

    # Make sure all beneficiaries have the same type of vaccine
    vaccine_types = [beneficiary["vaccine"] for beneficiary in beneficiary_dtls]
    statuses = [beneficiary["status"] for beneficiary in beneficiary_dtls]

    if len(set(statuses)) > 1:
        print(f"{Fore.RED}", end="")
        print(
            "\n================================= Important =================================\n"
        )
        print(
            f"All Beneficiaries trying to book slot in one attempt should be of same Vaccination Status (Same Dose). Found {statuses}"
        )
        os.system("pause")
        print(f"{Fore.RESET}", end="")
        sys.exit(1)

    # if all([beneficiary['status'] == 'Partially Vaccinated' for beneficiary in beneficiary_dtls]) else None
    vaccines = set(vaccine_types)
    if len(vaccines) > 1 and ("" in vaccines):
        vaccines.remove("")
        vaccine_types.remove("")
        print(f"{Fore.RESET}", end="")
        print(
            "\n================================= Important =================================\n"
        )
        print(
            f"Some of the Beneficiaries have a set the Vaccine Preference ({vaccines}) and some do not."
        )
        print(
            "Results will be filtered to show only according to the set Vaccine Preference."
        )
        os.system("pause")

    if len(vaccines) != 1:
        print(f"{Fore.RED}", end="")
        print(
            "\n================================= Important =================================\n"
        )
        print(
            f"All Beneficiaries in one attempt should have the same Vaccine type. Found {len(vaccines)}"
        )
        os.system("pause")
        print(f"{Fore.RESET}", end="")
        sys.exit(1)

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
    print(f"{Fore.YELLOW}", end="")
    search_option = input(
        """\nSearch by Pincode? OR by State & District? \nEnter 1 for Pincode or 2 for State & District. (Default 2) : """
    )
    print(f"{Fore.RESET}", end="")

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
    print(f"{Fore.YELLOW}", end="")
    minimum_slots = input(
        f"\nFilter out Centres with Vaccine availability less than ? Minimum {len(beneficiary_dtls)} : "
    )
    print(f"{Fore.RESET}", end="")
    if minimum_slots:
        minimum_slots = (
            int(minimum_slots)
            if int(minimum_slots) >= len(beneficiary_dtls)
            else len(beneficiary_dtls)
        )
    else:
        minimum_slots = len(beneficiary_dtls)

    # Get refresh frequency
    print(f"{Fore.YELLOW}", end="")
    refresh_freq = input(
        "How often do you want to load Data from the Portal (in Seconds)? Default 15. Minimum 5. : "
    )
    print(f"{Fore.RESET}", end="")
    refresh_freq = int(refresh_freq) if refresh_freq and int(refresh_freq) >= 5 else 15

    # Get search start date
    print(f"{Fore.YELLOW}", end="")
    start_date = input(
        "\nSearch for next seven day starting from when? \nUse 1 for Today, 2 for Tomorrow, or provide a date in the format DD-MM-YYYY. Default 2: "
    )
    print(f"{Fore.RESET}", end="")
    if not start_date:
        start_date = 2
    elif start_date in ["1", "2"]:
        start_date = int(start_date)
    else:
        try:
            datetime.datetime.strptime(start_date, "%d-%m-%Y")
        except ValueError:
            print(f"{Fore.BLUE}", end="")
            print("Invalid Date! Proceeding with Tomorrow's Date.")
            print(f"{Fore.RESET}", end="")
            start_date = 2

    # Get preference of Free/Paid option
    fee_type = getFeeTypePreference()

    print(
        "\n============================ PROCEED WITH CAUTION! ============================\n"
    )
    print(
        "===== BE CAREFUL WITH THIS OPTION! AUTO-BOOKING WILL BOOK THE FIRST AVAILABLE CENTRE, DATE, AND A RANDOM SLOT! =====\n"
    )
    print(f"{Fore.YELLOW}", end="")
    auto_book = input(
        "Do you want to Enable the Auto-Booking Function? (yes-please or no) Default no: "
    )
    print(f"{Fore.RESET}", end="")
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
