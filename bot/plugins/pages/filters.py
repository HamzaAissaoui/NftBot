from selenium.webdriver.common.by import By
from plugins.mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from core.log import logger
import requests
class FiltersPage:        
    @classmethod
    def open_filters(cls):
        random_sleep()
        driver.find_element(By.XPATH, value = '//android.view.View[contains(@content-desc, "Filter")]').click()
    
    @classmethod
    def filter_by(cls, filterName, value):
        random_sleep()
        logger.info(f'filtering by {filterName}')
        if filterName != 'Shoe mint':
            driver.find_element(By.XPATH, value = f'//android.view.View[@content-desc="{value}"]').click()

        else:
            startMap = {
                2: 995,
                1: 505,
                0: 410
            }

            endMap = {
                2: 505,
                1: 410,
                0: 315
            }
    
            #Shoe Mint Value Change
            requests.post(session_uri+'/actions', json = swipe_by_coords(1745, 1745, startMap[value], endMap[value]), headers = {'Content-Type': "application/json"}) 

            #Confirm Button
            requests.post(session_uri+'/actions', json = hand_tap(630, 2170), headers = {'Content-Type': "application/json"})  
