import pygame
import sys
import os
import mysql.connector
import random

pygame.init()

#create Settings file if not found
if (os.path.isfile("Settings.txt"))==False:
    f=open("Settings.txt","w")
    DefaultSettings=["normal",800,600,0,255,0]
    f.write(str(DefaultSettings[0])+"\n")
    for i in range(len(DefaultSettings)-1):
        f.write(str(DefaultSettings[i+1])+"\n")

    


f=open("Settings.txt","r")
line=str(f.read())
settings=line.split("\n")
for i in range(5):
    settings[i+1]=int(settings[i+1])

#settings definitions
Difficulty=settings[0]
ScreenWidth=settings[1]
ScreenHeight=settings[2]
CharRed=settings[3]
CharGreen=settings[4]
CharBlue=settings[5]
PlayerName=settings[6]



resolutions=[[1920,1080],[1768,922],[1680,1050],[1600,1024],[1600,900],[1440,900],[1366,768],[1360,768],[1280,1024],[1280,960],[1280,800],[1280,764],[1280,720],[1176,664],[1176,664],[1152,864],[1024,768],[800,600]]

font1=pygame.font.SysFont("Arial",40)
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))



class Button():
    def __init__(self, image, x_pos, y_pos):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos,self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)

    def InputTest(self, position):
        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            return True


class obstacle(object):
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    def __init__(self,MinObstSize,MaxObstSize,Char_starting_position,buffer):
        self.obstacleX = random.randint(0,ScreenWidth)
        self.obstacleY = random.randint(0,ScreenHeight)
        self.obstacleSize = random.randint(MinObstSize,MaxObstSize)
        #ensure that obstacle is generated at a suitable buffer distance from player starting position 
        while self.obstacleX < Char_starting_position[0]+buffer and self.obstacleY < Char_starting_position[1]+buffer and self.obstacleY > Char_starting_position[1]-buffer:
            self.obstacleX = random.randint(0,ScreenWidth)
            self.obstacleY = random.randint(0,ScreenHeight)
            self.obstacleSize = random.randint(MinObstSize,MaxObstSize)

        


    def LoadObstacle(self,ObstColour):
        pygame.draw.rect(screen,ObstColour,(self.obstacleX,self.obstacleY,self.obstacleSize,self.obstacleSize))

          
    def CollisionDetection(self,CharX,CharY,CharSize):
        if (CharX < self.obstacleX and CharX + CharSize > self.obstacleX) or (CharX > self.obstacleX and CharX < self.obstacleX + self.obstacleSize):
            if (CharY < self.obstacleY and CharY + CharSize > self.obstacleY) or (CharY > self.obstacleY and CharY < self.obstacleY + self.obstacleSize):
                return True

        if CharY >= ScreenHeight - CharSize or CharY <= 0:
            return True
        return False 


class Character(object):
    def __init__(self,Char_starting_position):
        self.CharX=Char_starting_position[0]
        self.CharY=Char_starting_position[1]
        self.CharSize=25
    
    def ChangeDirection(self,change_direction):                    
        if change_direction == False:
            change_direction = True
        else:
            change_direction = False
        return(change_direction)
            



