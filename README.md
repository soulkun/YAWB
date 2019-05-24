# YAWB - Yet Another WebReg Bot

## Helps you enroll in FULL courses

## Introduction

YAWB helps you enroll in FULL courses by attempting adding courses in a
regular basis.
Everything from logging in to logging out is o-matic so that it can be deployed 
to a remote server without interrupting your work.
YAWB is based on Selenium, a program that controlls your brouser just like a phantom.
To prevent being blocked by WebReg, YAWB executes every 25-35 seconds.

Currently WAWB does not support waitlists.

## Prerequisite

* Chrome or Chromium browser

## Deployment 

* Install Selenium

```bash
pip3 install selenium
```

* Download WebDriver and make it executable

https://sites.google.com/a/chromium.org/chromedriver/downloads

```bash
chmod +x ./webdriver
```

For macOS users: you may have to copy the webdriver to somewhere like /usr/local/bin/

* Clone from this repo

```bash
git clone https://github.com/maao666/YAWB.git

```

* Provide your UCInetID and password

```bash
export NET_ID="[Replace with your UCInetID]"
export ID_PASSWORD="[Replace with your Password]"
```

* Change the default course number

You may add course either by individual course codes or a range of course codes.

You may wanna modify add_courses.py

An interactive solution will be provided in the next release.
