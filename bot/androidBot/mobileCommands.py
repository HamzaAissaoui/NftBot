import requests, random
from selenium.webdriver.common.by import By
from pages.filters import FiltersPage
from mobileHelper import hand_tap, scroll_by_coords


class Commands:        
    
    def open_marketplace(self):
        requests.post(self.session_uri+'/actions', json = hand_tap(900, 2150), headers = {'Content-Type': "application/json"})  
        




