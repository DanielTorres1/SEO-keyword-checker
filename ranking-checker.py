#!/usr/bin/python3
import requests
import time
import argparse
import itertools
import sys
import urllib3
from urllib.parse import urlparse
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def google_search(query, api_keys, cxs, num_results=50, proxy=None, country="us", target_domain=None):
    """
    Realiza una búsqueda en Google Custom Search con rotación de API keys y soporte para país.
    Devuelve:
      - results (lista de diccionarios con título, link, posición)
      - position (posición del dominio si se encontró)
      - found_link (URL exacta si se encontró)
    """
    results = []
    url = 'https://www.googleapis.com/customsearch/v1'
    proxies = None

    if proxy:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

    key_cycle = itertools.cycle(zip(api_keys, cxs))
    position = None
    found_link = None

    for start in range(1, num_results + 1, 10):
        params = {
            'q': query,
            'start': start,
            'num': min(10, num_results - len(results)),
            'gl': country
        }

        success = False
        for attempt in range(len(api_keys)):
            api_key, cx = next(key_cycle)
            params['key'] = api_key
            params['cx'] = cx

            try:
                response = requests.get(url, params=params, proxies=proxies, timeout=10, verify=False)
                if response.status_code == 429:
                    print(f"⚠️  API Key {api_key} superó la cuota. Probando con otra...")
                    continue
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                print(f"❌ Error con {api_key}: {e}")
                continue

            if 'items' not in data:
                print(f"⚠️  Sin resultados o límite alcanzado con {api_key}.")
                continue

            for item in data['items']:
                link = item.get('link')
                position_actual = len(results) + 1
                results.append({
                    'title': item.get('title'),
                    'link': link,
                    'snippet': item.get('snippet'),
                    'position': position_actual
                })

                # ✅ Si encontramos el dominio, detener búsqueda inmediatamente
                if target_domain and target_domain.lower() in urlparse(link).netloc.lower():
                    position = position_actual
                    found_link = link
                    return results, position, found_link

            success = True
            break

        if not success:
            print("❌ Todas las API Keys fallaron.")
            break

        if len(results) >= num_results:
            break

        time.sleep(1)

    return results, position, found_link


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Checker: Verifica posición de dominio para keyword")
    parser.add_argument("--keyword", required=True, help="Palabra clave a buscar")
    parser.add_argument("--domain", required=True, help="Dominio objetivo (ej. imgur.com)")
    parser.add_argument("--country", default="us", help="Código de país (ej. us, mx, es)")
    parser.add_argument("--results", type=int, default=50, help="Número máximo de resultados a analizar (default: 50)")
    parser.add_argument("--proxy", help="Proxy opcional (ej. 127.0.0.1:8080)")

    args = parser.parse_args()

    keyword = args.keyword
    target_domain = args.domain
    country = args.country
    num_results = args.results
    proxy = args.proxy

    # 👉 Coloca aquí tus API Keys y CXS
    API_KEYS = [
        "AIzaSyD5uGhuQcFKDmWrVxTd5adUL3Xa6KIYqw0",
        "AIzaSyDY8uvgY59ZoZTknVbh8Sqw_RbvlaDBnOc",
        "AIzaSyDxcbpKRVue4biZlSgA0oqa2CAyjQjrudw",
        "AIzaSyDxZIEPe_pB49C6dbq9ZIENo2C9TZs9NcU",
        "AIzaSyDuzj4_7O9w22ME33s6nnTJvTHcImXv0w8"
    ]

    CXS = [
        "e157b66a291a844fd",
        "d20e90506037b4d59",
        "4268457f6e67d4c87",
        "97fcb125ed28a4c96",
        "e784b0d25d47e438f"
    ]

    if len(API_KEYS) != len(CXS):
        print("❌ Error: la cantidad de API_KEYS y CXS debe coincidir.")
        sys.exit(1)

    print(f"🔎 Buscando '{keyword}' en {country.upper()}...")

    search_results, position, found_link = google_search(
        keyword, API_KEYS, CXS,
        num_results=num_results,
        proxy=proxy,
        country=country,
        target_domain=target_domain
    )

    if position:
        print(f"\n✅ {target_domain} encontrado en la posición #{position}")
        print(f"🔗 {found_link}")
    else:
        print(f"\n❌ {target_domain} no se encontró en los primeros {num_results} resultados.")

    # 📝 Guardar resultados en formato: date|url|position
    output_file = f"seo_results_{keyword.replace(' ', '_')}_{country}.txt"
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    with open(output_file, "a") as f:
        for r in search_results:
            f.write(f"{fecha_hoy}|{r['link']}|{r['position']}\n")

    print(f"📄 Resultados guardados en {output_file}")