def CreateGrid(settings,obstacles,Char_starting_position,CharSize,num_of_obstacles):
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]


    #define grid as a 2D array with each section being character's size
    Grid=[]
    GridRow=[]

    GridSize = CharSize
    GridWidth = ScreenWidth // GridSize
    GridHeight = ScreenHeight // GridSize
    ObstacleCollision=False

    for i in range(GridHeight):
        GridRow=[]
        for j in range(GridWidth):
            ObstacleCollision=False
            RectX=ScreenWidth//GridSize*j
            RectY=ScreenHeight//GridSize*i
            for n in range(num_of_obstacles):
                if obstacles[n].CollisionDetection(RectX,RectY,CharSize)==True:
                    ObstacleCollision=True
                else:
                    ObstacleCollision=False
            if ObstacleCollision==True:
                GridRow.append(1)
                ObstacleCollision=False
            else:
                GridRow.append(0)
        Grid.append(GridRow)
    
    #calculate starting position on grid
    start=(Char_starting_position[0]//GridWidth,Char_starting_position[1]//GridHeight)
    if bfs(Grid,start,ScreenWidth-CharSize)==True:
        return True


def bfs(grid,start,end):
    visited=[]
    current=start
    while current[0] != end:
        if grid[current[0]][current[1]]==1:
            if len(visited)>0:
                visited.pop()
            else:
                return False
            current=visited[len(visited)-1]
        else:
            visited.append(current)
            neighbours=get_neighbours(grid,current[0],current[1])  
            for i in range(len(neighbours)):
                current=neighbours[i]

    
    return True


def get_neighbours(grid, row, col):
    neighbours = []
    if row > 0 and grid[row-1][col] == 0:
        neighbours.append((row-1, col))
    if row < len(grid)-1 and grid[row+1][col] == 0:
        neighbours.append((row+1, col))
    if col > 0 and grid[row][col-1] == 0:
        neighbours.append((row, col-1))
    if col < len(grid[0])-1 and grid[row][col+1] == 0:
        neighbours.append((row, col+1))
    return neighbours




def MenuScreen(settings):
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5
    SettingsWidth=ScreenHeight/5
    SettingsHeight=SettingsWidth

    settingsbutton_surface = pygame.image.load("settingsbutton.png")
    settingsbutton_surface = pygame.transform.scale(settingsbutton_surface,(SettingsWidth,SettingsHeight))
    settingsbutton = Button(settingsbutton_surface,ScreenWidth-50,50)

    playbutton_surface = pygame.image.load("playbutton.png")
    playbutton_surface = pygame.transform.scale(playbutton_surface,(ButtonWidth,ButtonHeight))
    playbutton = Button(playbutton_surface,ScreenWidth/2,ScreenHeight/3-180)

    leaderboardbutton_surface = pygame.image.load("leaderboardbutton.png")
    leaderboardbutton_surface = pygame.transform.scale(leaderboardbutton_surface,(ButtonWidth,ButtonHeight))
    leaderboardbutton = Button(leaderboardbutton_surface,ScreenWidth/2,ScreenHeight*2/3-180)

    quitbutton_surface = pygame.image.load("quitbutton.png")
    quitbutton_surface = pygame.transform.scale(quitbutton_surface,(ButtonWidth,ButtonHeight))
    quitbutton = Button(quitbutton_surface,ScreenWidth/2,ScreenHeight-180)

    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playbutton.InputTest(pygame.mouse.get_pos())==True:
                    game(settings,font1)
                if settingsbutton.InputTest(pygame.mouse.get_pos())==True:
                    settings=Settings(settings)
                if leaderboardbutton.InputTest(pygame.mouse.get_pos())==True:
                    LeaderBoard(settings)
                if quitbutton.InputTest(pygame.mouse.get_pos())==True:
                    f=open("Settings.txt","w")
                    f.write(str(settings[0])+"\n")
                    for i in range(len(settings)-1):
                        f.write(str(settings[i+1])+"\n")
                    pygame.quit()
                    sys.exit()
                

        screen.fill("white")

        playbutton.update()
        settingsbutton.update()
        leaderboardbutton.update()
        quitbutton.update()

        pygame.display.update()


def ReturnToMenu(CharX,CharY,CharSize):
    for i in range(300):
        pygame.draw.rect(screen,(255,255,255),(CharX-i*6,CharY-i*4,CharSize+i*23,CharSize+i*15))
        pygame.display.update()
    screen.fill("black")
    MenuScreen(settings)
                    



def Settings(settings):
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5

    difficultybutton_surface = pygame.image.load("difficultybutton.png")
    difficultybutton_surface = pygame.transform.scale(difficultybutton_surface,(ButtonWidth,ButtonHeight))
    difficultybutton = Button(difficultybutton_surface,ScreenWidth/6,ScreenHeight*3/4)
    
    resolutionbutton_surface = pygame.image.load("resolutionbutton.png")
    resolutionbutton_surface = pygame.transform.scale(resolutionbutton_surface,(ButtonWidth,ButtonHeight))
    resolutionbutton = Button(resolutionbutton_surface,ScreenWidth/2,ScreenHeight*3/4)

    colourbutton_surface = pygame.image.load("colourbutton.png")
    colourbutton_surface = pygame.transform.scale(colourbutton_surface,(ButtonWidth,ButtonHeight))
    colourbutton = Button(colourbutton_surface,ScreenWidth*5/6,ScreenHeight*3/4)

    exitsettingsbutton_surface = pygame.image.load("exitsettingsbutton.png")
    exitsettingsbutton_surface = pygame.transform.scale(exitsettingsbutton_surface,(ButtonWidth,ButtonHeight))
    exitsettingsbutton = Button(exitsettingsbutton_surface,ScreenWidth/2,ScreenHeight/3)    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if difficultybutton.InputTest(pygame.mouse.get_pos())== True:
                    settings[0]=DifficultySelection()
                if resolutionbutton.InputTest(pygame.mouse.get_pos())== True:
                    Resolution=ResolutionSelection(resolutions,screen,font1)
                    settings[1]=Resolution[0]
                    settings[2]=Resolution[1]
                if colourbutton.InputTest(pygame.mouse.get_pos())== True:
                    CharColour=ColourSelection()
                    settings[3]=CharColour[0]
                    settings[4]=CharColour[1]
                    settings[5]=CharColour[2]
                if exitsettingsbutton.InputTest(pygame.mouse.get_pos())== True:
                    MenuScreen(settings)

        screen.fill("white")

        difficultybutton.update()
        resolutionbutton.update()
        colourbutton.update()
        exitsettingsbutton.update()

        pygame.display.update()


def ColourSelection():
    CharRed=0
    CharGreen=0
    CharBlue=0
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5
    gradientlength=ScreenWidth/2
    gradientheight=ScreenHeight/8


    confirmbutton_surface = pygame.image.load("confirmbutton.png")
    confirmbutton_surface = pygame.transform.scale(confirmbutton_surface,(ButtonWidth,ButtonHeight))
    confirmbutton = Button(confirmbutton_surface,ScreenWidth/2,ScreenHeight-150)

    redgradient_surface = pygame.image.load("redgradient.png")
    redgradient_surface = pygame.transform.scale(redgradient_surface,(gradientlength,gradientheight))
    redgradient = Button(redgradient_surface,ScreenWidth/2,ScreenHeight/4-150)

    greengradient_surface = pygame.image.load("greengradient.png")
    greengradient_surface = pygame.transform.scale(greengradient_surface,(gradientlength,gradientheight))
    greengradient = Button(greengradient_surface,ScreenWidth/2,ScreenHeight/2-150)

    bluegradient_surface = pygame.image.load("bluegradient.png")
    bluegradient_surface = pygame.transform.scale(bluegradient_surface,(gradientlength,gradientheight))
    bluegradient = Button(bluegradient_surface,ScreenWidth/2,ScreenHeight*3/4-150)

    screen.fill("white")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirmbutton.InputTest(pygame.mouse.get_pos())==True:
                    if CharRed+CharGreen+CharBlue>50:
                        return(round(CharRed),round(CharBlue),round(CharGreen))
                if redgradient.InputTest(pygame.mouse.get_pos())==True:
                    CharRed=round(pygame.mouse.get_pos()[0]-(ScreenWidth-gradientlength)/2)*(255/gradientlength)
                    pygame.draw.rect(screen,(CharRed,CharGreen,CharBlue),(90,500,50,50))
                if greengradient.InputTest(pygame.mouse.get_pos())==True:
                    CharGreen=round(pygame.mouse.get_pos()[0]-(ScreenWidth-gradientlength)/2)*(255/gradientlength)
                    pygame.draw.rect(screen,(CharRed,CharGreen,CharBlue),(90,500,50,50))
                if bluegradient.InputTest(pygame.mouse.get_pos())==True:
                    CharBlue=round(pygame.mouse.get_pos()[0]-(ScreenWidth-gradientlength)/2)*(255/gradientlength)
                    pygame.draw.rect(screen,(CharRed,CharGreen,CharBlue),(90,500,50,50))
                    

                
        confirmbutton.update()
        redgradient.update()
        greengradient.update()
        bluegradient.update()
        pygame.display.update()    


def DifficultySelection():
    NewDifficulty=settings[0]
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5

    easybutton_surface = pygame.image.load("easybutton.png")
    easybutton_surface = pygame.transform.scale(easybutton_surface,(ButtonWidth,ButtonHeight))
    easybutton = Button(easybutton_surface,ScreenWidth/4,ScreenHeight/5)

    normalbutton_surface = pygame.image.load("normalbutton.png")
    normalbutton_surface = pygame.transform.scale(normalbutton_surface,(ButtonWidth,ButtonHeight))
    normalbutton = Button(normalbutton_surface,ScreenWidth/4,ScreenHeight*2/5)

    hardbutton_surface = pygame.image.load("hardbutton.png")
    hardbutton_surface = pygame.transform.scale(hardbutton_surface,(ButtonWidth,ButtonHeight))
    hardbutton = Button(hardbutton_surface,ScreenWidth/4,ScreenHeight*3/5)

    veryhardbutton_surface = pygame.image.load("veryhardbutton.png")
    veryhardbutton_surface = pygame.transform.scale(veryhardbutton_surface,(ButtonWidth,ButtonHeight))
    veryhardbutton = Button(veryhardbutton_surface,ScreenWidth/4,ScreenHeight*4/5)

    confirmbutton_surface = pygame.image.load("confirmbutton.png")
    confirmbutton_surface = pygame.transform.scale(confirmbutton_surface,(ButtonWidth,ButtonHeight))
    confirmbutton = Button(confirmbutton_surface,ScreenWidth-400,ScreenHeight-150)


    screen.fill("white")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirmbutton.InputTest(pygame.mouse.get_pos())==True:
                    return(NewDifficulty)
                if easybutton.InputTest(pygame.mouse.get_pos())==True:
                    NewDifficulty="easy"
                if normalbutton.InputTest(pygame.mouse.get_pos())==True:
                    NewDifficulty="normal"
                if hardbutton.InputTest(pygame.mouse.get_pos())==True:
                    NewDifficulty="hard"        
                if veryhardbutton.InputTest(pygame.mouse.get_pos())==True:
                    NewDifficulty="very hard"

                    

                
        confirmbutton.update()
        easybutton.update()
        normalbutton.update()
        hardbutton.update()
        veryhardbutton.update()
        pygame.display.update()    


def ResolutionSelection(resolutions,screen,font1):
    x=0
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5
    ArrowWidth=ScreenHeight/9
    ArrowHeight=ArrowWidth
    
    confirmbutton_surface = pygame.image.load("confirmbutton.png")
    confirmbutton_surface = pygame.transform.scale(confirmbutton_surface,(ButtonWidth,ButtonHeight))
    confirmbutton = Button(confirmbutton_surface,ScreenWidth/2,ScreenHeight-150)

    right_surface = pygame.image.load("rightbutton.png")
    right_surface = pygame.transform.scale(right_surface,(ArrowWidth,ArrowHeight))
    rightbutton = Button(right_surface,ScreenWidth/2+300,ScreenHeight/2)

    left_surface = pygame.image.load("leftbutton.png")
    left_surface = pygame.transform.scale(left_surface,(ArrowWidth,ArrowHeight))
    leftbutton = Button(left_surface,ScreenWidth/2-300,ScreenHeight/2)

    
    Restext=str(resolutions[x][0])+"X"+str(resolutions[x][1])
    Restext_surface=font1.render((Restext),False,(255,255,255))
    blank_surface=pygame.image.load("blankbutton.png")
    blank_surface=pygame.transform.scale(blank_surface,(ScreenWidth/4,ScreenHeight/7))
    
    screen.fill("white")
    text=(str(resolutions[x][0])+"X"+str(resolutions[x][1]))
    text_surface=font1.render((text),False,(255,255,255))
    screen.blit(blank_surface,(ScreenWidth/2-235,ScreenHeight/2-70,400,100))
    screen.blit(text_surface,(ScreenWidth/2-85,ScreenHeight/2-20,400,100))

    pygame.display.update()  



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirmbutton.InputTest(pygame.mouse.get_pos())==True:
                    screen = pygame.display.set_mode((resolutions[x][0],resolutions[x][1]))
                    return(resolutions[x])
                if rightbutton.InputTest(pygame.mouse.get_pos())==True:
                    x+=1                    
                    if x>len(resolutions)-1:
                        x=0         
                    text=(str(resolutions[x][0])+"X"+str(resolutions[x][1]))
                    text_surface=font1.render((text),False,(255,255,255))
                    screen.blit(blank_surface,(ScreenWidth/2-235,ScreenHeight/2-70,400,100))
                    screen.blit(text_surface,(ScreenWidth/2-85,ScreenHeight/2-20,400,100))
                    
                if leftbutton.InputTest(pygame.mouse.get_pos())==True:
                    x-=1
                    if x<0:
                        x=0
                    text=(str(resolutions[x][0])+"X"+str(resolutions[x][1]))
                    text_surface=font1.render((text),False,(255,255,255))
                    screen.blit(blank_surface,(ScreenWidth/2-235,ScreenHeight/2-70,400,100))
                    screen.blit(text_surface,(ScreenWidth/2-85,ScreenHeight/2-20,400,100))
                    

                    

                
        confirmbutton.update()
        rightbutton.update()
        leftbutton.update()
        pygame.display.update()    




def LeaderBoard(settings):
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    PlayerName=settings[6]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5

    menubutton_surface = pygame.image.load("menubutton.png")
    menubutton_surface = pygame.transform.scale(menubutton_surface,(ButtonWidth,ButtonHeight))
    menubutton = Button(menubutton_surface,ScreenWidth*3/4,ScreenHeight/2-200)

    
    
    PlayerLeaderboard=(ReadLeaderBoard(PlayerName))
    PlayerHighScore=str(PlayerLeaderboard[2])
    TopPlayers=TopScores()



    screen.fill("white")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menubutton.InputTest(pygame.mouse.get_pos())==True:
                    MenuScreen(settings)

    
        

        text1_surface=font1.render((PlayerHighScore),False,(0,0,0))
        screen.blit(text1_surface,(ScreenWidth*3/7,ScreenHeight/6))
        text2_surface=font1.render((PlayerName),False,(0,0,0))
        screen.blit(text2_surface,(ScreenWidth/7,ScreenHeight/6))
        text3_surface=font1.render(("Player Name"),False,(0,0,0))
        screen.blit(text3_surface,(ScreenWidth*3/7,ScreenHeight/14))
        text4_surface=font1.render(("Player High Score"),False,(0,0,0))
        screen.blit(text4_surface,(ScreenWidth/7,ScreenHeight/14))
        for i in range(len(TopPlayers)):
            TopPlayerName=str(TopPlayers[i][0])
            TopPlayerHighScore=str(TopPlayers[i][1])
            text5_surface=font1.render((TopPlayerName),False,(0,0,0))
            screen.blit(text5_surface,(ScreenWidth/7,ScreenHeight*(i+4)/12))
            text6_surface=font1.render((TopPlayerHighScore),False,(0,0,0))
            screen.blit(text6_surface,(ScreenWidth*3/7,ScreenHeight*(i+4)/12))

        

        menubutton.update()


        pygame.display.update()       


def AddFriend():
    x=0

def UpdateLeaderBoard(PlayerName,score):

    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="nour2005",
        database="mydatabase"
    )
    score=int(score)

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")


    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Player (
            PlayerName VARCHAR(255) PRIMARY KEY,
            PlayerHighScore INT
        )
    """)


    sql = "SELECT * FROM Player WHERE PlayerName = %s"
    val = (PlayerName,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    mycursor.execute("SELECT * FROM Player WHERE PlayerName=%s", (PlayerName,))
    result = mycursor.fetchone()

    

    if result:    
        if result[2]==0:
            mycursor.execute("UPDATE Player SET PlayerHighScore=%s WHERE PlayerName=%s", (score, PlayerName))
            mydb.commit()
        else:
            if score > result[2]:
                # compare highscore with new score
                sql = "UPDATE Player SET PlayerHighScore = %s WHERE PlayerName = %s"
                val = (score,PlayerName)
                mycursor.execute(sql, val)
                mydb.commit()
    else:
        #add this player to the table
        sql = "INSERT INTO Player (PlayerName, PlayerHighScore) VALUES (%s, %s)"
        val = (PlayerName,score)
        mycursor.execute(sql,val)
        mydb.commit()
    

def ReadLeaderBoard(PlayerName):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="nour2005",
        database="mydatabase"
    )


    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")


    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Player (
            PlayerName VARCHAR(255) PRIMARY KEY,
            PlayerHighScore INT
        )
    """)


    sql = "SELECT * FROM Player WHERE PlayerName = %s"
    val = (PlayerName,)
    mycursor.execute(sql, val)
    return(mycursor.fetchone())


