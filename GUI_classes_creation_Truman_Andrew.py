#Credits to: https://www.pygame.org/project-Typing+Game-1959-.html
#We derived and learned most of our text implementation from this program

#The reason for UTP-8 (8 space indentation)
#https://stackoverflow.com/questions/5685406/inconsistent-use-of-tabs-and-spaces-in-indentation

#May 31, 2018
#ICS3U1 - 01
#Truman Jian and Andrew Huang
#Final summative program
#Mr.Saleem

#Import libraries. From pygame.locals import can import local files

import pygame, sys, time
from pygame.locals import *

back_splash1 = pygame.image.load("background1.jpg")
back_splash1 = pygame.transform.scale(back_splash1,(800,700))

back_splash2 = pygame.image.load("background5.jpg")
back_splash2 = pygame.transform.scale(back_splash2,(800,600))

back_splash3 = pygame.image.load("background3.jpg")
back_splash3 = pygame.transform.scale(back_splash3,(800,600))



size = (width, height) = (800,700)
                                   
#Create sprites
                    


class TextInput(pygame.Surface):

    #Initializes with the following parameters
    
        def __init__(self, pos, font_size, size, text="", margin=0, text_colour = (10,10,10),\
                background_colour= (240,240,240)):
    
                    super().__init__(size)

        #Create objects associated with the variables
        
                    self.speed = 2
                    self.text = text
                    self.active = False
                    self.pos = pos
                    self.size = size
                    self.font_size = font_size
                    self.text_colour = text_colour
                    self.background_colour = background_colour
                    self.margin = margin

                    self.active_bg_colour = self.background_colour[0] - 55, \
                        self.background_colour[1] - 55, self.background_colour[2] - 55
                    
        def onclick(self):

        #Sets the self.active parameter to true, originally set to false
                    self.active = True

    #Can check the poisition of the mouse. Relates to event of mouse and
    #Position of the object
        
        def contains(self, pos):

                return (pos[0] >= self.pos[0] and\
                        pos[1] >= self.pos[1] and\
                        pos[0] <= self.pos[0]+self.size[0] and\
                        pos[1] <= self.pos[1]+self.size[1])
        
    #A function to display text onto the screen
	    
        def blit_on(self, surface):

                if self.active:
                        self.fill(self.active_bg_colour)
                else:
                        self.fill(self.background_colour)

                font = pygame.font.Font(None, self.font_size)
                text = font.render(self.text, 1, self.text_colour)
                self.blit(text, (self.margin,self.margin))
                surface.blit(self, self.pos)

        def key_get_pressed(self, key):
            
            #The text adds whatever the chr of the key, that is the character

                self.text += chr(key)

#Create a class to create captions, inherits pygame.Surface              
class Caption(pygame.Surface):

    #Create objects associated with the variables

        def __init__(self, pos, font_size, size, font, text,\
                     text_colour):
                pygame.Surface.__init__(self, size)
                
                self.text = text
                self.pos = pos
                self.size = size
                self.font = font
                self.font_size = font_size
                self.text_colour = text_colour

        #A function to display the text on the screen
                
        def blit_on(self, surface):
                
                font = pygame.font.SysFont(self.font, self.font_size)
                text = font.render(self.text, True, self.text_colour)
                surface.blit(text, (self.pos))
        

#Creates a class named button. Inherits pygame.Surface
class Button(pygame.Surface):

    #Initializing function for the creation of buttons
                                    
        def __init__(self, pos, size, colour, margin, fontsize, caption="", text_colour = (0,0,0)):

                pygame.Surface.__init__(self, size)

    #Create objects associated with the variables
                                
                self.onclick = None
                self.pressed = False
                self.hover = False
                                        
                self.caption = caption
                self.pos = pos
                self.size = size
                self.colour = colour
                self.text_colour = text_colour
                self.fontsize = fontsize
                
                self.margin = margin

    #Modifies existing colours for different scenarios
                                
                self.hover_colour = (min(self.colour[0]+100,255), \
                        min(self.colour[1]+100,255),min(self.colour[2]+100,255))
                self.neutral_colour = (min(self.colour[0]+50,255), \
                        min(self.colour[1]+50,255),min(self.colour[2]+50,255))

    #A function to display and detect the button
        def blit_on(self, surface):
                #Fills in colour accordingly
                                        
                if self.hover == True: 

                        self.fill(self.hover_colour)
                                        
                else:
                        self.fill(self.neutral_colour)

                font = pygame.font.Font(None,self.fontsize)
                text = font.render(self.caption, 1, self.text_colour)
                self.blit(text, (self.margin,self.margin))
                surface.blit(self, self.pos)
            
    #A function to detect the position of the mouse cursor
        def contains(self, pos):
                return (pos[0] >= self.pos[0] and\
                 pos[1] >= self.pos[1] and\
                 pos[0] <= self.pos[0]+self.size[0] and\
                 pos[1] <= self.pos[1]+self.size[1])

