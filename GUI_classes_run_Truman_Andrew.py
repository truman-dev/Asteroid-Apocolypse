#!/usr/bin/env python

#Note: Correct program to run!

#May 31, 2018
#ICS3U1 - 01
#Truman Jian and Andrew Huang
#Final summative program
#Mr.Saleem



# import the previous program to inherit
# import other libraries



import GUI_classes_creation_Truman_Andrew, random, time, pygame

back_splash4 = pygame.image.load("background4.png")
back_splash4 = pygame.transform.scale(back_splash4,(800,600))

back_splash5 = pygame.image.load("background2.jpg")
back_splash5 = pygame.transform.scale(back_splash5,(800,700))

pygame.mixer.init()
pygame.mixer.music.load("main_music2.wav")
pygame.mixer.music.play(-1,0)

#Initiate variables associated with the game function

size = (width, height) = (800,700)
half_width = width/2
height_adjustment = height - 100

#Initate global loop to control the entire program
global_loop = True

#Creating a Bullet class, inherits sprites class

class Bullet(pygame.sprite.Sprite):

        def __init__(self, bullet_x, bullet_y):

                #Call parent class constructor, initialize               
                pygame.sprite.Sprite.__init__(self)            
                self.image = pygame.image.load("bullet.png")
                self.image = pygame.transform.scale(self.image,(30,30))
                self.rect = self.image.get_rect()
                
                #determine position
                
                self.rect.centerx = bullet_x
                self.rect.bottom = bullet_y
                
                #set the bullet speed
                
                self.speedy=10

        def update(self):

                #Condition for destruction of sprite
                
                self.rect.y -= self.speedy
                if self.rect.bottom < 0:
                    self.kill()



class Explosion(pygame.sprite.Sprite):

        def __init__(self, center):

                #Call parent class and initialize sprite
                
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("explosion2.png")
                self.image = pygame.transform.scale(self.image,(60,60))
                self.rect = self.image.get_rect()

                #Detect the centre of the explosion
                
                self.rect.center = center
                self.last_update = pygame.time.get_ticks()
                self.frame_rate = 100
        
        def update(self):

                #Condition for sprite destruction.
                
                now = pygame.time.get_ticks()
                if now - self.last_update > self.frame_rate:
                        self.kill()

class Asteroid(pygame.sprite.Sprite):

        def __init__(self):

                #Call parent class and initialize sprite
                                   
                pygame.sprite.Sprite.__init__(self) #Call parent class constructor
                self.image = pygame.image.load("asteroid.png")
                self.image = pygame.transform.scale(self.image,(100,100))
                self.rect = self.image.get_rect()
                                   
                #Set the position
                self.rect.x = random.randint(0,width - 60)
                self.rect.y = random.randint(-20,0)
                self.speedy = 1

                
        def update(self):

                #Update function
                
                global live_counter
                self.rect.y += self.speedy

                #Detects if asteroid reaches the screen, updates live counter
                
                if self.rect.bottom > height - 50:
                    self.rect.x = random.randint(0,width - 60)
                    self.rect.y = random.randint(-20,0)
                    live_counter -= 1      
                    return live_counter
                    
class Cannon_image(pygame.sprite.Sprite):

        def __init__(self, image_x, image_y):

                pygame.sprite.Sprite.__init__(self)

                self.image = pygame.image.load("spaceship.png")
                self.image = pygame.transform.scale(self.image,(45,45))
                self.rect = self.image.get_rect()

                self.rect.x = image_x
                self.rect.y = image_y

        def update(self):
                pass

