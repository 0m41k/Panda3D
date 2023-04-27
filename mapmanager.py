import pickle

class Mapmanager:
    def __init__(self):
        self.model = 'block.egg'
        self.texture = ['stone.png']
        self.color = [
            (128/256, 128/256, 128/256, 1)
        ]
        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode('land')

    def addBlock(self, position):
        block = loader.loadModel(self.model)
        texture = loader.loadTexture(self.texture)
        block.setTexture(texture)
        color = self.getColor(position[2])
        block.setColor(color)
        block.setPos(position)
        block.reparentTo(self.land)
        block.setTag('at', str(position))

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split()
                for z in line:
                    for z0 in range(int(z)+1):
                        self.addBlock((x,y,z0))
                    x += 1
                y += 1
        return x,y

    def getColor(self, z):
        if z < len(self.color):
            return self.color[z]
        else:
            return self.color[-1]

    def findBlock(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))

    def isEmpty(self, pos):
        block = self.findBlock(pos)
        if block:
            return False
        else:
            return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 0
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y,z) 

    def delBlock(self, pos):
        blocks = self.findBlock(pos)
        for block in blocks:
            block.removeNode()

    def addBlockFrom(self,pos):
        _, _, z = pos
        new_pos = self.findHighestEmpty(pos)
        if new_pos <= z+1:
            self.addBlock(new_pos)

    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = (x, y ,z-1)
        self.delBlock(pos)

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('map.dat', 'wb') as file:
            pickle.dump(len(blocks), file)
            for block in blocks:
                pos = block.getPos()
                pos = tuple(map(int, pos))
                pickle.dump(pos, file)
                
    def loadMap(self):
        self.clear()
        with open('map.dat', 'rb') as file:
            length = pickle.load(file)
            for i in range(length):
                pos = pickle.load(file)
                self.addBlock(pos)

