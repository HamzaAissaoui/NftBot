from bot.plugins.pages import Pages
from core.log import logger
from plugins.mobileController import mobileController
from plugins.mobileCommands import Commands
controller = mobileController()


class mobileView:

    @classmethod
    def scrap_sneakers(cls, startFromPage=0,endAtPage=10):
        logger.warning('Started Scraping Sneakers')
        for i in range(2, -1, -1):
            controller.restart_app()
            Commands.open_marketplace()
            controller.filter_search(i)
            controller.scrap_pages(startFromPage=startFromPage,endAtPage=endAtPage)
        controller.fillAttributesTable()

    @classmethod
    def buy_sneakers(cls):
        """
        1. Open marketplace
        2. Check if I have money, if I don't return //DONE
        3. If I have money, filter by latest and a few other filters (like part 1) /// DONE
        4. for each sneaker in view (only first 6 sneakers):
            b. if not bought:
                - open sneaker
                - check attributes not 0, if yes skip sneaker
                - click base button
                - check which interval attributes belong to
                - check if cheapest price for that interval not 0, if it is skip sneaker
                - check if sneaker price at least 15% less than cheapest average price
                - if it is, buy and confirm
                - if it's not cheaper, try the other 5
        5. refresh and redo from step 2 for 5 times or until we don't have money anymore
        """
        controller.restart_app()
        Commands.open_marketplace()
        Pages.Marketplace.changeOrderFromTo('Lowest Price', 'Latest')

        for i in range(5):
            if controller.checkBalance(currency='SOL', minium=5.0):
                for j in range(2, -1, -1):
                    controller.filterBuyingSearch(loopIndex=i, shoe_mint_number=j)
                    #Start buying sneakers here
                    sneakersInView = Pages.Marketplace.get_sneakers_in_view_to_buy()
                    controller.buyValidSneakers(sneakersInView)
            
            else:
                logger.warning('out of money for now, going to sell or scrap sneakers')
                return

             
            
            



