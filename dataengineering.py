import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime


#lets us start a new google chrome session and driver becomes our main point of interaction with browseer where we can write commands
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # This will start Chrome maximized

driverStart = webdriver.Chrome(options=chrome_options) 
#does not return anything, simply opens site. DRIVERSTART IS HOW WE ACCESS THE PAGE AND INTERACT WITH IT
driverStart.get("https://www.ebay.com/") 
#waits 20 milliseconds for loading
wait = WebDriverWait(driverStart, 20)

#we use the driver to interact with html.
#allows us to send keys and click buttons as if we are a user ourselves
#finds the search box 
element = driverStart.find_element(By.NAME, "_nkw") 
#dont need to click we can straightaway send what we want to search

element.send_keys("bad batch attack shuttle")
element.submit()

#inputs searchbar and searches
element2 = driverStart.find_element(By.ID, "gh-as-a")

element2.click()
#clicks advanced settings


element3 = driverStart.find_element(By.ID, "s0-1-17-5[1]-[2]-LH_Sold").click()
element = driverStart.find_element(By.CLASS_NAME, "btn--primary").click()

#create a data dictionary to hold list of items
data = {

}
#create list of items to hold data. will represent columns
item_id_data_list = []
price_data_list = []
date_data_list = []
condition_data_list = []
z = 0
d = 0
while(True):
    item_square_individual = driverStart.find_element(By.CSS_SELECTOR,'.srp-results.clearfix')
    item_id = item_square_individual.find_elements(By.CSS_SELECTOR,'li[id]')
    item_price = driverStart.find_elements(By.CLASS_NAME, 's-item__price')
    start = 0
    price_detail_elements = driverStart.find_elements(By.CSS_SELECTOR, '.s-item__detail.s-item__detail--primary .s-item__price')
    for i in price_detail_elements:
        if not i.text == "":
            noDollarSign = i.text.replace("$","").replace(",","").strip()
            if noDollarSign.find('to') > -1:
                split = noDollarSign.split('to')
                sum = float(split[0]) + float(split[1])
                avg = sum/2
                price_data_list.append(avg)
            else:
                floatver = float(noDollarSign)
                price_data_list.append(floatver)

    #gets the individual item square so we can strip it of its date, price, etc 
    
    #only checks item squares with the id attribute 
    
    price_id_list = driverStart.find_elements(By.CLASS_NAME, 's-item__details')

    #price_elements = driverStart.find_elements(By.CLASS_NAME, 's-item_price')
    #print(price_elements)

    #for date
    date_id_list = driverStart.find_elements(By.CLASS_NAME, 's-item__title--tag')
    for i in date_id_list:
        date_id_date_only = i.find_element(By.CLASS_NAME, "POSITIVE")
        remove_sold = date_id_date_only.text.strip("Sold")
        date_data_list.append(remove_sold)

    #condition
    list_items_test = driverStart.find_element(By.ID, 'srp-river-results')
    condition = list_items_test.find_elements(By.CLASS_NAME, 'SECONDARY_INFO')
    for conditions in condition:
        condition_data_list.append(conditions.text)
   
    #itemId
    for items in item_id:
        item_id_value = items.get_attribute('id')
        if item_id_value:
            item_id_data_list.append(item_id_value)
        else:
            print("No ID attribute found")  

# Assuming price_id is a list of WebElements

    
        # Find the "Next" button. Adjust the selector as needed for the specific site.
    next_button = driverStart.find_element(By.CSS_SELECTOR, "button.pagination__next, a.pagination__next")

        # Check if the "Next" button is disabled. This may need to be adjusted depending on the site's HTML.
    if next_button.get_attribute("aria-disabled") == "true":
            print("Reached the last page.")
            break

        # Click the "Next" button to go to the next page.
    else: 
        next_button.click()

data = {
    "id": item_id_data_list,
    "price": price_data_list,
    "date": date_data_list,
    "condition": condition_data_list
}
df = pd.DataFrame(data)
df.to_csv('with_index.csv', index=True)

print(df)

print("hello")

input("Press Enter to close...")  # This will pause the script until you press Enter