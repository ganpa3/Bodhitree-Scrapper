#!/usr/bin/env python

import platform
import subprocess
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Enter login credentials
email = ""
password = ""

chrome_options = Options()
if "-h" in sys.argv:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")
    print("NOTE: Running headless state")

# Driver executable path
if platform.system() == "Windows":
    driver_path = "assets\\chromedriver_windows.exe"
else:
    driver_path = "./assets/chromedriver_linux"

try:
    browser = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
except:
    raise Exception("ERROR: Place the appropriate web driver in the assets folder")


def login():
    browser.get("https://pccoe.bodhi-tree.in/accounts/login/")
    browser.find_element_by_id("signinUsername").clear()
    browser.find_element_by_id("signinUsername").send_keys(email + Keys.RETURN)
    browser.find_element_by_id("signinPassword").clear()
    browser.find_element_by_id("signinPassword").send_keys(password + Keys.RETURN)


def main():
    login()

    videos = []

    for i in range(1, len(sys.argv)):
        url = sys.argv[i]
        if url == "-h":
            continue
        print(url)

        if "#item" in url:
            new_url = "/".join(url.split("/")[:-1])
            print(new_url)
            browser.get(new_url)
            WebDriverWait(browser, timeout=10).until(
                lambda b: b.find_elements_by_css_selector(".concept-playlist li")
            )[int(url[-1])].click()
        else:
            browser.get(url)

        video_url = (
            WebDriverWait(browser, timeout=10)
            .until(lambda b: b.find_element_by_css_selector("video"))
            .get_attribute("src")
        )
        name = video_url.split("/").pop()
        videos.append([name, video_url])
        time.sleep(1)

    browser.quit()
    print(videos)

    for i in range(len(videos)):
        subprocess.run(["curl", "-o", videos[i][0], videos[i][1]])


if __name__ == "__main__":
    main()
