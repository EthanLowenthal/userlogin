#Log Me In

Log Me In is a program to log users in and out. Log Me In supports email recovery, user settings, and even allows the users to log out!


##Installation
```
git clone https://github.com/kehillah-coding-2017/user-management-EthanLowenthal.git
```


##Running
Make shure your working directory is the one with all the files, not the one with the folder

The first time running, you need to create a file called 'users.db'

Run this:

```
export FLASK_APP=flaskr.py
export FLASK_DEBUG=1
flask run
```

It should run on http://127.0.0.1:5000/


The defualt username is admin, and the default password is default. This account cannot be changed or deleted. Any changes made to this account will be saved to a new account.
# userloginheroku
