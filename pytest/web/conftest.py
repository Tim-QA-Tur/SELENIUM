# импортируем модули и отдельные классы
import pytest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")  # фикстура будет работат в рамках тестовый функции (brauser)
def browser():

    """
    Basic fixture (базовая фикстура)
    """
    chrome_options = Options()
    chrome_options.add_argument("start-maximized") # открываем на полный экран
    chrome_options.add_argument("--disable-infobars") # отключаем инфо сообщения
    chrome_options.add_argument("--disable-extensions") # отключаем расширения
    chrome_options.add_argument("--disable-search-engine-choice-screen") # отключаем выбор движка для поиска
    # chrome_options.add_argument("--headless") # спец. режим "без браузера"
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver    # конструкция yield позволяет вернуть из фикстуры объект driver, чтобы использовать созданный объект драйвера в наших тестах
    driver.quit()   # инструкция позволяет закрыть браузер вне зависимости от того успешно или не успешно выполнился тест 

@pytest.fixture(scope="function")   # фикстура будет работат в рамках тестовый функции (knockout)
def knockout():
    """
    Knockout all pokemons (отправить в накаут всех живых покемонов)
    """
    header = {'Content-Type':'application/json','trainer_token': 'введите свой токен'}
    pokemons = requests.get(url='https://api.pokemonbattle-stage.ru/v2/pokemons', params={"trainer_id": введите свой ID тренера},
                            headers=header, timeout=3)
    if 'data' in pokemons.json():
        for pokemon in pokemons.json()['data']:
            if pokemon['status'] != 0:
                requests.post(url='https://api.pokemonbattle-stage.ru/v2/pokemons/knockout', headers=header,
                              json={"pokemon_id": pokemon['id']}, timeout=3)


