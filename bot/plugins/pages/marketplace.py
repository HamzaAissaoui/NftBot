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
        requests.post(session_uri+'/actions', json=swipe_by_coords(2000,
                      300), headers={'Content-Type': "application/json"})

    @classmethod
    def get_unsaved_sneakers_in_view(cls):
        random_sleep()
        sneakersList = driver.find_elements(
            By.XPATH, '//android.view.View[contains(@content-desc, "Walker")]')
        for sneakerElement in sneakersList:
            sneakerDescription = sneakerElement.get_attribute("content-desc")
            sneakerID = cls.getSneakerId(sneakerDescription)
            unsavedSneakers = []
            if cls.checkSneakerNonExistant(sneakerID):
                unsavedSneakers.append(sneakerElement)
        return unsavedSneakers

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
