#WIZARD BOT IS LIVE

import os
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from functools import partial
import asyncio
import time
from random import randint

#initializes bot, sets up command sign
Client = discord.Client()
bot = discord.ext.commands.Bot(command_prefix = '~')

#GAME STUFF
class Monster:
    def __init__(self, speed, damage, health, dmg_type):
        self.spd = speed 
        self.dmg = damage
        self.hp = health
        self.dmg_type = dmg_type
        self.is_alive = True

        #All integers.
        #Last one is 1 or 0 - there are two damage types. Magical and physical.
        #Physical is 0, Magical is 1.
        #Attacks return a tuple containing a 1 or a 0 as the first number, then the damage as the second number.

    #ACCESSORS
    def health(self):
        return self.hp
    def speed(self):
        return self.spd
    def damage(self):
        return self.dmg
    def life(self):
        return self.is_alive

    #MUTATORS
    def take_hit(self, damage):
        self.hp = self.hp - damage
        if self.hp <= 0:
            self.is_alive = False
    def make_attack(self):
        attack = ""
        attack += str(self.dmg_type)
        attack += " " 
        attack += str(self.dmg)
        return attack

class Player:
    def __init__(self):
        self.hp = 100 #Classic!
        self.dmg = 10
        self.shield = 0
        self.s_dur = 0
        self.is_alive = True

        #Player has four shield conditions.
        #0 - has no shield. 1 - Physical shield. 2 - Magical shield. 3 - Both.


    #ACCESSORS
    def damage(self):
        return self.dmg
    def life(self):
        return self.is_alive
    def shield_type(self):
        return self.shield
    def shield_dur(self):
        return self.s_dur
    def health(self):
        return self.hp

    #MUTATORS
    def take_hit(self, damage):
        self.hp = self.hp - damage
        if self.hp <= 0:
            self.is_alive = False
    def shield_hit(self):
        self.s_dur = self.s_dur - 1
        if self.s_dur == 0:
            self.shield = 0
        #Kills your shield when the durability hits 0.
    def heal(self, heal):
        self.hp = self.hp + heal
    def dangerify(self, damage):
        self.dmg = self.dmg + damage
    def get_shield(self, shield):
        #This one's a bit tricky. The shield is 0 or 1 - Physical or magical.
        #It then updates the player's shield accordingly.
        if shield == 0:
            if self.shield == 0:
                self.shield = 1
                self.s_dur = 10
            if self.shield == 2:
                self.shield = 3
                self.s_dur = 5
        elif shield == 1:
            if self.shield == 0:
                self.shield = 2
                self.s_dur = 10
            if self.shield == 1:
                self.shield = 3
                self.s_dur = 5
        #Shield durabilty goes to 5, regardless of what it was before, on picking up a SECOND shield.
        #Other four cases don't need to be covered.
    
#END OF CLASSES

#START OF EVENTS
#Some brief setup generic commands

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.content == "EAT THAT HORSE!":
        await message.channel.send(":horse:")
    await bot.process_commands(message)

@bot.command()
async def slap(ctx, arg):
    await ctx.send("You have slapped {1}!" .format(ctx, arg))

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, World!")

@bot.command()
async def echo(ctx, arg):
    await ctx.send(arg)

#Subfunction of the "~up" command
def to_upper(arg):
    return arg.upper()

@bot.command()
async def up(ctx, *, content: to_upper):
    await ctx.send(content)

@bot.command()
async def roll(ctx, arg):
    value = randint(1, int(arg))
    await ctx.send("You have rolled a {1}!" .format(ctx, value))