#Creates a BeginGUI class loop, which is responsible for the initial menu screen
class BeginGUI():

        def __init__(self, size):

                #Initialize and create list for the classes to be stored
                pygame.init()
                self.screen = pygame.display.set_mode(size)
                self.screen_name = pygame.display.set_caption('Asteroid Apocolypse - Menu Screen')
                self.button_start = []
                self.start_captions = []

        def run_initial(self):

                #Checks the condition of the global variable of the loop before beginning
                
                begin_running = self.check_boolean_begin_running
                while begin_running:
                                #Events
                                for event in pygame.event.get():
                                        if event.type == QUIT:
                                                pygame.quit()

                                        #Detects current status of the cursor
                                        elif event.type == MOUSEMOTION:
                                                for button in self.button_start:
                                                        if button.contains(event.pos): 
                                                                button.hover = True
                                                        else: 
                                                                button.hover = False
                                                                button.pressed = False

                                        #Detects if button had been pressed
                                             
                                        elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                                                for button in self.button_start:
                                                                        
                                                        if button.contains(event.pos): 
                                                                button.pressed = True

                                        #Activates what the button intends. Returns conditions to determine other
                                        #parts of the program
                                        
                                        elif event.type == MOUSEBUTTONUP and event.button == 1:

                                                for button in self.button_start:
                                                                
                                                        if button.pressed and button.onclick != None: 
                                                                initiate_game = button.onclick()
                                                                if initiate_game == 'easy':
                                                                        difficulty = 'easy'
                                                                        return difficulty
                                                                        begin_running = False
                                                                elif initiate_game == 'intermediate':
                                                                        difficulty = 'intermediate'
                                                                        return difficulty
                                                                        begin_running = False
                                                                elif initiate_game == 'expert':
                                                                        difficulty = 'expert'
                                                                        return difficulty
                                                                        begin_running = False
                                                                

                                                        button.pressed = False
                                            
                                #Draw/ update
                                                        
                                self.screen.blit(back_splash3,(0,0))
                                                        
                                for button in self.button_start:
                                        button.blit_on(self.screen)

                                for caption in self.start_captions:
                                        caption.blit_on(self.screen)

                                pygame.display.update()

                                #The rest of the attributes and objects will be completed in the other program
                pygame.quit()

        #Cross program referance. Checks what this function does on the other program

        def check_boolean_begin_running(self):
                pass

