import re
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ResultPage:
    """Работа со страницей результатов поиска."""

    RESULTS_LIST = (By.XPATH, '//div[@data-test-id="search-results-items-list"]')
    FIRST_TICKET_PRICE = (By.XPATH, '(//div[@data-test-id="price"])[1]')
    ANY_TICKET_PRICE = (By.XPATH, '//div[@data-test-id="price"]')
    NO_RESULTS_MESSAGE = (
        By.XPATH,
        '//*[contains(., "Ничего не найдено") or contains(., "Ничего не нашлось")]',
    )
    FAVORITE_BUTTON = (By.XPATH, "(//button[@data-test-id='button'])[1]")
    LOGIN_FORM_TITLE = (
        By.XPATH,
        "//button[@data-test-id='button']//div[@data-test-id='text' and contains(normalize-space(.), 'Войти в')]",
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 30)

    def wait_for_prices_loaded(self, timeout: int = 45) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.ANY_TICKET_PRICE)
        )

    def get_ticket_price(self) -> str:
        price_element = self.wait.until(
            EC.visibility_of_element_located(self.FIRST_TICKET_PRICE)
        )
        return price_element.text.strip()

    def is_price_valid(self, price_text: str) -> bool:
        if not price_text:
            return False
        return bool(re.search(r"\d", price_text))

    def has_no_results(self, timeout: int = 20) -> bool:
        short_wait = WebDriverWait(self.driver, timeout)
        try:
            msg = short_wait.until(
                EC.visibility_of_element_located(self.NO_RESULTS_MESSAGE)
            )
            if msg and msg.is_displayed():
                return True
        except Exception:
            pass
        try:
            prices = self.driver.find_elements(*self.ANY_TICKET_PRICE)
            visible_prices = [p for p in prices if p.is_displayed()]
            if len(visible_prices) == 0:
                return True
        except Exception:
            pass
        return False

    def click_favourite_button(self) -> None:
        btn = self.wait.until(EC.element_to_be_clickable(self.FAVORITE_BUTTON))
        btn.click()

    def is_login_form_displayed(self) -> bool:
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.LOGIN_FORM_TITLE)
            ).is_displayed()
        except Exception:
            return False

    def get_login_form_text(self) -> str:
        try:
            return self.driver.find_element(*self.LOGIN_FORM_TITLE).text
        except Exception:
            return ""
