import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# записываем в переменные ссылки на страницу
base_url = 'https://ru.wikipedia.org/wiki/'
category_base = 'Категория:Животные_по_алфавиту'
first_page_url = f'{base_url}{category_base}'

# функции для парсинга данных
def fetch_animals_from_category(url):
    all_animals = []  # Соберем все названия животных сюда
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Сбор текущих животных на странице
        current_animals = extract_animals(soup)
        all_animals.extend(current_animals)
        
        # Попробуем найти следующую страницу
        next_link = find_next_page_link(soup)
        if next_link is None:
            break  # Если следующей страницы нет, заканчиваем сбор
        else:
            url = next_link  # Переходим на следующую страницу
    
    return all_animals

def extract_animals(soup):
    """Функция собирает все названия животных с текущей страницы"""
    animals = []
    links = soup.select('.mw-category-group ul li a')
    for link in links:
        title = link.get_text().strip()
        if title:  # Проверяем наличие текста
            animals.append(title)
    return animals

def find_next_page_link(soup):
    """Ищем ссылку на следующую страницу"""
    next_button = soup.find('div', class_='mw-category-generated').find('a', string='Следующая страница')
    if next_button:
        return base_url[:-5] + next_button['href']
    return None

animals = fetch_animals_from_category(first_page_url)

# обработка данных
def remove_english_words(lst):
    # Регулярное выражение для поиска английских символов
    pattern = re.compile(r'[a-zA-Z]')

    # Дополнительно удаляем элементы, который нахоидилсь в тех же классах и эллементах, что и нжные нам
    lst.remove("Знаменитые животные по алфавиту")
    lst.remove("Породы по алфавиту")
    
    # Список для хранения очищенных слов
    cleaned_list = []
    
    for word in lst:
        print(word)
        if not pattern.search(word):
            cleaned_list.append(word)
            
    return cleaned_list


animals = remove_english_words(animals)

def count_animals(data_animals):
    # Русский алфавит
    russian_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    # Создаем словарь
    count_of_animal = {letter: 0 for letter in russian_letters}

    # Обрабатываем каждый элемент списка
    for animal in data_animals:
        first_letter = animal[0].upper()
        
        # Если первый символ входит в русский алфавит, увеличиваем счётчик
        if first_letter in count_of_animal:
            count_of_animal[first_letter] += 1

    return count_of_animal

dict_animal = count_animals(animals)

# сохраняем данные 
# Преобразуем словарь в DataFrame
df = pd.DataFrame(list(dict_animal.items()), columns=['beasts', 'count'])
# Сохраняем в CSV файл
df.to_csv('task2/beasts.csv', index=False, encoding='utf-8', sep=';')