def TopScores():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="nour2005",
        database="mydatabase"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT PlayerName, PlayerHighScore FROM Player ORDER BY PlayerHighScore DESC LIMIT 10")


    
    TopPlayers = mycursor.fetchall()
    return(TopPlayers)




def game(settings,font1):
    ObstColour=(255,0,0)
    Difficulty=settings[0]
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    CharRed=settings[3]
    CharBlue=settings[4]
    CharGreen=settings[5]
    PlayerName=settings[6]
    CharColour=(CharRed,CharGreen,CharBlue)
    Char_starting_position = [50,500]
    CharSpeed=random.random()
    change_direction = False
    score=0 
    level=0
    Pathfound=False
    game_over=False
    obstacles=[]
    MaxObstSize=180
    MinObstSize=80
    obstacles_loaded=False
    LevelComplete=True
    num_of_obstacles=15
    Char=Character(Char_starting_position)

    screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))

    if PlayerName=="":
        PlayerName=PlayerNameSelection(settings,font1)

    


    while not game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                sys.exit()
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    PauseMenu(settings)

                if event.key == pygame.K_SPACE:
                    change_direction=Char.ChangeDirection(change_direction)
                    print("space key pressed")


        

        if LevelComplete==True:
            if Difficulty=="easy":
                buffer=250
                CharSpeed=CharSpeed*0.9
                score=30*level
                LevelComplete=False
                if num_of_obstacles<=12:
                    num_of_obstacles+=1
        

            elif Difficulty=="normal":
                buffer=200
                CharSpeed=CharSpeed*1.1
                score=50*level
                LevelComplete=False
                if num_of_obstacles<=15:
                    num_of_obstacles+=1
                        
            elif Difficulty=="hard":
                buffer=150
                CharSpeed=CharSpeed*1.2
                score=70*level
                LevelComplete=False
                if num_of_obstacles<=18:
                    num_of_obstacles+=1
            elif Difficulty=="very hard":
                buffer=100
                CharSpeed=CharSpeed*1.4
                score=100*level
                LevelComplete=False
                if num_of_obstacles<=20:
                    num_of_obstacles+=1
            else:
                DifficultySelection()
        
        
            
        if LevelComplete==True:
            #obstacle initilisation
            obstacles=[]
            for i in range(num_of_obstacles):
                NewObstacle=obstacle(MinObstSize,MaxObstSize,Char_starting_position,buffer)
                obstacles.append(NewObstacle)
                obstacles[i].LoadObstacle(obstacles[i],ObstColour)
            Char=Character(Char_starting_position)

                
        #character movement

        if CharSpeed < 0.7:
            CharSpeed = CharSpeed*2.5
        
        if change_direction == True:
            Char.CharX += CharSpeed
            Char.CharY += CharSpeed
        else:
            Char.CharX += CharSpeed
            Char.CharY -= CharSpeed

        
        #level completion test    
        if Char.CharX >= ScreenWidth - Char.CharSize:
            LevelComplete=True
            Char=Character(Char_starting_position)
            obstacles_loaded = False
            level+=1
            obstacles=[]


        


        pygame.draw.rect(screen,CharColour,(Char.CharX,Char.CharY,Char.CharSize,Char.CharSize))
        pygame.display.update()
        screen.fill("black")
        Scoretext=str(score)
        Scoretext_surface=font1.render((Scoretext),False,(255,255,255))
        screen.blit(Scoretext_surface,(20,0,400,100))


        #obstacle initilisation
        if obstacles_loaded == False:
            obstacles=ObstacleInitilisation(num_of_obstacles,MinObstSize,MaxObstSize,Char_starting_position,buffer)
            obstacles_loaded=True
            Pathfound=False
        for i in range(num_of_obstacles):
            obstacles[i].LoadObstacle(ObstColour)
            


        if Pathfound==False:
            while CreateGrid(settings,obstacles,Char_starting_position,Char.CharSize,num_of_obstacles)==False:
                ObstacleInitilisation(num_of_obstacles,MinObstSize,MaxObstSize,Char_starting_position,buffer) 
            Pathfound=True                   
        


        #collision detection
        for i in range(num_of_obstacles):
            if obstacles[i].CollisionDetection(Char.CharX,Char.CharY,Char.CharSize)==True:
                UpdateLeaderBoard(PlayerName,score)
                ReturnToMenu(Char.CharX,Char.CharY,Char.CharSize)
                

