from bot.core.log import logger
from bot.models import Sneaker, Attributes, BoughtSneaker, db
from bot.plugins.mobileController import mobileController


controller = mobileController()
class mobileView:

    def scrap_sneakers(self):
        for i in range(2,-1,-1):
            controller.restart_app()
            controller.filter_search(i)


