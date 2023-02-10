class Room:
    def __init__(self, name, items, portals, visiblerooms):
        self.name = name
        self.items = items                      # Should be a list of items.
        self.portals = portals                  # Should be a list of portals
        self.visiblerooms = visiblerooms        # An array of room coordinates that can be seen from this room


class Item:         # For any items in game, from locks to things you can pick up and use.
    def __init__(self, name, cantake, description, onetimeuse=False):
        self.name = name
        self.cantake = cantake
        self.description = description
        self.onetimeuse = onetimeuse

    def action(self):
        return self.description


class Combinable(Item):
    def __init__(self, name, ingredient, outcome, cantake, description):
        Item.__init__(self, name, cantake, description)
        self.ingredient = ingredient            # Name of item this item will combine into.
        self.outcome = outcome                  # New item that will be made when this item is combined.
        # The description should describe the process of creating a new item.

    def action(self):
        return 'C'

    def combine(self, allitems):
        while True:
            playerinput = input('Use this item on what? : ')
            for useitem in allitems:
                if playerinput == useitem.name:
                    if self.ingredient == useitem.name:
                        print(self.description)
                        return True                                 # Successfully combined an item.
                    elif self.ingredient != useitem.name:
                        print('It did\'nt work.')
                        return False                                # It is not possible to combine this item.

            print('It doesn\'t appear this item exists. Are you sure you spelt it right?')


class CheeseBowl(Item):
    def __init__(self, name, goal):
        self.goal = goal                                    # How many cheeses are needed to win.
        self.points = 0                                     # How many cheeses are currently in the bowl.
        Item.__init__(self, name, False, 'cheese')

    def action(self):
        return f'Just {self.goal - self. points} to go!'


class Cheese(Item):
    def __init__(self, name, description):
        Item.__init__(self, name, True, description)

    def action(self):
        return 'G'

    def score(self, pot):
        pot.points += 1
        print(self.description)


class Key(Item):
    def __init__(self, name, description, door):
        Item.__init__(self, name, True, description)
        self.door = door                                # Name of the portal this key can unlock.

    def action(self):
        return 'K'

    def unlock(self, portals, allitems):

        while True:
            playerinput = input('Use this item on what? : ')

            for portal in portals:
                if playerinput == portal.name:
                    if portal.name == self.door:
                        portal.locked = False
                        print(self.description)
                        return True
                    else:
                        return False

            for useitem in allitems:                # Very basic because keys are not supposed to be used on items.
                if playerinput == useitem.name:
                    return False

            print('It doesn\'t appear this item exists. Are you sure you spelt it right?')


class Trap(Item):
    def __init__(self, name, description, mouse):
        Item.__init__(self, name, False, description, onetimeuse=True)
        self.mouse = mouse                              # The target of this trap.

    def action(self):
        self.mouse.alive = False
        return self.description


class DishTrap(Trap):
    def __init__(self, name, description, mouse, cat, cheese, safedescription, room):
        Trap.__init__(self, name, description, mouse)
        self.cat = cat
        self.cheese = cheese                                        # The cheese the trap holds.
        self.safedescription = safedescription                      # The description if the trap is triggered safely.
        self.room = room                                            # Where the trap drops the cheese

    def action(self):
        if self.cat.active:
            return Trap.action(self)
        else:
            return 'T'

    def opentreasure(self):
        print(self.safedescription)
        self.room.append(self.cheese)


class Catbait(Item):
    def __init__(self, name, description, cat):
        Item.__init__(self, name, False, description, onetimeuse=True)
        self.cat = cat

    def action(self):
        self.cat.active = False
        return self.description


class Portal:
    def __init__(self, name, coordinate, locked):
        self.name = name
        self.coordinate = coordinate    # This will be the index number of the room this will lead to in the map array.
        self.locked = locked            # Whether the mouse can get through the portal.


