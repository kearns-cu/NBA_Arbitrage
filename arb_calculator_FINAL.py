# Import MySQL
import csv
from pydoc import Helper
import sys
import mysql.connector

# Define mydb Connection
mydb = mysql.connector.connect(user='root',
                               password='',
                               host='localhost',
                               database='sportsodds')
cursor = mydb.cursor()


def options():
    # Prompt the user to select an option
    print("Select an option:")
    print("1. View today's games")
    print("2. View today's odds")
    print("3. Create a new event")
    print("4. Create a new odds record")
    print("5. Delete an event")
    print("6. Update a game's odds")
    print("7. Export odds to csv file")
    print("8. Perform arbitrage calculation")
    print("9. Exit")

    option = input("Enter option: ")

    # Call the appropriate function based on the user's selection
    if option == "1":
        view_today_games()
    elif option == "2":
        view_today_odds()
    elif option == "3":
        create_game()
    elif option == "4":
        create_odds()
    elif option == "5":
        delete_game()
    elif option == "6":
        update_game_odds()
    elif option == "7":
        export_odds()
    elif option == "8":
        arbitrage_calculation()
    elif option == "9":
        exit()
    else:
        print("Invalid option. Please try again.")

# View today's odds


def view_today_odds():
    # select the odds from the odds table
    query = "SELECT * FROM odds"
    cursor.execute(query)
    # fetch the data
    odds = cursor.fetchall()
    # print the odds to the user
    print("Odds:")
    for odd in odds:
        print(f"{odd[3]}: {odd[6]} vs. {odd[7]}: {odd[4]} / {odd[5]}")


# convert odd from american to decimal with a parameter


def convert_odds(odd):

    # convert odd from string to decimal
    odd = float(odd)
  # if odd is positive
    if odd > 0:
        return 1 + (odd / 100)
# if odd is negative
    else:
        return 1 - (100 / (odd * -1))


def odds_comparison(odd1, odd2):

    # convert odds to decimal
    odd1 = convert_odds(odd1)

    odd2 = convert_odds(odd2)

    arb_value = (1.0/odd1) + (1.0/odd2)

    # if 1 / odd1 + 1/ odd2 < 1
    if (arb_value < 1):
        return 1 - arb_value
    else:
        return 0


def arbitrage_calculation():

    # start transaction
    mydb.start_transaction()
    # select all the odds
    # enter a event name
    event_name = input("Enter event name: ")
    # select the odds for that event
    query = "SELECT * FROM odds WHERE event_name = %s"
    cursor.execute(query, (event_name,))
    odds = cursor.fetchall()

    odd1_list = []
    odd2_list = []
    for odd in odds:
        odd1_list.append(odd[4])
        odd2_list.append(odd[5])

    query = "CREATE TABLE IF NOT EXISTS arbitrage(odd1 INT, odd2 INT, arb_value DECIMAL(10, 2))"
    cursor.execute(query)

    # loop through the odds
    for odd1 in odd1_list:
        for odd2 in odd2_list:
            # if odd1 and odd2 are not the same
            if odd1 != odd2:
                # calculate the arbitrage value

                arb_value = odds_comparison(odd1, odd2)
                print(arb_value)

                # if arbitrage value is greater than 0
                if arb_value > 0:
                    query = "CREATE TABLE IF NOT EXISTS arbitrage(odd1 INT, odd2 INT, arb_value DECIMAL(10, 2))"
                    cursor.execute(query)
                    # insert arbitrage value into arbitrage table
                    query = "INSERT arbitrage(odd1, odd2, arb_value) VALUES (%s, %s, %s)"
                    # conver odd1 and odd2 to int
                    odd1 = int(odd1)
                    odd2 = int(odd2)
                    cursor.execute(query, (odd1, odd2, arb_value))

    # print the arbitrage table
    query = "SELECT * FROM arbitrage"
    cursor.execute(query)
    arbitrage = cursor.fetchall()
    print(event_name + " Arbitrage:")
    for arb in arbitrage:
        print(arb[0], arb[1], arb[2])

    # end transaction
    mydb.commit()


def create_game():

    # ask user to enter game
    event_name = input("Enter event name: ")
    team1 = input("Enter team 1: ")
    team2 = input("Enter team 2: ")
    status = input("Enter status: ")
    # query to create game
    query = "INSERT INTO games(event_name, status, team1, team2) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (event_name, status, team1, team2))
    mydb.commit()

# Create a new odds record using user input


def create_odds():

    # ask user to enter odds
    event_name = input("Enter event name: ")
    bookie = input("Enter bookie: ")
    odd1 = input("Enter odd 1: ")
    odd2 = input("Enter odd 2: ")
    team1 = input("Enter team 1: ")
    team2 = input("Enter team 2: ")
    # query to create odds
    query = "INSERT INTO odds(event_name, bookie, odd1, odd2, team1, team2) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (event_name, bookie, odd1, odd2, team1, team2))
    mydb.commit()

# delete record from games and odds table


def delete_game():
    # ask user to enter game

    event_name = input("Enter event name: ")
    # performed soft delete join to remove the event from games table, odds table, and outcomes table
    query = "DELETE games, odds, outcomes FROM games INNER JOIN odds ON games.event_name = odds.event_name INNER JOIN outcomes ON games.event_name = outcomes.event_name WHERE games.event_name = %s"
    cursor.execute(query, (event_name,))
    mydb.commit()

# Update a games odds using user input


def update_game_odds():
    # ask user to enter game
    event_name = input("Enter event name: ")
    odd1 = input("Enter original odds1: ")
    odd2 = input("Enter original odds2: ")
    newOdd1 = input("Enter new odds1: ")
    newOdd2 = input("Enter new odds2: ")
    # query to update odds
    query = "UPDATE odds SET odd1 = %s, odd2 = %s WHERE event_name = %s AND odd1 = %s AND odd2 = %s"
    cursor.execute(query, (newOdd1, newOdd2, event_name, odd1, odd2))
    mydb.commit()


# Export odds to csv file
def export_odds():
    # ask user to enter bookie

    bookie = input("Enter bookie: ")
    fileName = input("Enter file name ending in .csv: ")
    # query to export odds
    query = "SELECT * FROM odds WHERE bookie = %s"
    cursor.execute(query, (bookie,))
    odds = cursor.fetchall()
    # create a new csv file
    with open(fileName, 'w') as file:
        writer = csv.writer(file)
        for odd in odds:
            writer.writerow(odd)

    print("Exported odds to " + fileName)


# Create views for each games and its odds
def view_today_games():
    # Create a view to group odds by event

    query = "CREATE OR REPLACE VIEW group_odds AS SELECT team1, team2 FROM odds GROUP BY event_name"
    cursor.execute(query)
    mydb.commit()

    # print "group_odds
    query = "SELECT * FROM group_odds"
    cursor.execute(query)
    group_odds = cursor.fetchall()
    v = " v "
    print("Games Today:")
    for group_odd in group_odds:
        print(group_odd[0], v, group_odd[1])


def exit():
    print("Exiting program...")
    sys.exit()


while True:
    options()


# Close mydb Connection
mydb.close()
