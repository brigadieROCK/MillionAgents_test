# MillionAgents_test
Тестовое задание на вакансию "Младший специалист отдела разработки (Python) / Специалист по парсингу данных"
Написать парсер для сайта Метро (https://online.metro-cc.ru/)
Спарсить любую категорию, где более 100 товаров, для городов Москва и Санкт-Петербург и выгрузить в любой удобный формат(csv, json, xlsx). Важно, чтобы товары были в наличии.
Необходимые данные: 
  id товара из сайта/приложения, 
  наименование, 
  ссылка на товар, 
  регулярная цена, 
  промо цена, 
  бренд.

Парсер реализован на связке selenium и bs4, с выгрузкой данных в "test.xlsx". Собирает категорию "бытовая химия".
