from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
import os
import logging
import traceback

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

NET_ID = os.environ.get("NET_ID")
ID_PASSWORD = os.environ.get("ID_PASSWORD")
IS_RAMDOMLY_PAUSE = True


class CourseList:
    course_code_list = []
    raw_file = []

    def __init__(self):
        pass

    def __parse_raw_file__(self):
        for line_iterator in self.raw_file:
            alter_courses = []
            line_iterator = line_iterator + '\n'
            line_iterator = line_iterator[0: line_iterator.find('#')]
            line_iterator = line_iterator.strip()
            if line_iterator == '':
                continue
            for course_iterator in line_iterator.split():
                course_iterator = course_iterator.strip()
                if course_iterator == '':
                    continue
                alter_courses.append(course_iterator)

            self.course_code_list.append(alter_courses)

        logging.debug(self.course_code_list)

    def load_from_file(self, filename):
        with open(filename, encoding='utf-8') as f:
            self.raw_file = f.readlines()

        logging.debug(self.raw_file)
        self.__parse_raw_file__()

    def get_course_code_list(self):
        return self.course_code_list

    def add_individual_course(self, coursecode):
        for individual_course in self.course_code_list:
            if individual_course[0] == coursecode:
                return False
        self.course_code_list.append([str(coursecode)])
        return True

    def purge_list_with_course(self, coursecode):
        for courselist in self.course_code_list:
            thatsit = False
            for individual_course in courselist:
                if individual_course == str(coursecode):
                    thatsit = True
                    break
            if thatsit == True:
                self.course_code_list.remove(individual_course)


def input_by_letters(webelement_inputbox, content):
    webelement_inputbox.send_keys(content)
    pause_randomly()
    '''
    for individual_char in content:
        webelement_inputbox.send_keys(individual_char)
        if __debug__:
            pass
            #sleep(randint(1,5) * 0.01)
    '''


def pause_randomly():
    if IS_RAMDOMLY_PAUSE:
        sleep(randint(1, 8) * 0.1)


def log_in_with_credential(driver, netID, password):
    ucinetid_textbox = driver.find_element_by_id('ucinetid')
    input_by_letters(ucinetid_textbox, netID)

    pause_randomly()

    passwd_textbox = driver.find_element_by_id('password')
    input_by_letters(passwd_textbox, password)

    pause_randomly()

    login_button = driver.find_element_by_xpath(
        '//*[@id="login_button_span"]/input')
    login_button.click()

    # Raise an Exception if login failed
    driver.find_element_by_xpath(
        '/html/body/center[1]/table/tbody/tr/td/form[1]/input[4]')


def get_study_list(driver):
    show_study_list_button = driver.find_element_by_xpath(
        '/html/body/center[1]/table/tbody/tr/td/form[5]/input[4]')
    show_study_list_button.click()

    study_list = driver.find_element_by_xpath(
        '/html/body/center[2]/table/tbody/tr[2]/td')
    return study_list.text


def print_study_list_from_main_menu(driver):
    print(get_study_list(driver))


def search_course_in_study_list(driver, coursecode):
    pass


def enter_enrollment_window(driver):
    enrollment_button = driver.find_element_by_xpath(
        '/html/body/center[1]/table/tbody/tr/td/form[1]/input[4]')
    enrollment_button.click()


def add_course_by_range(driver, lower_range_int, upper_range_int):
    pause_randomly()
    for individual_course in range(lower_range_int, upper_range_int + 1, 1):
        add_course_by_code(driver, str(individual_course))


def add_course_by_code(driver, course_code):
    add_button = driver.find_element_by_xpath('//*[@id="add"]')
    add_button.click()

    course_code_textbox = driver.find_element_by_xpath(
        '/html/body/center[1]/form[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input')
    input_by_letters(course_code_textbox, str(course_code))

    logging.info("Attempting to add course " + str(course_code))

    send_request_button = driver.find_element_by_xpath(
        '/html/body/center[1]/form[2]/table/tbody/tr[1]/td/input[3]')
    send_request_button.click()


def safely_log_out(driver):
    try:
        logout_button = driver.find_element_by_xpath(
            '/html/body/center[1]/form/input[4]')
        logout_button.click()
    except:
        logging.info("No action performed to log out")


def add_course_from_list(driver, courselist):
    # TODO: don't waste time adding duplicated courses
    for courseiter in courselist:
        add_course_by_code(driver, courseiter)


def perform_add_batch_courses(driver, course_list):
    for alter_course_iter in course_list.get_course_code_list():
        add_course_from_list(driver, alter_course_iter)


def perform_session_operations(driver, course_list):
    pause_randomly()

    print_study_list_from_main_menu(driver)

    pause_randomly()

    enter_enrollment_window(driver)

    pause_randomly()

    #pylint: disable=unused-variable
    for i in range(2):
        perform_add_batch_courses(driver, course_list)
        pause_randomly()


def new_session(course_list):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--disable-extensions")
    #chrome_options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.reg.uci.edu/cgi-bin/webreg-redirect.sh')

    pause_randomly()
    try:
        log_in_with_credential(driver, NET_ID, ID_PASSWORD)
    except NoSuchElementException:
        logging.warning("Warning: Having trouble logging in.")
        driver.close()
        return False

    try:
        perform_session_operations(driver, course_list)
    except:  # (NoSuchElementException, KeyboardInterrupt):
        print(traceback.format_exc())
        logging.info("Safely logging out...")
        safely_log_out(driver)
        driver.close()
        logging.info("Driver closed")

    # Logging out WebReg
    safely_log_out(driver)

    pause_randomly()
    try:
        driver.close()
    except:
        pass


def main():
    course_list_1 = CourseList()
    course_list_1.load_from_file("courses to add.txt")
    if not (type(NET_ID) is str and type(ID_PASSWORD) is str):
        logging.error('ID or password cannot be empty')
        exit()

    while True:
        logging.info("Starting new session...")
        try:
            new_session(course_list_1)
        except Exception:
            logging.exception("Something awful happened!")

        time_to_sleep = randint(20, 35)
        if __debug__:
            logging.info("Halting for {0} seconds...".format(
                str(time_to_sleep)))
        sleep(time_to_sleep)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Exiting...")
