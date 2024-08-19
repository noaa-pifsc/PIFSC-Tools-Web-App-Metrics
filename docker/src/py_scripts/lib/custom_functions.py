# include required libraries
import time
import json
import pprint

# include selenium libraries
from datetime import datetime 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# import custom .py files for this project
from lib import app_config
from lib import project_scenario_config

# function to return the current formatted date in YYYYMMDD format
def get_formatted_date ():
    return datetime.today().strftime("%Y%m%d")

# function to return the current formatted date/time in YYYYMMDD HH:MM:SS AM/PM format
def get_formatted_datetime ():
    return datetime.today().strftime("%Y%m%d %I:%M:%S %p")

# function to log the formatted object in the log file, if print_log is True then also print the formatted object value to the stdout
def log_object (object, print_log):
    
    # open the designated log file for the current date
    with open("/app/logs/"+app_config.log_file_prefix+get_formatted_date()+".log", "a") as log_file:
        # add the formatted object to the designated log file
        pprint.pprint(object, log_file)
        
        # check if the object should also be printed to the stdout
        if (print_log):
            # print the formatted object to the stdout
            pprint.pprint(object)
    
# function to log the current entry in the log file, if print_log is True then also print the entry value to the stdout
def log_value (entry, print_log):
    
    #log the output for development/testing purposes
    
    # open the designated log file for the current date
    log_file = open("/app/logs/"+app_config.log_file_prefix+get_formatted_date()+".log", "a")

    # write the value (entry) to the open log file
    log_file.write(get_formatted_datetime()+ " - " + entry+"\n")
    
    # check if the entry should also be printed to the stdout
    if (print_log):
        # print the entry to the stdout
        print(entry)

    # close the file pointer for the log file
    log_file.close()

# function to process the network logs for the chrome webtools based on the logs array object, if print_log is True then also print the logs array values to the stdout.  Return the total number of web resource files that were downloaded for a given web request/page load
def process_browser_network_logs (logs, print_log_messages):

    # initialize the total number of web resource files downloaded
    total_files = 0;
    
    # initialize the total size of the web resource files downloaded
    total_file_size = 0;
    
    # loop through all elements in the logs array
    for entry in logs:
        
        # parse the json object in the message:message object value
        log = json.loads(entry["message"])["message"]
        
        # check if this is a network response received message
        if "Network.responseReceived" == log["method"]:
            # this is a network response received message

            # log the current log object in the designated log file, but not in the stdout (to reduce clutter)
            log_object (log, False)

            # check if the current resource file is from the disk cache
            if (not log["params"]["response"]["fromDiskCache"]):
                # the file is not from disk cache, include it in the total number/size of files
                
                # determine if the content length value in the JSON object is uppercase (Content-Length)
                uppercase_content_length = ("Content-Length" in log["params"]["response"]["headers"])
                
                # determine if the content length value in the JSON object is lowercase (content-length)
                lowercase_content_length = ("content-length" in log["params"]["response"]["headers"])
                
                # check if the Content-Length element exists:
                if (uppercase_content_length or lowercase_content_length):
                    # add the Content-Length element value to the total file size
                    
                    # check if the JSON content-length element is lowercase
                    if (lowercase_content_length): 
                        # the content-length element is lowercase
                    
                        # log the content length value for the current URL resource
                        log_value ("content length: "+str(log["params"]["response"]["headers"]["content-length"])+" for url: "+log["params"]["response"]['url'], False)
                        
                        # add the content length value for the current URL resource to the total_file_size variable:
                        total_file_size += int (log["params"]["response"]["headers"]["content-length"])
                    else:
                        # the content-length element is uppercase

                        # log the content length value for the current URL resource
                        log_value ("content length: "+str(log["params"]["response"]["headers"]["Content-Length"])+" for url: "+log["params"]["response"]['url'], False)
                        
                        # add the content length value for the current URL resource to the total_file_size variable:
                        total_file_size += int (log["params"]["response"]["headers"]["Content-Length"])
                else:
                    # add the encoded data length element value to the total file size variable
                    total_file_size += int (log["params"]["response"]["encodedDataLength"])


                    # log the encoded data length value for the current URL resource
                    log_value ("encodedDataLength: "+str(log["params"]["response"]["encodedDataLength"])+" for url: "+log["params"]["response"]['url'], False)
                
                # increment the total number of resource files that were downloaded
                total_files += 1

