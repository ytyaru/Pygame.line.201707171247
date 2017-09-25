import copy
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

