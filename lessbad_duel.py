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