from core.log import logger
from plugins.mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from selenium.webdriver.common.by import By


class SneakerPage:
    @classmethod
    def scrapSneaker(cls, sneakerId):
        logger.info('scrapping sneaker page')
        #Clicking on Base
        random_sleep(message='clicking on Base button')
        driver.find_element(By.XPATH, '//android.view.View[@content-desc="Base"]').click()
        price = cls.getPrice()
        efficiency = cls.getAttribute('Efficiency')
        resilience = cls.getAttribute('Resilience')
        luck = cls.getAttribute('Luck')
        #Save sneaker in database
        return sneakerId, price, efficiency, luck, resilience

    @classmethod
    def getPrice(cls):
        priceContent = driver.find_element(By.XPATH, '//android.view.View[contains(@content-desc, "SOL")]').get_attribute('content-desc')   
        price = float(priceContent.split(' ')[0])
        return price

    @classmethod
    def getAttribute(cls, attributeName):
        attributeElement = driver.find_element(By.XPATH, f'//android.view.View[@content-desc="{attributeName}"]/following-sibling::android.view.View[1]')
        return float(attributeElement.get_attribute('content-desc'))