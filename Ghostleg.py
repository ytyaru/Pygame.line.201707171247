import random
class Ghostleg:
    def __init__(self):
        self.__leg = None
        self.__goal = None
    # あみだくじを新規生成する
    def Create(self): self.__create_ghostleg()

    # あみだくじデータを返す
    @property
    def Ghostleg(self): return self.__leg
    # あみくだくじの結果を返す
    @property
    def Goals(self): return self.__goal
    # 1あみだくじあたりの最大縦線数
    @property
    def VerticalLineMaxNum(self): return 7
    # 1縦線あたりの最大横線数
    @property
    def HorizontalLineMaxNum(self): return 6

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
    def GetGoal(self, v_line_index):
        if len(self.__leg) < v_line_index: raise Exception('v_line_indexは {} 以下にして下さい。'.format(len(self.__leg)))
        
        now_line_index = v_line_index
        x = self.__get_leg_index_first_horizon_line(now_line_index, 0)
        y = 0
        for y in range(len(self.__leg[0])):
#            print(now_line_index, x, y)
            if 0 == now_line_index:
                if 1 == self.__leg[now_line_index][y]: now_line_index += 1
            elif len(self.__leg) == now_line_index:
                if 1 == self.__leg[now_line_index-1][y]: now_line_index += -1
            else:
                if 1 == self.__leg[now_line_index][y]: now_line_index += 1
                elif 1 == self.__leg[now_line_index-1][y]: now_line_index += -1                
        return self.__goal[now_line_index]

    def __get_leg_index_first_horizon_line(self, now_line_index, horizon_start_index):
        if 0 == now_line_index: return now_line_index
        elif len(self.__leg) == now_line_index: return now_line_index-1
        else:
            for h in range(horizon_start_index, len(self.__leg[0])):
                if 1 == self.__leg[now_line_index][h]: return now_line_index
                elif 1 == self.__leg[now_line_index-1][h]: return now_line_index-1
            return now_line_index # 左右のlegとも横線が1本もない場合

if __name__ == '__main__':
    g = Ghostleg()
    g.Create()
    print(str(0), g.GetGoal(0))