def ObstacleInitilisation(num_of_obstacles,MinObstSize,MaxObstSize,Char_starting_position,buffer):
    obstacles=[]
    for i in range(num_of_obstacles):
        NewObstacle=obstacle(MinObstSize,MaxObstSize,Char_starting_position,buffer)
        obstacles.append(NewObstacle)
    return(obstacles)
    

def PauseMenu(settings):
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5
    SettingsWidth=ScreenHeight/5
    SettingsHeight=SettingsWidth

    settingsbutton_surface = pygame.image.load("settingsbutton.png")
    settingsbutton_surface = pygame.transform.scale(settingsbutton_surface,(SettingsWidth,SettingsHeight))
    settingsbutton = Button(settingsbutton_surface,ScreenWidth-50,50)

    resumebutton_surface = pygame.image.load("resumebutton.png")
    resumebutton_surface = pygame.transform.scale(resumebutton_surface,(ButtonWidth,ButtonHeight))
    resumebutton = Button(resumebutton_surface,ScreenWidth/2,ScreenHeight/2+200)

    menubutton_surface = pygame.image.load("menubutton.png")
    menubutton_surface = pygame.transform.scale(menubutton_surface,(ButtonWidth,ButtonHeight))
    menubutton = Button(menubutton_surface,ScreenWidth/2,ScreenHeight/2-200)

    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resumebutton.InputTest(pygame.mouse.get_pos())==True:
                    return(0)
                if settingsbutton.InputTest(pygame.mouse.get_pos())==True:
                    settings=Settings(settings)
                if menubutton.InputTest(pygame.mouse.get_pos())==True:
                    MenuScreen(settings)
                

        screen.fill("white")

        resumebutton.update()
        settingsbutton.update()
        menubutton.update()

        pygame.display.update()                


