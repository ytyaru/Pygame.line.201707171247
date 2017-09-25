import Ghostleg
# あみだくじを描画する（2Byte文字。横線はハイフン）
class GhostlegDrawerC1H:
    def __init__(self, ghostleg=None):
        self.__leg = None
        self.Redraw(ghostleg)
    # あみだくじを描画する
    def Draw(self): return self.__leg
    def Redraw(self, ghostleg):
        self.__leg = ''
        if 1 == len(ghostleg.Ghostleg): self.__draw_2line(ghostleg)
        else: self.__draw_multi_line(ghostleg)
        self.__draw_goals(ghostleg)
        return self.__leg
    def __draw_2line(self, ghostleg):
        for y in range(len(ghostleg.Ghostleg[0])):
            if 1 == ghostleg.Ghostleg[0][y]: self.__leg += '├┤'
            else: self.__leg += '││'
            self.__leg += '\n'
        return self.__leg
    def __draw_multi_line(self, ghostleg):
        for y in range(len(ghostleg.Ghostleg[0])):
            for x in range(len(ghostleg.Ghostleg)):
                if 0 == x:
                    if 1 == ghostleg.Ghostleg[x][y]: self.__leg += '├'
                    else: self.__leg += '│'
                elif len(ghostleg.Ghostleg)-1 == x:
                    if 1 == ghostleg.Ghostleg[x-1][y]: self.__leg += '┤'
                    elif 1 == ghostleg.Ghostleg[x][y]: self.__leg += '├'
                    else: self.__leg += '│'
                    if 1 == ghostleg.Ghostleg[x][y]: self.__leg += '┤'
                    else: self.__leg += '│'
                else:
                    if 1 == ghostleg.Ghostleg[x-1][y]: self.__leg += '┤'
                    elif 1 == ghostleg.Ghostleg[x][y]: self.__leg += '├'
                    else: self.__leg += '│'
            self.__leg += '\n'
        return self.__leg
    def __draw_goals(self, ghostleg):        
        max_len = max([len(g) for g in ghostleg.Goals])
        for y in range(max_len):
            for x in range(len(ghostleg.Ghostleg)+1):
                if y < len(ghostleg.Goals[x]): self.__leg += ghostleg.Goals[x][y] # 文字インデックスyと行数を対応させる
                else: self.__leg += '　'
            self.__leg += '\n'
    def ReDrawSelectLine(self, ghostleg, select_line_index):
        self.Redraw(ghostleg)
        self.__overwite_line_to_goal(ghostleg, select_line_index)

    # 指定した選択肢の結果を返す
    def __overwite_line_to_goal(self, ghostleg, select_line_index):
        leg = ghostleg.Ghostleg
        if len(leg) < select_line_index: raise Exception('select_line_indexは {} 以下にして下さい。'.format(len(leg)))
        
        now_line_index = select_line_index
        x = self.__get_leg_index_first_horizon_line(now_line_index, 0)
        y = 0
        for y in range(len(leg[0])):
#            print(now_line_index, x, y)
            if 0 == now_line_index:
                if 1 == leg[now_line_index][y]: now_line_index += 1
            elif len(leg) == now_line_index:
                if 1 == leg[now_line_index-1][y]: now_line_index += -1
            else:
                if 1 == leg[now_line_index][y]: now_line_index += 1
                elif 1 == leg[now_line_index-1][y]: now_line_index += -1                
#            print(now_line_index, x, y)
        return self.__goal[now_line_index]

g = Ghostleg.Ghostleg()
g.Create()
drawer = GhostlegDrawerC1H(g)
print(drawer.Draw())
for i in range(len(g.Goals)): print(i, g.GetGoal(i))

