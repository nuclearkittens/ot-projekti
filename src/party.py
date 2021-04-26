import pygame as pg

from partymember import PartyMember

class Party:
    def __init__(self, clock, renderer):
        self._clock = clock
        self._renderer = renderer

        # self.items = ItemContainer()
        self.items = {}
        self.active_party = []
        self.group = pg.sprite.Group()

        self.ej = None
        self.witch = None

        self._create_party()

    @property
    def current_party(self):
        return self.group.sprites()

    def _create_party(self):
        # TODO: create all party members here even when they haven't joined yet;
        # add to group when joined
        self.ej = PartyMember(self._clock, self._renderer, 'ej', self.items)
        self.witch = PartyMember(self._clock, self._renderer, 'witch', self.items)
        # self.items.set_owner(self.ej)
        self.active_party.append(self.ej)
        self.active_party.append(self.witch)
        self.group.add(self.ej, self.witch)
        self.ej.joined, self.witch.joined = True, True

    def switch_members(self, add_char, rem_char):
        self.remove_from_active_party(rem_char, True)
        self.add_to_active_party(add_char)

    def add_to_active_party(self, char):
        if len(self.active_party) < 3:
            char.add_to_active_party()
            self.active_party.append(char)
        else:
            raise ValueError

    def remove_from_active_party(self, char, switch=False):
        if not switch:
            if len(self.active_party) <= 1:
                raise ValueError
        char.remove_from_active_party()
        self.active_party.remove(char)

    def add_item(self, item, qty=1):
        if item not in self.items:
            self.items[item] = qty
        else:
            self.items[item] += qty
            