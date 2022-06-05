import requests
from selenium.webdriver.common.by import By
from plugins.mobileHelper import hand_tap, swipe_by_coords, session_uri, driver, random_sleep
from core.log import logger


class Commands:

    @classmethod
    def open_marketplace(cls):
        random_sleep(4, 6, message='before opening marketplace')
        logger.info('opening marketplace.')
        requests.post(session_uri+'/actions', json=hand_tap(900, 2150),
                      headers={'Content-Type': "application/json"})

    @classmethod
    def skip_notice(cls):
        random_sleep(3, 5, message='before skipping notice')
        logger.info('skipping notice.')
        requests.post(session_uri+'/actions', json=hand_tap(1050,
                      2180), headers={'Content-Type': "application/json"})

    @classmethod
    def openSpendingAccount(cls):
        driver.find_element(By.XPATH, '//android.widget.ImageView[contains(@content-desc, "km")][1]/following-sibling::android.view.View[1]').click()
    
    @classmethod
    def clickBaseButton(cls):
        random_sleep(4, 5, message='before clicking on Base button')
        BaseButtonList = driver.find_elements(
                By.XPATH, '//android.view.View[@content-desc="Base"]')
        if BaseButtonList:
            BaseButtonList[0].click()
        else:
            random_sleep(8, 15, message='because sneaker is slow to load')
            BaseButtonList = driver.find_elements(
                By.XPATH, '//android.view.View[@content-desc="Base"]')
            if BaseButtonList:
                BaseButtonList[0].click()
            else:
                logger.warning('could not open sneaker, skipping')
                return 'skipped'  

    @classmethod
    def FastClickBaseButton(cls):
        BaseButtonList = driver.find_elements(
                By.XPATH, '//android.view.View[@content-desc="Base"]')
        if BaseButtonList:
            BaseButtonList[0].click()
        else:
            logger.warning('could not open sneaker, skipping')
            return 'skipped' 