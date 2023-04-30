from html_collection import html_collection, prices_collection
from params import params
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import sys
from utils import clean_path
from datetime import date
import os

def launch_html_collection(websites, marques, input_df):

    s = Service('chromedriver.exe')
    chromeOptions = Options()

    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--blink-settings=imagesEnabled=false")

    chromeOptions.add_argument('--ignore-certificate-errors-spki-list')

    # Adding argument to disable the AutomationControlled flag 
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    chromeOptions.add_experimental_option("useAutomationExtension", False) 

    driver = webdriver.Chrome(service=s, options=chromeOptions)
    driver.implicitly_wait(10)

    soup_df = pd.DataFrame()

    for website in websites:
        print("\n", f"---------------------- Extracting data from {website.upper()} -------------------------", "\n")
        for marque in marques :
            soup_df = html_collection(website, marque, input_df, soup_df, driver)
            print("\n", f"------{marque} information collected", "\n")

    print("\n", "Data collection complete.")

    return soup_df


def save_data(data, path):
    """
    Save the soup_df
    """
    path = clean_path(path)

    data.to_excel(path,index=False)

    print("\n", "Extraction saved in the selected folder.")


if __name__ =="__main__":

    #Choice of websites
    websites = ["manutan","bruneau","jpg","raja","bernard"]

    #Choice of brands
    marques = ["TORK","JEX","ST MARC","HARPIC","AJAX","ROSSIGNOL","ANSELL","BLAKLADER"]

    #Importing params
    input_df = params()

    #Launching html content collection for each website and brand
    soup_df = launch_html_collection(websites,marques,input_df)

    #Extracting products names, references and prices
    collect_df = prices_collection(soup_df, input_df)

    #Adding the date of the extraction
    today = date.today().strftime("%Y-%m-%d")
    collect_df.insert(0, 'Extraction_Date', today)

    #Saving data to the repository chosen by the user
    file_path = str(sys.argv[1])
    file_name = f"{today}_Extract.xlsx"
    path = os.path.join(file_path,file_name) #Concatenating the path of the folder and the name of the file
    save_data(collect_df, path)

