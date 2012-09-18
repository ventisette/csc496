# Functions followed by '*' are not fully document here as they are methods
# that are defined elsewhere.  
import pygame
import sys
from pygame.locals import *
import ctypes

#Initialize the pygame module
pygame.init()

class Window:
#Class Window used to create the window and draw objects to it.
    
#_________________________________Methods______________________________________#
#__init__########################################################################
    def __init__(self, width, height, title=None, background_img = None):
        ''' Name:__init__
            Description: Builds the window drawn to the screen with resolution,
                         background image or color and window title.
            Args: width, height - width and height of the window on start
                  title - title of the window
                  background_img - image drawn to the background of the window
            Called by:  Main to build window, only needs called once.
            Calls:      self.set_background(self, img)
                        self.set_title(self, title)
                        pygame.display.set_mode(resolution=(0,0), flags=0, depth=0)*
            Returns: ...
        '''
        self.SCREEN_WIDTH = width#Used later for fullscreen method.
        self.SCREEN_HEIGHT = height#Used later for fullscreen method.
        self.OLD_SCREEN_WIDTH = 0#Used later for fullscreen method.
        self.OLD_SCREEN_HEIGHT = 0#Used later for fullscreen method.
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)#Builds screen to specified height.
        if title != None:
            self.set_title(title)#Set the title of the window.
        #Checks to see if background_img is none.
        #If yes makes background black,
        #else if it's a tuple sets it to a color,
        #else sets it to an image.
        if background_img == None:
            self.ACTUAL_BACK_IMG = (0, 0, 0)
            self.SCREEN.fill(self.ACTUAL_BACK_IMG)
        elif isinstance(background_img, (list, tuple)):
            self.ACTUAL_BACK_IMG = background_img
            self.SCREEN.fill(self.ACTUAL_BACK_IMG)
        else:
            self.set_background(background_img)


#full_screen######################################################################## 
    def full_screen(self):
        ''' Name:full_screen
            Description: Full screens the window for windows, mac and linux computers.
            Args: ...
            Called by: Main calls this function to full screen the window.  
            Calls: subprocess.Popen(command, , )*
                   self.set_screen_dimensions(*args)                   
                   pygame.display.set_mode(resolution, flags=0, depth=0)*
                   user32.GetSystemMetrics( )*
                   self.set_background(img)
            Returns: ...
        '''
        try: #Try catch clause used as a way to determine if fullscreen should open for windows, mac or linux.
            user32 = ctypes.windll.user32
            screen = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) #Get resolution of monitor
        except Exception as e:
            process = subprocess.Popen("xrandr | grep '*'", shell = True, stdout = subprocess.PIPE, )
            output = process.communicate()[0]
        self.OLD_SCREEN_WIDTH = self.SCREEN_WIDTH #Store the original window screen width.
        self.OLD_SCREEN_HEIGHT = self.SCREEN_HEIGHT #Store the original window screen height.
        self.set_screen_dimensions(screen)#Set the new resolution.
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), FULLSCREEN)#Re-create the window.
        if isinstance(self.ACTUAL_BACK_IMG, (list, tuple) or self.ACTUAL_BACK_IMG == None):
            pass
        else:
            self.set_background(self.ACTUAL_BACK_IMG)
        self.draw_background() #Re-draw the background.
        
#exit_full_screen########################################################################         
    def exit_full_screen(self, screen_width, screen_height):        
        ''' Name: exit_full_screen
            Description: If the full_screen method is called this reverses it.
                         Or it does nothing if full_screen is not called.
            Args: screen_width - width of window on exiting full screen
                  screen_height - height of window on exiting full screen
            Called by: Main calls this function to exit full screen window.
            Calls: self.set_screen_dimensions(*args)
                   pygame.display.set_mode(resolution, flags, depth)*
                   self.set_background(img)
                   self.draw_background()
                   Returns: ...
        '''
        self.OLD_SCREEN_WIDTH = self.SCREEN_WIDTH
        self.OLD_SCREEN_HEIGHT = self.SCREEN_HEIGHT
        self.set_screen_dimensions(screen_width, screen_height)
        self.SCREEN = pygame.display.set_mode((screen_width, screen_height), 0, 32) #Resizes the window from full screen.
        if isinstance(self.ACTUAL_BACK_IMG, (list, tuple) or self.ACTUAL_BACK_IMG == None):
            pass
        else:
            self.set_background(self.ACTUAL_BACK_IMG)
        self.draw_background()#Draws the background to the window.

