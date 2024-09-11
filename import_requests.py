import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time
import random

def buscar_artigos_google_scholar(termo_busca, num_paginas=2):
    base_url = "https://scholar.google.com/scholar"
    artigos = []

    for i in range(num_paginas):
        params = {
            "q": termo_busca,
            "start": i * 10
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.select('.gs_r.gs_or.gs_scl'):
                titulo = item.select_one('.gs_rt a')
                autores = item.select_one('.gs_a')
                link = item.select_one('.gs_rt a')['href'] if item.select_one('.gs_rt a') else None
                
                if titulo and autores:
                    artigos.append({
                        "titulo": titulo.text,
                        "autores": autores.text,
                        "link": link
                    })
        
        time.sleep(random.uniform(5, 10))  # Pausa aleatória para evitar bloqueio

    return artigos

def buscar_artigos_sciencedirect(termo_busca, num_paginas=2):
    base_url = "https://www.sciencedirect.com/search"
    artigos = []

    for i in range(num_paginas):
        params = {
            "qs": termo_busca,
            "offset": i * 25
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.select('.result-item-content'):
                titulo = item.select_one('.result-list-title-link')
                autores = item.select_one('.author-list')
                link = urljoin(base_url, item.select_one('.result-list-title-link')['href']) if item.select_one('.result-list-title-link') else None
                
                if titulo and autores:
                    artigos.append({
                        "titulo": titulo.text.strip(),
                        "autores": autores.text.strip(),
                        "link": link
                    })
        
        time.sleep(random.uniform(5, 10))  # Pausa aleatória para evitar bloqueio

    return artigos

def salvar_resultados(artigos, nome_arquivo):
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["titulo", "autores", "link"])
        writer.writeheader()
        for artigo in artigos:
            writer.writerow(artigo)

def main():
    termo_busca = input("Digite o termo de busca: ")
    num_paginas = int(input("Digite o número de páginas a serem buscadas em cada fonte: "))
    
    print(f"Buscando artigos para: '{termo_busca}'")
    
    artigos_google = buscar_artigos_google_scholar(termo_busca, num_paginas)
    artigos_sciencedirect = buscar_artigos_sciencedirect(termo_busca, num_paginas)
    
    todos_artigos = artigos_google + artigos_sciencedirect
    
    salvar_resultados(todos_artigos, 'resultados_busca_automatizada.csv')
    
    print(f"Busca concluída. {len(todos_artigos)} artigos encontrados e salvos em 'resultados_busca_automatizada.csv'")

if __name__ == "__main__":
    main()