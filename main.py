from requests_html import HTMLSession
from datetime import datetime
import json

urls = {
    "Brent": "https://www.cmegroup.com/CmeWS/mvc/Margins/OUTRIGHT?1=1&sortField=exchange&sortAsc=true&clearingCode=BZ&sector=CRUDE%20OIL&exchange=NYM&pageSize=12&pageNumber=1&isProtected&_t=1679410164098",
    "WTI": "https://www.cmegroup.com/CmeWS/mvc/Margins/OUTRIGHT?1=1&sortField=exchange&sortAsc=true&sector=CRUDE+OIL&exchange=NYM&pageSize=12&pageNumber=1&isProtected&_t=1679501494337",
    "USDRUB": "https://www.cmegroup.com/CmeWS/mvc/Margins/OUTRIGHT?1=1&sortField=exchange&sortAsc=true&clearingCode=RU&sector=FX&exchange=CME&pageSize=12&pageNumber=1&isProtected&_t=1679501646476",
    "E-mini_SP500": "https://www.cmegroup.com/CmeWS/mvc/Margins/OUTRIGHT?1=1&sortField=exchange&sortAsc=true&sector=EQUITY+INDEX&exchange=CME&pageSize=12&pageNumber=1&isProtected&_t=1679501890743",
    "Gold_GC": "https://www.cmegroup.com/CmeWS/mvc/Margins/OUTRIGHT?1=1&sortField=exchange&sortAsc=true&clearingCode=GC&sector=METALS&exchange=CMX&pageSize=12&pageNumber=1&isProtected&_t=1679501980732",
    "10-Year T-Note(ZN)": "https://www.cmegroup.com/CmeWS/mvc/Margins/OUTRIGHT?1=1&sortField=exchange&sortAsc=true&clearingCode=21&sector=INTEREST RATES&exchange=CBT&pageSize=12&pageNumber=1&isProtected&_t=1679502854425"}

tickets = ["Brent", "WTI", "USDRUB", "E-mini_SP500", "Gold_GC", "10-Year T-Note(ZN)"]


def get_margin_rate(url):
    # Create an HTML session
    session = HTMLSession()

    # Send a GET request to the website
    response = session.get(url)

    # Extract the content using bs4
    result_page = response.text

    # Parse the result as JSON
    data = json.loads(result_page)
    margin = data['marginRates'][0]['maintenanceRate']

    return margin


date = datetime.now().strftime("%d/%m/%Y_%H:%M")


def check_margin():
    for ticket in tickets:
        try:
            with open(f'files_margin/{ticket}.txt', 'r+') as file:
                lines = file.readlines()
                last_line = lines[-1]
                margin_now = get_margin_rate(urls[ticket])
                if last_line.split()[0] != margin_now.strip(" USD"):
                    file.write(f'{margin_now.strip(" USD")} {date}\n')  # запись всегда производится в конец файла
                    print(f'ВНИМАНИЕ! Маржа изменилась на {ticket}: {margin_now}')
                else:
                    print(f'Маржа не изменилась на {ticket}: {margin_now} (old: {last_line.strip()})')
        except:
            print('Ошибка при работе с файлом')


check_margin()