def PlayerNameSelection(settings,font1):
    ScreenWidth=settings[1]
    ScreenHeight=settings[2]
    PlayerName=settings[6]
    ButtonWidth=ScreenWidth/3
    ButtonHeight=ScreenHeight/5
    

    confirmbutton_surface = pygame.image.load("confirmbutton.png")
    confirmbutton_surface = pygame.transform.scale(confirmbutton_surface,(ButtonWidth,ButtonHeight))
    confirmbutton=Button(confirmbutton_surface,ScreenWidth/2,ScreenHeight-150)


    
    inputtext_surface=font1.render((PlayerName),False,(255,0,255))
    blank_surface=pygame.image.load("blankbutton.png")
    blank_surface=pygame.transform.scale(blank_surface,(ScreenWidth/4,ScreenHeight/7))

    text_surface=font1.render(("Please Enter Your Player Name"),False,(0,0,0))
    

    screen.blit(inputtext_surface,(ScreenWidth/2-235,ScreenHeight/2-70,400,100))
    screen.blit(blank_surface,(ScreenWidth/2-235,ScreenHeight/2-70,400,100))

    


    screen.fill("white")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f=open("Settings.txt","w")
                f.write(str(settings[0])+"\n")
                for i in range(len(settings)-1):
                    f.write(str(settings[i+1])+"\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirmbutton.InputTest(pygame.mouse.get_pos())==True:
                    settings[6]=PlayerName
                    return(PlayerName)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    PlayerName = PlayerName[:-1]
                else:
                    PlayerName += event.unicode
                
        inputtext_surface=font1.render((PlayerName),False,(255,255,255))        
        screen.blit(blank_surface,((ScreenWidth/2-235,ScreenHeight/2-70,400,100)))
        screen.blit(inputtext_surface,(ScreenWidth/2-165,ScreenHeight/2-30,400,100))
        screen.blit(text_surface,(ScreenWidth/2-280,ScreenHeight/4))
        

        
        confirmbutton.update()
        pygame.display.update() 



MenuScreen(settings)

