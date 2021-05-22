import os
import sys

from colorama import Fore, Style, init

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


def getVaccinePreference():
    print(
        "\nIt seems that you're trying to find a Slot for your First Dose. Do you have a Preference for Vaccine Type?\n"
    )
    print(f"{Fore.YELLOW}", end="")
    preference = input(
        "Enter 0 for No Preference, 1 for COVISHIELD, 2 for COVAXIN, or 3 for SPUTNIK V. Default 0 : "
    )
    print(f"{Fore.RESET}", end="")
    preference = (
        int(preference) if preference and int(preference) in [0, 1, 2, 3] else 0
    )

    if preference == 1:
        return "COVISHIELD"
    elif preference == 2:
        return "COVAXIN"
    elif preference == 3:
        return "SPUTNIK V"
    else:
        return None


def getFeeTypePreference():
    print(f"{Fore.YELLOW}", end="")
    print("\nDo you have a Preference for Fee Type?")
    preference = input(
        "Enter 0 for No Preference, 1 for Free Only, or 2 for Paid Only. Default 0 : "
    )
    print(f"{Fore.RESET}", end="")
    preference = int(preference) if preference and int(preference) in [0, 1, 2] else 0

    if preference == 1:
        return ["Free"]
    elif preference == 2:
        return ["Paid"]
    else:
        return ["Free", "Paid"]
