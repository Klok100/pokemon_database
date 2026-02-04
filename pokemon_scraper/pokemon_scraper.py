import requests
from bs4 import BeautifulSoup

def scrape_pokedex_info():
    pokedex_table = list(soup.body.find("table", class_="vitals-table").tbody)
    dex_number = pokedex_table[1].td.strong.text

    types = []
    for type_ in pokedex_table[3].td.find_all("a"):
        types.append(type_.text)

    height = pokedex_table[7].td.text
    
    weight = pokedex_table[9].td.text

    abilities = []
    for ability in pokedex_table[11].td.find_all("a"):
        abilities.append(ability.text)

    return dex_number, types, height, weight, abilities

def scrape_stats():
    stats_table = list(soup.body.find_all("table", class_="vitals-table")[3].tbody)
    hp = stats_table[1].find("td", class_="cell-num").text
    attack = stats_table[3].find("td", class_="cell-num").text
    defense = stats_table[5].find("td", class_="cell-num").text
    sp_attack = stats_table[7].find("td", class_="cell-num").text
    sp_defense = stats_table[9].find("td", class_="cell-num").text
    speed = stats_table[11].find("td", class_="cell-num").text
    bst = list(soup.body.find_all("table", class_="vitals-table")[3].tfoot)[1].find("td", class_="cell-num cell-total").text
    
    return hp, attack, defense, sp_attack, sp_defense, speed, bst

def scrape_moves():
    moves = set()
    moves_table = soup.body.main.find("div", id="tab-moves-22")
    moves_level_up_table = moves_table.find_all("div", class_="grid-col span-lg-6")[0].find("table", class_="data-table").tbody
    moves_tm_table = moves_table.find_all("div", class_="grid-col span-lg-6")[1].find("table", class_="data-table").tbody

    for move in moves_level_up_table:
        moves.add(move.find("a", class_="ent-name").text)

    for move in moves_tm_table:
        moves.add(move.find("a", class_="ent-name").text)

    return moves

if __name__ == "__main__":
    URL = "https://pokemondb.net/pokedex/bulbasaur"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    pokemon = soup.body.h1.text
    dex_number, types, height, weight, abilities = scrape_pokedex_info()
    hp, attack, defense, sp_attack, sp_defense, speed, bst = scrape_stats()
    moves = scrape_moves()
    
    
