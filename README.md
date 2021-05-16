<p align="center">
  <img src="https://socialify.git.ci/dhhruv/Vac-Cowin/image?description=1&forks=1&language=1&owner=1&pattern=Plus&stargazers=1&theme=Dark">
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
	<a href="https://dev.to/dhhruv/vaccowin-check-available-slots-for-cowin-vaccination-right-from-your-terminal-23f5">
    	<img src="https://img.shields.io/badge/dev.to-0A0A0A?style=for-the-badge&logo=dev.to&logoColor=white">
    </a>
</p>

## About:

**[CoWIN Portal](https://www.cowin.gov.in/home)** is used to self-register yourself for the **Vaccination** process in India. Here you can register yourself with your Phone Number and avail a slot from the available slots in various Vaccination Centres around the country.

## Introduction:

**VacCowin** is a CLI based Python Script that can be used to **Automate** Covid Vaccination Slot Booking on Co-WIN Platform. This script rechecks after every few seconds and when the slots are available, it confirms the slot after you enter the captcha shown on the screen.

Since India has started the Vaccination Drive for those above 18 years of age, there is a very heavy rush and slots get booked soon. This script will come in handy for booking those slots as soon as they open.

The data used is retrieved using the open public/protected APIs at [API Setu](https://apisetu.gov.in/public/marketplace/api/cowin). It works on both Linux and Windows.

## Initial Setup:

1. Install Python
2. Clone this repository...
```sh
git clone https://github.com/dhhruv/Vac-Cowin.git
``` 
**OR** 
Download the Zip and Extract the content.

3. Install, create and activate virtual environment.
For instance we create a virtual environment named 'venv'.
```sh
pip install virtualenv
python -m virtualenv venv
venv\Scripts\activate.bat
```

4. Install dependencies
```sh
cd Vac-Cowin
pip install -r requirements.txt
```

### Team Members:
1.  [Dhruv Panchal](https://github.com/dhhruv)
2.  [Urveshkumar Patel](https://github.com/urvesh254)
3.  [Nirja Desai](https://github.com/nirami98)

### Important: 
- This is a Proof of Concept Project. **I OR the Team** do NOT endorse or condone, in any shape or form, automating any monitoring/booking tasks. **Use this at your own risk.**
- This **Python Script CANNOT book slots automatically**. It doesn't skip any of the steps that a User would have to take on the official portal. You will still have to enter the OTP and Captcha as you do in the CoWIN Portal.
- **Do NOT** use unless all the beneficiaries selected are supposed to get the same Vaccine and Dose. 
- There is **no option** to Register a new Phone/Mobile or add beneficiaries. This can be used only after beneficiary has been added through the official Portal/App.
- Be careful if you're choosing to use the auto-book feature. It will blindly select first available Vaccination **Centre, Date (Both Sorted Ascending) and a RANDOM slot**. I would not recommend using this feature unless and until it's crucial.
- If you accidentally booked a slot you didn't want to then don’t worry. You can always log in to the CoWIN Portal and cancel/re-schedule that.
- **API Details (Do read the first paragraph): https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2**


<p align='center'><b>Made with ❤ by Dhruv Panchal</b></p>


