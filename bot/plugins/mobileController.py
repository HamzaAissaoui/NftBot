
from bot.core.log import logger
from bot.plugins.mobileCommands import Commands
from mobileHelper import driver, random_sleep
from pages import Pages


class mobileController:
    
    def filter_search(self, shoe_mint_number):
        Commands.open_marketplace()
        Pages.Filters.open_filters()
        Pages.Filters.filter_by('Type', 'Sneakers')
        Pages.Filters.filter_by('Class', 'Walker')
        Pages.Filters.filter_by('Quality', 'Common')
        Pages.Filters.filter_by('Shoe mint', shoe_mint_number)

    def restart_app(self):
        try:
            driver.close_app()
        except:
            logger.warning('App is already closed!')
        
        random_sleep()
        driver.launch_app()
        Commands.skip_notice()



