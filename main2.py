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
startStat = [[10,4,3,10,100],[30,4,9,2,100],[10,9,3,2,100],[15,10,3,3,100]]

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
gameMenu = ['View your stats', 'Travel', 'Go to the Chop Shop', 'Your stash', 'Exit the game :(']
itemsShop = [['Health Potion','Mana Potion','Stat Boost','Ice Heal'],[50,50,200,25]]
itemDrop = [['Health Potion','Mana Potion','Stat Boost','Ice Heal','Vase','Ruby',"Piece of paper"],[50,50,200,25,50,300,0]]
stash = ['Health Potion', 'Mana Potion']
enemyTypes = [["Fire wolf","Ice Bandit","Royal Guard","Rat","The Royal Knight"],[12,8,5,1,20],[15,5,8,5,20],[30,6,30,10,50],[5,10,2,1,10],[50,120,75,30,150]]
escapeAttempt =[False,False]

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

def useItem():
    global status
    showStash(stash)
    uniqStashList = list(set(stash))
    if(len(stash) < 1):
        return
    chosenItem = checkMenuRange("What item will you use?",uniqStashList,True)
    if chosenItem == -1:
        return
    itemToUse = indexInList(uniqStashList[chosenItem],itemDrop[0])
    if(itemToUse == 0):
        playerStat[4] += 25
        print("You've been healed!")
    elif(itemToUse == 1):
        if(status == "Fine" or status == "Ice"):
            print("Burn Heal had no effect")
        else:
            print(f" {name} was Burn Healed!")
            status = "Fine"
    elif(itemToUse == 2):
        if(status == "Fine" or status == "Burn"):
            print("Ice Heal had no effect")
        else:
            print(name + " was Ice Healed!")
            status = "Fine"
    elif(itemToUse == 3):
        checkStatBoost = checkMenuRange("What stat would you like to temporarily boost?",["Attack","Dexterity","Defence","Mana"])
        numBoost = math.ceil(playerStat[checkStatBoost] * .1)
        playerStat[checkStatBoost] += numBoost
        statAdjust[checkStatBoost] += numBoost
        print("Stat Boosted!")
    else:
        print("")
        
    if(itemToUse > 3):
        print("There is a time and place for every item!")
        stars(1,2)
    else:
        print("Current Stats")
        for i in range(len(stats)):
            print(stats[i],playerStat[i])
        stash.remove(itemDrop[0][itemToUse])

def AttackSystem():
    global status
    runStat = random.randint(0,100)
    
    fightChoice = checkMenuRange("What are you gonna do against your enemy?",["Fight","Item","Run"])
    
    if(fightChoice == 0):
        attackType = checkMenuRange("Choose an attack!",["Weapon","Magic","Dodge"])
        monDefPercentage = max(1, 1 - enemyStats[2] / 12)
        if(attackType == 0):
            print("Clink clink")
            damage = playerStat[0] * monDefPercentage
            damage = max(1, math.floor(damage)) 
            print("Damage " + str(damage))
            enemyStats[4] -= damage
        elif(attackType == 1):
            print("Take this")
            critChance = random.randint(0,100)
            critBonus = 1
            if(critChance > 70):
                print("CRITICAL HIT!")
                critBonus = 1.4
            damage = (playerStat[3] * monDefPercentage) * critBonus
            print("Damage "+ str(damage))
            enemyStats[4] -= damage
        else:
            escapeAttempt[0] = True
        print("Monster Health " + str(enemyStats[4]))
        stars(1,2)
    elif(fightChoice == 1):
        useItem()
    else:
        if(playerStat[1]/20 * 100 <= runStat):
            print("Got away safely!")
            for i in range(len(statAdjust)):
                playerStat[i] -= statAdjust[i]
                statAdjust[i] = 0
            escapeAttempt[1] = True
            stars(2,1)
        else:
            print("Could not escape, you weren't fast enough :( !")
            
    return escapeAttempt
