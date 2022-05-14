from selenium.webdriver.common.by import By
from mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from bot.core.log import logger
import requests
from bot.models import Sneaker, Attributes, BoughtSneaker

class MarketplacePage:        

    @classmethod
    def scroll_next_page(cls, pageNum):
        if pageNum==0:
            return
        #Scrolling down to the next page
        requests.post(session_uri+'/actions', json = swipe_by_coords(2000, 300), headers = {'Content-Type': "application/json"}) 

    @classmethod
    def get_sneakers_in_view(cls):
        random_sleep()
        sneakersList = driver.find_element(By.XPATH, '//android.view.View[contains(@content-desc, "Walker")]')
        sneakersList = 1
        
