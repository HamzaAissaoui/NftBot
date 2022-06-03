from core.log import logger
from plugins.mobileController import mobileController
from models import Sneaker
controller = mobileController()


class mobileView:

    @classmethod
    def scrap_sneakers(cls, startFromPage=0,endAtPage=10):
        for i in range(2, -1, -1):
            controller.restart_app()
            controller.filter_search(i)
            controller.scrap_pages(startFromPage=startFromPage,endAtPage=endAtPage)
        controller.fillAttributesTable()
