# auth: AJ Boyd (AJfromMD)
# date: 6/17/2024
# file: menu_scraper.py
# desc: script that scrapes UMBC's dining website and retrieves menu options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, datetime, sys

# url to dining webpage
URL = 'https://dineoncampus.com/UMBC/whats-on-the-menu' 

# set up selenium webdriver
def setup_driver():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless') 
    driver = webdriver.Firefox(options=firefox_options)
    return driver

# scrape menu items for all meals of day
def scrape_menu():
    # goto dining url
    driver = setup_driver()
    driver.get(URL)
   
   # wait for webpage to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "menu-location-selector__BV_toggle_"))
    )
    
    try:
        # click menu dropdown
        dropdown = driver.find_element(By.ID, "menu-location-selector__BV_toggle_")
        dropdown.click()
        time.sleep(1)

        # select TRUE GRIT'S
        select = driver.find_element(By.ID, "building_5df7bf13c4b7ff10c2be4f7a")
        select.click()
        time.sleep(1)

        # construct menu string
        menu = ""
        menu_head = "\n===BREAKFAST===\n"
        
        # navigate to different meal menus by clicking tabs
        for i in range(3):
            if i == 1:
                menu_head = "\n=====LUNCH=====\n"
                lunch_tab = driver.find_element(By.ID, "__BVID__233___BV_tab_button__")
                lunch_tab.click()
            elif i == 2:
                menu_head = "\n====DINNER=====\n"
                dinner_tab = driver.find_element(By.ID, "__BVID__238___BV_tab_button__")
                dinner_tab.click()
            menu += menu_head
            time.sleep(1)
            
            # scrape menu with beautiful soup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # extract the menu items' names and descriptions; add them to the menu string
            menu_items = soup.find_all("td")  
            for j in range(0, len(menu_items), 3):
                name = menu_items[j].find(class_= "menu-item")
                # clean text
                if name:
                    name = name.get_text().replace("Nutritional Info", "").strip()
                else:
                    name = ""
                description = menu_items[j].get_text().replace(name, "").replace("Nutritional Info", "").strip()
                
                if(description != ""):
                    formatted_output = f"{name}\n    - {description}\n"
                else:
                    formatted_output = f"{name}\n"
                menu += formatted_output # add cleaned text to menu string
        
        # return menu string
        return menu
    except Exception as e:
        print(f"Error waiting for page to load: {e}")
    finally:
        driver.quit()
    
def main():
    start_time = time.time() # start of function
    menu = scrape_menu()
    end_time = time.time() # end of function
    print(menu)
    print("\nDelivered in:", str(end_time - start_time), "seconds")
    
if __name__ == "__main__":
    main()