#overlay######################################################################## 
    def overlay(self):
        '''Name: overlay
           Description: Draws the overlay if set over the window.
           Args: ...
           Called by: Main when ready to draw the overlay, should be after the self.draw methods.
           Calls: self.draw(Surface, location)
           Returns: ...
        '''
        self.draw(self.OVERLAY, (0, 0))
        
#draw########################################################################      
    def draw(self, source_pos, destination_pos):
        '''Name: draw
           Description: Draws or "blits" a surface to the destination given.
           Args: source_pos - Original surface source.
                 destination_pos - Where you want the source_pos to be drawn to.
           Called by: Main when you want to draw something.  
           Calls: Surface.blit(Surface, Rect)*
           Returns: ...
        '''
        self.SCREEN.blit(source_pos, destination_pos)
        
#update######################################################################## 
    def update(self):
        '''Name: update
           Description: Refreshes the application window, redraws everything.
           Args: ...
           Called by: Main after all the draw methods.
           Calls: pygame.display.update()*
           Returns: ...
        '''
        pygame.display.update()#refreshes the application window

#update_explicit######################################################################## 
    def update_explicit(self, update_list):
        '''Name: update_explicit
           Description: Same as update but explicitly for certain surfaces.
           Args: update_list - list of surfaces to updated
           Called by: Main after all the draw methods.
           Calls: pygame.display.update(Surface, Suraface list)*
           Returns: ...
        '''
        pygame.display.update(self.SCREEN, update_list)

    """
    """
#draw_background######################################################################## 
    def draw_background(self):
        '''Name: draw_background
           Description: Redraws the background whether it be a color or image.  Each way
                        handled a little differently. Sets up the image for the background window 
           Args: ...
           Called by: full_screen(screen_width, screen_height)
                      exit_fullscreen(screen_width, screen_height)
           Calls: Surface.fill(color, rect, special_flags)*
           Returns: ...
        '''
        if isinstance(self.ACTUAL_BACK_IMG, (list, tuple)):
            self.SCREEN.fill(self.ACTUAL_BACK_IMG)
        else:
            self.SCREEN.blit(self.SCREEN_BACK_IMG, (0, 0) )#copies the background image created earlier to the screen
            
#write######################################################################## 
    def write(self, text, location, color = (255, 255, 255)):
        '''Name: write
           Description: Allows for text to be written to the screen.
           Args: text - The text you want to display on the window.
                 location - Where the text should be printed to the window.
                 color - Text color.
           Called by: Main with other draw statements from this module.
           Calls: self.FONT.render(string, , color)*
                  self.draw(Surface, rect)
           Returns: ...
        '''
        source = self.FONT.render(str(text), 1, color)
        destination = source.get_rect()
        destination.center = location
        self.draw(source, destination)

