import pymongo
from pymongo import MongoClient
import random


cluster = MongoClient("MONGODB LINK")
db = cluster["DB NAME"]
collection = db["COLLECTION NAME"]
"""
post = {"_id": 0, "name": "Ata", "password": "atasoyata", "money": 5}
collection.insert_one(post)

post = {"_id": 1, "name": "Hulusi", "password": "hulus", "money": 5}
collection.insert_one(post)
"""
# collection.delete_many({})


def register():
    username = input("Enter the username : ")
    result = collection.find_one({"name": username})
    if result == None:
        password = input("Enter the password : ")
        post = {"name": username, "password": password, "money": 5}
        collection.insert_one(post)
        return True
    else:
        return False


def login():
    global globalusername
    globalusername = input("Enter the username : ")
    results = collection.find_one({"name": globalusername})
    if results == None:
        return False
    else:
        dbpassword = results["password"]
        inputpassword = input("Enter the password : ")
        if inputpassword == dbpassword:
            return True
        else:
            return False


def main():
    _pass = False
    while _pass == False:
        q = input("Enter 1 to login or 2 to register: ")
        if q == "1":
            if login() == True:
                _pass = True
        else:
            register()
    while True:
        q = input()
        if q == "showmoney":
            print(showmoney())
        elif q == "cf":
            coinfilip()
        elif q == "bj":
            blackjack()


def showmoney():
    username = input("Enter the username to see money: ")
    results = collection.find_one({"name": username})
    if results == None:
        return "User is not valid"
    else:
        money = results["money"]
        return f"{username} has {money}$"


def coinfilip():
    global globalusername
    options = ["head", "tail"]
    value = int(input("Enter the value you want to bet : "))
    if value < 1:
        print("Value must be bigger that or equal to 1")
    else:
        results = collection.find_one({"name": globalusername})
        money = results["money"]
        if value > money:
            print("You dont have enough money ")
        else:
            useroption = input("head or tail : ")
            if useroption == random.choice(options):
                print(f"You won and gain {value}$ ")
                newmoney = money + value
                results = collection.update_one(
                    {"name": globalusername}, {"$set": {"money": newmoney}}
                )
            else:
                print(f"You lost {value}$ ")
                newmoney = money - value
                results = collection.update_one(
                    {"name": globalusername}, {"$set": {"money": newmoney}}
                )


def blackjack():
    global globalusername
    results = collection.find_one({"name": globalusername})
    money = results["money"]
    value = int(input("Enter the number you bet :  "))
    if value < 1:
        print("Value must be bigger that or equal to 1")
    elif money < value:
        print("You dont have enough money ")
    else:
        cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        dealerCard1 = random.choice(cards)
        dealerCard2 = random.choice(cards)
        userCard1 = random.choice(cards)
        userCard2 = random.choice(cards)
        print(
            f" You {userCard1} + {userCard2} = {userCard1 + userCard2}  \n Dealer {dealerCard1} + ? \n [c]ontinue  [s]top"
        )
        userTotal = userCard1 + userCard2
        dealerTotal = dealerCard1 + dealerCard2
        stop = False
        while userTotal < 21 and dealerTotal < 21 and stop == False:
            q = input()
            if q == "c":
                userTotal += random.choice(cards)
                dealerTotal += random.choice(cards)
                print(f" You {userTotal} \n Dealer {dealerTotal} \n [c]ontinue  [s]top")
            else:
                stop = True
        print(f" You : {userTotal} \n Dealer : {dealerTotal}")
        if userTotal > 21 and dealerTotal > 21:
            print(f"You both busted")
        elif userTotal > 21 and dealerTotal < 22:
            print(f"You lost {value}$")
            newmoney = money - value
            results = collection.update_one(
                {"name": globalusername}, {"$set": {"money": newmoney}}
            )
        elif userTotal < 22 and dealerTotal > 21:
            print(f"You won {value}$")
            newmoney = money + value
            results = collection.update_one(
                {"name": globalusername}, {"$set": {"money": newmoney}}
            )
        elif userTotal == dealerTotal:
            print("It was tie")
        else:
            if userTotal > dealerTotal:
                print(f"You won {value}$")
                newmoney = money + value
                results = collection.update_one(
                    {"name": globalusername}, {"$set": {"money": newmoney}}
                )
            else:
                print(f"You lost {value}$")
                newmoney = money - value
                results = collection.update_one(
                    {"name": globalusername}, {"$set": {"money": newmoney}}
                )


main()