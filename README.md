# p1mon-django
p1monitor with python-django backend

A p1 monitor project to read Dutch smart meters (electricity and gas) through the P1 USB connection.

This project was forked from the p1mon project at https://www.ztatz.nl/ .
The project design was appreciated and therefore retained.
The front-end was borrowed with minor edits.
The PHP back-end was replaced with a python django backend.
Calculations were replaced with data table operations using pandas.

# Installation guidelines 
(e.g. raspberry pi)

1. Set up the django test webserver (terminal1):
- set up a python3 environment
- install the python3 virtual environment (pip install requirements.txt )
- migrate the data bases (python migrate.py)
- create a super user (python manage.py createsuperuser)
- run webserver (python manage.py runserver 0.0.0.0:8000)

2. Read data from your smart meter (terminal2):
- connect the usb to p1 cable to your smart meter
- read the p1 connection and store in SQL database (python p1mon_serReader_dork_min.py)

3. Convert the serial data to historical data using the python conversion scripts, scheduled in crontab.

4. Visit your testserver at <ip_address>:8000 or localhost:8000 (web browser). 

5. Deploy the webserver properly (e.g. nginx + uwsgi)

# Development
Enjoy!
And let me know if you have issues or implemented some upgrades.
