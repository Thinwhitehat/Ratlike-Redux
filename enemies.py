'''Definitions for enemies.'''
import baseclasses as bc
import actions
import strategies as st

class Rat(bc.Enemy):
    name = 'Rat'
    desc = 'It thinks it\'s the main character'
    max_hp = 6
    max_exh = 70
    exh_rec = 9
    dmg_base = 3
    stagger_base = 4
    atks = [
        (actions.Bite, 1)
    ]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
class Goblin(bc.Enemy):
    name = 'Goblin'
    desc = 'A Stinky Goblin! Look out for it\'s pointy spear!'
    max_hp = 13
    max_exh = 45
    exh_rec = 4
    dmg_base = 4
    stagger_base = 5
    strategy = st.Goblin