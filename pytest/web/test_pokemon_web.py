# импортируем модули и отдельные классы
import pytest
import requests

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Locators:
    """
    Class for locators  # Локаторы  объявим как статические переменные на уровне класса. Это удобно, если локатор используется в нескольких местах класса.
    """
    EMAIL = '[class*="k_form_control"] [id="k_email"]'
    PASSWORD = '[class*="k_form_control"] [id="k_password"]'
    LOGIN = '[class*="k_form_send_auth"]'
    TRAINER_ID = '[class="header_card_trainer_id_num"]'
    ALERT = '[class*="auth__error"]'
    POK_TOTAL_COUNT = '[class*="pokemons"] [class*="total-count"]'

URL = 'https://pokemonbattle-stage.ru/' # сайт который тестируем
    
    # каждый тест должен начинаться с test_
def test_positive_login_stage(browser):
    """
    TRP-1. Positive cases  # позитивный тест 
    """
    # определяем адрес страницы для теста и переходим на неё
    browser.get(URL)
    
    # assert True, ''  для того чтобы поставить breakpoind
    
    # ищем по селектору инпут "Email", кликаем по нему и вводим значение email
    email_input = WebDriverWait(browser, timeout=10,poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, Locators.EMAIL)))
    email_input.click()
    email_input.send_keys('USER EMAIL')
    # email.send_keys(user@mail.ru') # введи тут email своего тестового аккаунта на stage окружении

	# ищем по селектору инпут "Password", кликаем по нему и вводим значение пароля
    password = browser.find_element(by=By.CSS_SELECTOR, value=Locators.PASSWORD)
    password.click()
    password.send_keys('USER PASSWORD') # введи тут пароль своего тестового аккаунта на stage окружении

	# ищем по селектору кнопку "Войти" и кликаем по ней
    enter = browser.find_element(by=By.CSS_SELECTOR, value=Locators.LOGIN)
    enter.click()

    # ждем успешного входа и обновления страницы
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.url_to_be('URL'))

	# ищем элемент на странице, который содержит ID тренера
    trainer_id = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Locators.TRAINER_ID)))

	# сравниваем полученный ID из кода теста с ID вашего тестового тренера
    assert int(trainer_id.text) == введите ID тренера, 'Unexpected ID trainer'
    
    # Чтобы каждый раз не писать код для новых тестов, можно переиспользовать, изменить существуюший. Для этого создаем новый файл conftest.py.
    # Conftest.py создадим Fixtura для настройки и запуска браузера. Это вспомогательная функция, ее можно вызвать из любого теста
    
    # Создаем переменные CASES, список кортежей для негативной проверки
CASES = [
    ('1', 'USER EMAIL.INVALID', 'USER PASSWORD.VALID', ('Введите корректную почту')),   # сообшение, которое видим при ввода Логин без @, правильный пароль,
    ('2', 'USER EMAIL.VALID', 'USER PASSWORD.INVALID', ('Неверные логин или пароль')),  # Правильный логин, НЕправильный пароль,
    ('3', 'USER EMAIL.INVALID', 'USER PASSWORD.VALID', ('Введите корректную почту')),     # Логин без домена, правильный пароль,
    ('4', '', 'USER PASSWORD.VALID', ('Введите почту')),                            # Поле логина пустое, правильный пароль,
    ('5', 'USER EMAIL.VALID', '', ('Введите пароль'))                                # Правильный логин, поле пароль пустое.
]

@pytest.mark.parametrize('case_number, email, password, exp_alert', CASES)  # описание параметризации
def test_negative_login_stage(case_number, email, password, exp_alert, browser):   # параметры тестовый функции
    """
    TRP-2. Negative cases (негативный тест, параметризованный)
    """
    logger.info(f'Negative case № {case_number}')  # уровень логирование показывающее насколько критичная инфор-я должна отображатся, в данном случае "info" информационная

    browser.get(URL)

    email_input = WebDriverWait(browser, timeout=20,poll_frequency=2).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, Locators.EMAIL)))
    email_input.click()
    email_input.send_keys(email)  # Здесь email должно содержать заведомо неправильное значение

    password_input = browser.find_element(by=By.CSS_SELECTOR, value=Locators.PASSWORD)
    password_input.click()
    password_input.send_keys(password)  # Аналогично, password должно содержать заведомо неправильное значение

    enter_button = browser.find_element(by=By.CSS_SELECTOR, value=Locators.LOGIN)
    enter_button.click()
    
   
    alert = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Locators.ALERT)))

    assert alert.text == exp_alert, 'Unexpected alert message'


   # Теперь создадим большой сквозной сценарий, который будет заключатся:
   # 1. Логинимся, переходим на странице тренера, создаем покемона с помощью API методов POST
   # а также отправить в накаут, чтобы создать нового покемона, и проверяем на вэб интерфейсе, 
   # что покемон созданный через API успешно добавлен. 
   # своего рода интеграция API методов и методов selenium

   # В новом тесте создадим фикстуру knockout (накаут) в conftest.py, так как есть лимит на создание покемона
def test_check_api(browser, knockout):
    """
    TPR-3. Check create pokemon by api request  (создание нового покемона через API метод)
    """
    browser.get(url=URL)

    email = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, Locators.EMAIL)))
    email.click()
    email.send_keys('USER EMAIL.VALID') # вводим валидную почту

    password = browser.find_element(by=By.CSS_SELECTOR, value=Locators.PASSWORD)
    password.click()
    password.send_keys('USER PASSWORD.VALID')  № вводим правильный пароль

    enter = browser.find_element(by=By.CSS_SELECTOR, value=Locators.LOGIN)
    enter.click()
    
    # Ожидание пока страница с покемонами загрузилась полностью
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
    
    # После загрузки страницы, кликает на ID чтобы переходить на страницу тренера
    trainer = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, Locators.TRAINER_ID)))
    trainer.click()
    
    # Ожидание пока страница тренера загрузилась полностью
    pok = WebDriverWait(browser, timeout=10, poll_frequency=2).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, '[class*="pokemon_one_body_content_inner_pokemons"]')))
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        lambda x: 'feature-empty' not in pok.get_attribute('class'))
    
    # После зарузки страницы, находим элемент Total_Count (Покемоны) и сохрянаем значение покемонов 
    # на тукущий момент перед добавлением через API и после добавления кол покемонов увеличился
    pokemon_count_before = browser.find_element(by=By.CSS_SELECTOR, value=Locators.POK_TOTAL_COUNT)
    count_before = int(pokemon_count_before.text)

    # определение body (тело) запроса, для создания нового покемона
    body_create = {
        "name": "Atos",  # придумайте имя для покемона или можно сгенерировать случайные значения для имени передав строку "generate"
        "photo_id": 68   # аватар для покемона от 1 до 1000 или можно сгенерировать случайное фото передав число -1
    }
    # Выполнения POST запроса на создания нового покемона (в хедер указываем токен тренера)
    header = {'Content-Type':'application/json','trainer_token': 'введите свой токен'}
    response_create = requests.post(url='https://api.pokemonbattle-stage.ru/v2/pokemons', headers=header, json=body_create, timeout=3)
    
    # В ответ ожидаем статус код 201 (Покемон успешно создан)
    assert response_create.status_code == 201, 'Unexpected response status_code'

    # после создание нового покемона нужно обновить страницу
    browser.refresh()

    # После добавления нового покемона кол-во покемонов увеличится на 1
    assert WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.text_to_be_present_in_element(

        (By.CSS_SELECTOR, Locators.POK_TOTAL_COUNT), f'{count_before+1}')), 'Unexpected pokemons count'


