
from time import sleep
from config.settings import Settings
from core.log import logger
from plugins.mobileCommands import Commands
from .mobileHelper import driver, random_sleep
from .pages import Pages
from models import Session


class mobileController:

    def filter_search(self, shoe_mint_number):
        logger.info('started filtering sneakers.')
        Commands.open_marketplace()
        Pages.Filters.open_filters()
        Pages.Filters.filter_by('Type', 'Sneakers')
        Pages.Filters.filter_by('Class', 'Walker')
        Pages.Filters.filter_by('Quality', 'Common')
        Pages.Filters.filter_by('Shoe mint', shoe_mint_number)
        random_sleep(1.5, 3.5)

    def scrap_pages(self, numberPages):
        for pageNum in range(0, numberPages):
            """
            1. Get sneakers infos
            2. for each one check if their ID exists in the database
            3. if it does not exist, open it and save its information
            4. if it exists skip it
            5. scroll down and repeat"""
            Pages.Marketplace.scroll_next_page(pageNum)
            sneakersInView = Pages.Marketplace.get_unsaved_sneakers_in_view()
            print('Reached End')
            for sneakerElement in sneakersInView:
                print(sneakerElement.get_attribute("content-desc"))

    def restart_app(self):
        random_sleep()
        logger.info('restarting app.')
        try:
            driver.close_app()
        except:
            logger.warning('App is already closed!')
        random_sleep()
        driver.start_activity(Settings.get_app_package(),
                              Settings.get_wait_activity())
        Commands.skip_notice()

    def quit_driver(self):
        driver.quit()
