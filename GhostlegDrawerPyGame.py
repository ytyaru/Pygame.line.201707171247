import sys, copy, pygame
import Ghostleg
class Main:
    @staticmethod
    def Run(method, title=None):
        pygame.init()
        if title: pygame.display.set_caption(title)
        clock = pygame.time.Clock()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit();
            method()
            """
            self.__screen.Fill()
            self.__draw_vartical_lines()
            self.__draw_horizon_lines()
            self.__draw_goals()
            self.__draw_select_lines()
            """
            pygame.display.flip()
            clock.tick(60) # 60 FPS
        
class Screen:
    def __init__(self, width=320, height=240, color=(0,0,0)):
        self.__color = color
        self.__size = (width, height)
        self.__screen = pygame.display.set_mode(self.__size)
    @property
    def Screen(self): return self.__screen
    @property
    def Size(self): return self.__size
    def Fill(self): self.__screen.fill(self.__color)

# 指定した頂点リストに応じた等速直線アニメーションをする
class LinesAnimation:
    def __init__(self, pointlist, color=(255,0,0), width=2):
        if len(pointlist) < 2: raise Exception('pointlistは少なくとも2つ以上の座標を入れて下さい。例: [[0,0], [0,50]]')
        self.__color = color
        self.__width = width
        self.__pointlist = pointlist
        
        self.__now_pointlist_index = 1
        self.__now_pointlist = [copy.deepcopy(self.__pointlist[0]), copy.deepcopy(self.__pointlist[0])]
        self.__frame = 0
        self.__frame_max = 0
        self.__frame_target = 0
        self.__anime_direct_x = 0
        self.__anime_direct_y = 0
        self.__get_frame_target()
        print(self.__pointlist)
    def draw(self, screen):
        pygame.draw.lines(screen, self.__color, False, self.__now_pointlist, self.__width)
        self.__animation()
    def __animation(self):
        if self.__now_pointlist_index < len(self.__pointlist):
            self.__move()
            self.__set_frame()
    # 移動
    def __move(self):
        rate = self.__frame / self.__frame_max
        self.__now_pointlist[-1][0] = int(self.__pointlist[self.__now_pointlist_index-1][0] + (abs(self.__pointlist[self.__now_pointlist_index][0] - self.__pointlist[self.__now_pointlist_index-1][0]) * rate) * self.__anime_direct_x)
        self.__now_pointlist[-1][1] = int(self.__pointlist[self.__now_pointlist_index-1][1] + (abs(self.__pointlist[self.__now_pointlist_index][1] - self.__pointlist[self.__now_pointlist_index-1][1]) * rate) * self.__anime_direct_y)
    def __set_frame(self):
        target = not(self.__frame_target)
        if self.__frame < self.__frame_max: self.__frame += 1
        else: self.__frame = 0; self.__append_next_coordinate()
    # 次の頂点を用意する
    def __append_next_coordinate(self):
        self.__now_pointlist_index += 1
        print(self.__now_pointlist_index, self.__now_pointlist[-1], self.__now_pointlist)
        if self.__now_pointlist_index < len(self.__pointlist):
            self.__now_pointlist.append(copy.deepcopy(self.__pointlist[self.__now_pointlist_index-1]))
            self.__get_frame_target()
    # x,yのうち差が大きいほうをframeにする(1pixcel/1tick以下にするため)
    def __get_frame_target(self):
        diff_x = (self.__pointlist[self.__now_pointlist_index][0] - self.__pointlist[self.__now_pointlist_index-1][0])
        diff_y = (self.__pointlist[self.__now_pointlist_index][1] - self.__pointlist[self.__now_pointlist_index-1][1])
        self.__anime_direct_x = 1 if 0 < diff_x else -1
        self.__anime_direct_y = 1 if 0 < diff_y else -1
        self.__frame_target = 1 if abs(diff_x) < abs(diff_y) else 0
        self.__frame_max = abs(diff_y) if abs(diff_x) < abs(diff_y) else abs(diff_x)
#        print('f_max:{} dx:{} dy:{}'.format(self.__frame_max, diff_x, diff_y))

# あみだくじを描画する
class GhostlegDrawerPyGame:
    def __init__(self, ghostleg):
        self.__leg = None
        self.__ghostleg = ghostleg
        self.__screen = Screen()
        self.__width = 8
        self.__color = (255,255,255)
        self.__to_goal_pointlist = None # ゴールまでの頂点リスト（self.__legから生成する）
        self.__select_line_color = (255,0,0)
        self.__select_line_width = 2
        self.__linesanim = None
