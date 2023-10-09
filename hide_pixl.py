from watches import *
from enum import Enum
import dolphin_memory_engine as DME


fairyWork = 0x804CD030
marioPouchWork = 0x804CEA28

class PixlState(Enum):
    STAY = 1
    FOLLOW = 2

class Pixl:
    pixlInventory = marioPouchWork + 0xC4
    def __init__(self, pixlId) -> None:
        pixlAddress = fairyWork + 4 + 208 * pixlId
        self.state = MemoryWatch(f'Pixl State {pixlId}', pixlAddress + 0x28, Datatype.WORD)
        self.x = MemoryWatch(f'Pixl x {pixlId}', pixlAddress + 0x48, Datatype.FLOAT)
        self.y = MemoryWatch(f'Pixl y {pixlId}', pixlAddress + 0x4C, Datatype.FLOAT)
        self.z = MemoryWatch(f'Pixl z {pixlId}', pixlAddress + 0x50, Datatype.FLOAT)
        self.isActive = MemoryWatch(f'Pixl State {pixlId}', Pixl.pixlInventory + 4 * pixlId + 1, Datatype.BOOL)

    def setPosition(self, x, y, z):
        self.x.write(x)
        self.y.write(y)
        self.z.write(z)

if __name__ == '__main__':
    # Test
    DME.hook()

    pixls = [Pixl(0), Pixl(1), Pixl(2), Pixl(3)]

    xAddress = get_watch('Coordinate X')
    yAddress = get_watch('Coordinate Y')
    zAddress = get_watch('Coordinate Z')
    
    while True:
        for pixl in pixls:
            x = MemoryWatch.read(xAddress)
            y = MemoryWatch.read(yAddress)
            z = MemoryWatch.read(zAddress)

            pixl.isActive.write(True)
            pixl.state.write(PixlState.STAY)
            pixl.setPosition(0, -1000, 0)
