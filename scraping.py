import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from urllib.parse import urljoin
from model import Model_MenuNav

def scraping_ufu(db: Session):
    url = "https://www.ufu.br"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")

    menus = []
    
    nav_items = soup.select("nav#block-ufu-rodape-2 ul.nav.navbar-nav li.nav-item a.nav-link")
    
    for link in nav_items:
        texto = link.get_text(strip=True)
        href = link.get("href")
        
        if texto and href:
            href = urljoin(url, href)  # Converte links relativos para absolutos
            menus.append({'texto': texto, 'link': href})  # Armazena os dados

    # Exibindo os menus coletados no console
    print("Menus coletados:", menus)

    # Salva os menus no banco de dados
    for menu in menus:
        db.add(Model_MenuNav(menuNav=menu['texto'], link=menu['link']))
    
    db.commit()
    return menus
