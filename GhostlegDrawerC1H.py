import Ghostleg
# あみだくじを描画する（1Byte文字。横線はハイフン）
class GhostlegDrawerC1H:
    def __init__(self, ghostleg=None):
        self.__leg = None
        self.Redraw(ghostleg)
    # あみだくじを描画する
    def Draw(self): return self.__leg
    def Redraw(self, ghostleg):
        self.__leg = ''
        for y in range(len(ghostleg.Ghostleg[0])):
            for x in range(len(ghostleg.Ghostleg)):
                self.__leg += '|'
                self.__leg += '-' if 1 == ghostleg.Ghostleg[x][y] else ' '
                if x == len(ghostleg.Ghostleg) - 1: self.__leg += '|'
#                if x == len(ghostleg.Ghostleg) - 1 and 0 == (x % 2): self.__leg += '|'
            self.__leg += '\n'
        self.__draw_goals(ghostleg)
        return self.__leg
    def __draw_goals(self, ghostleg):        
        max_len = max([len(g) for g in ghostleg.Goals])
        for y in range(max_len):
            for x in range(len(ghostleg.Ghostleg)+1):
                if y < len(ghostleg.Goals[x]): self.__leg += ghostleg.Goals[x][y] # 文字インデックスyと行数を対応させる
                else: self.__leg += '　'
            self.__leg += '\n'
            

g = Ghostleg.Ghostleg()
g.Create()
drawer = GhostlegDrawerC1H(g)
print(drawer.Draw())
for i in range(len(g.Goals)): print(i, g.GetGoal(i))

