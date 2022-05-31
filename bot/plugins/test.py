from plugins.mobileHelper import driver, session_uri, hand_tap, swipe_by_coords
from selenium.webdriver.common.by import By
import requests

def getSneakerId(description : str):
    """Returns the Sneaker ID which is after the # symbol"""
    descList = description.split('\n')
    hashTagIndex = descList.index('#')
    return descList[hashTagIndex+1]

def get_sneakers_ids():
    print('hi')
    sneakersList = driver.find_elements(By.XPATH, '//android.view.View[contains(@content-desc, "Walker")]')
    for sneaker in sneakersList:
        sneakerDescription = sneaker.get_attribute("content-desc")
        sneakerID = getSneakerId(sneakerDescription)
        print(sneakerID)
    driver.quit()

    
def filter_by(filterName, value):
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