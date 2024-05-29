from datetime import datetime

import requests
from bs4 import BeautifulSoup
from .models import *

class CurrencyParser:
    @staticmethod
    def parse_countries():
        url = "https://www.iban.ru/currency-codes"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table", class_="table")
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")
            code = cells[0].text.strip()
            name = cells[1].text.strip()
            currency = cells[2].text.strip()
            country, created = Country.objects.get_or_create(
                code=code, defaults={"name": name, "currency": currency}
            )
            if created:
                country.save()

    @staticmethod
    def parse_rates(start_date, end_date, currency_code):
        currency = {"USD": 52148, "EUR": 52170, "GBP": 52146, "JPY": 52246, "TRY": 52158, "INR": 52238,
                    "CNY": 52207}
        cur = currency_code
        # за точку отсчёта взято 01.09.2010
        param = Parameter.objects.first()
        base_date = param.date
        base_url = f"https://www.finmarket.ru/currency/rates/?id=10148&pv=1&cur={currency.get(cur)}&bd={base_date.day}&bm={base_date.month}&by={base_date.year}&ed={base_date.day}&em={base_date.month}&ey={base_date.year}&x=48&y=13#archive"
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="karramba")
        base_row = table.find_all("tr")[2]
        base_cells = base_row.find_all("td")
        base_rate = float(base_cells[2].text.replace(",", "."))
        print(base_rate,' RATE ', cur)
        url = f"https://www.finmarket.ru/currency/rates/?id=10148&pv=1&cur={currency.get(cur)}&bd={start_date.day}&bm={start_date.month}&by={start_date.year}&ed={end_date.day}&em={end_date.month}&ey={end_date.year}&x=48&y=13#archive"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="karramba")
        cells = table.find_all("tr")
        for cell in cells:
            row = cell.find_all("td")
            if row:
                newRow, created = CurrencyRate.objects.get_or_create(
                    code=cur,
                    date=datetime.strptime(row[0].text, "%d.%m.%Y").date(),
                    defaults={"rate": float(row[2].text.replace(",", "."))},
                )
                if created:
                    newRow.save()
                    print('TIME ',datetime.strptime(row[0].text, "%d.%m.%Y").date(), " TIME2 ", base_date.strftime("%d.%m.%Y"))
                    relative_change = (float(row[2].text.replace(",", "."))-base_rate) / base_rate * 100
                    print("RELATIVE ", relative_change, 'COUNTRY', cur)
                    newExchangeRate, created = ExchangeRate.objects.get_or_create(
                        date=datetime.strptime(row[0].text, "%d.%m.%Y").date(),
                        country=cur,
                        base_rate=base_rate,
                        rate=float(row[2].text.replace(",", ".")),
                        relative_change=relative_change,
                    )
                    if created:
                        newExchangeRate.save()

