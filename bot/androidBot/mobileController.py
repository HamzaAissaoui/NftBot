
import imp
from bot.helper import logger
from time import sleep
from bot.androidBot.mobileCommands import Commands
from mobileHelper import driver
from pages import Pages

commands = Commands()
class mobileController:
    
    def filter_search(self, shoe_mint_number):
        commands.open_marketplace()
        Pages.Filters.open_filters()
        Pages.Filters.filter_by_sneakers()
        

    def restart_app(self):
        try:
            driver.close_app()
        except:
            logger.warning('App is already closed!')
        sleep(1)
        driver.launch_app()
    



