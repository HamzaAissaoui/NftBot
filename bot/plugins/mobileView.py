from core.log import logger
from plugins.mobileController import mobileController

controller = mobileController()


class mobileView:

    def __init__(self, session):
        self.session = session
        controller.session = session

    def scrap_sneakers(self):
        for i in range(2,-1,-1):
            controller.restart_app()
            controller.filter_search(i)
            controller.scrap_pages(40)
            

    