class Cannon(pygame.sprite.Sprite):

        def __init__(self):
                
                super().__init__() #Call parent class constructor

                #Call parent class and initialize sprite
                
                self.image = pygame.image.load("spaceship.png")
                self.image = pygame.transform.scale(self.image,(80,80))
                self.rect = self.image.get_rect()
                
                #initialize the position of the Cannon
        
                self.rect.x = width/2 - 40
                self.rect.bottom = height - 90
                self.speedx=5

        def update(self):

                global half_width
                
                keys=pygame.key.get_pressed() #Detects if key is pressed

                #Keys allow adjustment of ship's position
                
                if keys[pygame.K_LEFT]:
                    self.rect.x -= self.speedx
                    half_width = self.rect.x + 40 - self.speedx

                    
                if keys[pygame.K_RIGHT]:
                    self.rect.x += self.speedx
                    half_width = self.rect.x + 40 + self.speedx

                #constrain the ship to the screen, checks conditions
                    
                if self.rect.left < 0:
                    self.rect.right = width
                    
                if self.rect.right > width:
                    self.rect.left= 0

                return half_width, self.rect.top

              
class Type_TextInput(GUI_classes_creation_Truman_Andrew.TextInput):
    
        def __init__(self):
                super().__init__((10, 600), 100, (780, 80))

        #Create class that enables text to be inputted

        def key_pressed(self, key):

	#Enter key allows current text inputted to be erase
                
                if key == 13:
                        self.text = ""
                        
	# BACKSPACE, deletes last element of list
                elif key == 8:
                        self.text = self.text[:-1]

        #Allows characters to be inputted in the list
                        
                elif key in range(256):
                        self.text += chr(key)

#Activate GUI class allows the creation of the game loop. Inherits the loop and other classes
#In order to be created
                        
