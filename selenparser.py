import traceback
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import warnings
import pandas as pd

url_from_bs = 'https://online.metro-cc.ru'
url_category = 'https://online.metro-cc.ru/category/bytovaya-himiya'

warnings.filterwarnings('ignore')

options = webdriver.ChromeOptions()
options.add_argument("--headless")
client = webdriver.Chrome(options=options)
client.implicitly_wait(10)
client.get(url_category)
wait = WebDriverWait(client, 10)

podcat_mass = client.find_elements(by=By.CLASS_NAME, value='catalog-heading-link')
result = []

url_category_mass = []
for p_url in podcat_mass[1:]:
    url_category_mass.append(p_url.get_attribute('href'))


for url in url_category_mass:
    count = 1

    while True:
        try:
            client.get(url + '?page=' + str(count))
            elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'simple-button')))
            podcat_souper = BeautifulSoup(client.page_source, 'html.parser')
            product_mass = podcat_souper.find_all('div', class_='catalog-2-level-product-card')

            for product in product_mass:
                product_id = product.get('data-sku')
                link = url_from_bs + product.find('a', class_='product-card-photo__link').get('href')
                client.get(link)
                try:
                    elem = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'product-price__sum-rubles')))
                except TimeoutException:
                    continue

                product_souper = BeautifulSoup(client.page_source, 'html.parser')
                name = product_souper.find('h1', class_='product-page-content__product-name').text.replace('\n',
                                                                                                           '').strip()
                try:
                    prices = product_souper.find('div', class_='product-unit-prices__trigger').find_all('span', class_='product-price__sum')
                    if len(prices) > 1:
                        promo_price = prices[0].find('span', class_='product-price__sum-rubles').text
                        try:
                            promo_price += prices[0].find('span', class_='product-price__sum-penny').text
                        except:
                            pass
                        regular_price = prices[1].find('span', class_='product-price__sum-rubles').text
                        try:
                            regular_price += prices[1].find('span', class_='product-price__sum-penny').text
                        except:
                            pass
                    else:
                        regular_price = prices[0].find('span', class_='product-price__sum-rubles').text
                        promo_price = None
                        try:
                            regular_price += prices[0].find('span', class_='product-price__sum-penny').text
                        except:
                            pass
                except:
                    continue

                atribute_list = product_souper.find('ul', class_='product-attributes__list')
                brand = None
                for attr in atribute_list:
                    if attr.find('span', class_='product-attributes__list-item-name-text').text.lower().strip().replace('\n','') == 'бренд':
                        brand = attr.find('a').text.strip().replace('\n','')


                result.append({'id товара':product_id, 'наименование':name, 'ссылка на товар':link, 'регулярная цена':regular_price, 'промо цена':promo_price, 'бренд':brand})
            count += 1

        except TimeoutException:
            if client.find_element(by=By.CLASS_NAME, value='empty-page__desc').text == 'Мы ничего не нашли по выбранным параметрам':
                break
            else:
                continue
        except:
            traceback.print_exception()
            continue

pd.DataFrame(result).to_excel('test.xlsx')