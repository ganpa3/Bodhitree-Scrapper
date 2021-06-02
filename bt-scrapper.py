#!/usr/bin/env python3

import os
import platform
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Enter login credentials
email = ""
password = ""

if not email or not password:
    raise Exception("ERROR: Enter email and password **in** the bt-scrapper.py file.")

"""
Sometimes, the given expected score for Bodhitree quizzes is different from the actual expected score. This is because
(Bodhitree is shit) the number of attempts/scores fluctuate or the content gets boom!
So to balance those changes, a per subject fluctuation has to be maintained.
And this is what this balance dictionary is about!

The format is "Subject-Name" : [out video score fluctuation, in video score fluctuation]
For e.g., in the DM course of Div. A and B, the actual attainable out video score is 59,
whereas the given max out video score is 60. This fluctuation is noted here.
"""

balance = {
    "Discrete Mathematics SE Comp A & B": [2, 0],
    "Object Oriented Programming using C++ , Division B and D": [0, 2],
    "Fundamental of Data Structures": [0, 6],
    "Computer Graphics Lab (Div - B)": [9, 0],
    "Humanity and Social Science": [0, 0],
    "Digital Electronics Lab ( SE COMP B Division)": [0, 3],
    "Data Structure Laboratory_SE_B": [0, 1],
    "DELD Theory SE COMP Div B-Dr. Ranjanikar": [0, 0],
    "Computer Graphics": [0, 0],
    "Software Engineering-Div B-Dr. Ranjanikar": [0, 0],
    "SE COMP Microprocessor Lab(BatchA1&A2,B1,B2,B3,B4))": [0, 0],
    "COMP SEB Microprocessor": [0, 0],
    "Principles of Programming Language": [0, 0],
    "SE B Data Structure & Algorithm Laboratory": [0, 0],
}

chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("log-level=3")

if len(sys.argv) > 1:
    chrome_options.add_argument("--headless")
    print("NOTE: Running headless state")

# Driver executable path
if platform.system() == "Windows":
    DRIVER_PATH = os.path.join(ASSETS_DIR, "chromedriver_windows.exe")
else:
    DRIVER_PATH = os.path.join(ASSETS_DIR, "chromedriver_linux")

try:
    browser = webdriver.Chrome(
        options=chrome_options,
        executable_path=DRIVER_PATH,
    )
except:
    raise Exception(
        "ERROR: Web driver not found (place it in assets folder) or version doesn't match with installed browser."
    )

print(
    """
The process usually takes 1-2 minutes! (Don't interfere).
NOTE: Remembering the fluctuations in the number of quizzes is your responsibility.
Actual number of quizzes keep changing, so the output isn't 100% accurate all the time.
"""
)


def login():
    browser.get("https://pccoe.bodhi-tree.in/accounts/login/")

    # Entering Credentials
    browser.find_element_by_id("signinUsername").clear()
    browser.find_element_by_id("signinUsername").send_keys(email + Keys.RETURN)
    browser.find_element_by_id("signinPassword").clear()
    browser.find_element_by_id("signinPassword").send_keys(password + Keys.RETURN)


def main():
    login()

    # HACK. Bodhitree changed their landing page. Redirect to old landing page, since courses are fetched using that page.
    browser.get("https://pccoe.bodhi-tree.in/courseware/courseslist/")

    # Student's name
    name = (
        WebDriverWait(browser, timeout=20)
        .until(lambda b: b.find_element_by_css_selector(".dropdown-toggle"))
        .text
    )

    # List of all the courses enrolled
    courses = browser.find_elements_by_css_selector(".mycourseTitle a")

    # Opening all courses in new tabs
    for course in courses:
        course.send_keys(Keys.CONTROL + Keys.RETURN)

    # Maintaining list of visited tabs
    visited = [browser.current_window_handle]

    # To check whether all quizzes are completed
    check = False
    imbalanced = False

    for tab in browser.window_handles:
        if tab not in visited:
            browser.switch_to.window(tab)
            visited.append(tab)

            # Click on leaderboard of each subject
            WebDriverWait(browser, timeout=20).until(
                lambda b: b.find_element_by_css_selector("#sideList-score-card")
            ).click()

            try:
                scores = [
                    score.text.split("\n")
                    for score in WebDriverWait(browser, timeout=20).until(
                        lambda b: b.find_elements_by_css_selector(".panel-title")
                    )
                ]
            except:
                raise Exception("ERROR: Connection Error!")

            course_title = browser.find_element_by_css_selector(".courseTitle").text

            try:
                expected_out_video_score = (
                    int(
                        browser.find_element_by_xpath(
                            "//span[@data-reactid='.1.1.0.0.0.0.1.0.0.1']"
                        ).text
                    )
                    - balance[course_title][0]
                )
                expected_in_video_score = (
                    int(
                        browser.find_element_by_xpath(
                            "//span[@data-reactid='.1.1.0.0.0.0.1.0.1.1']"
                        ).text
                    )
                    - balance[course_title][1]
                )
            except:
                expected_out_video_score = int(
                    browser.find_element_by_xpath(
                        "//span[@data-reactid='.1.1.0.0.0.0.1.0.0.1']"
                    ).text
                )
                expected_in_video_score = int(
                    browser.find_element_by_xpath(
                        "//span[@data-reactid='.1.1.0.0.0.0.1.0.1.1']"
                    ).text
                )
                imbalanced = True

            for i in scores:
                if i[1] == name:
                    out_video_score = int(i[3])
                    in_video_score = int(i[5])
                    output = ""
                    title_printed = False

                    if expected_out_video_score > out_video_score:
                        output = (
                            "Course Name: "
                            + course_title
                            + "\nRemaining out video score: "
                            + str(expected_out_video_score - out_video_score)
                            + "\n"
                        )
                        check = title_printed = True

                    if expected_in_video_score > in_video_score:
                        if title_printed is False:
                            output = "Course Name: " + course_title + "\n"
                            check = title_printed = True
                        output += (
                            "Remaining in video score:"
                            + str(expected_in_video_score - in_video_score)
                            + "\n"
                        )

                    if output:
                        print(output)
                    break

    if imbalanced:
        print("If possible, add your course fluctuation value in the balance dictionary above")
    if not check:
        print("Well Done! All quizzes completed.\n")

    browser.quit()


if __name__ == "__main__":
    main()
