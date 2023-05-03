from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

import pygraphviz as pgv
import re
import numpy as np
import pandas as pd

from ibmq_calibration_fetcher.utils import *

def fetch_and_save_system_calibration_data(driver, system, today):
    driver.get(f"https://quantum-computing.ibm.com/services/resources?tab=systems&view=grid&system={system}")
    driver.implicitly_wait(30)
    tab_list = driver.find_element(by=By.CSS_SELECTOR, value=".duo--ContentSwitcher")
    tabs = tab_list.find_elements(By.TAG_NAME, 'button')

    # click the third tab to get the table
    tabs[2].click()

    # table
    table = driver.find_element(by=By.CSS_SELECTOR, value=".iqx-table")

    # header
    header = table.find_element(By.TAG_NAME, 'thead')
    header_labels = header.text.split("\n")
    width = len(header_labels)

    # table body
    body = table.find_element(By.TAG_NAME, 'tbody')
    table_dom = BeautifulSoup(body.get_attribute("innerHTML"), features="html.parser")
    rows = table_dom.find_all('tr')
    df_rows = list(map(make_df_row, rows))
    df_values = np.array(df_rows)
    df = pd.DataFrame(df_values)
    df.columns = header_labels
    df = df.set_index("Qubit")

    def is_floaty(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    df = df.replace("", "0.0")
    column_mask = df.applymap(is_floaty).all(0).values

    simple_values_df = df.loc[:, column_mask].astype("float64")
    simple_values_df.to_csv(f"./{today}-{system}-values.csv")

    # write remaining columns as graphs
    edge_maps_df = df.loc[:, ~column_mask]
    for name in edge_maps_df:
        column = edge_maps_df.loc[:, name]
        graph = edge_text_column_to_graphviz_graph(column)
        with open(f"./{today}-{system}-{name}.dot", "w") as f:
            f.write(str(graph))

    # Summarize:
    print(f"Finished {system}")
    print("MEANS:")
    print(simple_values_df.mean(axis=0))
    print("STD DEVS:")
    print(simple_values_df.std(axis=0))
