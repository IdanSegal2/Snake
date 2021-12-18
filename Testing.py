from Board import *
from Snake import *


lizzy = Snake()
assert lizzy.get_coordinates() == [(10, 10), (10, 9), (10, 8)]
assert lizzy.get_direction() == 'up'
lizzy._Snake__change_direction('right',False)
assert lizzy.get_coordinates() == [(11, 10), (10, 10), (10, 9)]
lizzy._Snake__change_direction('up',False)
assert lizzy.get_coordinates() == [(11, 11), (11, 10), (10, 10)]
lizzy._Snake__change_direction('left',False)
assert lizzy.get_coordinates() == [(10, 11), (11, 11), (11, 10)]
lizzy._Snake__change_direction('down',False)
assert lizzy.get_coordinates() == [(10, 10), (10, 11), (11, 11)]
lizzy._Snake__change_direction('down',True)
assert lizzy.get_coordinates() == [(10,9),(10, 10), (10, 11), (11, 11)]
lizzy._Snake__change_direction('left',True)
assert lizzy.get_coordinates() == [(9,9),(10,9),(10, 10), (10, 11), (11, 11)]

lizzy.move('right',False)
assert lizzy.get_coordinates() == [(8,9),(9,9),(10,9),(10, 10), (10, 11)]
lizzy.move('left',False)
assert lizzy.get_coordinates() == [(7,9),(8,9),(9,9),(10,9),(10, 10)]
lizzy.move('down',False)
assert lizzy.get_coordinates() == [(7,8),(7,9),(8,9),(9,9),(10,9)]
lizzy.move('down',True)
assert lizzy.get_coordinates() == [(7,7),(7,8),(7,9),(8,9),(9,9),(10,9)]

boa = Board()

