import tabulate
from colorama import Fore, Style, init

init(convert=True)


def viableOptions(resp, minimum_slots, min_age_booking, fee_type, dose):
    print(f"{Fore.RESET}", end="")
    options = []
    if len(resp["centers"]) >= 0:
        for center in resp["centers"]:
            for session in center["sessions"]:
                availability = min(
                    session[f"available_capacity_dose{dose}"],
                    session["available_capacity"],
                )
                if (
                    (availability >= minimum_slots)
                    and (session["min_age_limit"] <= min_age_booking)
                    and (center["fee_type"] in fee_type)
                ):
                    out = {
                        "name": center["name"],
                        "district": center["district_name"],
                        "pincode": center["pincode"],
                        "center_id": center["center_id"],
                        "vaccine": session["vaccine"],
                        "fee_type": center["fee_type"],
                        "available": availability,
                        "date": session["date"],
                        "slots": session["slots"],
                        "session_id": session["session_id"],
                    }
                    options.append(out)

                else:
                    pass
    else:
        pass

    return options


def displayTable(dict_list):
    """
    This function
        1. Takes a list of dictionary
        2. Add an Index column, and
        3. Displays the data in tabular format
    """
    header = ["idx"] + list(dict_list[0].keys())
    rows = [[idx + 1] + list(x.values()) for idx, x in enumerate(dict_list)]
    print(f"{Fore.RESET}", end="")
    print(tabulate.tabulate(rows, header, tablefmt="grid"))


def displayInfoDict(details):
    print(f"{Fore.RESET}", end="")
    for key, value in details.items():
        if isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                print(f"\t{key}:")
                displayTable(value)
            else:
                print(f"\t{key}\t: {value}")
        else:
            print(f"\t{key}\t: {value}")
