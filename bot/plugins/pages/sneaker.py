from bot.plugins.mobileCommands import Commands
from core.log import logger
from plugins.mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from selenium.webdriver.common.by import By
from models import Attributes, BoughtSneaker, Session, Sneaker
from random import randint
from appium.webdriver.common.appiumby import AppiumBy


class SneakerPage:
    @classmethod
    def scrapSneaker(cls, sneaker_id):
        # Clicking on Base
        if Commands.clickBaseButton() == 'skipped':
            return 'skipped'

        price = cls.getPrice('SOL')
        efficiency = cls.getAttribute('Efficiency')
        resilience = cls.getAttribute('Resilience')
        luck = cls.getAttribute('Luck')
        attributes_sum = efficiency+luck+resilience
        if attributes_sum == 0.0:
            logger.warning('sneaker not available, skipped')
            return

        # Save sneaker in database
        sneakerToSave = Sneaker(sneaker_id=sneaker_id, efficiency=efficiency, luck=luck, resilience=resilience,
                                attributes_sum=attributes_sum, price=price)
        with Session as session:
            session.add(sneakerToSave)
            session.commit()
        logger.info(f'sneaker {sneaker_id} saved')

    @classmethod
    def getPrice(cls, currency):
        priceContent = driver.find_element(
            By.XPATH, f'//android.view.View[contains(@content-desc, "{currency}")]').get_attribute('content-desc')
        price = float(priceContent.split(' ')[0])
        return price

    @classmethod
    def getAttribute(cls, attributeName):
        attributeElement = driver.find_element(
            By.XPATH, f'//android.view.View[@content-desc="{attributeName}"]/following-sibling::android.view.View[1]')
        return float(attributeElement.get_attribute('content-desc'))

    @classmethod
    def buySneaker(cls, sneaker_id):
        '''4. for each sneaker in view (only first 6 sneakers):
            b. if not bought:
                - open sneaker //DONE
                - check attributes not 0, if yes skip sneaker
                - click base button
                - check which interval attributes belong to
                - check if cheapest price for that interval not 0, if it is skip sneaker
                - check if sneaker price at least 15% less than cheapest average price
                - if it is, buy and confirm
                - if it's not cheaper, try the other 5
        '''

        random_sleep(2.5, 4, message='waiting for sneaker to load')
        if not cls.checkSneakerOpen():
            return 'skipped'

        # Clicking on Base
        if Commands.FastClickBaseButton() == 'skipped':
            return 'skipped'

        price = cls.getPrice('SOL')
        efficiency = cls.getAttribute('Efficiency')
        resilience = cls.getAttribute('Resilience')
        luck = cls.getAttribute('Luck')
        attributes_sum = efficiency+luck+resilience
        if attributes_sum == 0.0:
            logger.warning('sneaker not available, skipped')
            return

        if not cls.sneakerPriceCheaperThanAverage(attributes_sum, price):
            return

        # buy and confirm sneaker on app here
        try:
            driver.find_element(AppiumBy.ACCESSIBILITY_ID,
                                'BUY NOW').click()  # Clicking on Buy Button
            random_sleep(0.5, 1)
            driver.find_element(AppiumBy.ACCESSIBILITY_ID,
                                'CONFIRM').click()  # Clicking on Confirm Button
                                
        except Exception as e:
            logger.warning('error buying sneaker')
            logger.debug(e.args[0])
            return

        # save bought sneaker in database
        sellingPrice = cls.setSellingPrice(price)
        boughtSneakerToSave = BoughtSneaker(
            sneaker_id=sneaker_id, buying_price=price, selling_price=sellingPrice)
        with Session as session:
            session.add(boughtSneakerToSave)
            session.commit()
        logger.info(f'sneaker {sneaker_id} saved')

    @classmethod
    def setSellingPrice(cls, price):
        percentage = randint(5, 10) / 100
        return float(price + price * percentage)

    @classmethod
    def sneakerPriceCheaperThanAverage(cls, attributes_sum, price):
        with Session as session:
            attribute = session.query(Attributes).filter(
                Attributes.min_attribute_sum <= attributes_sum,
                Attributes.max_attribute_sum >= attributes_sum
            ).first()
            if attribute.total_sneakers == 0:
                logger.warning('no sneakers in interval, skipped')
                return False

            else:
                acceptablePrice = attribute.cheapest_average_price - \
                    (attribute.cheapest_average_price * 15 / 100)
                if price <= acceptablePrice:
                    logger.info('acceptable price, buying sneaker')
                    return True

                else:
                    logger.warning('sneaker too expensive, skipped')
                    return False

    @classmethod
    def checkSneakerOpen(cls):
        attributeElement = driver.find_elements(
            By.XPATH, f'//android.view.View[@content-desc="Efficiency"]/following-sibling::android.view.View[1]')

        if not attributeElement:
            logger.warning('sneaker not open, skipped')
            return False
        else:
            return True
