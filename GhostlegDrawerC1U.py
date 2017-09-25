import random
class Ghostleg:
    def __init__(self):
        self.__leg = None
        self.__goal = None
    # あみだくじを新規生成する
    def create(self):
        self.__create_ghostleg()
    # ゴールの数を決める
    def __get_goal_num(self): return 2 + int(random.random() * 6) # 2〜7
    def __get_max_horizon_line(self): return 6
    # ゴールを新規生成する
    def __create_ghostleg(self):
        del self.__leg
        v_num = self.__get_goal_num()
        h_num = self.__get_max_horizon_line()
        print(v_num)
        self.__leg = [[0 for y in range(h_num)] for x in range(v_num - 1)]
#        self.__leg = [[0 for i in range(3)] for j in range(5)]
        print(self.__leg)
        self.__create_goal()
        self.__create_horizon_line()
    # ゴールを新規生成する
    def __create_goal(self):
        all_goals = ['大吉', '中吉', '小吉', '吉', '末吉', '凶', '大凶']
        random.shuffle(all_goals)
        del self.__goal
        self.__goal = all_goals[:len(self.__leg)+1]
        print(self.__goal)

    def __create_horizon_line(self):
        for y in range(len(self.__leg[0])):
            for x in range(len(self.__leg)):
                value = int(random.random() * 2) # 0 or 1
                if 0 < x and 1 == self.__leg[x-1][y]: value = 0
                self.__leg[x][y] = value
        print(self.__leg)
    
    # 指定した選択肢の結果を返す
    def get_goal(self, v_line_index):
        if len(self.__leg) <= v_line_index: raise Exception('v_line_indexは {} 未満にして下さい。'.format(len(self.__leg)))
        select_line_index = v_line_index
        now_line_index = v_line_index
        x = self.get_leg_index(now_line_index)
        # line_index: 0,1, 2,3, 4,5, 6,7
        # leg_index:   0  1 2  3 4  5 6
        for y in range(len(self.__leg[0])):
#            if now_line_index
#            if self.__leg[x][y]:
            print(now_line_index)
            if 1 == self.__leg[x][y]:
                now_line_index = self.get_next_line(x, now_line_index)
                x = self.get_leg_index(now_line_index)
        print(now_line_index)
        return self.__goal[now_line_index]
    
    def get_leg_index(self, now_line_index): return now_line_index - 1 if 0 < now_line_index else 0
    def get_next_line(self, leg_index, now_line_index):
        if 0 == leg_index: return 1 if 0 == now_line_index else 0
        elif 1 == leg_index: return 2 if 1 == now_line_index else 1
        elif 2 == leg_index: return 3 if 2 == now_line_index else 2
        elif 3 == leg_index: return 4 if 3 == now_line_index else 3
        elif 4 == leg_index: return 5 if 4 == now_line_index else 4
        elif 5 == leg_index: return 6 if 5 == now_line_index else 5
        elif 6 == leg_index: return 7 if 6 == now_line_index else 6

g = Ghostleg()
g.create()
print(str(0), g.get_goal(0))
