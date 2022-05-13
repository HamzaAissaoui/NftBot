from selenium.webdriver.common.by import By
from mobileHelper import hand_tap, scroll_by_coords, driver, SESSION_BASE_URI

class FiltersPage:
        
    @classmethod
    def open_filters(cls):
        driver.find_element(By.XPATH, value = '//android.view.View[contains(@content-desc, "Filter")]').click()
    
    @classmethod
    def filter_by_sneakers(cls):
        driver.find_element(By.XPATH, value = '//android.view.View[@content-desc="Sneakers"]').click()