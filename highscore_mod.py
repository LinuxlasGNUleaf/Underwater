import pickle
import operator

def readHighscores():
    highscores = {}
    # read from file
    file = open("high.score","rb")

    try:
        highscores = pickle.load(file)
    except EOFError:
        print('Highscore file empty or corrupted!')
    file.close()
    return highscores

def sortHighscoresbyValue(highscores):
    _list = sorted(highscores.items(), key=operator.itemgetter(1), reverse=True)
    return _list

def addHighscore(highscores,name,score):
    if (highscores[name]<score):
        highscores[name] = score

def saveHighscores(highscores):
    #writing new list to file
    file = open("high.score","wb")
    pickle.dump(highscores,file)
    file.close()

highscores = {}
hs_list = []
highscores = readHighscores()
hs_list = sortHighscoresbyValue(highscores)

def printHighscores(highscores):
    _list = sortHighscoresbyValue(highscores)
    print("The existing file contains the following:")
    for row in _list:
        a,b = row
        space = (20-len(a))*" "
        print("Name: {}{}Score: {}".format(a,space,b))
    print("")

print("HighscoreModifier v1.0 by JaWs\n")
print("""
you have the following commands for use:

add:name:score      --> adds an entry
remove:name         --> removes an entry
stop                --> DO NOT ctrl-C to stop or your changes will be lost!!!

You can use the add command to edit a existing entry, too.
DON'T YOU DARE TO USE SPACES TO MESS UP WITH THE PARSER!
""")
command = ""
run = True

printHighscores(highscores)
while run:
    command = input("user@HighscoreModifier: ")
    cmd_list = command.split(":")
    if len(cmd_list) == 1:
        if cmd_list[0] == "stop":
            run = False
        else:
            print("unkown command. cannot parse.")
    elif len(cmd_list) == 2:
        if cmd_list[0] == "remove":
            try:
                highscores.pop(cmd_list[1])
            except KeyError:
                print("Name '{}' not found! Check spelling. cannot parse.".format(cmd_list[1]))
                continue
            print("removed entry '{}'.".format(cmd_list[1]))
            printHighscores(highscores)
            saveHighscores(highscores)
        else:
            print("unkown command. cannot parse.")
    elif len(cmd_list) == 3:
        if cmd_list[0] == "add":
            try:
                highscores[cmd_list[1]] = int(cmd_list[2])
                print("edited entry: {} --> {}".format(cmd_list[1],cmd_list[2]))
                printHighscores(highscores)
                saveHighscores(highscores)
            except TypeError:
                print("Your input score is not valid! cannot parse.")
        else:
            print("unknown command. cannot parse.")

saveHighscores(highscores)
print("stopped.")