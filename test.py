from Bullet.Model import *
from Bullet.SnakeModel import *
from Bullet.DrawerConnector import *

if __name__ == "__main__":
    bc = DrawerConnector(0.00833333, True)

    snake = Snake(nodeLength = 0.25, gap = 0.)

    bc.addModel(snake)
    dt = 0.3

    while True:
        bc.render()
        
