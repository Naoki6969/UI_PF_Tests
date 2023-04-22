import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome("C:/yandexdriver.exe") #использую яндекс браузер
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   pytest.driver.find_element(By.ID, 'email').send_keys('naok6969@gmail.com')
   pytest.driver.find_element(By.ID, 'pass').send_keys('naoki6969')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')

   yield

   pytest.driver.quit()


def test_different_names():
    """Тест проверяет что  у всех питомцев разные имена"""

    names_list = []
    names = WebDriverWait(pytest.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[1]')))
    for i in range(len(names)):
        names_list.append(names[i].text)
    assert len(names_list) == len(set(names_list))



def test_all_my_pets():
    """Тест проверяет наличие всех питомцев"""

    quantity = WebDriverWait(pytest.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
    left_info = pytest.driver.find_element(By.XPATH, '//body/div[1]/div[1]/div[1]')
    num = left_info.get_attribute('innerText')

    assert str(len(quantity) - 1) in num


def test_photo():
    """Тест проверяет что хотя бы у половины питомцев есть фото"""

    count_photo = 0
    images = WebDriverWait(pytest.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//tbody/tr/th/img')))

    for i in range(len(images)):
        if images[i].get_attribute('src'):
            count_photo += 1

    assert len(images) / count_photo <= 2

def test_name_age_breed():
    """Тест проверяет что у всех питомцев есть имя, возраст, порода"""

    names = WebDriverWait(pytest.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[1]')))
    breeds = WebDriverWait(pytest.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[2]')))
    ages = WebDriverWait(pytest.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//tbody/tr/td[3]')))

    for i in range(len(names)):
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''


def test_unique_pets():
    """Тест проверяет что в списке нет повторяющихся питомцев"""

    pets_list = []
    pets = WebDriverWait(pytest.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//tbody/tr')))
    for i in pets:
        pets_list.append(i.text)

    assert len(pets_list) == len(set(pets_list))
