from Setting import *

class Button:
    def __init__(self,rect,fg = None,text = "",font_size = 32,text_color = (255,255,255),border_width = None,border_color = None,font = "assets/FC_Friday_Medium.ttf"):
        '''
        :param rect: (x,y,w,h) of button
        :param fg: color of button
        :param text_color: color of text
        :param text: text its self
        :param font_size: font size
        :param screen: screen
        :param border_color: color of border
        '''
        self.rect = rect
        self.text_color = text_color
        self.screen = SCREEN

        self.color = fg
        self.border_color = border_color
        self.border_width = border_width

        self.clicked = False

        self.font = pygame.font.Font(font, font_size)
        self.text = self.font.render(text, True, text_color).convert_alpha()
        self.text_rect = self.text.get_rect()
        self.text_x = self.rect[0]+(self.rect[2] - self.text_rect[2])/2
        self.text_y = self.rect[1]+(self.rect[3] - self.text_rect[3])/2

    def is_clicked(self):
        if self.clicked:
            self.clicked = False
            return True
        else:
            return False

    def run(self):
        self.clicked = False

        pos = (-1, -1)
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

        if self.color:
            pygame.draw.rect(self.screen,self.color,self.rect)
        if self.border_color and self.border_width:
            pygame.draw.rect(self.screen,self.border_color,self.rect,self.border_width)

        self.screen.blit(self.text, (self.text_x,self.text_y,self.text_rect[2],self.text_rect[1]))

        if self.rect[0] <= pos[0] <= self.rect[0]+self.rect[2] and self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
            self.clicked = True
