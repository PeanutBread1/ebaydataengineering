import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import boto3
import os

def run():
    #lets us start a new google chrome session and driver becomes our main point of interaction with browseer where we can write commands
    driverStart = webdriver.Chrome() 
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
    element2 = driverStart.find_element(By.ID, "gh-as-a")
    element2.click()
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
        item_square_individual = driverStart.find_element(By.CLASS_NAME,'srp-results')
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
            remove_sold = date_id_date_only.text.strip("Sold").strip()
            dateObject = datetime.strptime(remove_sold, '%b %d, %Y')
            reformattedDateObject = dateObject.strftime("%m/%d/%Y")
            date_data_list.append(reformattedDateObject)

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
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f"listings_{current_date}.csv" 

    # Upload the file

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    sortedDf = df.sort_values(by='date')
    csv_filename = 'listings.csv'
    sortedDf.to_csv(csv_filename, index=False)

    s3_client = boto3.resource('s3')
    bucket = s3_client.Bucket('ebay-bucket-1234')
    bucket.upload_file(Key = file_name, Filename = "./listings.csv")
    #using access key in dummy-user access keys filecsv
    print(df)

    print("hello")

    input("Press Enter to close...")  # This will pause the script until you press Enter
if __name__ == '__main__':
    run()
def lambda_handler(event, context):
    # Your script logic goes here
    print("Lambda function triggered.")
    
    # For demonstration purposes, let's print the current date and time
    print("Current date and time:", datetime.now())
    run()
    # You can include your existing script logic here
    
    # For example, if you have the code to upload CSV files to S3, you can call that code here
    
    # Remember to replace this placeholder logic with your actual script logic
    
    # Return a response (optional)
    return {
        "statusCode": 200,
        "body": "Lambda function executed successfully."
    }
