from Bullet.Model import *
from Bullet.SnakeModel import *
from Bullet.DrawerConnector import *

if __name__ == "__main__":
    bc = DrawerConnector(0.00833333)

    while True:
        bc.render()
        
