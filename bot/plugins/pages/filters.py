from selenium.webdriver.common.by import By
from mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from bot.core.log import logger
import requests
class FiltersPage:        
    @classmethod
    def open_filters(cls):
        random_sleep()
        driver.find_element(By.XPATH, value = '//android.view.View[contains(@content-desc, "Filter")]').click()
    
    @classmethod
    def filter_by(cls, filterName, value):
        random_sleep()
        if filterName != 'Shoe mint':
            driver.find_element(By.XPATH, value = f'//android.view.View[@content-desc="{value}"]')

        else:
            startMap = {
                2: "100%, 7",
                1: "29%, 2",
                0: "14%, 1"
            }
            startX, yCoord = driver.find_element_by_accessibility_id(startMap[value]).location.values()
            endMap = {
                2: 505,
                1: 410,
                0: 315
            }

            #Shoe Mint Value Change
            requests.post(session_uri+'/actions', json = swipe_by_coords(yCoord, yCoord, startX, endMap[value]), headers = {'Content-Type': "application/json"}) 

            #Confirm Button
            requests.post(session_uri+'/actions', json = hand_tap(630, 2170), headers = {'Content-Type': "application/json"})  
