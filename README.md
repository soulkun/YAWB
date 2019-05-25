# YAWB - Yet Another WebReg Bot

## Helps you enroll in FULL courses

![banner](assets/repository_banner.jpg "Repository Banner Image")

## Introduction

YAWB helps you enroll in FULL courses by attempting adding courses in a
regular basis.
Everything from logging in to logging out is o-matic so that it can be deployed
to a remote server without interrupting your work.
YAWB is based on Selenium, a program that controlls your brouser just like a phantom.
To prevent being blocked by WebReg, YAWB executes every 25-35 seconds.

YAWB simulates what a real person does so you'll never get banned.

Currently YAWB does not support waitlists.

## Prerequisite

* Chrome or Chromium browser

## Deployment

* Install Selenium

```bash
pip3 install selenium
```

* Download WebDriver and make it executable

<https://sites.google.com/a/chromium.org/chromedriver/downloads>

```bash
chmod +x ./webdriver
```

* Make YAWB yours

```bash
git clone https://github.com/maao666/YAWB.git
```

* Provide your UCInetID and password

```bash
export NET_ID="[Replace with your UCInetID]"
export ID_PASSWORD="[Replace with your Password]"
```

* Add some juice

You may add your own courses to ```courses to add.txt```

```courses to add.txt``` will be fetched prior to each session, so
 it can be modified during runtime.

* Fire it up

```bash
cd ./YAWB
python3 ./add_courses.py
```

* We humbly ask you for a star if this bot does help you.
