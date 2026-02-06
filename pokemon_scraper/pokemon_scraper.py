import requests
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_pokedex_info(curr_entry_num):
    pokedex_table = list(soup.body.find("div", id=f"tab-basic-{curr_entry_num}").find_next("table").tbody)
    pokedex_table = list(filter(lambda x: x != "\n", pokedex_table))

    dex_number = pokedex_table[0].td.strong.text
    height = pokedex_table[3].td.text
    weight = pokedex_table[4].td.text

    types = []
    for type_ in pokedex_table[1].td.find_all("a"):
        types.append(type_.text)

    abilities = []
    for ability in pokedex_table[5].td.find_all("a"):
        abilities.append(ability.text)

    return dex_number, types, height, weight, abilities

def scrape_stats():
    stats_table = soup.body.find("div", id="dex-stats").find_next("table")
    idv_stats_table = list(filter(lambda x: x != "\n", list(stats_table.tbody)))
    bst_stats_table = list(filter(lambda x: x != "\n", list(stats_table.tfoot)))

    hp = idv_stats_table[0].find("td", class_="cell-num").text
    attack = idv_stats_table[1].find("td", class_="cell-num").text
    defense = idv_stats_table[2].find("td", class_="cell-num").text
    sp_attack = idv_stats_table[3].find("td", class_="cell-num").text
    sp_defense = idv_stats_table[4].find("td", class_="cell-num").text
    speed = idv_stats_table[5].find("td", class_="cell-num").text
    bst = bst_stats_table[0].find("td", class_="cell-num cell-total").text
    
    return hp, attack, defense, sp_attack, sp_defense, speed, bst

def scrape_moves():
    moves = set()
    moves_table = list(soup.body.main.find_all("div", class_="sv-tabs-panel active")[1].find_all("h3"))
    
    for subtable_heading in moves_table:
        if (subtable_heading.find_next_siblings("div", limit=1) != []):
            move_subtable = subtable_heading.find_next("table").tbody
            for move in move_subtable:
                moves.add(move.find("a", class_="ent-name").text)

    return moves

if __name__ == "__main__":
    URL = "https://pokemondb.net/pokedex/bulbasaur"    
    driver = webdriver.Firefox()
    driver.get(URL)

    curr_entry_num = 1

    with open("pokemon_database.csv", "w", newline='') as csvfile:
        fieldnames = ["Name", "Pokedex Number", "Types", "Height", "Weight", "Abilities", "HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed", "BST", "Moves"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while(True):
            driver.find_element(By.LINK_TEXT, "Legends: Z-A").find_element(By.XPATH, "./following-sibling::*[1]").click()
            page = driver.page_source
            soup = BeautifulSoup(page, "html.parser")

            pokemon = soup.body.h1.text
            dex_number, types, height, weight, abilities = scrape_pokedex_info(curr_entry_num)
            hp, attack, defense, sp_attack, sp_defense, speed, bst = scrape_stats()
            moves = scrape_moves()

            pokemon_entry = { "Name" : pokemon,
                            "Pokedex Number" : dex_number,
                            "Types" : types,
                            "Height" : height, 
                            "Weight" : weight, 
                            "Abilities" : abilities, 
                            "HP" : hp,
                            "Attack" : attack, 
                            "Defense" : defense,
                            "Sp. Attack" : sp_attack,
                            "Sp. Defense" : sp_defense,
                            "Speed" : speed, 
                            "BST" : bst,
                            "Moves" : moves }
            writer.writerow(pokemon_entry)
            curr_entry_num = curr_entry_num + 1

            if (driver.find_elements(By.CLASS_NAME, "entity-nav-next") == []):
                print("DONE")
                break

            time.sleep(1)
            driver.find_element(By.CLASS_NAME, "entity-nav-next").click()
            