class Mouse:  # The player
    def __init__(self):
        self.items = []         # The mouse's inventory
        self.alive = True
        self.room = 0           # The coordinate of the room the mouse is in.

    def removeitem(self, roomitems, item_name):  # Removes and potentially edit items that have been used.
        success = False

        for item in range(len(roomitems)):
            if roomitems[item].name == item_name:
                roomitems.pop(item)
                success = True
                break
        if not success:
            for item in range(len(self.items)):
                if self.items[item].name == item_name:
                    self.items.pop(item)
                    break

    def observesituation(self, catsleeping, catposition, catactive, rooms):

        # Looking at items in room.

        print(f'You are in {rooms[self.room].name}.\nThere is: ')
        if len(rooms[self.room].items) > 0:
            for item in rooms[self.room].items:
                print(f'   {item.name}')
        else:
            print('   nothing')
        print('in this room.')

        # Looking at items carried by mouse.

        print('You have :')
        if len(self.items) > 0:
            for item in self.items:
                print(f'   {item.name}')
        else:
            print('   nothing')

        # Check portals

        print('You can go:')

        for portal in rooms[self.room].portals:
            print('   ' + portal.name)


        # Cat check

        if catactive:
            for room in rooms[self.room].visiblerooms:
                if catposition == room:
                    if not catsleeping:
                        print(f'You can see the cat prowling around in {rooms[room].name}')
                    else:
                        print(f'The cat is sleeping in {rooms[room].name}')
        print('\n')

    def getinput(self, roomitems, portals):
        movedone = False
        while not movedone:
            playerinput = input('What do you do? : ').lower()

            #  Mouse movement.

            if playerinput[:2] == 'go':
                for portal in portals:
                    if playerinput[2:] == ' ' + portal.name:
                        if not portal.locked:
                            self.room = portal.coordinate
                            print('You move!')
                            movedone = True
                        else:
                            print('You can not pass. You must find an item.')
                            movedone = True

            #  Item use.

            elif playerinput[:3] == 'use':
                allitems = []
                for item in self.items:
                    allitems.append(item)
                for item in roomitems:
                    allitems.append(item)

                for item in allitems:
                    if playerinput[3:] == ' ' + item.name:
                        if item.action() == 'C':                            # Item is a Combinable
                            if item.combine(allitems):                      # The item has been successfully combined.
                                roomitems.append(item.outcome)
                                self.removeitem(roomitems, item.name)
                                self.removeitem(roomitems, item.ingredient)
                                movedone = True
                                break
                            else:
                                print('You can not use this item on that.')
                                movedone = True
                                break
                        elif item.action() == 'K':                          # Item is a key.
                            if item.unlock(portals, allitems):              # Successfully unlocking a portal
                                self.removeitem(roomitems, item.name)
                                movedone = True
                                break
                            else:
                                print('You can not use this item on that.')
                                movedone = True
                                break
                        elif item.action() == 'G':                          # Item is cheese.
                            for useitem in allitems:
                                if useitem.name == 'pot':
                                    item.score(useitem)
                                    self.removeitem(roomitems, item.name)
                                    movedone = True
                                    break
                            if not movedone:
                                print('Some cheese! Put this in the pot to score!')
                                movedone = True
                            break

                        elif item.action() == 'T':                          # Items that may be treasure.
                            item.opentreasure()

                            if item.onetimeuse:
                                self.removeitem(roomitems, item.name)
                                movedone = True
                                break

                        else:
                            print(item.action())                                   # Item is anything else.
                            if item.onetimeuse:
                                self.removeitem(roomitems, item.name)
                            movedone = True
                            break

                if not movedone:
                    print('There is no such item.')

            #  Taking items

            elif playerinput[:4] == 'take':
                for item in range(len(roomitems)):
                    if playerinput[4:] == ' ' + roomitems[item].name:
                        if roomitems[item].cantake:
                            print('You take the item!')
                            self.items.append(roomitems.pop(item))
                            movedone = True
                            break
                        else:
                            print('This item cannot be taken.')
                            break
                if not movedone:
                    print('Move not possible.')

            #  Waiting

            elif playerinput == 'wait':
                print('You wait!')
                movedone = True

            print('\n')


class Cat:  # Main enemy of the game.
    def __init__(self, patrolarea):
        self.naptimer = 3                               # Ticks down for every turn.
        self.napping = False
        self.active = True
        self.patrolarea = patrolarea                    # The array of areas the cat will prowl.
        self.room = 0                                   # Room in the array the cat is currently in.
        self.isforward = True                           # The direction the cat is facing.

    def checkmouse(self, mouse, atemessage='Catted!'):
        if mouse.room == self.patrolarea[self.room]:
            mouse.alive = False
            print(atemessage)

    def returnroom(self):
        return self.patrolarea[self.room]

    def patrol(self, mouse):
        if not self.napping and self.active:

            # Checking if the mouse walked into the cat's area.

            self.checkmouse(mouse, 'In a fit of REALLY poor judgement,' 
                                   ' you walked straight into the cat\'s mouth.\nOops.')

            # Moving.

            if self.isforward:
                self.room += 1
                if self.room == len(self.patrolarea) - 1:           # Checking if the cat has hit the boundary
                    self.isforward = False                          # and needs to turn around.
            else:
                self.room -= 1
                if self.room == 0:                                  # Check if cat has hit the start
                    self.isforward = True                           # and needs to turn around.

            # Checking if the cat has moved into the mouse's area.
            self.checkmouse(mouse, 'Oh no! You got caught, and eaten, by the cat! Better luck next time.')
            self.naptimer -= 1

            # Check if cat is going to nap

            if self.naptimer < 1:
                self.napping = True
                self.naptimer = 2

        elif self.napping and self.active:

            # Check if mouse stumbled onto the sleeping cat.

            self.checkmouse(mouse, 'Fool! You should know this cat can hear you, even when napping! You\'re dead!')

            # Check if cat is going to wake up.

            self.naptimer -= 1

            if self.naptimer < 1:
                self.napping = False
                self.naptimer = 3
