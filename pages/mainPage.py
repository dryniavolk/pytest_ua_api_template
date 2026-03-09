from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time


BASE_URL = "https://www.aviasales.ru/"


class MainPage:
    """Page Object для главной страницы Aviasales."""

    COOKIE_ACCEPT_BUTTON = (By.XPATH, "//button[@data-test-id='accept-cookies-button']")
    ORIGIN_INPUT = (By.XPATH, "//input[@data-test-id='origin-input']")
    DESTINATION_INPUT = (By.XPATH, "//input[@data-test-id='destination-input']")
    DATE_START = (By.XPATH, "//button[@data-test-id='start-date-field']")
    DATE_END = (By.XPATH, "//button[@data-test-id='end-date-field']")
    SEARCH_BUTTON = (By.XPATH, "//button[@data-test-id='form-submit']")
    PASSENGERS_FIELD = (By.XPATH, "//button[@data-test-id='passengers-field']")
    INFANTS_PLUS_BUTTON = (By.XPATH, "(//button[@data-test-id='increase-button'])[3]")
    INFANTS_COUNT = (By.XPATH, "//div[@data-test-id='number-of-infants']//div[@data-test-id='passenger-number']")
    DATE_CALENDAR = (By.CSS_SELECTOR, "div[class*='Calendar']")
    ORIGIN_SUGGEST = (By.XPATH, "//ul[@id='avia_form_origin-menu']")
    DESTINATION_SUGGEST = (By.CSS_SELECTOR, "ul.suggest__list li:first-child")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

    def navigate(self) -> None:
        self.driver.get(BASE_URL)
        try:
            self.wait.until(EC.presence_of_element_located(self.COOKIE_ACCEPT_BUTTON))
            self.accept_cookies()
        except Exception:
            pass

    def accept_cookies(self) -> bool:
        try:
            cookie_btn = self.wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BUTTON))
            cookie_btn.click()
            self.wait.until(EC.invisibility_of_element_located(self.COOKIE_ACCEPT_BUTTON))
            return True
        except Exception:
            return False

    def fill_departure_city(self, city: str) -> None:
        origin_field = self.wait.until(EC.element_to_be_clickable(self.ORIGIN_INPUT))
        origin_field.clear()
        origin_field.send_keys(city)
        try:
            first_option = self.wait.until(EC.element_to_be_clickable(self.ORIGIN_SUGGEST))
            first_option.click()
        except Exception:
            origin_field.send_keys(Keys.RETURN)
        time.sleep(0.5)  # небольшая пауза для стабилизации
        assert origin_field.get_attribute("value") == city

    def fill_arrival_city(self, city: str) -> None:
        dest_field = self.wait.until(EC.element_to_be_clickable(self.DESTINATION_INPUT))
        dest_field.clear()
        dest_field.send_keys(city)
        try:
            first_option = self.wait.until(EC.element_to_be_clickable(self.DESTINATION_SUGGEST))
            first_option.click()
        except Exception:
            dest_field.send_keys(Keys.RETURN)
        time.sleep(0.5)  # небольшая пауза для стабилизации

    def select_departure_date(self, start_date: str) -> str:
        date_start = self.wait.until(EC.element_to_be_clickable(self.DATE_START))
        self.driver.execute_script("arguments[0].click();", date_start)
        
        calendar_locators = [
            (By.CSS_SELECTOR, "div[class*='Calendar']"),
            (By.CSS_SELECTOR, "div[class*='calendar']"),
            (By.XPATH, "//div[contains(@class, 'calendar')]"),
        ]
        
        calendar_found = False
        for locator in calendar_locators:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(locator))
                calendar_found = True
                break
            except Exception:
                continue
        
        if not calendar_found:
            date_start.send_keys(Keys.CONTROL + "a")
            date_start.send_keys(start_date)
            date_start.send_keys(Keys.ENTER)
            return start_date
        
        day_button = (By.XPATH, f"//div[@data-test-id='date-{start_date}']/ancestor::button")
        try:
            btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(day_button))
            self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            date_start.send_keys(Keys.CONTROL + "a")
            date_start.send_keys(start_date)
            date_start.send_keys(Keys.ENTER)
        
        return start_date

    def select_return_date(self, end_date: str) -> str:
        date_end = self.wait.until(EC.element_to_be_clickable(self.DATE_END))
        self.driver.execute_script("arguments[0].click();", date_end)
        
        calendar_locators = [
            (By.CSS_SELECTOR, "div[class*='Calendar']"),
            (By.CSS_SELECTOR, "div[class*='calendar']"),
        ]
        
        for locator in calendar_locators:
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(locator))
                break
            except Exception:
                continue
        
        day_button = (By.XPATH, f"//div[@data-test-id='date-{end_date}']/ancestor::button")
        try:
            btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(day_button))
            self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            date_end.send_keys(Keys.CONTROL + "a")
            date_end.send_keys(end_date)
            date_end.send_keys(Keys.ENTER)
        
        return end_date

    def click_search(self) -> None:
        search_btn = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        self.driver.execute_script("arguments[0].click();", search_btn)
        WebDriverWait(self.driver, 20).until(
            lambda d: any(s in d.current_url for s in ("search", "params=", "aviasales"))
        )
        self.switch_to_results_tab()

    def switch_to_results_tab(self) -> None:
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def add_infant(self) -> str:
        passengers_field = self.wait.until(EC.element_to_be_clickable(self.PASSENGERS_FIELD))
        self.driver.execute_script("arguments[0].click();", passengers_field)
        infant_plus = self.wait.until(EC.element_to_be_clickable(self.INFANTS_PLUS_BUTTON))
        self.driver.execute_script("arguments[0].click();", infant_plus)
        passenger_info = self.wait.until(EC.visibility_of_element_located(self.INFANTS_COUNT))
        passenger_text = passenger_info.text
        self.driver.find_element(By.TAG_NAME, "body").click()
        return passenger_text
