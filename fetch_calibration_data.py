#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from datetime import datetime

from ibmq_calibration_fetcher.fetcher import fetch_and_save_system_calibration_data

def main():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    now = datetime.now().isoformat()

    for system in ["ibm_washington", "ibm_sherbrooke", "ibm_kyiv"]:
        fetch_and_save_system_calibration_data(driver, system, now)

    driver.quit()

if __name__ == "__main__":
    main()
