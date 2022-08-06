from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

# GUI Imports
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

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

# Creates GUI window using PyQt5 (Source used: https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QApplication.html)
def create_window(qualifying_offer, player_list):
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Qualifying Offer Calculator')
    window.setFixedSize(QSize(500, 500))
    window.setStyleSheet("background-color: blue")
    layout = QGridLayout()
    qualifying_offer_btn = QPushButton('Show Qualifying Offer Calculation')
    qualifying_offer_btn.setStyleSheet("background-color: white")
    qualifying_offer_msg = QLabel('')
    qualifying_offer_msg.setStyleSheet("background-color: white")

    # Helper function to show qualifying offer when button is pressed
    def show_qualifying_offer():
        qualifying_offer_msg.setText("$%.0f" % qualifying_offer)

    qualifying_offer_btn.clicked.connect(show_qualifying_offer)

    player_list_btn = QPushButton('Show Top 10 Highest Salaries of %s' % player_list[0][2])
    player_list_btn.setStyleSheet("background-color: white")
    player_list_msg = QLabel('')
    player_list_msg.setStyleSheet("background-color: white")

    # Helper function to show players with highest salaries when button is pressed
    def show_highest_salaries():
        player_list_msg.setText("".join("%s: $%s\n" % (player[0], player[1]) for player in player_list[:10]))

    player_list_btn.clicked.connect(show_highest_salaries)

    total_salary_btn = QPushButton('Show Total Salary of Top 125 Paid Players')
    total_salary_btn.setStyleSheet("background-color: white")
    total_salary_msg = QLabel('')
    total_salary_msg.setStyleSheet("background-color: white")

    # Helper function to show total salary when button is pressed
    def show_total_salaries():
        total_salary_msg.setText("$%.0f" % sum(int(value[1]) for value in player_list))

    total_salary_btn.clicked.connect(show_total_salaries)


    layout.addWidget(qualifying_offer_btn, 0, 0)
    layout.addWidget(qualifying_offer_msg, 0, 100)
    layout.addWidget(player_list_btn, 50, 0)
    layout.addWidget(player_list_msg, 50, 100)
    layout.addWidget(total_salary_btn, 100, 0)
    layout.addWidget(total_salary_msg, 100, 100)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())


def main():
    player_list = get_player_list()
    clean_data(player_list)
    sorted_player_list = sorted(player_list, key= lambda player: int(player[1]), reverse= True)[:125]
    qualifying_offer = sum(int(value[1]) for value in sorted_player_list) / 125
    create_window(qualifying_offer, sorted_player_list)

if __name__ == "__main__":
    main()