#        print(pygame.font.get_fonts()) # 使えるフォント名

    def Select(self, select_line_index):
        if len(self.__ghostleg.Ghostleg) < select_line_index: raise Exception('select_line_indexは {} 以下にして下さい。'.format(len(self.__ghostleg.Ghostleg)))
        self.__create_to_goal_pointlist(select_line_index)
        self.__linesanim = LinesAnimation(self.__to_goal_pointlist, self.__select_line_color, self.__select_line_width)
    
    # あみだくじを描画する
    def Draw(self):
        self.__screen.Fill()
        self.__draw_vartical_lines()
        self.__draw_horizon_lines()
        self.__draw_goals()
        self.__draw_select_lines()

    def __draw_vartical_lines(self):
        for xi in range(len(self.__ghostleg.Ghostleg)+1):
            start = (20 + xi * 40, 20)
            end = (20 + xi * 40, self.__screen.Size[1] - 40)
            pygame.draw.line(self.__screen.Screen, self.__color, start, end, self.__width)

    def __draw_goals(self):
        font = pygame.font.Font("/usr/share/fonts/truetype/migmix/migmix-1m-regular.ttf", 12)
        for i in range(len(g.Goals)):
            self.__screen.Screen.blit(font.render(g.Goals[i], False, self.__color), (20 + i * 40, self.__screen.Size[1] - 40))
    def __draw_horizon_lines(self):
        for yi in range(len(self.__ghostleg.Ghostleg[0])):
            for xi in range(len(self.__ghostleg.Ghostleg)):
                if 1 == self.__ghostleg.Ghostleg[xi][yi]:
                    start = (20 + xi * 40, 20 + (yi+1) * 24)
                    end = (20 + (xi+1) * 40, 20 + (yi+1) * 24)
                    pygame.draw.line(self.__screen.Screen, self.__color, start, end, self.__width)

    # 選択肢からゴールまでの頂点リストを生成する
    def __create_to_goal_pointlist(self, select_line_index):
        self.__to_goal_pointlist = None
        self.__to_goal_pointlist = []
        now_line_index = select_line_index
        x = self.__get_leg_index_first_horizon_line(now_line_index, 0)
        self.__to_goal_pointlist.append([20 + now_line_index * 40, 20])
        for y in range(len(self.__ghostleg.Ghostleg[0])):
            if 0 == now_line_index:
                if 1 == self.__ghostleg.Ghostleg[now_line_index][y]: # └
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__to_goal_pointlist.append([20 + (now_line_index+1) * 40, 20 + ((y+1) * 24)])
                    now_line_index += 1
                else: # │
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__to_goal_pointlist.append([20 + now_line_index * 40, 20 + (y+2) * 24])
            elif len(self.__ghostleg.Ghostleg) == now_line_index:
                if 1 == self.__ghostleg.Ghostleg[now_line_index-1][y]: # ┘
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__to_goal_pointlist.append([20 + (now_line_index-1) * 40, 20 + ((y+1) * 24)])
                    now_line_index += -1
                else: # ｜
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__to_goal_pointlist.append([20 + now_line_index * 40, 20 + (y+2) * 24])
            else:
                if 1 == self.__ghostleg.Ghostleg[now_line_index][y]: # └
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__to_goal_pointlist.append([20 + (now_line_index+1) * 40, 20 + ((y+1) * 24)])
                    now_line_index += 1
                elif 1 == self.__ghostleg.Ghostleg[now_line_index-1][y]: # ┘                
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__to_goal_pointlist.append([20 + (now_line_index-1) * 40, 20 + ((y+1) * 24)])
                    now_line_index += -1
                else: # ｜
                    self.__set_pointlist_value(now_line_index, y+1)
                    self.__to_goal_pointlist.append([20 + now_line_index * 40, 20 + (y+2) * 24])
        self.__to_goal_pointlist.append([self.__to_goal_pointlist[-1][0], self.__screen.Size[1] - 40])
        print(self.__to_goal_pointlist)
        return self.__to_goal_pointlist

    # 1つ前のと同じ座標ならセットしない
    def __set_pointlist_value(self, now_line_index, y):
        if (self.__to_goal_pointlist[-1][0] != 20 + now_line_index * 40
            or self.__to_goal_pointlist[-1][1] != 20 + (y * 24)):
            self.__to_goal_pointlist.append([20 + now_line_index * 40, 20 + (y * 24)])

    def __get_leg_index_first_horizon_line(self, now_line_index, horizon_start_index):
        if 0 == now_line_index: return now_line_index
        elif len(self.__ghostleg.Ghostleg) == now_line_index: return now_line_index-1
        else:
            for h in range(horizon_start_index, len(self.__ghostleg.Ghostleg[0])):
                if 1 == self.__ghostleg.Ghostleg[now_line_index][h]:return now_line_index
                elif 1 == self.__ghostleg.Ghostleg[now_line_index-1][h]: return now_line_index-1
            return now_line_index # 左右のlegとも横線が1本もない場合
    def __draw_select_lines(self):
        if self.__to_goal_pointlist:
            if self.__linesanim: self.__linesanim.draw(self.__screen.Screen)


g = Ghostleg.Ghostleg()
g.Create()
drawer = GhostlegDrawerPyGame(g)
for i in range(len(g.Goals)): print(i, g.GetGoal(i))
drawer.Select(0)
#drawer.Draw()
main = Main()
main.Run(drawer.Draw, title="あみだくじ描画")
