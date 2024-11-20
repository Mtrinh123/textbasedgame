import time
import random
import math
import pygame

# Plays menu music
pygame.init()
pygame.mixer.init()

def play_music(filename, volume=0.105):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()


play_music('Festival Town.mp3')

# Create your character 
classes = ['Wizard', 'Knight', 'Bard', 'Assassin']
stats = ['Attack', 'Dexterity', 'Defense', 'Mana', 'Health']
startStat = [[2,4,3,10,100],[7,4,9,2,100],[3,9,3,2,100],[5,10,3,3,100]]

# Starting stat 
playerName = ""
playerStat = [0,0,0,0,0]
statAdjust = [0,0,0,0,0]
playerClass = -1
gold = 1000
status = "Alive, Hopefully"

playerLevel = 0
playerEXP = 0

# Locations for this game
currLocation = "Your home"
diffPlaces = [['Mistvale', 'Emberreach Castle', 'Greythrone Forest', 'Your home'], [75,300,150,0]]
distHome = 0

# Things you can do in this game 
gameMenu = ['View your stats', 'Fast Travel', 'Go to the Chop Shop', 'Your stash', 'Exit the game :(']
itemsShop = [['Health Potion','Mana Potion','Stat Boost','Ice Heal'],[50,50,200,25]]
itemDrop = [['Health Potion','Mana Potion','Stat Boost','Ice Heal','Vase','Ruby',"Piece of paper"],[50,50,200,25,50,300,0]]
stash = ['Health Potion', 'Mana Potion']

# Iteration a loop to see if activity is in gameMenu
def indexInList(item, myList):
    foundIndex = -1
    for i in range(len(myList)):
        if item == myList[i]:
            foundIndex = i
            break
    return foundIndex

# Change list inputs to text
def listToText(myList):
    combinedText = "\n"
    for i in range(len(myList)):
        combinedText += str(i) + ") " + myList[i] + "\n"
    return combinedText + "\n"

# Inputs number into menu for activity, list error if number isn't in range
def checkMenuRange(question, listName, isCancelable=False):
    index = int(input(question + listToText(listName)))
    while True:
        if isCancelable and index == -1:
            return index
        elif index < 0 or index > len(listName) - 1:
            index = int(input("Invalid choice please try again\n"))
        else:
            return index

# Add some stars in the menu 
def stars(numRows, numSleep):
    sLine = "*" * 10
    for i in range(numRows):
        print(sLine)
    time.sleep(numSleep)

def showStash(stashList):
    if not stashList:
        print("Inventory is EMPTY!")
        return
    
    # Create a dictionary to count each unique item
    item_counts = {}
    
    for item in stashList:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1
    
    # Display the items and their counts
    print("Your stash contains:")
    for i, (item, count) in enumerate(item_counts.items()):
        print(f"{i}) {item} x{count}")
        
# Name your character
name = input('What is your name Traveler?\n')
print(f'You are now known as {name} in the lands of GreyThorne')
stars(4, 1)

# Display class and starting stats for each class
for i in range(len(classes)):
    print(f"\n{classes[i]}:")
    for j in range(len(stats)):
        print(f"{stats[j]:<10}: {startStat[i][j]:>3}")
print()

# Choose your class and set player stats
pClass = checkMenuRange("Choose your Class: ", classes)
print(f'You have chosen {classes[pClass]}!')
playerStat = startStat[pClass]  # Set player stats based on chosen class
playerClass = pClass  # Save chosen class index

stars(2, 3)
print(f"From now on, you shall be known as {name} the {classes[pClass]}.")
stars(1, 3)
print(f"You are now in the lands of Mistvale! Welcome to your new adventure, traveler.")

# Main loop for the game
inGameLoop = True
while inGameLoop and playerStat[4] > 0:  # Check health stat to ensure the player is alive
    choices = checkMenuRange("My traveler, what would you like to do right now?", gameMenu)
    if choices == 0:
        # View your stats
        print("Your Stats:")
        for i, stat in enumerate(stats):
            print(f"{stat}: {playerStat[i]}")
        print(f"Gold: {gold}")
        print(f"Status: {status}")
        stars(2, 1)
    
    elif choices == 1:
        # Fast Travel
        location = checkMenuRange("Where would you like to travel?", diffPlaces[0])
        print(f"Traveling to {diffPlaces[0][location]}...")
        currLocation = diffPlaces[0][location]
        stars(2, 1)
    
    elif choices == 2:
        play_music('Shop.mp3', 0.105)

        while True:
            print(f"You currently have {gold} gold right now!!!")
            shopChoice = checkMenuRange("Welcome to my Shop! My Name is Chop, how may I help you? Would you like to Buy an item or Sell an item?", ["Buy", "Sell", "Show Inventory", "Exit the shop"], True)
        
            if shopChoice == -1:
                break
        
            elif shopChoice == 0:
            # Buy
                buyChoice = checkMenuRange("What would you like to buy? This is what I have in stock right now, traveler!", itemsShop[0])
                itemName = itemsShop[0][buyChoice]
                itemPrice = itemsShop[1][buyChoice]
                quantity = int(input(f"How many {itemName}s would you like to buy? "))
                totalCost = itemPrice * quantity
            
                if gold >= totalCost:
                    for _ in range(quantity):
                        stash.append(itemName)
                    gold -= totalCost
                    print(f"Purchased {quantity} x {itemName} for {totalCost} gold. Remaining balance: {gold}.")
                    showStash(stash)
                else:
                    print(f"Sorry, you can't afford {quantity} x {itemName}. You need {totalCost} gold but only have {gold}.")
            elif shopChoice == 1:
            # Sell items
                if stash:
                    showStash(stash)  # Display items available to sell
                    sellChoice = checkMenuRange("What would you like to sell?", list(set(stash)))
                
                    if sellChoice != -1:
                    # Identify the item selected by the user
                        itemName = list(set(stash))[sellChoice]
                        itemIndex = indexInList(itemName, itemDrop[0])
                        sellPrice = math.floor(itemDrop[1][itemIndex] * 0.9)
                    
                    # Calculate how many of the selected item the player has
                        itemCount = stash.count(itemName)
                        print(f"You have {itemCount} x {itemName}. Each sells for {sellPrice} gold.")
                    
                    # Ask the player how many they want to sell
                        quantity = int(input(f"How many {itemName}s would you like to sell? "))
                    
                        if quantity > itemCount:
                            print(f"You only have {itemCount} x {itemName}.")
                        else:
                            totalSale = sellPrice * quantity
                            confirmChoice = checkMenuRange(f"Sell {quantity} x {itemName} for {totalSale} gold?", ["Yes", "No"])
                        
                            if confirmChoice == 0:
                            # Update the player's gold and remove the sold items from stash
                                gold += totalSale
                                for _ in range(quantity):
                                    stash.remove(itemName)
                            
                            print(f"Sold {quantity} x {itemName} for {totalSale} gold. Current balance is {gold}.")
                            # Display the updated stash after selling
                            showStash(stash)
                    else:
                        print("Sale cancelled.")
                else:
                    print("You have nothing to sell.")
        
            elif shopChoice == 2:
            # Show inventory
                showStash(stash)
        
            elif shopChoice == 3:
                print("Thank you for visiting Chop's Shop! Come back anytime.")
                play_music('Festival Town.mp3')
                break


    elif choices == 3:
        # View stash
        if stash:
            showStash(stash)
        else:
            print("Your stash is empty.")
        
    
    elif choices == 4:
        break