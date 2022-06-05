
from time import sleep
from config.settings import Settings
from core.log import logger
from plugins.mobileCommands import Commands
from .mobileHelper import driver, random_sleep
from .pages import Pages
from models import Attributes, Session, Sneaker
from sqlalchemy import update


class mobileController:

    def filter_search(self, shoe_mint_number):
        logger.info('started filtering sneakers.')
        Pages.Filters.open_filters()
        Pages.Filters.filter_by('Type', 'Sneakers')
        Pages.Filters.filter_by('Class', 'Walker')
        Pages.Filters.filter_by('Quality', 'Common')
        Pages.Filters.filter_by('Shoe mint', shoe_mint_number)
        Pages.Filters.confirmFilters()
        random_sleep(3, 6, message='before starting to scrap')

    def scrap_pages(self, startFromPage, endAtPage):
        repeatedSneakers = 0

        # Scrolling to the page we start scrolling from
        if startFromPage > 1:
            for i in range(0, startFromPage):
                Pages.Marketplace.scroll_next_page(i)

        for pageNum in range(startFromPage, endAtPage):
            """
            1. Get sneakers infos
            2. for each one check if their ID exists in the database
            3. if it does not exist, open it and save its information
            4. if it exists skip it
            5. scroll down and repeat"""
            Pages.Marketplace.scroll_next_page(pageNum)
            unsavedSneakers = Pages.Marketplace.get_unsaved_sneakers_in_view()
            if not unsavedSneakers:
                repeatedSneakers+1

            if repeatedSneakers > 5:
                logger.warning(
                    'either reached the end or you need to update the starting page and ending page, changing filters or finalizing scrapping')
                break

            logger.warning('opening unsaved sneakers')
            for sneakerElement in unsavedSneakers:
                random_sleep(3, 6, message='before saving next sneaker')
                sneakerElement['element'].click()
                scrappingStatus = Pages.Sneaker.scrapSneaker(
                    sneakerElement['sneaker_id'])
                if scrappingStatus != 'skipped':
                    driver.back()

        Sneaker.deleteOldsneakers()

    def fillAttributesTable(self):
        """From sneakers table do a query that gets all sneakers with attribute sum between min and max:
        1. get count(*)
        2. get prices
        3. order by price Ascending then calculate the average of the first 10 sneakers(cheapest) """
        logger.info('calculating attributes and cheapest prices')
        minAttribute = 0.1
        maxAttribute = 1
        while maxAttribute <= 30:
            with Session as session:
                total_sneakers = session.query(Sneaker.id).filter(
                    Sneaker.attributes_sum >= minAttribute,
                    Sneaker.attributes_sum <= maxAttribute
                ).count()
                prices = session.query(Sneaker.price).filter(
                    Sneaker.attributes_sum >= minAttribute,
                    Sneaker.attributes_sum <= maxAttribute
                ).order_by(Sneaker.price).all()

                # Calculating cheapest average price
                cheapest_average_price = 0
                prices = [r for r, in prices]
                if len(prices) >= 10:
                    cheapest_average_price = sum(prices[:10]) / 10
                elif len(prices) > 0:
                    cheapest_average_price = sum(prices) / len(prices)

                # Updating into attributes table
                AttributeToUpdate = session.query(Attributes).filter(
                    Attributes.max_attribute_sum == maxAttribute).first()
                AttributeToUpdate.total_sneakers = total_sneakers
                AttributeToUpdate.cheapest_average_price = cheapest_average_price
                session.commit()

                # Incrementing min and max attributes
                minAttribute += 1
                maxAttribute += 1
        logger.info('Finished calculating attributes and cheapest prices')

    def checkBalance(self, currency, minimum):
        logger.info('checking balance')
        Commands.openSpendingAccount()
        balance = Pages.Sneaker.getAttribute(currency)     
        driver.back()   
        return float(balance) >= minimum

    def filterBuyingSearch(self, loopIndex, shoe_mint_number):
        if loopIndex == 0:
            self.filter_search(shoe_mint_number)
        else:
            Pages.Filters.open_filters()
            Pages.Filters.filter_shoe_mint(shoe_mint_number)
            Pages.Filters.confirmFilters()
            random_sleep(1, 3, message='before starting to buy')

    def buyValidSneakers(self, sneakersList):
        pass

    def restart_app(self):
        random_sleep(message='before restarting app')
        logger.info('restarting app.')
        try:
            driver.close_app()
        except:
            logger.warning('App is already closed!')
        random_sleep(message='while app restarts')
        driver.start_activity(Settings.get_app_package(),
                              Settings.get_wait_activity())
        Commands.skip_notice()

    def quit_driver(self):
        driver.quit()
