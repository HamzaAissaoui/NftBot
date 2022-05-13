from time import sleep
from bot.helper import logger
from bot.models import Sneaker, Attributes, BoughtSneaker, db
from bot.androidBot.mobileController import mobileController


controller = mobileController()
class mobileView:

    def scrap_sneakers(self):
        for i in range(3):
            controller.restart_app()
            controller.filter_search(i)