class ActivateGUI(GUI_classes_creation_Truman_Andrew.GUI_typing, Bullet, Cannon_image, Explosion, Asteroid,  Cannon):

        def __init__(self):
                
                #Initalizes the screen size and loop
                GUI_classes_creation_Truman_Andrew.GUI_typing.__init__(self,(800,700))

                #Initializes classes that are imported
                Bullet.__init__(self, 0, 0)
                Cannon_image.__init__(self, 0,0)
                Explosion.__init__(self, (10,10))
                Asteroid.__init__(self)
                Cannon.__init__(self)
                
                global word_counter, a

                #Creates a list from reading of text file of words
                #Allows a random word from the list to be chose that will be displayed
                #The word lists that the compiler reads off depends on the difficulty of the game
                
                self.words = []
                if difficulty == 'easy':
                        self.read_wordlist("wordlist1.txt")
                elif difficulty == 'intermediate':
                        self.read_wordlist("wordlist2.txt")
                elif difficulty == 'expert':
                        self.read_wordlist("wordlist3.txt")
                        
                self.word = random.choice(self.words)
                self.word_counter = 0
                self.character_counter = 0
                self.start_time = time.time()

                # Creates various buttons objects. The functions used are listed later on.

                pause_button = GUI_classes_creation_Truman_Andrew.Button((600,10), (50,30), (200, 100, 0),(5,10),16,"PAUSE")
                pause_button.onclick = self.pause_button_clicked
                self.buttons.append(pause_button)
                
                exit_button = GUI_classes_creation_Truman_Andrew.Button((720,10), (50,30),(0, 100, 200), (10,10),16,"EXIT")
                exit_button.onclick = self.exit_button_clicked
                self.buttons.append(exit_button)

                reset_button = GUI_classes_creation_Truman_Andrew.Button((650,10), (70,30),(0, 200, 100),(2,10),16,"MENU MENU")
                reset_button.onclick = self.reset_button_clicked
                self.buttons.append(reset_button)

                # Creates captions object and displays it on the screen.

                self.word_caption = GUI_classes_creation_Truman_Andrew.Caption((10, 50), 60, (800, 100),"Impact", self.word,(255,255,255))
                self.captions.append(self.word_caption)
                        
                self.info_caption = GUI_classes_creation_Truman_Andrew.Caption((10, 10), 20, (450, 40), "Times New Roman","",(255,255,255))
                self.captions.append(self.info_caption)

                self.info_caption1 = GUI_classes_creation_Truman_Andrew.Caption((600, 50), 20, (450, 40),"Times New Roman","",(0,0,0))
                self.captions.append(self.info_caption1)

                #The creates an object from input text function.
                
                self.input_word = Type_TextInput()
                self.input_word.active = True
                self.text_inputs.append(self.input_word)


                #Spawns the initial cannon and asteroids.
                
                self.spawn_asteroids(3)
                self.spawn_cannon()

                self.draw_lives(600,70, 2)
       
        #Function: checks if the amount of sprites fall below 2, and then spawns more asteroids
        def check_sprites(self):

                if len(self.sprites) < 4:
                        self.spawn_asteroids(1)

                if len(self.sprites) > 4:
                        self.sprites.remove(self.sprites[0])

        #Function to spawn asteroids. Adds to allsprites, the individual group and the list.
        def spawn_asteroids(self,amount):
                for i in range (amount):
                        asteroid= Asteroid()
                        self.allsprites.add(asteroid)
                        self.asteroids.add(asteroid)
                        self.sprites.append(asteroid)

        #Function to spawn cannons. Adds to allsprites, and the individual group
        def spawn_cannon(self):
                cannon = Cannon()
                self.cannon.add(cannon)
                self.allsprites.add(cannon)
        
        def draw_lives(self, x, y, lives):

                for i in range(lives):
                        
                        image_x = x + i * 50
                        image_y = y
                        self.live_image = Cannon_image(image_x, image_y )
                        self.cannon_images.add(self.live_image)
                        self.allsprites.add(self.live_image)
                        self.life_sprites.append(self.live_image)

                image_x = x + 2 * 50
                image_y = y
                self.live_image1 = Cannon_image(image_x, image_y )
                self.cannon_images.add(self.live_image1)
                self.allsprites.add(self.live_image1)
                self.life_sprites.append(self.live_image1)
                

        #Function to spawn explosions. Adds to allsprites, and the individual group
        def spawn_explosions(self, center):

                explosion = Explosion(center) 
                self.allsprites.add(explosion)
                self.explosions.add(explosion)

        #Function to shoot the bullet. Allows creation of bullet object.      
        def shoot(self,bullet_x,bullet_y):

                bullet = Bullet(bullet_x,bullet_y)
                self.bullets.add(bullet)
                self.allsprites.add(bullet)

        #Defines the function for the exit_button. Sets boolean conditions allowing to exit the loop               
        def exit_button_clicked(self):
                
                flag = False
                return flag

        #The pause buttons creates a new loop, which runs until the user enters a response.
        def pause_button_clicked(self):

                #Creates a list of buttons to appended
                
                self.pause_buttons = []
                pause_running = True
                while pause_running:
                            
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pause_running = False

                            elif event.type == pygame.MOUSEMOTION:
                                for button in self.pause_buttons:
                                    
                                    if button.contains(event.pos): 
                                            button.hover = True
                                            
                                    else: 
                                            button.hover = False
                                            button.pressed = False
                                            
                            #Uses mechanism  to detect cursor position inherited from button class
                                
                            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                                for button in self.pause_buttons:
                                                        
                                    if button.contains(event.pos): 
                                        button.pressed = True

                            #Allows detection of whether the button is clicked. Returns
                            #The boolean condition

                            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                                for button in self.pause_buttons:
                                                
                                        if button.pressed and button.onclick != None:
                                                response = button.onclick()

                                                if response == False:

                                                        pause_running = False

                                                elif response == "Quit Game":

                                                        flag = False
                                                        return flag
                                                        pause_running = False     

                                        button.pressed = False

                             #checks if button has been pressed, and then executes the button's
                             #Supposed function.

                        #Creation of the button objects
                                        
                        self.screen.blit(back_splash5,(0,0))
                        exit_pause_button = GUI_classes_creation_Truman_Andrew.Button((300,250), (200,60), (100, 0, 200),(20,25),30,"BACK TO GAME")
                        exit_pause_button.onclick = self.exit_pause_button_clicked
                        self.pause_buttons.append(exit_pause_button)

                        quit_pause_button = GUI_classes_creation_Truman_Andrew.Button((300,375), (200,60), (220, 20,60),(40,25),30,"QUIT GAME")
                        quit_pause_button.onclick = self.quit_pause_button_clicked
                        self.pause_buttons.append(quit_pause_button)

                        #Draws the button objects onto the screen.
                        
                        for button in self.pause_buttons:
                            button.blit_on(self.screen)

                        pygame.display.update()

        #Function returns a boolean condition, which helps in exiting the loop
                        
        def exit_pause_button_clicked(self):

                response = False
                return response

        #Function that checks for boolean condition of inital loop

        def check_boolean_begin_running(self):

                global begin_running
                return begin_running

        #Function that checksfor boolean condition of main game loop
        
        def check_boolean_running(self): #

                global running
                return running

        #Function allows a condition to be returned, which helps in exiting loops
        def quit_pause_button_clicked(self):

                response = "Quit Game"
                return response

        #Reset button allows to bypass final score screen.            
        def reset_button_clicked(self): #

                flag = 'double_exit'
                return flag    

        #Mechanism allows a new word in the list to be displayed
        #Chosen randomly
        #Also shoots (creation of bullet object) when called
        
        def right_word_entered(self):
                
                    global correct_word_count
                    
                    self.character_counter += len(self.word)
                    self.word_counter += 1
                    self.input_word.text = ""
                    self.word = random.choice(self.words)
                    self.word_caption.text = self.word
                    
                    self.shoot(half_width, height_adjustment)
                    self.check_sprites()

                    correct_word_count += 1
                    return correct_word_count
                
        #Checks on current status of game. Returns either current amount of lives
        #Or a mechanism to quit the game loop.
                
        def live_counter_check(self):
                
                if live_counter <= 0:
                        lose_game = False
                        return lose_game
                else:
                        return live_counter

        #Inloop updates statistics as the game progresses.
        #Also checks if word is entered correctly
                
        def inloop(self):
                
                    global speed, charspeed
                    
                    if self.word_caption.text == self.input_word.text:
                            self.right_word_entered()
                
                    now = time.time()
                    if not self.word_counter == 0:
                            speed = self.word_counter / (now - self.start_time)
                            speed = round(speed, 2)
                            charspeed = 60. * self.character_counter / (now - self.start_time)
                            charspeed = round(charspeed, 2)
                            word_count = self.word_counter
                    self.info_caption.text = "Words typed: " + str(self.word_counter) + \
                        "       speed (words/s): " + str(speed) + "       speed (chars/m): " + str(charspeed)

                    self.info_caption1.text = "Lives Remaining: " + str(live_counter)

                    return speed, charspeed

        #Function to read the current file name. Credited to the program we based our work on.
                
        def read_wordlist(self, filename):
                    f = open(filename, "r")
                    lines = f.readlines()
                    f.close()
                    self.words = []
                    for line in lines:
                            self.words.append(line[:-1].lower())

                    #Works by putting the words on the text editor into a list
                    #Words from the list are then chosen randomly to be displayed


