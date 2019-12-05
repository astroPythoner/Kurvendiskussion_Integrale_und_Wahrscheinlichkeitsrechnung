class Punkt():
    x = 0
    y = 0
    name = ""

    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def get_koordinaten(self):
        return [self.x,self.y]

    def __str__(self):
        return "("+str(self.x)+" | "+str(self.y)+")"