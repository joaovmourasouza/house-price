from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from lib.operations.browser import load
import time

def links(links):
    list_intermediary_dataset = list()
    counter = 0
    for link in links:
        navegador = load()
        intermediary_dataset = dict()
        navegador.get(link)
        time.sleep(5)

        def find_element_safe(xpath):
            try:
                element = navegador.find_element(By.XPATH, xpath).text
                return element
            except NoSuchElementException:
                return 'Sem informacao'

        intermediary_dataset['titulo'] = find_element_safe('//*[@id="description-title"]/div/span')
        intermediary_dataset['descricao'] = find_element_safe('//*[@id="description-title"]/div/div/div/span/span')
        intermediary_dataset['preco'] = find_element_safe('//*[@id="price-box-container"]/div[1]/div[1]/span')
        intermediary_dataset['area util por m²'] = find_element_safe('//*[@id="details"]/div/div/div[1]/div[2]/span[2]')
        intermediary_dataset['quartos'] = find_element_safe('//*[@id="details"]/div/div/div[2]/div[2]/a')
        intermediary_dataset['banheiros'] = find_element_safe('//*[@id="details"]/div/div/div[3]/div[2]/span[2]')
        intermediary_dataset['vagas garagem'] = find_element_safe('//*[@id="details"]/div/div/div[4]/div[2]/span[2]')
        intermediary_dataset['rua/avenida'] = find_element_safe('//*[@id="location"]/div/div[1]/div/div/div/span[1]')
        intermediary_dataset['bairro e cep'] = find_element_safe('//*[@id="location"]/div/div[1]/div/div/div/span[2]')
        intermediary_dataset['caracteristica do imovel'] = find_element_safe('//*[@id="adview"]/div[3]/div/div[3]/div[2]/div[4]/div/div[1]/div')
        intermediary_dataset['caracteristica do condominio'] = find_element_safe('//*[@id="adview"]/div[3]/div/div[3]/div[2]/div[5]/div/div[1]/div')
        intermediary_dataset['custo condominio'] = find_element_safe('//*[@id="price-box-container"]/div[1]/div[3]/div/span[2]')
        intermediary_dataset['iptu'] = find_element_safe('//*[@id="price-box-container"]/div[1]/div[4]/div/span[2]')
        navegador.quit()
        print(intermediary_dataset)
        list_intermediary_dataset.append(intermediary_dataset)
        counter += 1
        print(f'Total: {counter} / {len(links)}')
    return list_intermediary_dataset