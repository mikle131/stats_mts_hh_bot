from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import telebot
from telebot import types
import requests
from selenium.webdriver.chrome.options import Options
import os

markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn1=types.KeyboardButton('Получить данные')
markup.add(btn1)

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

def get_vacancies_mts():
    driver.get("https://job.mts.ru/")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    driver.execute_script("window.scrollBy(0, 870)")
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "header__job-count")))
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "header__title")))
    sleep(2)
    counts = [int(i.text.split()[0]) for i in driver.find_elements(By.CLASS_NAME, "header__job-count")]
    elems = [i.text for i in driver.find_elements(By.CLASS_NAME, "header__title")]
    res = dict()
    for i in range(len(counts)):
        res[elems[i]] = counts[i]
    return res

def get_num_vacancies_hh():
    url = 'https://api.hh.ru/employers/3776'
    r = requests.get(url)
    e=r.json()
    return e['open_vacancies']


token = '7533477541:AAF6LkjA2iMgLeDgIQjf8OzRnFEJwIMhNnk'
bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет! Думаю, функционал понятен)", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == 'Получить данные':
        num_vacs_hh = str(get_num_vacancies_hh())
        data_mts = get_vacancies_mts()
        res_text_hh = f'Вакансий по hh: {num_vacs_hh}'
        bot.send_message(message.chat.id,res_text_hh, reply_markup=markup)
        res_text_mts = f'Вакансий по МТС: {sum(data_mts.values())}' + '\n\nСреди них:'
        for naming in data_mts:
            res_text_mts += f'\n{naming} - {data_mts[naming]} вакансий'
        bot.send_message(message.chat.id,res_text_mts, reply_markup=markup)


bot.polling()