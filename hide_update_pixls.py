from watches import *
from pixl import *

def delete_pixls():
    deleting_pixls = []

    for i in range(5,12):
        deleting_pixls.append(get_watch(f'Pixl slot {i}'))

    for pixl in deleting_pixls:
        pixl.write(0x0000000)

def write_pixls(slot_number, value):
    pixl = get_watch(f'Pixl slot {slot_number}')
    pixl.write(0x0010000 + int(value, base=16))

if __name__ == '__main__':
    dme.hook()
    pixls = [Pixl(0), Pixl(1), Pixl(2), Pixl(3)]

    xAddress = get_watch('Coordinate X')
    yAddress = get_watch('Coordinate Y')
    zAddress = get_watch('Coordinate Z')
    
    while True:
        for i, pixl in enumerate(pixls):
            x = MemoryWatch.read(xAddress)
            y = MemoryWatch.read(yAddress)
            z = MemoryWatch.read(zAddress)

            pixl.isActive.write(True)
            pixl.state.write(PixlState.STAY)
            pixl.setPosition(x, y + 10 * i, z)

        delete_pixls()
        write_pixls(1,'E1')
        write_pixls(2,'E1')
        write_pixls(3,'E2')
        write_pixls(4,'200')