#Class inherits from the class of BeginGUI on the other program. It adds all the sprites and items into the
#Loop to run

class BeginGUI(GUI_classes_creation_Truman_Andrew.BeginGUI):

         def __init__(self):

            super().__init__((800,600))

            #Creation of buttons of each difficulty and tutorial

            button_start1 = GUI_classes_creation_Truman_Andrew.Button((300,220), (220,60),(128,128,128), (37,20),40,"BEGINNER")
            button_start1.onclick = self.start_button_clicked_easy
            self.button_start.append(button_start1)

            button_start2 = GUI_classes_creation_Truman_Andrew.Button((300,300), (220,60),(128,128,128), (5,20),40,"INTERMEDIATE")
            button_start2.onclick = self.start_button_clicked_intermediate
            self.button_start.append(button_start2)

            button_start3 = GUI_classes_creation_Truman_Andrew.Button((300,380), (220,60),(128,128,128), (50,20),40,"EXPERT")
            button_start3.onclick = self.start_button_clicked_hard
            self.button_start.append(button_start3)

            button_tutorial = GUI_classes_creation_Truman_Andrew.Button((300,460), (220,60),(0, 100, 200), (10,20),40,"HOW TO PLAY")
            button_tutorial.onclick = self.tutorial_button_clicked
            self.button_start.append(button_tutorial)

            #Displays the title of the game
            
            self.info_caption1 = GUI_classes_creation_Truman_Andrew.Caption((70,20),80, (700,40),"Impact", "ASTEROID",(255,255,255))
            self.info_caption2 = GUI_classes_creation_Truman_Andrew.Caption((340,90),80, (700,40),"Impact", "APOCOLYPSE",(255,255,255))
            self.start_captions.append(self.info_caption1)
            self.start_captions.append(self.info_caption2)

         #The following functions determine the difficulty, which is which word list to choose from.
         def start_button_clicked_easy(self):

                initiate_game = 'easy'
                return initiate_game

         def start_button_clicked_intermediate(self):

                initiate_game = 'intermediate'
                return initiate_game

         def start_button_clicked_hard(self):

                initiate_game = 'expert'
                return initiate_game

        #The tutorial button generates a loop displaying the tutorial screen

         def tutorial_button_clicked(self):

                #Creates a list of buttons to append and associated boolean
                
                self.tutorial_buttons = []
                self.tutorial_captions = []
                tutorial_running = True
                while tutorial_running:

                        #Events
                        
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                tutorial_running = False

                            elif event.type == pygame.MOUSEMOTION:
                                for button in self.tutorial_buttons:
                                    
                                    if button.contains(event.pos): 
                                            button.hover = True
                                            
                                    else: 
                                            button.hover = False
                                            button.pressed = False
                                            
                            #Uses mechanism  to detect cursor position inherited from button class
                                
                            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                                for button in self.tutorial_buttons:
                                                        
                                    if button.contains(event.pos): 
                                        button.pressed = True

                            #Allows detection of whether the button is clicked. Returns
                            #The boolean condition

                            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                                for button in self.tutorial_buttons:
                                                
                                        if button.pressed and button.onclick != None:
                                                tutorial_response = button.onclick()

                                                if tutorial_response == False:

                                                        tutorial_running = False
   

                                                button.pressed = False

                             #checks if button has been pressed, and then executes the button's
                             #Supposed function.

                        
                        #Creation of the button objects
                                        
                        self.screen.blit(back_splash4,(0,0))
                        
                        self.tutorial_caption1 = GUI_classes_creation_Truman_Andrew.Caption((150,100),50, (700,40),"Impact", "",(255,255,255))
                        self.tutorial_caption1.text = "HOW TO PLAY TUTORIAL"
                        self.tutorial_captions.append(self.tutorial_caption1)

                        self.tutorial_caption2 = GUI_classes_creation_Truman_Andrew.Caption((50,195),30, (700,40),"Times New Roman", "",(255,255,255))
                        self.tutorial_caption2.text = "1. SELECT ONE OF THE FOLLOWING DIFFICULTIES"
                        self.tutorial_captions.append(self.tutorial_caption2)
        
                        self.tutorial_caption3 = GUI_classes_creation_Truman_Andrew.Caption((50,245),30, (700,40),"Times New Roman", "",(255,255,255))
                        self.tutorial_caption3.text = "2. WORD WILL APPEAR IN THE TOP LEFT CORNOR"
                        self.tutorial_captions.append(self.tutorial_caption3)

                        self.tutorial_caption4 = GUI_classes_creation_Truman_Andrew.Caption((50,295),30, (700,40),"Times New Roman", "",(255,255,255))
                        self.tutorial_caption4 .text = "3. POSITION THE CANNON BELOW THE ASTEROID"
                        self.tutorial_captions.append(self.tutorial_caption4)

                        self.tutorial_caption5 = GUI_classes_creation_Truman_Andrew.Caption((50,345),30, (700,40),"Times New Roman", "",(255,255,255))
                        self.tutorial_caption5 .text = "4. TYPE IN THE DISPLAYED WORD TO FIRE"
                        self.tutorial_captions.append(self.tutorial_caption5)
                        
                        exit_tutorial_button = GUI_classes_creation_Truman_Andrew.Button((300,450), (200,60), (100, 0, 200),(20,25),30,"BACK TO MENU")
                        exit_tutorial_button.onclick = self.exit_tutorial_button_clicked
                        self.tutorial_buttons.append(exit_tutorial_button)

                        #Draws the objects
                        for button in self.tutorial_buttons:
                                button.blit_on(self.screen)

                        for caption in self.tutorial_captions:
                                caption.blit_on(self.screen)

                        pygame.display.update()

         def exit_tutorial_button_clicked(self):

                tutorial_response = False
                return tutorial_response

