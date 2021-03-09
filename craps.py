""" This program is to play Craps, one of the games available at MHIO Casino """

import random
import time
import os
import json

class Gambler():
    '''These will represent the players and keep track of their balance'''

    def __init__(self, name, balance=1000):
        self.name = name
        self.balance = balance
        self.bet_amount = 0

    def show_stats(self):
        print("")
        print(f"Name: {self.name}")
        print(f"Balance: {self.balance} credits")
        print(f"Bet Amount: {self.bet_amount}")

    def change_name(self, new_name):
        self.name = new_name

    def panhandle(self):
        print("You hit the streets to beg for cash...")
        try_again = "yes"
        while try_again == "yes":
            panhandle_time = random.randint(3, 10)
            panhandle_amount = random.randint(1, 100)
            time.sleep(panhandle_time)
            print("Congrats! You found someone to take pity on you.")
            print(f"You gained {panhandle_amount} credits!")
            self.balance += panhandle_amount
            try_again = input("Would you like to keep begging for cash?")
        print("You go back into the casino.")

    def make_bet(self, amount):
        if amount <= self.balance and amount >= 0:
            self.balance -= amount
            self.bet_amount = amount
        else:
            print("You do not have enough money for that bet!")
            print(f"Balance: {self.balance}")
            new_bet = int(input("Please input a new bet"))
            self.make_bet(new_bet)

    def win_bet(self):
        self.balance += 2 * self.bet_amount
        print(f"You won your bet of {self.bet_amount}")
        self.bet_amount = 0

    def lose_bet(self):
        print(f"You lose your bet of {self.bet_amount}")
        self.bet_amount = 0

    def tie_bet(self):
        print(f"The bet is a tie!")
        self.balance += self.bet_amount
        self.bet_amount = 0

    def pass_line(self):
        come_out_roll = dice_roll(2)
        print(f"Your Roll: {come_out_roll}")

        if come_out_roll in (2, 3, 12):
            print("You lose because you got a 2, 3, or 12 on your come-out roll!")
            self.lose_bet()

        elif come_out_roll in (7, 11):
            print("You win because you got a 7 or 11 on your come-out roll!")
            self.win_bet()
        else:
            print(f"{come_out_roll} is now your point number.")
            point_number = come_out_roll
            bonus_total = -1
            while bonus_total not in (point_number, 7):
                bonus_total = dice_roll(2)
                print(f"Bonus Roll: {bonus_total}")
                if bonus_total == point_number:
                    print(f"You win because you got your point number ({point_number}) before a 7!")
                    self.win_bet()
                elif bonus_total == 7:
                    print(f"You lose because you got a 7 before your point number ({point_number})!")
                    self.lose_bet()
                else:
                    print("Roll again!")

    def dont_pass_line(self):
        come_out_roll = dice_roll(2)
        print(f"Your Roll: {come_out_roll}")

        if come_out_roll in (2, 3):
            print("You win because you got a 2 or a 3 on your come-out roll!")
            self.win_bet()
        elif come_out_roll in (7, 11):
            print("You lose because you got a 7 or 11 on your come-out roll!")
            self.lose_bet()
        elif come_out_roll == 12:
            print("You tie because you rolled a 12!")
            self.tie_bet()
        else:
            print(f"{come_out_roll} is now your point number.")
            point_number = come_out_roll
            bonus_total = -1
            while bonus_total not in (point_number, 7):
                bonus_total = dice_roll(2)
                print(f"Bonus Roll: {bonus_total}")
                if bonus_total == point_number:
                    print(f"You lose because you got your point number ({point_number}) before a 7!")
                    self.lose_bet()
                elif bonus_total == 7:
                    print(f"You win because you got a 7 before your point number ({point_number})!")
                    self.win_bet()
                else:
                    print("Roll again!")




def dice_roll(num_dice):

    roll_total = 0
    for dice in range(num_dice):
        roll_total += random.randint(1, 6)

    return roll_total



def main():

    welcome_message = input("Welcome to the Craps Table! Are you a new or returning player?\n" 
                            "1. New\n" 
                            "2. Returning\n")

    if welcome_message == "1":
        user_name = input("What is your name?")
        player = Gambler(user_name.title())
        player.show_stats()
    elif welcome_message == "2":
        return_username = input("What is your name?")
        file_load = open("userlist.txt", "r")
        dict_load = json.load(file_load)
        if dict_load["name"] == return_username.title():
            player = Gambler(dict_load["name"], dict_load["balance"])
        else:
            print("Username not found. Created a new user.")
            player = Gambler(return_username.title(), balance=1000)


    player.show_stats()


    keep_going = "yes"
    while keep_going == "yes":

        print()
        user_choice = input("What would you like to do?\n\n"
                            "1. Pass Line Bet\n" 
                            "2. Do Not Pass Line Bet\n"
                            "3. Go out and panhandle for credits\n"
                            "4. Quit  \n")

        if user_choice == "1" and player.balance > 0:
            user_bet = int(input("How much would you like to bet?"))
            player.make_bet(user_bet)
            player.pass_line()
        elif user_choice == "2" and player.balance > 0:
            user_bet = int(input("How much would you like to bet?"))
            player.make_bet(user_bet)
            player.dont_pass_line()
        elif user_choice == "3":
            player.panhandle()
        elif user_choice == "4":
            break
        else:
            print("Please select a correct option.")
            continue

        player.show_stats()

        keep_going = input("Do you wish to continue?")


    print("Have a nice day- we have saved your progress.")
    player_export = player.__dict__
    with open("userlist.txt", "w") as json_file:
        json.dump(player_export, json_file)


main()

