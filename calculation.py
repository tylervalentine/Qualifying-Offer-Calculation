from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

# GUI Imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget

# class for data-related methods
class Data():

    # Gets player list from data URL, with each player having their own unique list within the final player list
    def get_player_list():
        data = urlopen("https://questionnaire-148920.appspot.com/swe/data.html")
        html_data = BeautifulSoup(data, features='html.parser')
        text = [words.getText() for words in html_data.find_all('td')]
        player_list = []
        for i in range(0, len(text), 4):
            player = text[i: i+4]
            player_list.append(player)
        
        return player_list

    # Cleans up data for each player, specifically formatting issues with salary values and reformats names
    def clean_data(player_list):
        for player in player_list:
            # Salary cleaning
            salary = player[1]
            if salary.isnumeric():
                continue
            elif salary == "no salary data" or len(salary) == 0:
                player[1] = 0
            else:
                player[1] = player[1].replace("$", "")
                player[1] = player[1].replace(",", "")
            # Name cleaning
            split_name = player[0].split(",")
            player[0] = "%s %s" % (split_name[1].strip(), split_name[0].strip())

# Class to create GUI window using PyQt5 (Source used: https://www.pythonguis.com/tutorials/creating-your-first-pyqt-window/)
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qualifying Offer Calculation")

        # Data variables
        player_list = Data.get_player_list()
        Data.clean_data(player_list)
        sorted_player_list = sorted(player_list, key= lambda player: int(player[1]), reverse= True)[:125]
        qualifying_offer = sum(int(value[1]) for value in sorted_player_list) / 125

        # Create a QHBoxLayout instance
        layout = QHBoxLayout()

        # Add widgets to the layout
        qualifying_offer_lbl = QLabel("Qualifying Offer Amount:\n\n $%s" % "{:,}".format(int(qualifying_offer)))
        qualifying_offer_lbl.setStyleSheet("background-color: blue; color: white;")
        top_paid_players_lbl = QLabel("Top 10 Highest Salaries of %s:\n\n" % sorted_player_list[0][2] + "%s".rstrip() % "".join("%s: $%s\n" % (player[0], "{:,}".format(int(player[1]))) for player in sorted_player_list[:10]))
        top_paid_players_lbl.setStyleSheet("background-color: blue; color: white;")
        total_salary_lbl = QLabel("Total Salary of Top 125 Paid Players:\n\n $%s" % "{:,}".format(sum(int(value[1]) for value in sorted_player_list)))
        total_salary_lbl.setStyleSheet("background-color: blue; color: white;")
        layout.addWidget(qualifying_offer_lbl)
        layout.addWidget(top_paid_players_lbl, 1)
        layout.addWidget(total_salary_lbl, 2)

        # Set the layout on the application's window
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())