#Creates class EndGUI by inheriting the loop from the other program and then adding the objects
                        
class EndGUI(GUI_classes_creation_Truman_Andrew.FinishGUI):

        def __init__(self):

            super().__init__((800,600))

            global correct_word_count, speed, charspeed

            #The creation of the caption objects
            
            self.info_caption1 = GUI_classes_creation_Truman_Andrew.Caption((40, 190), 31, (700, 40),"Impact", "",(250,250,250))
            self.info_caption1.text = "NUMBER OF WORDS TYPED: " + str(correct_word_count)
            self.info_caption2 = GUI_classes_creation_Truman_Andrew.Caption((40, 240), 31, (700, 40),"Impact", "",(250,250,250))
            self.info_caption2.text = "AVERAGE WORDS TYPED PER SECOND: " + str(speed) + " words/s"
            self.info_caption3 = GUI_classes_creation_Truman_Andrew.Caption((40,290), 31, (700, 40),"Impact", "",(250,250,250))
            self.info_caption3.text = "AVERAGE CHARACTERS TYPED PER MINUTE: " + str(charspeed) + " chars/min"
            self.info_caption4 = GUI_classes_creation_Truman_Andrew.Caption((40,120),45, (700,40),"Impact", "STATISTICS:",(250,250,250))
            self.info_caption5 = GUI_classes_creation_Truman_Andrew.Caption((300,40),60, (700,40),"Impact", "GAME OVER",(255,0,0))

            self.end_captions.append(self.info_caption1)
            self.end_captions.append(self.info_caption2)
            self.end_captions.append(self.info_caption3)
            self.end_captions.append(self.info_caption4)
            self.end_captions.append(self.info_caption5)

            #Creation of button objects
                
            end_button = GUI_classes_creation_Truman_Andrew.Button((280,370), (240,60),(50, 200, 50), (20,20),40,"QUIT SCREEN")
            end_button.onclick = self.end_button_clicked
            self.button_end.append(end_button)

            back_to_main = GUI_classes_creation_Truman_Andrew.Button((280,460), (240,60),(0, 100, 200), (40,20),40,"MAIN MENU")
            back_to_main.onclick = self.back_button_clicked
            self.button_end.append(back_to_main)

        #Functions that define what each button does
            
        def end_button_clicked(self):

            final_response = False
            return final_response

        def back_button_clicked(self):
                
            live_counter = 3
            final_response = 'back'
            return final_response
                
#Inditates this is the main program to run
        
if __name__ == "__main__":

        #global loop controls the relation of BeginGUI, ActivateGUI, and EndGUI
        #pygame quits after it is exited
        
        while global_loop:

                #Define boolean conditions and variables to be used

                running = True
                begin_running = True
                end_flag = True
                
                correct_word_count = 0
                speed = 0
                charspeed = 0
                live_counter = 3

                #creation of the objects from the respective GUI classes
                
                begingui = BeginGUI()
                difficulty = begingui.run_initial()
                activate_gui = ActivateGUI()
                skip_end = activate_gui.run()

                #Checking for boolean conditions to determine when to exit loops

                
                if skip_end == True:
                      end_flag = False  

                if end_flag == True:
                        endgui = EndGUI()
                        condition_global_flag_loop = endgui.run_final()

                        if  condition_global_flag_loop == True:
                                global_loop = False

        #Quits the game
        pygame.quit()
        
        


