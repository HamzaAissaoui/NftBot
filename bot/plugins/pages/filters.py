from selenium.webdriver.common.by import By
from plugins.mobileHelper import hand_tap, swipe_by_coords, driver, session_uri, random_sleep
from core.log import logger
import requests


class FiltersPage:
    @classmethod
    def open_filters(cls):
        random_sleep(3, 6, message='before opening filters page')
        driver.find_element(
            By.XPATH, value='//android.view.View[contains(@content-desc, "Filter")]').click()

    @classmethod
    def filter_by(cls, filterName, value):
        random_sleep(2, 4, message='before choosing filter')
        logger.warning(f'filtering by {filterName} value {value}')
        if filterName != 'Shoe mint':
            driver.find_element(
                By.XPATH, value=f'//android.view.View[@content-desc="{value}"]').click()

        else:

            startMap = {
                2: 995,
                1: 505,
                0: 410
            }

            endMap = {
                2: 505,
                1: 410,
                0: 315
            }

            # Shoe Mint Value Change
            requests.post(session_uri+'/actions', json=swipe_by_coords(1745, 1745,
                          startMap[2], endMap[value]), headers={'Content-Type': "application/json"})

    @classmethod
    def filter_shoe_mint(cls, endvalue):
        random_sleep(2, 4, message='before choosing filter')
        logger.warning(
            f'filtering by Shoe Mint from value {endvalue}')
        startValue = endvalue+1
        if endvalue == 2:
            startValue = 0

        Map = {
            2: 505,
            1: 410,
            0: 315
        }

        # Shoe Mint Value Change
        requests.post(session_uri+'/actions', json=swipe_by_coords(1745, 1745,
                                                                   Map[startValue], Map[endvalue]), headers={'Content-Type': "application/json"})

    @classmethod
    def confirmFilters():
        # Confirm Button
        requests.post(session_uri+'/actions', json=hand_tap(630,
                                                            2170), headers={'Content-Type': "application/json"})
