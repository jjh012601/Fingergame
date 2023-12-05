import global_variables
import pygame, random, time
from menu import Menu

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None,65)
        self.score_font = pygame.font.Font("kenvector_future.ttf",20)
        self.problem = {"num1":0,"num2":0,"result":0}
        self.operation = ""
        self.symbols = self.get_symbols()
        self.reset_problem = False
        items = ("Start", "", "", "")
        self.menu = Menu(items,ttf_font="XpressiveBlack Regular.ttf",font_size=50)
        self.show_menu = True
        self.score = 0
        self.count = 0
        self.background_image = pygame.image.load("background.jpg").convert()
        self.correct = None
        self.correct_time = None

    def get_symbols(self):
        """ Return a dictionary with all the operation symbols """
        symbols = {}
        sprite_sheet = pygame.image.load("symbols.png").convert()
        image = self.get_image(sprite_sheet,0,0,64,64)
        symbols["addition"] = image

        return symbols

    def get_image(self,sprite_sheet,x,y,width,height):
        image = pygame.Surface([width,height]).convert()
        image.blit(sprite_sheet,(0,0),(x,y,width,height))
        return image

    def addition(self):
        """ These will set num1,num2,result for addition """
        a = random.randint(1,5)
        b = random.randint(0,5)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a + b
        self.operation = "addition"

    def check_result(self):
        if self.problem["result"] == global_variables.fingerCount:
            self.score += 5
            self.reset_problem = True
            self.correct_time = time.time()

    def set_problem(self):
        if self.operation == "addition":
            time.sleep(0.5)
            self.addition()

    def process_events(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_menu:
                    if self.menu.state == 0:
                        self.operation = "addition"
                        self.set_problem()
                        self.show_menu = False
                        self.score = 0
                else:
                    self.check_result()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    # set score to 0
                    self.score = 0
                    self.count = 0

        return False

    def run_logic(self):
        self.menu.update()
        if global_variables.fingerCount == self.problem["result"]:
            self.correct = True
            self.correct_time = time.time()  # 정답을 맞춘 시간을 저장합니다.
            time.sleep(0.5)  # 정답을 맞추고 0.5초 동안 대기합니다.


    def display_message(self,screen,items):
        """ display every string that is inside of a tuple(args) """
        for index, message in enumerate(items):
            label = self.font.render(message,True,BLACK)

            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)

            t_h = len(items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            
            screen.blit(label,(posX,posY))
              

    def display_frame(self,screen):

        screen.blit(self.background_image,(0,0))

        time_wait = False
        if self.show_menu:
            self.menu.display_frame(screen)
        elif self.count == 20:
            msg_1 = "You answered " + str(self.score / 5) + " correctly"
            msg_2 = "Your score was " + str(self.score)
            self.display_message(screen,(msg_1,msg_2))
            self.show_menu = True
            # reset score and count to 0
            self.score = 0
            self.count = 0
            time_wait = True
        else:
            label_1 = self.font.render(str(self.problem["num1"]),True,BLACK)
            label_2 = self.font.render(str(self.problem["num2"])+" = ?",True,BLACK)
            t_w = label_1.get_width() + label_2.get_width() + 64
            posX = (SCREEN_WIDTH / 2) - (t_w / 2)
            screen.blit(label_1,(posX,50))
            screen.blit(self.symbols[self.operation],(posX + label_1.get_width(),40))
            screen.blit(label_2,(posX + label_1.get_width() + 64,50))
            score_label = self.score_font.render("Score: "+str(self.score),True,BLACK)
            screen.blit(score_label,(10,10))
            # 스크린에 fingerCount 폰트 출력
            finger_font = pygame.font.Font(None, 150)
            finger_surface = finger_font.render(str(global_variables.fingerCount), True, (0, 0, 0))
            posX = (SCREEN_WIDTH / 2) - (finger_surface.get_width() / 2)
            posY = (SCREEN_HEIGHT / 2)
            screen.blit(finger_surface, (posX, posY))

            if self.correct is not None:  # None이 아니라면 이미 정답 여부가 결정된 상태입니다.
                result_font = pygame.font.Font(None, 300)  # 더 큰 글꼴
                if self.correct:
                    result_surface = result_font.render('O', True, (0, 255, 0))  # 맞았을 때는 초록색 'O'
                    posX = (SCREEN_WIDTH / 2) - (result_surface.get_width() / 2)
                    posY = (SCREEN_HEIGHT / 2) - 50
                    screen.blit(result_surface, (posX, posY))

                    if time.time() -self.correct_time >0.3:
                        self.correct = None

        pygame.display.flip()

        if self.reset_problem:
            self.set_problem()
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            pygame.time.wait(3000)