#GAME EVENT
@bot.command()
async def game(ctx):
    await ctx.send("Game started! Choose a starting buff - 'Health' or 'Damage'.")

    def check(m):
        if m.author == ctx.author:
            return m.content == "Health" or m.content == "Damage" or m.content == "CMSC280 FREE PASS"
        else:
            return False

    gamer = Player() #Initializing player class

    msg = await bot.wait_for("message", check=check)
    if msg.content == "Health":
        await ctx.send("+25 HP!")
        gamer.heal(25)
    elif msg.content == "Damage":
        await ctx.send("+5 Damage!")
        gamer.dangerify(5)
    elif msg.content == "CMSC280 FREE PASS":
        await ctx.send("Free shield!")
        gamer.get_shield(1)
        gamer.get_shield(0)

    await ctx.send("OPTIONS: You can 'Block', 'Dodge' or 'Attack' a monster. Alternatively, you may 'Die'.")

    slain_enemies = 0


    def continue_check(m): #Check used several times 
        if m.author == ctx.author:
            return m.content == "Yes" or m.content == "No"
        else:
            return False

    while gamer.life() == True:
        game_roll = randint(1, 1) #placeholder
        if game_roll == 1:
            #Monster speed is between 5 and 12.
            #Monster health is between 40 and 120.
            #Monster damage is between 5 and 20.
            #Monster damage type is random one or the other (physical or magical).

            m_speed = randint(5, 12)
            m_hp = randint(40, 120)
            m_dmg = randint(5, 20)
            m_type = randint(0, 1)
            danger = Monster(m_speed, m_dmg, m_hp, m_type) #Initializing monster class
            print(f"Monster generated.")
            await ctx.send("There is a beast, and you must tenderize it!")

            while danger.life() == True:
                await ctx.send("Monsters speed is {1}, damage {2}, health {3}." .format(ctx, danger.speed(), danger.damage(), danger.health()))
            
                m_attk_str = danger.make_attack()
                m_attk = m_attk_str.split(" ")
                if "0" in m_attk:
                    await ctx.send("The monster is about to bite you!")
                elif "1" in m_attk:
                    await ctx.send("The monster is about to breathe fire at you!")

                def game_response(m): #Player response
                    if m.author == ctx.author:
                        return m.content == "Block" or m.content == "Dodge" or m.content == "Attack" or m.content == "Die"
                    else:
                        return False
                #Reactions to the monster's attack
                try:
                    g_msg = await bot.wait_for("message",timeout=m_speed, check=game_response)
                    if g_msg.content == "Block":
                        if "0" in m_attk:
                            if gamer.shield_type() == 1 or gamer.shield_type() == 3:
                                gamer.shield_hit()
                                await ctx.send("You block the attack!")
                                if gamer.shield_type() == 0:
                                    await ctx.send("Your shield shatters from the force of the blow.")
                            else:
                                await ctx.send("You try to block it, but your shield isn't rated for this kind of damage!")
                                bp_damage = int(m_attk[1])
                                gamer.take_hit(bp_damage)
                                curhp = gamer.health()
                                await ctx.send("Your health is {1}." .format(ctx, curhp))
                        if "1" in m_attk:
                            if gamer.shield_type() == 2 or gamer.shield_type() == 3:
                                gamer.shield_hit()
                                await ctx.send("You block the attack!")
                                if gamer.shield_type() == 0:
                                    await ctx.send("Your shield falls to pieces in a burst of multicolored light.")
                            else:
                                await ctx.send("The magical assault burns right through your shield!")
                                bm_damage = int(m_attk[1])
                                gamer.take_hit(bm_damage)
                                curhp = gamer.health()
                                await ctx.send("Your health is {1}." .format(ctx, curhp))

                    if g_msg.content == "Dodge":
                        await ctx.send("You roll to one side, avoiding some of the damage!")
                        d_damage = int(m_attk[1])
                        hit = d_damage - randint(5, 18)
                        gamer.take_hit(hit)
                        await ctx.send("Your health is {1}." .format(ctx, gamer.health()))

                    if g_msg.content == "Attack":
                        await ctx.send("You strike at the monster, but in doing so, expose yourself to the blow!") #Heh. Expose yourself. Good one, me.
                        a_damage = int(m_attk[1])
                        hit = a_damage + randint(5, 10)
                        gamer.take_hit(hit)
                        danger.take_hit(gamer.damage())
                        await ctx.send("Your health is {1}." .format(ctx, gamer.health()))

                    if g_msg.content == "Die":
                        await ctx.send("You die before the blow hits, confusing the monster.")
                        gamer.take_hit(gamer.health())

                except asyncio.TimeoutError:
                    await ctx.send("You didn't move fast enough! The attack lands!")
                    t_damage = int(m_attk[1])
                    gamer.take_hit(t_damage)
                    await ctx.send("Your health is {1}." .format(ctx, gamer.health()))

                if gamer.life() == False:
                    break

                await ctx.send("The monster rears back! Quickly, hit the thing!")

                def attack_response(m):
                    if m.author == ctx.author:
                        return m.content == "Attack"
                    else:
                        return False
                try:
                    a_msg = await bot.wait_for("message", timeout=m_speed, check=attack_response)
                    if a_msg.content == "Attack":
                        await ctx.send("You hit the monster!")
                        danger.take_hit(gamer.damage())

                except asyncio.TimeoutError:
                    await ctx.send("You didn't move fast enough!")

                #Right, by this point, the monster has attacked, and the player has attacked.
                #Need to check if the player is dead or not.
                if gamer.life() == False:
                    break
                #Only other option now is that the monster is still alive, requiring another turn, or it's dead, in which case...

            #We should end up here, outside the loop.

            if gamer.life() == True: #Necessary. Can break above loop without being alive, due to 'Die'.
                await ctx.send("The monster has been defeated.")
                slain_enemies = slain_enemies + 1
                lootroll = randint(0, 4)
                #Five cases. 0 - nothing. 1 - Physical shield. 2 - Magic shield. 3 - Health. 4 - Damage.
                if lootroll == 0:
                    await ctx.send("The monster dropped nothing.")
                if lootroll == 1:
                    await ctx.send("In the monster's digestive tract, you find a metal shield!")
                    gamer.get_shield(0)
                if lootroll == 2:
                    await ctx.send("In the monster's spleen, you find a runic shield, glowing with spellcraft!")
                    gamer.get_shield(1)
                if lootroll == 3:
                    healthroll = randint(5, 30)
                    await ctx.send("The monster's blood is a powerful restorative! You heal for {1}." .format(ctx, healthroll))
                    gamer.heal(healthroll)
                if lootroll == 4:
                    dmgroll = randint(3, 12)
                    await ctx.send("You monster's bones make an excellent weapon! Your damage increases by {1}." .format(ctx, dmgroll))
                    gamer.dangerify(dmgroll)

            #Loot handled. Looping again after describing player stats.

                await ctx.send("Your health is {1} and your damage is {2}." .format(ctx, gamer.health(), gamer.damage()))
                if gamer.shield_type() == 0:
                    await ctx.send("You have no shield.")
                elif gamer.shield_type() == 1:
                    await ctx.send("You have a sturdy metal shield. It can take {1} more hits." .format(ctx, gamer.shield_dur()))
                elif gamer.shield_type() == 2:
                    await ctx.send("You have a rune-inscribed shield. It can take {1} more hits." .format(ctx, gamer.shield_dur()))
                elif gamer.shield_type() == 3:
                    await ctx.send("You have an inscribed metal shield. Powerful! It can take {1} more hits." .format(ctx, gamer.shield_dur()))


                await ctx.send("Continue?")
                con_msg = await bot.wait_for("message", check=continue_check)
                if con_msg.content == "No":
                    break
        #End of combat loop. Player is dead.
        if game_roll == 2:
            await ctx.send("You encounter a great and terrible wizard.")
            await ctx.send("Continue?")
            con_msg = await bot.wait_for("message", check=continue_check)
        if game_roll == 3:
            await ctx.send("You stumble into a trap!")
            await ctx.send("Continue?")
            con_msg = await bot.wait_for("message", check=continue_check)
        if game_roll == 4:
            await ctx.send("Rocks fall, everyone dies.")
            await ctx.send("Continue?")
            con_msg = await bot.wait_for("message", check=continue_check)
        if game_roll == 5:
            await ctx.send("A man just walks up and punches you. What a jerk.")
            await ctx.send("Continue?")
            con_msg = await bot.wait_for("message", check=continue_check)
        #Placeholder maneuvers. Plan to expand game later with more events.
        #Get duel working for demo

    await ctx.send("You have died. Nice try, though! You killed {1} monsters." .format(ctx, slain_enemies))
    
