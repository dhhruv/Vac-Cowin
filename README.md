
<p align="center">
	<img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
</p>
<p align="center">   
	<a href="https://dev.to/dhhruv/book-cowin-vaccination-slots-directly-from-your-terminal-7nb">
    	<img src="https://img.shields.io/badge/dev.to-0A0A0A?style=for-the-badge&logo=dev.to&logoColor=white">
    </a>
</p>

## Table of Contents:

 <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#how-to-use">How to Use</a></li>
    <li><a href="#working-screenshots">Working Screenshots</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#team-members">Team Members</a></li>
    <li><a href="#important">Important</a></li>

  </ol>

## Introduction

**[CoWIN Portal](https://www.cowin.gov.in/home)** is used to self-register yourself for the **Vaccination** process in India. Here you can register yourself with your Phone Number and avail a slot from the available slots in various Vaccination Centres around the country.

## About

**VacCowin** is a CLI based Python Script that can be used to perform tasks such as OTP Generation till Vaccination Slot Booking from Co-WIN Platform directly from your Terminal.  This script rechecks after every few seconds and when the slots are available, it **confirms the slot only after you enter the captcha shown on the screen.**

Since India has started the Vaccination Drive for those above 18 years of age, there is a very heavy rush and slots get booked soon. This script will come in handy for booking those slots as soon as they open.

**IMPORTANT: This is a Proof of Concept (POC) Project. I OR the Team do NOT endorse or condone, in any shape or form, automating any monitoring/booking tasks. It's only made for Educational Purposes. Use this at your own risk.**

The data used is retrieved using the open APIs at [API Setu](https://apisetu.gov.in/public/marketplace/api/cowin). It works on both Linux and Windows.

## Getting Started

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
## How To Use

1. Run the Script after performing the Initial Steps of [Getting Started](#getting-started):
	`python VacCowin.py`
2. Select the Beneficiaries. Read the Important notes. You can select multiple beneficiaries by providing comma-separated index values such as `1,2`:

```
Running VacCowin...
Enter the Registered Mobile Number: ██████████
Successfully Requested OTP for the Mobile Number ██████████ at 2021-05-23 09:28:41.669816..
Enter OTP (If you do not recieve OTP in 2 minutes, Press Enter to Retry): ██████████
Validating OTP. Please Wait...
Token Generated: ██████████████████████████████████████████████████████████████████████

Fetching the Registered Beneficiaries...
+-------+----------------+---------------+-----------+-------+----------------------+
|   idx |        bref_id | name          | vaccine   |   age | status               |
+=======+================+===============+===========+=======+======================+
|     1 | ██████████████ | █████████████ | ███████   |    ██ | ██████████████       |
+-------+----------------+---------------+-----------+-------+----------------------+

    ################# IMPORTANT THINGS TO BE REMEMBERED #################
    
    # 1. While selecting Beneficiaries, make sure that selected Beneficiaries are all taking the same dose: either their First OR Second.
    #    Please do no try to club together booking for first dose for one Beneficiary and second dose for another Beneficiary. Recommended to do both seperately.
    
    # 2. While selecting Beneficiaries, also make sure that Beneficiaries selected for second dose are all taking the same vaccine: COVISHIELD OR COVAXIN OR SPUTNIK V.
    #    Please do no try to club together booking for Beneficiary taking COVISHIELD with Beneficiary taking COVAXIN and other possibilities.
    
    # 3. If you're selecting multiple Beneficiaries, make sure all are of the same Age Group (45+ or 18+) as defined by the Government.
    #    Please do not try to club together booking for Younger and Older Beneficiaries at the same time.

    #####################################################################
```
```
Enter comma separated index numbers of Beneficiaries to book for : 1
```


3. Ensure that the Beneficiaries are getting selected:
```
Selected Beneficiaries are:  
+-------+----------------+---------------+-----------+-------+----------------------+
|   idx |        bref_id | name          | vaccine   |   age | status               |
+=======+================+===============+===========+=======+======================+
|     1 | ██████████████ | █████████████ | ███████   |    ██ | ██████████████       |
+-------+----------------+---------------+-----------+-------+----------------------+
```

4. Selecting the State:
```
+-------+-----------------------------+  
| idx   | state                       |  
+=======+=============================+  
| 1     | Andaman and Nicobar Islands |  
+-------+-----------------------------+  
| 2     | Andhra Pradesh              |  
+-------+-----------------------------+
+-------+-----------------------------+
+-------+-----------------------------+  
| 35    | Uttar Pradesh               |  
+-------+-----------------------------+  
| 36    | Uttarakhand                 |  
+-------+-----------------------------+  
| 37    | West Bengal                 |  
+-------+-----------------------------+
```
```
Enter State Index from the Table: 12
```
	
5. Select the Districts you are interested in. Multiple Districts can be selected by providing comma-separated index values...
```
+-------+-------------------------+
|   idx | district                |
+=======+=========================+
|     1 | Ahmedabad               |
+-------+-------------------------+
|     2 | Ahmedabad Corporation   |
+-------+-------------------------+
|    .. | ......                  |
+-------+-------------------------+
|    41 | Valsad                  |
+-------+-------------------------+
```
```
Enter comma separated index numbers of Districts to monitor : 2
```
6. Ensure that the correct Districts are getting selected...
```
Selected Districts are:
+-------+---------------+-----------------------+--------------+
|   idx |   district_id | district_name         |   alert_freq |
+=======+===============+=======================+==============+
|     1 |           770 | Ahmedabad Corporation |          660 |
+-------+---------------+-----------------------+--------------+
```

7. Additional Information regarding Vaccination Availability, Loading Data, Date etc... to be added by the User. 
```
Filter out Centres with Vaccine availability less than ? Minimum 1 :
How often do you want to load Data from the Portal (in Seconds)? Default 15. Minimum 5. :

Search for next seven day starting from when?
Use 1 for Today, 2 for Tomorrow, or provide a date in the format DD-MM-YYYY. Default 2:

Do you have a Preference for Fee Type?
Enter 0 for No Preference, 1 for Free Only, or 2 for Paid Only. Default 0 :
```

8. Program will now start to monitor the slots in these Districts every 15 seconds.
```
===================================================================================  
Centres are available in Ahmedabad Corporation from 24-05-2021 as of 2021-05-23 09:29:10: 0
No Options Available right now. Next Update in 15 seconds..
```

9. If at any stage your Token becomes invalid, then the Program will make a Beep and Prompt for ```y``` or ```n```. If you would like to continue, provide ```y``` and proceed to allow using same Mobile Number
```
Token is INVALID! 
Do you want to try for a new Token? (y/n Default y): y
Enter the Registered Mobile Number: ███████████
Enter OTP: ███████████
```  

11. When a Center with more than minimum number of Slots is available, the Program will make a Beep sound - having different frequency for different districts. It will then display the available options as shown in the [Screenshot](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss7.png).
	

12. Before the Next Update, you'll have 10 seconds to provide a choice in the given format ```centerIndex.slotIndex``` eg: The input```1.4``` will select the First Vaccination Center and its Fourth Slot.

## Working Screenshots:

1. Generating OTP and Token...

![SS1](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss1.png)

2.  Fetching Registered Beneficiaries...

![SS2](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss2.png)

3.  Selecting Beneficiaries...

![SS3](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss3.png)

4.  Additional Information to be entered for Slot Booking...

![SS4](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss4.png)

5.  Auto-Booking Function...

![SS5](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss5.png)

6.  Save Information as JSON File...

![SS6](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss6.png)

7.  Displaying Available Vaccination Centers and Booking Slots (Auto-Booking ON)...

![SS7](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss7.png)

8.  Successfully Booking a Slot **(If and only if you enter the Captcha correctly and in the mean time, all the slots are not booked)**

![SS8](https://github.com/dhhruv/Vac-Cowin/blob/master/assets/ss8.png)

<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


### Team Members:

1.  [Dhruv Panchal](https://github.com/dhhruv)
2.  [Urveshkumar Patel](https://github.com/urvesh254)
3.  [Nirja Desai](https://github.com/nirami98)

### Important:

- This is a Proof of Concept Project. **I OR the Team** do NOT endorse or condone, in any shape or form, automating any monitoring/booking tasks. **It's only made for Educational Purposes. Use this at your own risk.**
- This **Python Script CANNOT book slots automatically**. It doesn't skip any of the steps that a User would have to take on the official portal. You will still have to enter the OTP and Captcha as you do in the CoWIN Portal.
- **Do NOT** use unless all the beneficiaries selected are supposed to get the same Vaccine and Dose.
- There is **no option** to Register a new Phone/Mobile or add beneficiaries for now. This can be used only after beneficiary has been added through the official Portal/App.
- Be careful if you're choosing to use the auto-book feature. It will blindly select first available Vaccination **Centre, Date (Both Sorted Ascending) and a RANDOM slot**. I would not recommend using this feature unless and until it's crucial.
- If you accidentally booked a slot you didn't want to then don’t worry. You can always log in to the CoWIN Portal and cancel/re-schedule that.
- This goes without saying but, once you get your shot, please do help out any people around you who may not have a laptop or the know-how. For instance any sort of domestic help or literally the thousands of people who don't have the knowledge or luxury as we do.
- **API Details (Do read the first paragraph): https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2**

<p align='center'><b>Made with ❤ by Dhruv Panchal</b></p>
