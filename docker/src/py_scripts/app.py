# include required libraries
import time

#specify the start timer for the entire test suite
test_suite_start_timer = time.time()


import os
import random
import string
from datetime import datetime, timedelta 

# include selenium libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# import custom .py include files:
from lib import custom_functions     # defines custom functions used to 
from lib import app_config           # defines runtime application configuration values
from lib import login_credentials    # defines web login credentials
from lib import project_scenario_config

    
    
# set the variable to also print all log messages or not:
print_log_messages = True

# create the .csv file to capture the web performance metrics

# check if the .csv file exists
if os.path.isfile('/app/data/'+app_config.csv_output_file):
    # the .csv file exists

    # open the .csv file in append mode
    fp = open("/app/data/"+app_config.csv_output_file, "a")
else:
    # the .csv file does not exist

    # create the .csv file in write mode:
    fp = open("/app/data/"+app_config.csv_output_file, "x")

    # create the .csv header row
    fp.write('"App Name","Metrics App Location","Test App Location","Date/Time","Page Name","Action","# Files","Total File Size (KB)","Total Response Time (s)","Screenshot File"'+"\n")


# set the selenium options:
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")
# options.add_argument('--enable-javascript')
options.add_argument('ignore-certificate-errors')
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

prefs = {"download.default_directory" : "/app/data"};

options.add_experimental_option("prefs",prefs);

# create the chrome webdriver object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# enable the network cache
driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":False})

# custom_functions.log_value("load the page", print_log_messages)

# start the timer
start_timer=round(time.time()*1000)


"""
START - 1. Request the base_web_url defined in the application configuration
"""

# check the value of the app_location
if (project_scenario_config.app_location == "remote"):
    # this a remote application, use the remote_web_url

    custom_functions.log_value("This is a remote application: "+app_config.remote_web_url, print_log_messages)
    
    # load the URL in the web browser
    driver.get(app_config.remote_web_url) 
else:
    # this a local application, use the local_web_url

    custom_functions.log_value("This is a local application: "+app_config.local_web_url, print_log_messages)
    
    # load the URL in the web browser
    driver.get(app_config.local_web_url) 
    


"""
Custom code for defining web actions and wait conditions goes here including start/stop timers and .csv file content
"""
custom_functions.log_value("All of the web actions in the test suite have completed", print_log_messages)

# calculate the elapsed time in minutes based on the test_suite_start_timer variable and the current time
total_time_min=round(((time.time()-test_suite_start_timer)/60), 2)

# log the elapsed time for the entire test suite
custom_functions.log_value('total elapsed time (min): '+str(total_time_min), print_log_messages)

# selenium driver session cleanup:

# close the selenium driver
driver.close()

# quit the selenium driver
driver.quit()


