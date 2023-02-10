import Game_Components

# Making all objects.

mouse = Game_Components.Mouse()
cat = Game_Components.Cat([3, 4, 5])

# Cheeses

cheddar = Game_Components.Cheese('cheddar', 'The cheddar melts into the pot!')
gouda = Game_Components.Cheese('gouda', 'The gouda makes it\'s way into the pot!')
feta = Game_Components.Cheese('feta', 'The feta floats around in the pot!')
cheesepot = Game_Components.CheeseBowl('pot', 3)

# Keys

rope = Game_Components.Key('string', 'You throw the string over the top of the counter, and you can now climb up it!',
                           'kitchen counter')
lockpickset = Game_Components.Key('lock pick set', 'You pick the vault door lock open!', 'vault door')

# Traps

poisoncheese = Game_Components.Trap('strange cheese',
                                    'You take a bite. It is poison! You die pretty much '
                                    'immediately, and the cat comes over and turns you into stew.',
                                    mouse)
dishtrap = Game_Components.DishTrap('cheese dish', 'You try to free the cheese, but this dish was put on a '
                                                   'pressure plate. The alarm goes off, and the cat charges into'
                                                   ' the room for a bite. Oops.',
                                    mouse,
                                    cat,
                                    feta,
                                    'You move the dish off the pressure plate. The alarm goes off, but the'
                                    ' cat is too occupied to even care about it. Out comes the feta!',
                                    None)

# Cat bait

catbait = Game_Components.Catbait('opened can', 'You rattle the can, the cat comes skittering in.'
                                                ' He takes the can from you and runs off.', cat)

# Other items.
lockpick = Game_Components.Combinable('lock pick', 'tension tool', lockpickset, True, 'You combine the pick'
                                                                                      ' with the tool to make a '
                                                                                      'full lock picking set!')
tensiontool = Game_Components.Combinable('tension tool', 'lock pick', lockpickset, True, 'You combine the pick'
                                                                                         ' with the tool to make a '
                                                                                         'full lock picking set!')

canopener = Game_Components.Combinable('can opener', 'cat food', catbait, True, 'You open the can with the can opener!')
catfood = Game_Components.Item('cat food', False, 'A can of smelly cat food. He goes crazy for this stuff.')


# Portals

# Room 0: Western mouse hole.
room0hall = Game_Components.Portal('hall', 3, False)
room0center = Game_Components.Portal('east', 1, False)

# Room 1: Central mouse hole.
room1west = Game_Components.Portal('west', 0, False)
room1kitchen = Game_Components.Portal('kitchen', 4, False)
room1east = Game_Components.Portal('east', 2, False)

# Room 2: Eastern mouse hole.
room2hall = Game_Components.Portal('hall', 5, False)
room2center = Game_Components.Portal('west', 1, False)

# Room 3: West hall.
room3hole = Game_Components.Portal('mouse hole', 0, False)
room3kitchen = Game_Components.Portal('kitchen', 4, False)
room3livingroom = Game_Components.Portal('living room', 6, False)

# Room 4: Kitchen
room4hole = Game_Components.Portal('mouse hole', 1, False)
room4easthall = Game_Components.Portal('east', 5, False)
room4counter = Game_Components.Portal('kitchen counter', 7, True)
room4westhall = Game_Components.Portal('west', 3, False)

# Room 5: East hall.
room5hole = Game_Components.Portal('mouse hole', 2, False)
room5vault = Game_Components.Portal('vault door', 8, True)
room5kitchen = Game_Components.Portal('kitchen', 4, False)

# Room 6: Living room
room6hall = Game_Components.Portal('hall', 3, False)

# Room 7: Counter
room7kithcen = Game_Components.Portal('kitchen', 4, False)

# Room 8: Vault
room8hall = Game_Components.Portal('hall', 5, False)


# Actual rooms
room0 = Game_Components.Room('western mouse hole', [cheesepot], [room0hall, room0center], [3])
room1 = Game_Components.Room('central mouse hole', [rope], [room1east, room1kitchen, room1west], [4])
room2 = Game_Components.Room('eastern mouse hole', [], [room2hall, room2center], [5])
room3 = Game_Components.Room('west hall', [poisoncheese], [room3hole, room3kitchen, room3livingroom], [4, 5])
room4 = Game_Components.Room('kitchen', [], [room4hole, room4westhall, room4counter, room4easthall], [3, 5])
room5 = Game_Components.Room('east hall', [lockpick], [room5hole, room5vault, room5kitchen], [4, 3])
room6 = Game_Components.Room('living room', [cheddar], [room6hall], [3])
room7 = Game_Components.Room('kitchen counter', [tensiontool, catfood, gouda], [room7kithcen], [4])
room8 = Game_Components.Room('vault', [dishtrap, canopener], [room8hall], [5])

# Make sure dish trap knows where to drop the cheese.

dishtrap.room = room8.items

# The map

rooms = [room0, room1, room2, room3, room4, room5, room6, room7, room8]

# Print a tutorial.

input('Welcome to the Mouse Text Adventure!\n\nYou will be playing as a mouse trying to make cheese soup. He needs to'
      ' collect three cheeses spread throughout the house, and put them into the pot.\nThis will be'
      ' challenging, because there is a hungry cat in the house trying to hunt you down.\n\n How to play:\n'
      'type go (location) to move to another room\ntype take (item name) to take an item from the environment.\n'
      'type use (item) to use an item. Items have many different effects. You can even use items that are not in your'
      ' inventory.\ntype wait to stay in place for one turn. This will be a very useful move in your quest.\n\n'
      'Good luck!\npress enter to continue')

print('\n\n\n')

# Gameplay
gameon = True

while gameon:

    # 'Drawing'
    mouse.observesituation(cat.napping, cat.returnroom(), cat.active, rooms)

    # Movement
    mouse.getinput(rooms[mouse.room].items, rooms[mouse.room].portals)
    cat.patrol(mouse)

    # Game end states
    if not mouse.alive:
        gameon = False

    if cheesepot.points >= cheesepot.goal:
        gameon = False
        print('You win!')
