import streamlit as st
from html_collection import html_collection, prices_collection
from params import params
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm


def launch_html_collection(websites, marques, input_df):

    """
    Function that loops over each website and brands and collect the html content at each iteration using Selenium for Google Chrome

    Parameters
    ----------
    websites : list of the website names
    marques : list of the brands
    input_df : dataframe from parameters

    Returns
    -------
    A dataframe with the name of the website, name of the brand and the html content
    
    """


    # s = Service('chromedriver.exe')

    @st.experimental_singleton
    def get_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

    chromeOptions = Options()

    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument("--blink-settings=imagesEnabled=false")

    chromeOptions.add_argument('--ignore-certificate-errors-spki-list')

    # Adding argument to disable the AutomationControlled flag 
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    chromeOptions.add_experimental_option("useAutomationExtension", False) 

    driver = get_driver()

    driver.implicitly_wait(10)

    soup_df = pd.DataFrame()

    for website in tqdm(websites):
        print("\n", f"---------------------- Extracting data from {website.upper()} -------------------------", "\n")
        for marque in marques :
            soup_df = html_collection(website, marque, input_df, soup_df, driver)
            print("\n", f"------{marque} information collected", "\n")

    print("\n", "Data collection complete.")

    return soup_df


#Choice of websites
websites = ["manutan"] #"manutan","bruneau","jpg","raja","bernard"

marques = ["TORK","JEX"]

input_df = params()

result = st.button('Launch collection')

if result:

    #Launching html content collection for each website and brand
    soup_df = launch_html_collection(websites,marques,input_df)

    #Extracting products names, references and prices
    collect_df = prices_collection(soup_df, input_df)

    st.dataframe(collect_df)

# st.markdown("""# This is a header
# ## This is a sub header
# This is text""")

# df = pd.DataFrame({
#     'first column': list(range(1, 11)),
#     'second column': np.arange(10, 101, 10)
# })

# # this slider allows the user to select a number of lines
# # to display in the dataframe
# # the selected value is returned by st.slider
# line_count = st.slider('Select a line count', 1, 10, 3)

# # and used to select the displayed lines
# head_df = df.head(line_count)

# head_df