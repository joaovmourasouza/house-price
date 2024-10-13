from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from lib.operations.browser import load
import json
import re
import os

def number_of_pages(base_url):
    navegador = load()
    navegador.get(base_url)
    WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
    itens_numbers = WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/div[2]/div/p'))).text
    itens_numbers = int(re.findall(r'\d+', itens_numbers)[-1])
    return -(-itens_numbers // 50)

def ajusting_links(initial_link, number_of_page):
    return f"{initial_link}?o={number_of_page+1}"

def check_if_links_already_exist():
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    full_path = os.path.join(base_path, 'output/links')
    if os.path.exists(full_path):
        if len(os.listdir(full_path)) > 0:
            file_to_load = sorted(os.listdir(full_path))[0]
            with open(os.path.join(full_path, file_to_load), 'r') as f:
                links_extracted_loaded = json.load(f)
            return links_extracted_loaded

def links():
    extract_and_filtered_links = list()
    previous_links = check_if_links_already_exist()
    base_url = "https://www.olx.com.br/imoveis/venda/apartamentos/estado-ba/sul-da-bahia/ilheus"
    qtd_of_pages = number_of_pages(base_url=base_url)
    
    for page in range(qtd_of_pages):
        navegador = load()
        link = ajusting_links(base_url, page)
        navegador.get(link)
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cookie-notice-ok-button"]'))).click()
        WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.ESCAPE)
        WebDriverWait(navegador, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-content"]/div[4]/div')))
        all_links = navegador.find_elements(By.XPATH, '//*[@id="main-content"]/div[4]/div')
        links_withdraw_ads = [i for i in range(1, len(all_links)) if i not in [6, 12, 23, 34, 45]]
        for ads in links_withdraw_ads:
            xpath_of_div = f'//*[@id="main-content"]/div[4]/div[{ads}]'
            scroll_to_div = navegador.find_element(By.XPATH, xpath_of_div)
            navegador.execute_script("arguments[0].scrollIntoView();", scroll_to_div)
            xpath_of_href = f'//*[@id="main-content"]/div[4]/div[{ads}]/section/a'
            link = navegador.find_element(By.XPATH, xpath_of_href).get_attribute('href') 
            if previous_links is not None and link is not None:
                if link not in previous_links:
                    extract_and_filtered_links.append(link)
            elif link is not None:
                extract_and_filtered_links.append(link)
    return extract_and_filtered_links