#Creates the loop for the main game                                        
class GUI_typing(pygame.sprite.Sprite):

            def __init__(self, size):

                        #Initializes the screen
                        global running                
                        pygame.init()
                        self.clock = pygame.time.Clock()
                        self.screen = pygame.display.set_mode(size)

                        #Create sprite groups 
                        self.screen_name = pygame.display.set_caption('Asteroid Apocolypse - Running')
                        self.allsprites = pygame.sprite.Group()
                        self.asteroids = pygame.sprite.Group()
                        self.bullets = pygame.sprite.Group()
                        self.cannon = pygame.sprite.Group()
                        self.explosions = pygame.sprite.Group()
                        self.cannon_images = pygame.sprite.Group()

                        #Creates lists for the sprites
                        
                        self.sound = pygame.mixer.Sound("Explosion.wav")
                        self.buttons = []
                        self.captions = []
                        self.sprites = []
                        self.life_sprites = []
                        self.text_inputs = []
                        
            #Main game running loop      
            def run(self):

                    #Set boolean values
                    double_exit = False
                    running = self.check_boolean_running()
                    
                    while running:

                                #events
                                for event in pygame.event.get():
                                        if event.type == QUIT:
                                                running = False

                                        #Detection of mouse cursor
                                        elif event.type == MOUSEMOTION:
                                                for button in self.buttons:
                                                        if button.contains(event.pos): 
                                                                button.hover = True
                                                        else: 
                                                                button.hover = False
                                                                button.pressed = False

                                        #Determines if a button is pressed
                                        elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                                                for button in self.buttons:
                                                        
                                                        if button.contains(event.pos): 
                                                                button.pressed = True

                                                #Enables text to be input      
                                                for text_input in self.text_inputs:
                                                        
                                                        if text_input.contains(event.pos):

                                                                text_input.onclick()
                                                        else:
                                                                text_input.active = False
                                                                
                                        #Determines what the button does, and what values returned
                                        elif event.type == MOUSEBUTTONUP and event.button == 1:

                                                for button in self.buttons:
                                                
                                                        if button.pressed and button.onclick != None: 
                                                                 flag = button.onclick()
                                                                 if flag == False:
                                                                        running = False
                                                                 if flag == 'double_exit':
                                                                        reset_exit = True
                                                                        return reset_exit
                                                                        running = False

                                                        button.pressed = False

                                        #Detects for input of text
                                        elif event.type == KEYDOWN:
                                                
                                                for text_input in self.text_inputs:

                                                        if text_input.active:
                                                                text_input.key_pressed(event.key)
                                                                   
                                #Updates
                                                                
                                self.inloop()

                                #Kills sprites accordingly

                                life_value = self.live_counter_check()
                                if life_value == False:
                                        live_counter = 3
                                        running = False

                                elif life_value == 1:
                                        self.live_image.kill()
                                        
                                elif life_value == 2:
                                        self.live_image1.kill()        
                                        
                                self.allsprites.update()

                                self.hits = pygame.sprite.groupcollide(self.bullets, self.asteroids, True, True)
                                for hit in self.hits:
                                        self.sound.play()
                                        self.sprites.remove(self.sprites[0])
                                        self.spawn_explosions(hit.rect.center)
                                
                                self.screen.blit(back_splash1,(0,0))

                                self.clock.tick(60)

                                #Draw sprites
                                
                                for button in self.buttons:
                                        button.blit_on(self.screen)
                        
                                for caption in self.captions:
                                        caption.blit_on(self.screen)
                        
                                for text_input in self.text_inputs:
                                        text_input.blit_on(self.screen)


                                self.allsprites.draw(self.screen) 
                                pygame.display.update()

                                #The rest of the attributes and objects will be completed in the other program
                                
            #Functions used from the other program
            def inloop(self):
                pass

            def live_counter_check(self):
                pass
        
            def spawn_explosions(self, exp_x, exp_y):
                pass

            def draw_lives(self, x, y, lives):
                pass

            def check_boolean_running(self):
                pass

#Creates finsih GUI class, end screen
class FinishGUI():

        def __init__(self, size):

                #Initialize and establish lists
                
                pygame.init()
                self.screen = pygame.display.set_mode(size)
                self.screen_name = pygame.display.set_caption('Asteroid Apocolypse - Game Over Screen')
                self.button_end = []
                self.end_captions = []

        #Runs end screen 
        def run_final(self):

                end_running = True
                while end_running:
                                #Events
                                for event in pygame.event.get():

                                        #Determines to quit the global loop in the other program
                                        if event.type == QUIT:
                                                quit_global_flag = True
                                                return quit_global_flag
                                                end_running = False

                                        #Detects mouse cursor status
                                        elif event.type == MOUSEMOTION:
                                                for button in self.button_end:
                                                        if button.contains(event.pos): 
                                                                button.hover = True
                                                        else: 
                                                                button.hover = False
                                                                button.pressed = False

                                        #Determines if button is clicked   
                                        elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                                                for button in self.button_end:
                                                                        
                                                        if button.contains(event.pos): 
                                                                button.pressed = True
                                                                
                                        #Executes the function of the clicked button, and returns their values
                                        elif event.type == MOUSEBUTTONUP and event.button == 1:

                                                for button in self.button_end:
                                                                
                                                        if button.pressed and button.onclick != None: 
                                                                final_response = button.onclick()
                                                                if final_response == False:
                                                                        quit_global_flag = True
                                                                        return quit_global_flag
                                                                        end_running = False
                                                                if final_response == 'back':
                                                                        end_running = False
                                                                

                                                button.pressed = False
                                           
                                #Draw / Update
                                                
                                self.screen.blit(back_splash2,(0,0))
                                                        
                                for button in self.button_end:
                                        button.blit_on(self.screen)

                                for caption in self.end_captions:
                                        caption.blit_on(self.screen)

                                pygame.display.update()

                                #The rest of the attributes and objects will be completed in the other program

                

        
