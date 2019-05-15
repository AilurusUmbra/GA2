
# A Simple Point class (represents an x,y coordinate)
#
class Point:
    #class variables define min/max coords
    xMax=100
    xMin=-100
    yMax=200
    yMin=-200
    
    #class method to check if point is within limits
    @classmethod
    def checkLimits(cls,p):
        if p.x > cls.xMax or p.x < cls.xMin:
            raise Exception("Error, x-coord is out of bounds!")
        if p.y > cls.yMax or p.y < cls.yMin:
            raise Exception("Error, y-coord is out of bounds!")
        
    # __init__ function is the constructor
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        self.checkLimits(self)
    
    #move the point by x,y    
    def moveBy(self,x,y):
        self.x+=x
        self.y+=y
        self.checkLimits(self)

    #move the point to x,y
    def moveTo(self,x,y):
        self.x=x
        self.y=y
        self.checkLimits(self)
     
    #calculate Hamming distance between two points   
    def distanceTo(self, p2):
        return abs(self.x-p2.x) + abs(self.y-p2.y)
        
    # __str__ generates string representation of objects   
    def __str__(self):
        return '['+str(self.x)+','+str(self.y)+']'

