<p align="center">
  <img src="https://github.com/dhhruv/Vac-Cowin/blob/master/assets/thumbnail.png">
  <h2 align="center" style="margin-top: -4px !important;">Check Available Slots for CoWIN Vaccination right from your Terminal!</h2>
  <p align="center">
    <a href="https://github.com/dhhruv/Vac-Cowin/blob/master/LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-informational">
    </a>
    <a href="https://www.python.org/">
    	<img src="https://img.shields.io/badge/python-v3.8-informational">
    </a>
  </p>
</p>
<p align="center">
	<img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
</p>
<p align="center">   
	<a href="">
    	<img src="https://img.shields.io/badge/dev.to-0A0A0A?style=for-the-badge&logo=dev.to&logoColor=white">
    </a>
</p>

## About:

**[CoWIN Portal](https://www.cowin.gov.in/home)** is used to self-register yourself for the **Vaccination** process in India. Here you can register yourself with your Phone Number and avail a slot from the available slots in various Vaccination Centres around the country.

## Introduction:

**VacCowin** is a Python Script to find open slots for Vaccination in India based on your **pincode (or multiple pincodes) or State and District**. This script will recheck after every few minutes and as soon the slots open, inform you via Beeping sound & Desktop notification.

Since India has started the Vaccination Drive for those above 18 years of age, there is a very heavy rush and slots get booked soon. This script will come in handy for finding those slots as soon as they open.

The data is retrieved using the open public APIs at [API Setu](https://apisetu.gov.in/public/marketplace/api/cowin). It works on both Linux and Windows.

## Setup:

1. Install Python
2. Clone this repository...
```sh
git clone https://github.com/dhhruv/Vac-Cowin.git
```

3. Install, create and activate virtual environment.
For instance we create a virtual environment named 'venv'.
```sh
pip install virtualenv
python -m virtualenv venv
venv\Scripts\activate.bat
```

4. Install dependencies
```sh
pip install -r requirements.txt
```
## Input:

| Tags              | Actions                                                         |
|-------------------|-----------------------------------------------------------------|
| `-h, --help`      | Show the Help Message and exiting the program.               |
| `-p, --pincode `           | Pincode(s) to look for slots.     |
| `-a, --age`| Age of the User(Default = 18).                                |
| `-d, --date`           | Date to check Vaccination(Format = DD-MM-YYYY).                           |
| `-w, --wizard`               | For a User Friendly Interface.     |
| `-i, --interval`               | Interval in which to read Data from CoWin Website in Seconds. (Default = 300)    |
| `-s, --state`               | The State you want to search for.     |
| `-t, --district`               | The District you want to search for.    |



## Usage 
**1.  Using Pincode(s):**
-   You can check the available slots by entering Pincode(s) using `-p` specified with age using `-a`.
**Example: `python VacCowin.py -p 382150 -a 47`**
![Method 1](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/Method1.gif)

**2.  Using State and District:**
-   You can check the available slots by entering State using `-s` and District using`-t` specified with age using `-a`.
**Example: `python VacCowin.py -s Gujarat -t Ahmedabad -a 19`**
![Method 2](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/Method2.gif)

**3.  Using Wizard Mode(For Beginners):**
-    If you're a beginner then you can specify `-w` in the Terminal or directly run the Script to enter the Wizard Mode for Beginners.
**Examples:
`python VacCowin.py -w`**
**OR**
**`python VacCowin.py`**

-   Enter the Information asked to check the Available Slots.
![Method 3](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/Method3.gif)

**Note:- Either Proceed through Pincode Method OR (State and District) Method for a reliable response.** 

<p align='center'><b>Made with ❤ by Dhruv Panchal</b></p>


