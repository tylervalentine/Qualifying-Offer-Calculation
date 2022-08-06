from bs4 import BeautifulSoup
from urllib.request import urlopen
import pprint
import tkinter as tk

def get_player_list():
    data = urlopen("https://questionnaire-148920.appspot.com/swe/data.html")
    html_data = BeautifulSoup(data, features='html.parser')
    text = [words.getText() for words in html_data.find_all('td')]
    player_list = []
    for i in range(0, len(text), 4):
        player = text[i: i+4]
        player_list.append(player)
    
    return player_list

def clean_data(player_list):
    for player in player_list:
        salary = player[1]
        if salary.isnumeric():
            continue
        elif salary == "no salary data" or len(salary) == 0:
            player[1] = 0
        else:
            player[1] = player[1].replace("$", "")
            player[1] = player[1].replace(",", "")
        split_name = player[0].split(",")
        player[0] = "%s %s" % (split_name[1].strip(), split_name[0].strip())


def main():
    player_list = get_player_list()
    clean_data(player_list)
    sorted_player_list = sorted(player_list, key= lambda player: int(player[1]), reverse= True)[:125]
    pprint.pprint(sorted_player_list)
    print(sum(int(value[1]) for value in sorted_player_list) / 125)

if __name__ == "__main__":
    main()