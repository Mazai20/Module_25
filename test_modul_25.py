import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email,valid_password

# driver = webdriver.Firefox()
# driver.get("http://somedomain/url_that_delays_loading")
# element = WebDriverWait(driver, 10).until(
# EC.presence_of_element_located((By.ID, "myDynamicElement")))


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome("C:/dr/chromedriver.exe")
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # входим в мои питомцы
    pytest.driver.find_element_by_xpath('//a[text()="Мои питомцы"]').click()


def test_checking():
    #Вводим emaill
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # входим в мои питомцы
    pytest.driver.find_element_by_xpath('//a[text()="Мои питомцы"]').click()
    # ждем безусловно 2 секунды для прогрузки страницы "Мои питомцы"
    pytest.driver.implicitly_wait(2)
    # pytest.driver.get("https://petfriends.skillfactory.ru/my_pets")
    # Ищем имена, фото и описания питомцев на странице

    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')

    # проверяем, что все поля не пустые:

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''  # на странице нет питомцев без фото
        assert names[i].text != ''  # на странице нет питомцев без Имени
        assert descriptions[i].text != ''  # на странице нет питомцев с пустым полем для указания Породы и возраста
        assert ', ' in descriptions[i]  # проверяем, что между породой и лет есть запятая (значит есть оба значения)
        parts = descriptions[i].text.split(", ")  # Создаём список, где разделитель значений - запятая
        assert len(parts[0]) > 0  # Проверяем, что длина текста в первой части списка и
        assert len(parts[1]) > 0  # ...и во второй > 0, значит там что-то да указано! Если нет -> FAILED!


def test_number_of_pets_ok():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # входим в мои питомцы
    pytest.driver.find_element_by_xpath('//a[text()="Мои питомцы"]').click()

    # ждем безусловно 2 секунды,чтобы страница прогрузилась
    pytest.driver.implicitly_wait(2)
    # ищем количество питомцев на странице
    number_of_pets = pytest.driver.find_elements_by_xpath('//th[@scope="row"]')
    # ищем количество питомцев в тексте профиля пользователя
    statistic_user = pytest.driver.find_elements_by_xpath('//div[@class=".col-sm-4 left"]')
    for item in statistic_user:
        statistic = item.text  # получаем текст из класса .col-sm-4 left"
        # проверяем, что количества совпали
        assert str(len(number_of_pets)) in statistic


def test_more_pets_with_photo():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # входим в мои питомцы
    pytest.driver.find_element_by_xpath('//a[text()="Мои питомцы"]').click()
    # ждем с условием что на странице прогрузились атрибуты питомцев (имена,типы,возраст)
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div#all_my_pets > table > tbody > tr > th")))
    # ищем количество питомцев на странице
    number_of_pets = pytest.driver.find_elements_by_xpath('//th[@scope="row"]')
    # ищем количество фото питомцев на странице через количество питомцев без фото
    number_of_pets_without_photoes = pytest.driver.find_elements_by_xpath('//img[@src=""]')
    number_of_pets_with_photoes = len(number_of_pets) - len(number_of_pets_without_photoes)
    # проверка что количество питомцев с фото хотя бы в 2 раза больше общего кол-ва питомцев
    assert int(len(number_of_pets)) <= (number_of_pets_with_photoes) * 2


def test_all_pets_has_name_age_type():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # входим в мои питомцы
    pytest.driver.find_element_by_xpath('//a[text()="Мои питомцы"]').click()
    # ждем с условием что на странице прогрузились атрибуты питомцев (имена,типы,возраст)
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[1]/tbody[1]/tr[1]/td[1]")))
    # ищем атрибуты питомцев
    attribute_of_pets = pytest.driver.find_elements_by_xpath('//tr/td')
    # проверка что атрибуты заполнены
    assert attribute_of_pets != ''


def test_all_pets_has_different_name():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # входим в мои питомцы
    pytest.driver.find_element_by_xpath('//a[text()="Мои питомцы"]').click()
    # ждем с условием что на странице прогрузились атрибуты питомцев (имена,типы,возраст)
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td")))
    # ищем имена питомцев
    names_of_pets = pytest.driver.find_elements_by_css_selector('td:nth-child(2)')
    # # создаем множество без повторов имен
    unique_names_of_pets = set(names_of_pets)
    # сравниваем длину списка имен с и без повторов
    assert len(names_of_pets) == len(unique_names_of_pets)
