# from database.db_util import load_item_info, load_item_effects

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
        '''Use an item. Takes a character object (target) as the argument.'''
        for effect in self._effects:
            if effect[0] == 'heal':
                target_attr, amount = effect[1], effect[2]
                self._heal(target, target_attr, amount)

    def _heal(self, target, target_attr, amount):
        '''Use a healing item.'''
        if target_attr == 'hp':
            if isinstance(amount, int):
                target.curr_hp += amount
            else:
                target.curr_hp += int(amount * target.max_hp)
        if target_attr == 'mp':
            if isinstance(amount, int):
                target.curr_mp += amount
            else:
                target.curr_mp += int(amount * target.max_mp)

    # def _load_info(self):
    #     '''Fetches the item information from the game database.'''
    #     cur = self._conn.cursor()
    #     cur.execute('SELECT name, descr FROM Items WHERE id=?', (self._id,))
    #     return cur.fetchone()

    # def _load_effects(self):
    #     '''Fetches the item's effects from the game database.'''
    #     cur = self._conn.cursor()
    #     cur.execute(
    #         '''SELECT E.effect, E.target_attr, E.amount
    #         FROM Effects E, ItemEffects I
    #         WHERE E.id=I.effect_id AND I.item_id=?''', (self._id,)
    #         )
    #     rows = cur.fetchall()
    #     for row in rows:
    #         self._effects.append(tuple(row))

    @property
    def name(self):
        '''Returns the name of an item.'''
        return self._name

    @property
    def description(self):
        '''Returns the description of an item.'''
        return self._descr
