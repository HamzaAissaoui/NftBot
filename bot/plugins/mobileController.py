
from bot.helper import logger
from time import sleep
from bot.plugins.mobileCommands import Commands
from mobileHelper import driver
from pages import Pages


class mobileController:
    
    def filter_search(self, shoe_mint_number):
        Commands.open_marketplace()
        Pages.Filters.open_filters()
        Pages.Filters.filter_by('Type', 'Sneakers')
        Pages.Filters.filter_by('Class', 'Walker')
        Pages.Filters.filter_by('Quality', 'Common')
        

    def restart_app(self):
        try:
            driver.close_app()
        except:
            logger.warning('App is already closed!')
        sleep(1)
        driver.launch_app()
    



