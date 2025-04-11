import json
from bs4 import BeautifulSoup
from models import OpenedBuyOrder

FIELDS = ['pc_number', 'cod', 'dt_solicitation', 'dt_delivery', 'buy_order_value', 'supplier', 'description', 'status']

def extract_rows_from_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    if not table:
        raise ValueError("Nenhuma <table> encontrada no HTML.")

    rows = []
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        values = [td.get_text(strip=True) for td in tds]
        if values:
            rows.append(";".join(values))

    return rows

def parse_rows_to_models(rows, fields):
    models = []
    for row in rows:
        values = row.split(";", len(fields) - 1)
        if len(values) < len(fields):
            continue  # Ignora linhas incompletas

        data = dict(zip(fields, values))
        model = OpenedBuyOrder(**data)
        models.append(model.serialize())

    return models

def generate_json_from_html(html_content, json_output_path):
    rows = extract_rows_from_html_content(html_content)
    models = parse_rows_to_models(rows, FIELDS)

    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(models, json_file, indent=4, ensure_ascii=False)
