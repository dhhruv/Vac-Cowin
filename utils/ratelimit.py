import sys
import time

from colorama import Fore, Style, init

init(convert=True)


def handleRateLimited():

    print()
    for i in range(5, 0, -1):
        print(f"{Fore.RED}", end="")
        msg = f"Rate Limited by CoWIN. Waiting for {i} seconds.."
        print(msg, end="\r", flush=True)
        print(f"{Fore.RESET}", end="")
        sys.stdout.flush()
        time.sleep(1)

    print(
        "(You can reduce your refresh frequency. Please note that other devices/browsers using CoWIN/Umang/Arogya Setu also contribute to same limit.)"
    )
    time.sleep(2)
    print(f"{Fore.RESET}", end="")