def monsterAttack():
    global status
    if(status != "Alive, Hopefully"):
        if(status == "Burn"):
            playerStat[4] -=5 
            print(f"{name} was hurt by burn")
        else:
            playerStat[4] -=3 
            print(f'{name} was hurt by ice')
        
        print(name + " health is now " + str(playerStat[4]))
    print("Time for the enemy to attack")
    stars(1,1)
    attackOptionChance = random.randint(0,100)
    pDefPercentage = max(1, 1 - playerStat[2] / 12)
    if(enemyChoice == 0):
        #Fire Wolf
        if(attackOptionChance < 45):
            print("Fire ball!")
            playerStat[4] -= enemyStats[3] * pDefPercentage
            burnChance = random.randint(0,100)
            if(burnChance < 30):
                print(f"{name} was burned from attack!")
                pStatus = "Burn"
        elif(attackOptionChance < 90):
            print("HEAD BUTT!")
            playerStat[4] -= enemyStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if (tauntChance < 10):
                print("Fire heal!")
                enemyStats[4] *= 1.1
            else:
                print("Howls!")
    elif(enemyChoice == 1):
        #Ice Bandit
        if(attackOptionChance < 45):
            print("ICE AXE!")
            playerStat[4] -= enemyStats[3] * pDefPercentage
            burnChance = random.randint(0,100)
            if(burnChance < 30):
                print(f" {name} recieved frost bite from attack!")
                status = "Ice cold"
        elif(attackOptionChance < 90):
            print("HIGH KICK!")
            playerStat[4] -= enemyStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if (tauntChance < 10):
                print("SELF HEAL!")
                enemyStats[4] *= 1.1
            else:
                print("NICE TRY TRAVELER, HIT HARDER!!?")
    elif(enemyChoice == 2):
        # Royal Guard
        if(attackOptionChance < 50):
            #Taunt
            print("Stand Back puny traveler or face my steel")
        else:
            print("Take this traveler")
            playerStat[4] -= (enemyStats[0] * pDefPercentage)
    elif(enemyChoice == 3):
        # Rat
        print("Squeaks!")
        playerStat[4] -= (enemyStats[0] * pDefPercentage)
    else:
        # The Royal Knight
        print("You bested the royal guard, Prepare to bested by me")
        if(attackOptionChance < 45):
            print("TAKE MY BLADE")
            playerStat[4] -= enemyStats[3] * pDefPercentage
        elif(attackOptionChance < 90):
            print("SLAP, CRACKLE, POP")
            playerStat[4] -= enemyStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if(tauntChance < 10):
                print("DOUBLE SELF HEAL!!!!!")
                enemyStats[4] *= 1.2
            else:
                print("YOU ARE NOTHING BUT A PEASANT!")
    print(f"{name} health:" + str(playerStat[4]))         
    

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
        # Travel
        travelChoice = checkMenuRange("Where would you like to travel to? ",diffPlaces[0],True)
        if travelChoice == -1:
            isTravel = False
        else:
            isTravel = True
            print("And so " + name + " set off on their journey to "+diffPlaces[0][travelChoice])
            if(diffPlaces[1][travelChoice] == distHome):
                print("Well that was fast! You're already there!")
                isTravel = False
        #Travel Loop
        distanceDivider = random.randint(3,6)
        distanceTraveled = math.ceil(diffPlaces[1][travelChoice]/distanceDivider)
        isTravelNeg = diffPlaces[1][travelChoice] < int(distHome)
        while(isTravel and playerStat[4] > 0):
            if(not isTravelNeg):
                distHome += distanceTraveled
                if(distHome >= diffPlaces[1][travelChoice]):
                    print("You have reached " + diffPlaces[0][travelChoice])
                    isTravel = False
            else:
                distHome -= distanceTraveled
                if(distHome <= diffPlaces[1][travelChoice]):
                    print("You have reached " + diffPlaces[0][travelChoice])
                    isTravel = False
            if( not isTravel):
                distHome = diffPlaces[0][travelChoice]
                break
            
            if(random.randint(0,100) < 60):
                inFight = True
                enemyPercentage = random.randint(0,100)
                enemyChoice = -1
        
                if(enemyPercentage <= 25):
                    enemyChoice = 3
                elif(enemyPercentage <= 55):
                    enemyChoice = 0
                elif(enemyPercentage <= 85):
                    enemyChoice = 1
                elif(enemyPercentage < 99):
                    enemyChoice = 2
                else:
                    enemyChoice = 4
                enemyStats = [enemyTypes[1][enemyChoice],enemyTypes[2][enemyChoice],enemyTypes[3][enemyChoice],enemyTypes[4][enemyChoice],enemyTypes[5][enemyChoice]]
                stars(1,2)
                print("You have been challenged to fight "+ enemyTypes[0][enemyChoice])
                stars(1,1)
                chanceAdditional = 0
                currentTurn = -1
                if(playerStat[1] > enemyStats[1]):
                    chanceAdditional = random.randint(25,50)
                turnChance = 50 + chanceAdditional    
                
                if(random.randint(0,100) < turnChance):
                    currentTurn *= -1
                    
                while(inFight and playerStat[4] > 0):
                    if(currentTurn == 1):
                        escapeAttempt = AttackSystem()
                        if(escapeAttempt[1]):
                            escapeAttempt[1] = False
                            break
                    else:
                        incChance = 0
                        if(playerStat[1] > enemyStats[1]):
                            incChance = random.randint(25,50)
                        dChance = 25 + incChance
                        failChance = random.randint(0,100)
                        if(escapeAttempt[0]):
                            if(failChance < dChance):
                                print(f"{name} HAS NARROWLY AVOIDED ATTACK!")
                            else:
                                print("DODGE FAILED")
                                monsterAttack()
                            escapeAttempt[0] = False
                        else:
                            monsterAttack()
                    stars(1,2)
                    
                    currentTurn *= -1
                    
                    if(playerStat[4] <= 0):
                        print(f" The might {name} has been bested.. may they rest in peices")
                        break
                    if(enemyStats[4] <= 0):
                        print(f"{name} has defeated the monster!")
                        print("What would you like to do next?")
                        print("1) Continue exploring")
                        print("2) Return to town")
                        next_choice = int(input())
                        if next_choice == 1:
                            print(f"{name} continues their exploration.")
                            stars(1, 1)
                            break  # Continue traveling and exploring
                        elif next_choice == 2:
                         choices = checkMenuRange("My traveler, what would you like to do right now?", gameMenu)
                         break


            else:
                stars(1,1)
                print("Traveling......")
                stars(1,1)
                pickUpChance = random.randint(0,100)
                if(pickUpChance < 20):
                    itemFound = itemDrop[0][0]
                elif(pickUpChance < 30):
                    itemFound = itemDrop[0][1]
                elif(pickUpChance < 40):
                    itemFound = itemDrop[0][2]
                elif(pickUpChance < 45):
                    itemFound = itemDrop[0][3]
                elif(pickUpChance < 65):
                    itemFound = itemDrop[0][4]
                elif(pickUpChance < 69):
                    itemFound = itemDrop[0][5]
                else:
                    itemFound = itemDrop[0][6]
                    
                print(name + " has found " + itemFound)
                addItemCheck = checkMenuRange("Would you like to add this item to your inventory?",["Yes","No"])
                if(addItemCheck == 0):
                    print(itemFound + " was added to your inventory")
                    stash.append(itemFound)
                else:
                    print(itemFound + " was discarded")
                
                stars(1,1)
                print(name + " continues their journey!")
                stars(1,2)
            
    
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
        print(f"Goodbye, {name}! You have left the game.")
        inGameLoop = False
        break