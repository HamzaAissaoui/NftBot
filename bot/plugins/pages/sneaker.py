from core.log import logger
from plugins.mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from selenium.webdriver.common.by import By
from models import Session, Sneaker


class SneakerPage:
    @classmethod
    def scrapSneaker(cls, sneaker_id):
        logger.info('scrapping sneaker page')
        # Clicking on Base
        random_sleep(4, 5, message='before clicking on Base button')
        try:
            driver.find_element(
                By.XPATH, '//android.view.View[@content-desc="Base"]').click()
        except:
            logger.warning('could not open sneaker, skipping')
            return 'skipped'
            
        price = cls.getPrice()
        efficiency = cls.getAttribute('Efficiency')
        resilience = cls.getAttribute('Resilience')
        luck = cls.getAttribute('Luck')
        attributes_sum = efficiency+luck+resilience
        if luck == 0.0 and resilience == 0.0 and efficiency == 0.0:
            logger.warning('sneaker not available, skipped')
            return
            
        # Save sneaker in database
        sneakerToSave = Sneaker(sneaker_id=sneaker_id, efficiency=efficiency, luck=luck, resilience=resilience,
                                attributes_sum=attributes_sum, price=price)
        with Session as session:
            session.add(sneakerToSave)
            session.commit()

    @classmethod
    def getPrice(cls):
        priceContent = driver.find_element(
            By.XPATH, '//android.view.View[contains(@content-desc, "SOL")]').get_attribute('content-desc')
        price = float(priceContent.split(' ')[0])
        return price

    @classmethod
    def getAttribute(cls, attributeName):
        attributeElement = driver.find_element(
            By.XPATH, f'//android.view.View[@content-desc="{attributeName}"]/following-sibling::android.view.View[1]')
        return float(attributeElement.get_attribute('content-desc'))
