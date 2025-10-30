import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

email = "alexv9999@mail.ru"
password = "qwaszx1"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get('https://petfriends.skillfactory.ru/login')
    #driver.maximize_window()
    driver.implicitly_wait(10) #Для работы с карточками животных

    yield driver

    driver.quit()


def test_mypets(driver):
    # Вводим емайл и пароль для входа на сайт
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass').send_keys(password)
    btn_entr = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    btn_entr.click()

    # Проверяем, что попали на главную страницу
    assert driver.find_element(By.TAG_NAME,'h1').text == "PetFriends"

    # Переходим на страницу Мои питомцы
    driver.find_element(By.CLASS_NAME, "navbar-toggler-icon").click()
    driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # Проверяем что попали на страницу "Мои питомцы"
    assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    #Находим инфо о количестве питомцев.
    my_data = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='.col-sm-4 left']")))
    my_text = my_data.text.split('\n')
    count_pets = int(my_text[1].split(' ')[1])
    print(f"На странице {count_pets} питомцев")

    # Находим инфо о питомцах. Так же используем неявные ожидания из фикстуры.
    images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    types = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    # Проверяем количество питоцев
    assert count_pets == len(images), f"Количество питомцев не совпадает с количеством карточек с инфо"
    print("№1 - Количество питомцев совпадает с количеством карточек")

    #pets_info = []
    pets_names = set()
    pets_images = 0

    for i in range(len(names)):
        #Проверяем, что у всех питомцев есть имя, возраст и вид
        assert names[i].text != '', f"Нет имени!"
        assert types[i].text != '', f"Нет вида животного!"
        assert ages[i].text != '', f"Нет возраста!"

        src = images[i].get_attribute('src')
        if src != '' and src != None:
            pets_images += 1

        pets_names.add(names[i])

    print("№3 - У всех питомцев есть имя, возраст и порода")

    # Проверяем, что хотя бы у половины питомцев есть фото
    assert pets_images >= count_pets / 2, f"Меньше половины питомцев с фото!"
    print("№2 - Более половины питомцев имеет фото")

    # Проверяем, что у всех питомцев разные имена
    assert len(names) == len(pets_names), f"Есть неуникальные имена!"
    print("№4 - У всех питомцев разные имена")

    # Создаем список и множество всех питомцев
    all_pets = list(zip(names, types, ages))
    unique_pets = set(all_pets)

    #Проверяем, что в списке нет повторяющихся питомцев
    assert len(unique_pets) == len(all_pets), f"Есть неуникальные питомцы!"
    print("№5 - В списке нет повторяющихся питомцев")
