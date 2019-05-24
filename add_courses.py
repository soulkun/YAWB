from selenium import webdriver
from time import sleep
from random import randint
import os

NET_ID = os.environ.get("NET_ID")
ID_PASSWORD = os.environ.get("ID_PASSWORD")

def input_by_letters(webelement_inputbox, content):
    for individual_char in content:
        webelement_inputbox.send_keys(individual_char)
        if __debug__:
            sleep(randint(1,10) * 0.01)

def log_in_with_credential(driver, netID, password):
    ucinetid_textbox = driver.find_element_by_id('ucinetid')
    input_by_letters(ucinetid_textbox, netID)

    if __debug__:
        sleep(0.5)

    passwd_textbox = driver.find_element_by_id('password')
    input_by_letters(passwd_textbox, password)

    if __debug__:
        sleep(0.5)

    login_button = driver.find_element_by_xpath('//*[@id="login_button_span"]/input')
    login_button.click()

def print_study_list(driver):
    show_study_list_button = driver.find_element_by_xpath('/html/body/center[1]/table/tbody/tr/td/form[5]/input[4]')
    show_study_list_button.click()

    study_list = driver.find_element_by_xpath('/html/body/center[2]/table/tbody/tr[2]/td')
    print(study_list.text)

def enter_enrollment_window(driver):
    enrollment_button = driver.find_element_by_xpath('/html/body/center[1]/table/tbody/tr/td/form[1]/input[4]')
    enrollment_button.click()

def add_course_by_range(driver, lower_range_int, upper_range_int):
    if __debug__:
        sleep(0.5)
    for individual_course in range(lower_range_int,upper_range_int + 1, 1):
        add_course_by_code(driver, str(individual_course))

def add_course_by_code(driver, course_code_str):
    add_button = driver.find_element_by_xpath('//*[@id="add"]')
    add_button.click()

    course_code_textbox = driver.find_element_by_xpath('/html/body/center[1]/form[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input')
    input_by_letters(course_code_textbox, course_code_str)

    send_request_button = driver.find_element_by_xpath('/html/body/center[1]/form[2]/table/tbody/tr[1]/td/input[3]')
    send_request_button.click()

def safely_log_out(driver):
    logout_button = driver.find_element_by_xpath('/html/body/center[1]/form/input[4]')
    logout_button.click()

def new_session():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    #options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh')

    if __debug__:
        sleep(0.5)

    log_in_with_credential(driver, NET_ID, ID_PASSWORD)

    if __debug__:
        sleep(0.5)

    print_study_list(driver)

    if __debug__:
        sleep(0.5)

    enter_enrollment_window(driver)

    if __debug__:
        sleep(0.5)

    add_course_by_range(driver, 16525, 16530)
    add_course_by_range(driver, 16525, 16530)
    add_course_by_range(driver, 16525, 16530)

    if __debug__:
        sleep(1)

    # Logging out WebReg
    safely_log_out(driver)

    if __debug__:
        sleep(1)

    driver.close()

def main():
    while True:
        new_session()
        if __debug__:
            print("Halting for a couple of seconds")
        sleep(randint(20,35))

if __name__ == '__main__':
    main()