#check_quit_event######################################################################## 
    def check_quit_event(self):
        '''Name: check_quit_event
           Description: Checks to see if the window is close. 
           Args: ...
           Called by: Main method right before the update event 
           Calls: pygame.quit()*
           Returns: ...
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                pygame.quit()
        
##Needs work, I'll fix it later when the project is closer to completion.
#    def resize(self, *args):
#        print args
#        for objects in args:
#            print objects
#            obj_ary = list(objects[0])
#            obj_size = objects[1]
#            if objects[2] != None:
#                increase_size_x = objects[2]
#            else:
#                increase_size_x = 0
#            if objects[3] != None:
#                increase_size_y = objects[3]
#            else:                    
#                increase_size_y = 0
#            for obj in obj_ary:
#                if self.OLD_SCREEN_WIDTH != 0 or self.OLD_SCREEN_HEIGHT != 0:
#                    x_ratio = round((obj.X + (obj.WIDTH/2)) / self.OLD_SCREEN_WIDTH, 10)
#                    y_ratio = round((obj.Y + (obj.HEIGHT/2)) / self.OLD_SCREEN_HEIGHT, 10)
#                else:
#                    x_ratio = round((float(self.SCREEN_WIDTH)/float((self.SCREEN_WIDTH*2))), 1)
#                    y_ratio = round((float(self.SCREEN_HEIGHT)/float((self.SCREEN_HEIGHT*2))), 1)
#                obj.WIDTH = (self.SCREEN_WIDTH/obj_size) + increase_size_x
#                obj.HEIGHT = (self.SCREEN_HEIGHT/obj_size) + increase_size_y
#                obj.X = (self.SCREEN_WIDTH * x_ratio) - obj.WIDTH/2
#                obj.Y = (self.SCREEN_HEIGHT * y_ratio) - obj.HEIGHT/2
#                surf = pygame.Surface((obj.WIDTH, obj.HEIGHT), 0, obj.IMG)
#                obj.IMG = pygame.transform.smoothscale(obj.IMG, (obj.WIDTH, obj.HEIGHT), surf) 
#                surf = pygame.Surface((obj.WIDTH, obj.HEIGHT), 0, obj.IMG)
#                return surf
##

#_________________________________getters______________________________________#
#get_screen_width########################################################################
    def get_screen_width(self):
        '''Name: get_screen_width
           Description: Returns the windows width
           Args: ...
           Called by: ...
           Calls: ...
           Returns: self.SCREEN_WIDTH - Current width of the window.
        '''
        return self.SCREEN_WIDTH

#get_screen_height########################################################################    
    def get_screen_height(self):
        '''Name: get_screen_height
           Description: Returns the windows height
           Args: ...
           Called by: ...
           Calls: ...
           Returns: self.SCREEN_HEIGHT - Current height of the window.
        '''
        return self.SCREEN_HEIGHT
    
#_________________________________setters______________________________________#
#set_title########################################################################
    def set_title(self, title):
        '''Name: set_title
           Description: Sets the title of displayed window.
           Args: title - The title you want give the window.
           Called by: __init__
           Calls: pygame.display.set_caption(title, icontitle)*
           Returns: ...
        '''
        self.TITLE = title
        pygame.display.set_caption(title, title)

#set_font#######################################################################
    def set_font(self, Filename, size):
        '''Name: set_font
           Description: Changes the font for the write method.  Once
                        the font is created it cannot be changed.
           Args: Filename - Filename to load a new font from or python file object
                 size - height of the font in pixels
           Called by: ...
           Calls: pygame.font.Font(filename/object, size)
           Returns: ...
        '''
        #look into using pygame.freetype module, much better than this
        self.FONT = pygame.font.Font(Filename, size)
        
#set_overlay_transparency######################################################################## 
    def set_overlay_transparency(self, opacity=255):
        ''' Name: set_overlay_transparency
            Description: Sets the transparency of the overlayed image.
            Args: opacity - level of transparency of overlay (not quite working right with images yet)
            Called by: What ever you want when you want to use it.
            Calls:  Surface.set_alpha(opacity)*
            Returns: ...
        '''
        self.OVERLAY.set_alpha(opacity)

#set_background_overlay########################################################################            
    def set_background_overlay(self, overlay = None, opacity=255):        
        ''' Name: set_background_overlay
            Description: Sets an overlay of an image or color over the entire screen.
            Args: overlay - tuple/list or image to lay over window.
                  opacity - level of transparency of overlay (not quite working right with images yet)
            Called by:  Main when you want to lay something over the window.
            Calls:  pygame.surface(resolution)*
                    Surface.fill( )*
                    pygame.image.load( )*
            Returns: ...
        '''
        if isinstance(overlay, (list, tuple)):
            self.OVERLAY = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.OVERLAY.fill(overlay)
        elif isinstance(overlay, str):
            self.OVERLAY = pygame.image.load(overlay).convert_alpha() #Set alpha is used for transparent images.
        self.OVERLAY.set_alpha(opacity) #Set alpha is to set level of transparency for surface.

#set_screen_dimensions########################################################################
    def set_screen_dimensions(self, *args):
        ''' Name: set_screen_dimensions
            Description: Sets the width and height of the window.
            Args: *args - designed for tuples and multiple values EX: funct(x, y) or funct((x, y))
            Called by: exit_full_screen(screen_width, screen_height)
                       full_screen(screen_width, screen_height) 
            Calls: ...
            Returns: ...
        '''
        if len(args) == 1:
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = args[0]
        else:
            self.SCREEN_WIDTH = args[0]
            self.SCREEN_HEIGHT = args[1]

#set_background######################################################################## 
    def set_background(self, img):
        ''' Name:set_background
            Description: Sets the background window image or color
                         based on the type of argument passed into
                         the method, whether it's a tuple/list or
                         a string.  Must be one of the three.
            Args:   img - tuple/list or string, what's displayed in the window background
            Called by:  __init__
            Calls:  pygame.image.load(filename).convert()*
                    pygame.transform.smoothscale(surface, (resolution), destination surface)*
            Returns: ...
        '''
        if isinstance(img, (list, tuple)):
            self.ACTUAL_BACK_IMG = img
        else:
            self.ACTUAL_BACK_IMG = img
            background_img = pygame.image.load(img).convert()#Converts the image to a format useable by python.
            self.SCREEN_BACK_IMG = background_img
            self.SCREEN_BACK_IMG = pygame.transform.smoothscale(self.SCREEN_BACK_IMG, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))#Stretches image to fill area.

