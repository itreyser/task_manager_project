import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver_new():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)
    return driver


def test1_hw18(driver_new):
    driver_new.get("https://omayo.blogspot.com/")
    element = driver_new.find_element(By.ID, "textbox1")
    element.clear()
    element.send_keys("Selenium test")
    assert element.get_attribute('value') == "Selenium test"
    driver_new.quit()


def test2(driver_new):
    driver_new.get("https://omayo.blogspot.com/")
    element = driver_new.find_element(By.ID, "drop1")
    select = Select(element)
    select.select_by_visible_text("doc 3")
    assert select.first_selected_option.text == 'doc 3'
    driver_new.quit()


def test3(driver_new):
    driver_new.get('https://demoqa.com/webtables')
    driver_new.find_element(By.CSS_SELECTOR, "button[id='addNewRecordButton']").click()
    driver_new.find_element(By.CSS_SELECTOR, "input[id='firstName']").send_keys("John")
    driver_new.find_element(By.CSS_SELECTOR, "input[id='lastName']").send_keys("Doe")
    driver_new.find_element(By.CSS_SELECTOR, "input[id='userEmail']").send_keys("john.doe@example.com")
    driver_new.find_element(By.CSS_SELECTOR, "input[id='age']").send_keys("30")
    driver_new.find_element(By.CSS_SELECTOR, "input[id='salary']").send_keys("50000")
    driver_new.find_element(By.CSS_SELECTOR, "input[id='department']").send_keys("IT")
    driver_new.find_element(By.CSS_SELECTOR, "button[id='submit']").click()
    elements = driver_new.find_elements(By.XPATH, "//*[text()='John']")

    assert len(elements) == 1, "Проверка, что в списке больше чем 1 элемент"

    edit_button = driver_new.find_element(By.XPATH, "//*[text()='John']/..//div[last()]/span[@title='Edit']")
    edit_button.click()
    driver_new.find_element(By.CSS_SELECTOR, "input[id='salary']").clear()
    driver_new.find_element(By.CSS_SELECTOR, "input[id='salary']").send_keys("55000")
    driver_new.find_element(By.CSS_SELECTOR, "input[id='age']").clear()
    driver_new.find_element(By.CSS_SELECTOR, "input[id='age']").send_keys("35")
    driver_new.find_element(By.CSS_SELECTOR, "button[id='submit']").click()

    edit_salary = driver_new.find_elements(By.XPATH, "//*[text()='John']/../div[text()='55000']")
    assert len(edit_salary) == 1, "Проверка, что изменена зарплата"

    edit_age = driver_new.find_elements(By.XPATH, "//*[text()='John']/../div[text()='35']")
    assert len(edit_age) == 1, "Проверка, что изменился возраст"

    elements_del = driver_new.find_element(By.XPATH, "//*[text()='John']/..//div[last()]/span[@title='Delete']")
    elements_del.click()

    element_after_del = driver_new.find_elements(By.XPATH, "//*[text()='John']")
    assert len(element_after_del) == 0, "Проверка, что строка удалена"
    driver_new.quit()
