from django.http import JsonResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd

def home(request):
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")[1:]

    resumo = []

    for row in rows:

        cols = row.find_all('td')

        cotacao = cols[2].text.strip().replace('.', '').replace(',', '.')
        ffo_yield = cols[3].text.strip().replace('.', '').replace(',', '.').replace('%', '')
        dividend_yield = cols[4].text.strip().replace('.', '').replace(',', '.').replace('%', '')
        pvp = cols[5].text.strip().replace(',', '.')

        fundo = {
        "Papel": cols[0].text.strip(),
        "Segmento": cols[1].text.strip(),
        "Cotação": float(cotacao),
        "FFO Yield": float(ffo_yield),
        "Dividend Yield": float(dividend_yield),
        "P/VP": float(pvp),
        "ValorDeMercado": cols[6].text.strip(),
        "LiquidezDiária": cols[7].text.strip(),
        "QuantidadeImóveis": cols[8].text.strip(),
        "PreçoM2": cols[9].text.strip(),
        "AluguelM2": cols[10].text.strip(),
        "CapRate": cols[11].text.strip(),
        "VacanciaMedia": cols[12].text.strip()
    }
    resumo.append(fundo)

    dataset = pd.DataFrame(resumo)
    dataset_json = dataset.to_json(orient="records")
    #dataset_html = dataset.to_html(index=False)
    
    return JsonResponse(dataset_json, safe=False)
    #return render(request, 'filtro/dados.html', {'dataset': dataset.to_dict(orient='records')})
