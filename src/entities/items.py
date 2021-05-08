class Item:
    '''Class for item objects.

    attr:
        name: str; name of the item
        descr: str; description of the item and its effects
        effects: list; tuples consisting of item's effects;
                includes the type of effect, target attribute and the value
                the target attribute is changed
    '''
    def __init__(self, item_id):
        '''Constructor for the item class. Imports database methods to
        load relevant info (imported outside top-level to avoid circular
        import).

        args:
            item_id: str; unique identifier for an item
        '''
        from database.db_util import load_item_info, load_item_effects
        self._id = item_id

        data = load_item_info(self._id)

        self._name = data['name']
        self._descr = data['descr']
        self._effects = load_item_effects(self._id)

    def use(self, target):
        '''Use an item. Takes a character object (target) as the argument.
        
        return:
            info: lst; info for creating a DamageText object
        '''
        def heal(target, target_attr, amount):
            '''Use a healing item.'''
            info = []
            if target_attr == 'hp':
                if isinstance(amount, float):
                    amount *= target.max_hp
                target.curr_hp += int(amount)
                info.append(('hp', int(amount)))
                # button = target.battlesprite.create_dmg_txt_button('hp', int(amount))
            if target_attr == 'mp':
                if isinstance(amount, float):
                    amount *= target.max_mp
                target.curr_mp += int(amount)
                info.append(('mp', int(amount)))
                # button = target.battlesprite.create_dmg_txt_button('mp', int(amount))
            return info

        info = []
        for effect in self._effects:
            if effect[0] == 'heal':
                target_attr, amount = effect[1], effect[2]
                heal_info = heal(target, target_attr, amount)
                for elem in heal_info:
                    info.append(elem)
            return info

    @property
    def name(self):
        '''Returns the name of an item.'''
        return self._name

    @property
    def description(self):
        '''Returns the description of an item.'''
        return self._descr