#    log_value ("the value of total_files is: "+str(total_files), True)
#    log_value ("the value of total_file_size is: "+str(total_file_size), True)

    # return the total number of resource files downloaded and the total file size (in KB) for the given web request/page load
    return total_files, round(total_file_size/1024, 2)



# function to wait for a web request/page load to be ready and then captures the metrics for the elapsed time before the page is ready, and the total number/size of files using the process_browser_network_logs function.  The .csv file in the data volume is appended with information for the web request/page load.  A screenshot is saved in the data volume with the corresponding file name
# The functions behavior is based on the following arguments:
# stale_element (when applicable) is the WebElement that needs to be stale before the page processing continues
# clickable_element is the id of the element that needs to be clickable before the page processing continues
# by_method is the method used from the By class (e.g. By.XPATH, By.ID)
# start_timer is the timestamp before the action was initiated
# driver is the selenium driver used to get the logs, page name, etc.
# print_log_messages is a boolean to indicate if the log messages should also be printed to stdout
# fp is the file pointer to the .csv output file
# screenshot_suffix has the suffix for the screenshot file name (if any) to differentiate when the same page is filtered, reloaded, submitted, etc.
# web_action is a text string that describes the action that was taken in the given web request (e.g. page load, form submission)
def wait_for_response (stale_element, by_method, clickable_element_id, start_timer, driver, print_log_messages, fp, screenshot_suffix, web_action):

    log_value ("running wait_for_response ("+str(stale_element)+", "+str(by_method)+", "+clickable_element_id+", "+str(start_timer)+", driver, "+str(print_log_messages)+", fp, "+str(screenshot_suffix)+")", print_log_messages)

    try:
        
#        log_object(by_method, True)
        
        if stale_element is not None:
            elem = WebDriverWait(driver, 30).until(
            EC.staleness_of(stale_element) #This is a select element that is used to refresh the page
            )

            log_value("The stale element was found, wait for the clickable element", print_log_messages)
        
        log_value ("wait for the specified element to be clickable: "+clickable_element_id, print_log_messages)
        
        
        # wait until the login username field is clickable:
        elem = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((by_method, clickable_element_id)))      
    finally:
        

        
        log_value ("The try section has finished executing, execute the finally section", print_log_messages)
        
        # stop the timer
        end_timer=round(time.time()*1000)

        # calculate the elapsed time based on the start/end timer variables
        total_time_ms=end_timer-start_timer

        log_value("page title: "+driver.title+" was loaded", print_log_messages)

        # log the elapsed time for the page load
        log_value('total elapsed time (ms): '+str(total_time_ms), print_log_messages)

        # retrieve the total number of files and total file size from the network performance logs
        total_files, total_file_size = process_browser_network_logs(driver.get_log("performance"), print_log_messages)  

#        custom_functions.log_value ("The try portion of the initial page load is done executing", print_log_messages)

#         custom_functions.log_value (driver.current_url, print_log_messages)

        screenshot_file = driver.title.replace("/", " ")+("" if screenshot_suffix is None else " "+screenshot_suffix)+'.png'

        # save the screenshot from the web request/page load
        driver.save_screenshot('/app/data/screenshots/'+screenshot_file)

        fp.write('"'+app_config.app_name+'","'+project_scenario_config.container_location+'","'+project_scenario_config.app_location+'","'+time.strftime('%m/%d/%Y %I:%M:%S %p', time.localtime(start_timer/1000))+'","'+driver.title+'","'+web_action+'","'+str(total_files)+'","'+str(total_file_size)+'","'+str(round(total_time_ms / 1000, 3))+'","'+screenshot_file+'"'+"\n")

        return True

