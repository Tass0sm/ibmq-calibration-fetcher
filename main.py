#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime

from ibmq_calibration_fetcher.fetcher import fetch_and_save_system_calibration_data

def main():
    driver = webdriver.Chrome()
    now = datetime.now().isoformat()

    for system in ["ibm_washington", "ibm_sherbrooke", "ibm_kyiv"]:
        fetch_and_save_system_calibration_data(driver, system, now)

    driver.quit()

if __name__ == "__main__":
    main()