@bot.command()
#Shoutout to my friend Janine for helping me cut this beast of a function in half.
async def duel(ctx, *, member: discord.Member):
    await ctx.send("You have challenged {1} to a duel! How do you respond {1}?".format(ctx, member))
    duelee = member # Discord member, shown as 'Wizard of Chaos#2459' or similar
    player1 = Player()
    dueler = ctx.author # ditto
    player2 = Player()

    def filter_tokens(msg, tokens):
        """Returns a list of tokens from the sequence that appear in the message."""
        text = msg.content.strip().lower()
        return [t for t in tokens if t in text]

    def check(m): # Check if duel is accepted
        return m.author == duelee and bool(filter_tokens(m, ('accept', 'decline')))

    try:
        msg = await bot.wait_for("message", timeout=20, check=check)
        tokens = filter_tokens(msg, ('accept', 'decline'))
        if len(tokens) > 1:
            await ctx.send("Your indecision has weirded out your opponent. Good job.")
            return
        if 'decline' == tokens[0]:
            await ctx.send("You have declined the challenge, everyone judges you.") #Coward.
            return
        if 'accept' == tokens[0]:
            await ctx.send("You have accepted the duel!")
    except asyncio.TimeoutError:
        await ctx.send("{1} appears to be absent. Coward.".format(ctx, duelee))
        return

    await ctx.send(
        "The duel has begun. The three attacks are 'critical strike', 'power attack', and 'flurry'. "
        "You can hit someone from the 'left' or the 'right', or just not pick a direction. "
        "You can also 'die'."
        )
    await ctx.send(
        "Critical strikes cannot be parried. "
        "Power attacks cannot be parried or blocked. "
        "Flurries cannot be blocked or dodged effectively."
        )
    #Slightly more in-depth explanation:
    #Critical strikes are blocked from the same direction they came in.
    #Attempting to roll in any direction other than the opposite of the incoming attack results in a hit.
    #Critical strikes cannot be parried, like, at all.
    #Flurries must be parried from the same direction. They can be dodged for reduced damage. They cannot be blocked.
    #Power attacks cannot be blocked or parried and MUST be dodged, to the opposite of the incoming direction.
    #Dodges have to go in the opposite direction or they fail.

    #Attack / defense checks based on incoming messages
    def attack_check(m, a):
        return m.author == a and bool(filter_tokens(m, attacks))
    def defense_check(m, a):
        return m.author == a and bool(filter_tokens(m, defenses))

    atk_time = 5 # Reaction time for players in seconds, set to 10 for demo, 5 during actual play
    attacks = ("critical strike", "flurry", "power attack", "die")
    defenses = ("parry", "dodge", "block", "die")
    dirs = ("left", "right")

    while True: # External infinite loop.
        for actor1, actor2, stats1, stats2 in ((duelee, dueler, player1, player2), (dueler, duelee, player2, player1)): # Turn order loop.
            if not(player2.life() and player1.life()): # Check if either player died during any turn.
                await ctx.send("{1} wins!".format(ctx, duelee if player1.life() else dueler))
                return

            await ctx.send("It's {1}'s turn to attack.".format(ctx, actor1))
            try:
                a1_msg = await bot.wait_for("message", timeout=20, check=lambda m: attack_check(m, actor1))
            except asyncio.TimeoutError:
                await ctx.send("{1} does nothing.".format(ctx, actor1))
                continue

            attack_tokens = filter_tokens(a1_msg, attacks)
            attack_dirs = filter_tokens(a1_msg, dirs)
            if len(attack_tokens) > 1 or len(attack_dirs) > 1:
                await ctx.send("{1} has wasted too much time on indecisive action and got confused!".format(ctx, actor1))
                continue

            attack_token = attack_tokens[0]
            attack_dir = attack_dirs[0] if attack_dirs else "top"
            if "die" == attack_token:
                await ctx.send("{1} screams that {2} will never understand their pain, then slits their wrists!".format(ctx, actor1, actor2))
                stats1.take_hit(100) # It's no surprise the emo movement failed, no surprise at all.
                continue

            await ctx.send("{1} throws out a {2} from the {3}!".format(ctx, actor1, attack_token, attack_dir))

            try:
                a2_msg = await bot.wait_for("message", timeout=atk_time, check=lambda m: defense_check(m, actor2))
            except asyncio.TimeoutError:
                await ctx.send("{1} doesn't move fast enough, and gets hit!".format(ctx, actor2))
                stats2.take_hit((20, 15, 10)[attacks.index(attack_token)])
                await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                continue

            defense_tokens = filter_tokens(a2_msg, defenses)
            defense_dirs = filter_tokens(a2_msg, dirs)
            if len(defense_tokens) > 1 or len(defense_dirs) > 1:
                await ctx.send("{1} doesn't get their act together fast enough and gets hit!".format(ctx, actor2))
                stats2.take_hit((20, 15, 10)[attacks.index(attack_token)])
                await ctx.send("{1} 's health is {2}.".format(ctx, actor2, player2.health()))
                continue

            defense_token = defense_tokens[0]
            defense_dir = defense_dirs[0] if defense_dirs else "top"
            if "die" == defense_token:
                await ctx.send("{1} accepts their fate and allows the blow to crush their skull!".format(ctx, actor2))
                stats2.take_hit(100)
                continue

            # A whole bunch of if/elif/else chains. Asyncio REALLY does not like when you try to call outside functions.
            # CRITICAL STRIKE:
            if "critical strike" == attack_token:
                if "left" == attack_dir:                                    
                    if "block" == defense_token:
                        if "left" == defense_dir:
                            await ctx.send("{1} blocks the strike.".format(ctx, actor2))
                        else:
                            await ctx.send("{1} tries to block, but misses the direction of the blow!".format(ctx, actor2))
                    elif "parry" == defense_token:
                        await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!".format(ctx, actor2))
                        stats2.take_hit(20)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if "left" == defense_dir:
                            await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!".format(ctx, actor2))
                            stats2.take_hit(40)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        elif "right" == defense_token:
                            await ctx.send("{1} dodges the blow.".format(ctx, actor2))
                        else:
                            await ctx.send("{1} misses the dodge.".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                elif "right" == attack_dir:
                    if "block" == defense_token:
                        if "right" == defense_dir:
                            await ctx.send("{1} blocks the strike.".format(ctx, actor2))
                        else:
                            await ctx.send("{1} tries to block, but misses the direction of the blow!".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "parry" == defense_token:
                        await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!".format(ctx, actor2))
                        stats2.take_hit(20)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if "right" == defense_dir:
                            await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!".format(ctx, actor2))
                            stats2.take_hit(40)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        elif "left" == defense_dir:
                            await ctx.send("{1} dodges the blow.".format(ctx, actor2))
                        else:
                            await ctx.send("{1} misses the dodge.".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                else:
                    if "block" == defense_token:
                        if defense_dir != "top":
                            await ctx.send("{1} fails to block the central strike!".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        else:
                            await ctx.send("{1} blocks the strike.".format(ctx, actor2))
                    elif "parry" == defense_token:
                        await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!".format(ctx, actor2))
                        stats2.take_hit(20)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if defense_dir != "top":
                            await ctx.send("{1} tries to roll, but gets slapped anyway!".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        else:
                            await ctx.send("{1} dodges the blow.".format(ctx, actor2))
            #All critical strike maneuvers handled.

            #FLURRY:
            if "flurry" == attack_token:
                if "left" == attack_dir:
                    if "block" == defense_token:
                        await ctx.send("{1} attempts to block the blows, but there's just too many!".format(ctx, actor2))
                        stats2.take_hit(10)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "parry" == defense_token:
                        if "left" == defense_dir:
                            await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!".format(ctx, actor2, actor1))
                            stats1.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor1, stats1.health()))
                        else:
                            await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!".format(ctx, actor2))
                            stats2.take_hit(15)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if "left" == defense_dir:
                            await ctx.send("{1} tries to roll out of the way, but rolls straight into the blows!".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        elif "right" == defense_dir:
                            await ctx.send("{1} dodges most of the blows, but takes one across the back!".format(ctx, actor2))
                            stats2.take_hit(5)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        else:
                            await ctx.send("{1} misses the dodge.".format(ctx, actor2))
                            stats2.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                elif "right" == attack_dir:
                    if "block" == defense_token:
                        await ctx.send("{1} attempts to block the blows, but there's just too many!".format(ctx, actor2))
                        stats2.take_hit(10)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "parry" == defense_token:
                        if "right" == defense_dir:
                            await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!".format(ctx, actor2, actor1))
                            stats1.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor1, stats1.health()))
                        else:
                            await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!".format(ctx, actor2))
                            stats2.take_hit(15)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if "right" == defense_dir:
                            await ctx.send("{1} tries to roll out of the way, but rolls straight into the blows!".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        elif "left" == defense_dir:
                            await ctx.send("{1} dodges most of the blows, but takes one across the back!".format(ctx, actor2))
                            stats2.take_hit(5)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        else:
                            await ctx.send("{1} misses the dodge.".format(ctx, actor2))
                            stats2.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                else:
                    if "block" == defense_token:
                        await ctx.send("{1} attempts to block the blows, but there's just too many!".format(ctx, actor2))
                        stats2.take_hit(10)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "parry" == defense_token:
                        if defense_dir != "top":
                            await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!".format(ctx, actor2))
                            stats2.take_hit(5)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        else:
                            await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!".format(ctx, actor2, actor1))
                            stats1.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor1, stats1.health()))
                    elif "dodge" == defense_token:
                        if defense_dir != "top":
                            await ctx.send("{1} tries to roll, but gets slapped anyway!".format(ctx, actor2))
                            stats2.take_hit(15)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        else:
                            await ctx.send("{1} dodges most of the blows, but takes one hit anyway!".format(ctx, actor2))
                            stats2.take_hit(5)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
            #Flurry maneuvers handled.

            #POWER ATTACK:
            if "power attack" == attack_token:
                if "left" == attack_dir:
                    if "block" == defense_token:
                        await ctx.send("{1} tries to block, but the blow is too much!".format(ctx, actor2))
                        stats2.take_hit(10)
                    elif "parry" == defense_token:
                        await ctx.send("{1} attempts to parry, but the blow is too much!".format(ctx, actor2))
                        stats2.take_hit(10)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if "left" == defense_dir:
                            await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        elif "right" == defense_dir:
                            await ctx.send("{1} dodges the blow.".format(ctx, actor2))
                        else:
                            await ctx.send("{1} misses the dodge.".format(ctx, actor2))
                            stats2.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                elif "right" == attack_dir:
                    if "block" == defense_token:
                        await ctx.send("{1} tries to block, but the blow is too much!".format(ctx, actor2))
                        stats2.take_hit(10)
                    elif "parry" == defense_token:
                        await ctx.send("{1} attempts to parry, but the blow is too much!".format(ctx, actor2))
                        stats2.take_hit(10)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if "right" == defense_dir:
                            await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!".format(ctx, actor2))
                            stats2.take_hit(20)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        elif "left" == defense_dir:
                            await ctx.send("{1} dodges the blow.".format(ctx, actor2))
                        else:
                            await ctx.send("{1} misses the dodge.".format(ctx, actor2))
                            stats2.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                else:
                    if "block" == defense_token:
                        await ctx.send("{1} tries to block, but the blow is too much!".format(ctx, actor2))
                        stats2.take_hit(10)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "parry" == defense_token:
                        await ctx.send("{1} attempts to parry, but the blow is too much!".format(ctx, actor2))
                        stats2.take_hit(10)
                        await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                    elif "dodge" == defense_token:
                        if defense_dir:
                            await ctx.send("{1} tries to roll, but gets slapped anyway!".format(ctx, actor2))
                            stats2.take_hit(10)
                            await ctx.send("{1} 's health is {2}.".format(ctx, actor2, stats2.health()))
                        else:
                            await ctx.send("{1} dodges the blow.".format(ctx, actor2))
            # Power attacks handled.
            # All attacks handled. Next player's attack.
#END DUEL

#Sets up a group of commands.
#The bot.group initializes the group. The test is just whatever can include a subcommand.
#To write subfunctions its @initial.command().

@bot.group()
async def test(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("INVALID")

@test.command()
async def highfive(ctx):
    await ctx.send("Up top!")

#Called by "~test [command]" 
#Quick example of how this works; no need to use it with current stuff
#DUEL COMMAND

@test.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send('{0} joined on {0.joined_at}' .format(member))




#Actual run command for the bot. Numerals and garbage are the "token" for the bot, allowing it to sorta log in to its own account.
#No steal pls.
bot.run('NjQzNTM0NTM2NzM0NjcwODU4.Xc7_mQ.iSu0vF3l0_OmwOPwWcDt101o5BQ')