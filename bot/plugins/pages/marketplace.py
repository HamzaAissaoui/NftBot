from selenium.webdriver.common.by import By
from plugins.mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from core.log import logger
import requests
from models import Session, Sneaker, Attributes, BoughtSneaker
from sqlalchemy import select


class MarketplacePage:

    @classmethod
    def scroll_next_page(cls, pageNum):
        if pageNum == 0:
            return

        # Scrolling down to the next page
        logger.warning(f'scrolling to page {pageNum} of sneakers')
        requests.post(session_uri+'/actions', json=swipe_by_coords(2000,
                      300), headers={'Content-Type': "application/json"})
        random_sleep(2.5, 4.5, message='while sneakers load')

    @classmethod
    def get_unsaved_sneakers_in_view(cls):
        random_sleep(message='to make sure sneakers are loaded')
        sneakersList = driver.find_elements(
            By.XPATH, '//android.view.View[contains(@content-desc, "Walker")]')
        unsavedSneakers = []
        for sneakerElement in sneakersList:
            sneakerDescription = sneakerElement.get_attribute("content-desc")
            sneakerID = cls.getSneakerId(sneakerDescription)
            if cls.checkSneakerNonExistant(sneakerID):
                unsavedSneakers.append({'element':sneakerElement, 'sneaker_id': sneakerID})
            else:
                logger.warning('sneaker already saved')
        return unsavedSneakers

    @classmethod
    def get_sneakers_in_view_to_buy(cls):
        random_sleep()
        sneakersList = driver.find_elements(
            By.XPATH, '//android.view.View[contains(@content-desc, "Walker")]')
        return sneakersList


    @classmethod
    def changeOrderFromTo(cls, currentOrder, newOrder):
        random_sleep(3, 5, 'before opening order list')
        driver.find_element(By.XPATH, f'//android.widget.ImageView[@content-desc="{currentOrder}"]').click()
        random_sleep(1, 3, f'before changing order to {newOrder}')
        driver.find_element(By.XPATH, f'//android.view.View[contains(@content-desc, "{newOrder}")]').click()


    @classmethod
    def checkSneakerNonExistant(cls, sneakerId):
        with Session as session:
            return session.query(Sneaker.id).filter_by(
                sneaker_id=sneakerId).first() is None

    @classmethod
    def getSneakerId(cls, description: str):
        """Returns the Sneaker ID which is after the # symbol"""
        descList = description.split('\n')
        hashTagIndex = descList.index('#')
        return descList[hashTagIndex+1]
