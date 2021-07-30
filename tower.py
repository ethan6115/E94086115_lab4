import pygame
import os
import math
from settings import WIN_WIDTH, WIN_HEIGHT  #將視窗大小import

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        x1, y1 = enemy.get_pos()   #獲得enemy的位置
        distance=math.sqrt((self.center[0] - x1)**2 + (self.center[1] - y1)**2)  #算出enemy跟塔的距離
        if distance<=self.radius:   #若是距離小於攻擊範圍則 return True
            return True
        else:
            return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        transparent_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA) #設定surface的大小為視窗大小
        transparency = 40 
        #將圓的位置訂在surface上center的位置
        pygame.draw.circle(transparent_surface, (255, 255, 255, transparency),self.center,self.radius) 
        #將surface的位置訂在視窗的(0,0)，使視窗和surface重和，這樣center的位置就會正確
        win.blit(transparent_surface,[0,0])
       
        


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """
        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        #當cd_count小於cd_max_count時 return False
        if self.cd_count <self.cd_max_count:
            self.cd_count+=1
            return False
        else:       #當cd_count大於等於於cd_max_count時 return True
            self.cd_count=1
            return True

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        
        enemy_list=enemy_group.get()#用get獲得行軍中的list
        enemy_amount=len(enemy_list)#用enemy_amount記錄enemy的數量
        if self.is_cool_down():     #當tower不再冷卻時執行以下
            if enemy_list:          #當list不是空的時候執行以下
                for n in range(0,enemy_amount):
                    target=enemy_list[n]       #從隊列的第一隻enemy一隻一隻看
                    if self.range_circle.collide(target):   #如果target在tower的範圍內
                        target.get_hurt(self.damage)   #tower範圍內的第一隻target受到傷害
                        break                          #然後停止迴圈直到下一次冷卻結束

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        if x-35<=self.rect.center[0]<=x+35 and y-35<=self.rect.center[1]<=y+35:  #如果點擊的位置在圖片的範圍裡就回傳True
            return True
        else:
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

