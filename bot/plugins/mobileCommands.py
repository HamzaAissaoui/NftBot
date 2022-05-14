import requests
from selenium.webdriver.common.by import By
from mobileHelper import hand_tap, scroll_by_coords, session_uri, driver,random_sleep
from bot.core.log import logger
class Commands:        
    
    @classmethod
    def open_marketplace(cls):
        logger.info('opening marketplace.')
        random_sleep()
        requests.post(session_uri+'/actions', json = hand_tap(900, 2150), headers = {'Content-Type': "application/json"})  
        
    @classmethod
    def skip_notice(cls):
        random_sleep()
        requests.post(session_uri+'/actions', json = hand_tap(1050, 2180), headers = {'Content-Type': "application/json"})  

        
 





