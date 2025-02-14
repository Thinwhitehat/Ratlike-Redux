import baseclasses as bc
import random
random.seed()

class Rest(bc.Action):
    name = 'Rest'
    desc = 'Pause and recover your balance'
    use_msg = 'recovers their balance.'
    def resolve(self):
        self.src.exhaust -= self.src.exh_rec
        return super().resolve() # exhaust is taken off once in here too

class Stab(bc.Attack):
    '''Default attack for daggers and knives'''
    name = 'Stab'
    desc = 'A hard stab'
    use_msg = 'stabs quickly!'
    dmg_mod = 0.8
    stagger_mod = 0.8
    reach = 3
    exh_cost = 12
    styles = ['quick']

class Jab(bc.Attack):
    '''Default reaction for daggers. Goblin standard attack'''
    name = 'Jab'
    desc = 'A quick jab'
    use_msg = 'jabs at their opponent!'
    dmg_mod = 0.6
    stagger_mod = 0.5
    reach = 1
    exh_cost = 6
    styles = ['quick']

class Lunge(bc.Attack):
    '''High range high stagger spear attack'''
    name = 'Lunge'
    desc = 'An aggressive lunge!'
    use_msg = 'lunged forwards!'
    dmg_mod = 1.5
    stagger_mod = 1.2
    reach = 10
    exh_cost = 17
    
class Smash(bc.Attack):
    '''Med range high stagger'''
    name = 'Smash!'
    desc = 'A powerful overhead slam!'
    use_msg = 'smashed viciously!'
    dmg_mod = 1
    stagger_mod = 1.5
    reach = 7
    exh_cost = 17
    styles = ['heavy']

class Bite(bc.Attack):
    name = 'Bite'
    desc = 'Chomp!'
    use_msg = 'bites viciously!'
    dmg_mod = 0.3
    stagger_mod = 0.3
    reach = 3
    exh_cost = 3

class Dodge(bc.CounterAttack):
    '''Standard Dodge action. Checks for a reaction_class on it\'s source.'''
    name = 'Dodge'
    desc = 'Dodge incoming attacks this turn'
    use_msg = 'jumps back!'
    reach = 0
    exh_cost = 25 # each dodge adds more stagger
    def __init__(self, source: bc.Entity, **kwargs):
        super().__init__(source.get_reaction(), source, **kwargs)
        self.used:bool = False

    def attack(self, atk: bc.Attack):
        if not self._can_dodge():
            self.use_msg = 'was too tired to dodge!'
            return super().attack(atk)
        if self._dodge_succeeds(atk):
            print(f'   {atk.tgt.name} dodged the attack!')
            if not self.used and self.reaction_class is not None:
                print(f'     and reacts!')
                self.react(target = atk.src)
                self.used = True
                self.silent = True
        else:
            return super().attack(atk)

    def _can_dodge(self) -> bool:
        if self.src.exhaust >= self.src.max_exh:
            print(f' {self.src.name} is too exhausted to dodge!')
            return False
        else:
            return True
    def _dodge_succeeds(self, atk: bc.Attack) -> bool:
        roll = random.randint(1,100)
        if 'heavy' in atk.styles:
            return True
        roll = random.choice(range(10))
        if roll < 2: # 20 chance to fail
            return False
        if roll >= 4: # 60%
            return True
        if 'quick' in atk.styles and roll < 4: # quick is harder to dodge
            return False
        else:
            return True
     
class Block(bc.Action):
    name = 'Block'
    desc = 'Shields Up!'
    def attack(self, atk:bc.Attack):
        print(' The attack is blocked!')
        dmg_m = 0.5
        stgr_m = 0.5
        reflect_m = 0.4
        if 'heavy' in atk.styles:
            dmg_m *= 1.5
            stgr_m *= 1.8
            reflect_m *= 0.7
        if 'quick' in atk.styles:
            dmg_m *= 0.8
            reflect_m *= 1.6
        super().attack(atk, dmg_mod=dmg_m, stagger_mod=stgr_m)
        atk.src._take_damage(0, int(atk.stagger() * reflect_m))

class TrollReady(bc.Action):
    name = 'Troll smash prep'
    desc = ''
    use_msg = 'raises his club over his head!'