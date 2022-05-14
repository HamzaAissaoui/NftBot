from selenium.webdriver.common.by import By
from mobileHelper import hand_tap, scroll_by_coords, driver, SESSION_BASE_URI, random_sleep


class FiltersPage:        
    @classmethod
    def open_filters(cls):
        random_sleep()
        driver.find_element(By.XPATH, value = '//android.view.View[contains(@content-desc, "Filter")]').click()
    
    @classmethod
    def filter_by(cls, filterName, value):
        random_sleep()
        driver.find_element(By.XPATH, value = f'//android.view.View[@content-desc="{value}"]').click()
