#Log Me In
[![Build Status](https://travis-ci.org/EthanLowenthal/userlogin.svg?branch=master)](https://travis-ci.org/EthanLowenthal/userlogin)
##Running On: http://ethansloginapp.herokuapp.com/login

Log Me In is a program to log users in and out. Log Me In supports email recovery, user settings.


##Installation
```sh
git clone https://github.com/EthanLowenthal/userlogin.git
```

###Dependencies
```sh
pip install -r reqirements.txt
```
*That is the right code, but it only works when I manually type it in*


##Running
Make shure your working directory is the one with all the files, not the one with the folder

The first time running, you need to create a file called 'users.db'

###Normal
```python
python run.py
```

###Debug Mode
```sh
export FLASK_APP=flaskr.py
export FLASK_DEBUG=1
flask run
```

It should run on http://127.0.0.1:5000/ or http://0.0.0.0:5000/


The defualt username is admin, and the default password is default. This account cannot be changed or deleted. Any changes made to this account will be saved to a new account.

