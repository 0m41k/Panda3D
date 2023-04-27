KEY_CHANGE_CAMERA = 'c'
KEY_CHANGE_MOD = 'z'

KEY_FORWARD = 'w'
KEY_BACK = 's'
KEY_LEFT = 'a'
KEY_RIGHT = 'd'

KEY_TURN_LEFT = 'n'
KEY_TURN_RIGHT = 'm'

KEY_UP = 'e'
KEY_DOWN = 'q'

KEY_BUILD = 'b'
KEY_DESTROY = 'v'

KEY_SAVE = 'i'
KEY_LOAD = 'l'

class Hero:
    def __init__(self,pos,land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel('smiley')
        self.hero.setPos(pos)
        self.hero.setColor((0,0,0,1))
        self.hero.reparentTo(render)
        self.cameraBind()
        self.acceptEvents()
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,1.5)
        self.cameraOn = True
    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
    def cameraChange(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    
    def acceptEvents(self):
        base.accept(KEY_CHANGE_CAMERA, self.cameraChange)
        base.accept(KEY_CHANGE_MOD, self.change_mode)

        base.accept(KEY_FORWARD, self.forward)
        base.accept(KEY_FORWARD + '-repeat', self.forward)

        base.accept(KEY_LEFT, self.left)
        base.accept(KEY_LEFT + '-repeat', self.left)

        base.accept(KEY_RIGHT, self.right)
        base.accept(KEY_RIGHT + '-repeat', self.right)

        base.accept(KEY_BACK, self.back)
        base.accept(KEY_BACK + '-repeat', self.back)

        base.accept(KEY_TURN_LEFT, self.turn_left)
        base.accept(KEY_TURN_LEFT + '-repeat', self.turn_left)

        base.accept(KEY_TURN_RIGHT, self.turn_right)
        base.accept(KEY_TURN_RIGHT + '-repeat', self.turn_right)

        base.accept(KEY_UP, self.up)
        base.accept(KEY_UP + '-repeat', self.up)

        base.accept(KEY_DOWN, self.down)
        base.accept(KEY_DOWN + '-repeat', self.down)

        base.accept(KEY_DESTROY, self.destroy)
        base.accept(KEY_BUILD, self.build)

        base.accept(KEY_LOAD, self.land.loadMap)
        base.accept(KEY_SAVE, self.land.saveMap)

    def check_dir(self,angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 115:
            return (1,1)
        elif angle <= 200:
            return (0,1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1,0)
        elif angle <= 335:
            return (-1,-1)
        else:
            return (0,-1)

    def look_at(self, angle):
        x = int(self.hero.getX())
        y = int(self.hero.getY())
        z = int(self.hero.getZ())

        dx, dy = self.check_dir(angle)

        x_to = x + dx
        y_to = y + dy
        return (x_to, y_to, z)

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            x,y,z = pos
            z += 1
            pos = (x,y,z)
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def move_to(self,angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)
        
    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)        

    def turn_left(self):
        heading = self.hero.getH()
        heading += 10
        self.hero.setH(heading)

    def turn_right(self):
        heading = self.hero.getH()
        heading -= 10
        self.hero.setH(heading)
    
    def up(self):
        if self.mode:
            z = self.hero.getZ()
            self.hero.setZ(z+1)

    def down(self):
        if self.mode:
            z = self.hero.getZ()
            self.hero.setZ(z-1)

    def change_mode(self):
        self.mode = not self.mode

    def build(self):
        angle = self.hero.getH() %360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.addBlockFrom(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)
