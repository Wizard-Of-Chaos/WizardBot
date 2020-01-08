@bot.command()
async def duel(ctx, *, member: discord.Member):
    await ctx.send("You have challenged {1} to a duel! How do you respond {1}?" .format(ctx, member))
    duelee = member #Discord member, shown as 'Wizard of Chaos#2459' or similar
    player1 = Player()
    dueler = ctx.author #ditto
    player2 = Player()
    def check(m): #Check to for accepting the duel
        if m.author == duelee:
            return m.content == "Accept" or m.content == "Decline"
        else:
            return False
    try:
        msg = await bot.wait_for("message", timeout=20, check=check)
        if msg.content == "Accept":
            await ctx.send("You have accepted the duel!")
        elif msg.content == "Decline":
            await ctx.send("You have declined the challenge, everyone judges you.") #Coward.
    except asyncio.TimeoutError:
        await ctx.send("{1} appears to be absent. Coward." .format(ctx, duelee))
        return
    await ctx.send("The duel has begun. The three attacks are 'critical strike', 'power attack', and 'flurry'. You can hit someone from the 'left' or the 'right', or just not pick a direction. You can also 'die'.")
    await ctx.send("Critical strikes cannot be parried. Power attacks cannot be parried or blocked. Flurries cannot be blocked or dodged effectively.")
    #Slightly more in-depth explanation:
    #Critical strikes are blocked from the same direction they came in. Attempting to roll in any direction other than the opposite of the incoming attack results in a hit.
    #Critical strikes cannot be parried, like, at all.
    #Flurries must be parried from the same direction. They can be dodged for reduced damage. They cannot be blocked.
    #Power attacks cannot be blocked or parried and MUST be dodged, to the opposite of the incoming direction.
    #Dodges have to go in the opposite direction or they fail.
    
    atk_time = 5 #Reaction time for players in seconds, set to 10 for demo, 5 during actual play
    while player1.life() == True and player2.life() == True:
        await ctx.send("It's {1}'s turn to attack." .format(ctx, duelee))

        #Attack / defense checks based on incoming messages
        def p1_attack_check(m):
            if m.author == duelee:
                if "critical strike" in m.content or "flurry" in m.content or "power attack" in m.content or "die" in m.content:
                    return True
            else:
                return False
        def p1_defense_check(m):
            if m.author == duelee:
                if "parry" in m.content or "dodge" in m.content or "block" in m.content or "die" in m.content:
                    return True
            else:
                return False
        def p2_attack_check(m):
            if m.author == dueler:
                if "critical strike" in m.content or "flurry" in m.content or "power attack" in m.content or "die" in m.content:
                    return True
            else:
                return False
        def p2_defense_check(m):
            if m.author == dueler:
                if "parry" in m.content or "dodge" in m.content or "block" in m.content or "die" in m.content:
                    return True
            else:
                return False
                
        #Whole bunch of if/elif/else chains. Asyncio REALLY does not like when you try to call outside functions.
        try:
            p1_msg = await bot.wait_for("message", timeout=20, check=p1_attack_check)
            
            if "die" in p1_msg.content:
                await ctx.send("{1} screams that {2} will never understand their pain, then slits their wrists!" .format(ctx, duelee, dueler))
                player1.take_hit(100) #It's no surprise the emo movement failed
                
            #CRITICAL STRIKE:
            if "critical strike" in p1_msg.content:
                
                if "left" in p1_msg.content:
                    await ctx.send("{1} throws out a critical strike from the left!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)
                        elif "block" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} blocks the strike." .format(ctx, dueler))
                            else:
                                await ctx.send("{1} tries to block, but misses the direction of the blow!" .format(ctx, dueler))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!" .format(ctx, dueler))
                            player2.take_hit(20)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, dueler))
                                player2.take_hit(40)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            elif "right" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, dueler))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(20)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))

                elif "right" in p1_msg.content:
                    await ctx.send("{1} throws out a critical strike from the right!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)
                        elif "block" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} blocks the strike." .format(ctx, dueler))
                            else:
                                await ctx.send("{1} tries to block, but misses the direction of the blow!" .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!" .format(ctx, dueler))
                            player2.take_hit(20)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, dueler))
                                player2.take_hit(40)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            elif "left" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, dueler))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(20)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))

                else:
                    await ctx.send("{1} throws out a critical strike from the top!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)                        
                        elif "block" in p2_msg.content:
                            if "left" in p2_msg.content or "right" in p2_msg.content:
                                await ctx.send("{1} fails to block the central strike!" .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} blocks the strike." .format(ctx, dueler))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!" .format(ctx, dueler))
                            player2.take_hit(20)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content or "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll, but gets slapped anyway!" .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} dodges the blow." .format(ctx, dueler))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(20)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))

            #All critical strike maneuvers handled.
            
            #FLURRY:
            if "flurry" in p1_msg.content:
            
                if "left" in p1_msg.content:
                    await ctx.send("{1} throws out a flurry of blows from the left!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} attempts to block the blows, but there's just too many!" .format(ctx, dueler))
                            player2.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "parry" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!" .format(ctx, dueler, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!" .format(ctx, dueler))
                                player2.take_hit(15)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blows!" .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            elif "right" in p2_msg.content:
                                await ctx.send("{1} dodges most of the blows, but takes one across the back!" .format(ctx, dueler))
                                player2.take_hit(5)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(15)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                elif "right" in p1_msg.content:
                    await ctx.send("{1} throws out a flurry of blows from the right!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} attempts to block the blows, but there's just too many!" .format(ctx, dueler))
                            player2.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "parry" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!" .format(ctx, dueler, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!" .format(ctx, dueler))
                                player2.take_hit(15)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blows!" .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            elif "left" in p2_msg.content:
                                await ctx.send("{1} dodges most of the blows, but takes one across the back!" .format(ctx, dueler))
                                player2.take_hit(5)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(15)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                else:
                    await ctx.send("{1} throws out a flurry of blows from the top!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)                        
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} attempts to block the blows, but there's just too many!" .format(ctx, dueler))
                            player2.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "parry" in p2_msg.content:
                            if "left" in p2_msg.content or "right" in p2_msg.content:
                                await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!" .format(ctx, dueler))
                                player2.take_hit(5)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!" .format(ctx, dueler, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content or "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll, but gets slapped anyway!" .format(ctx, dueler))
                                player2.take_hit(15)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} dodges most of the blows, but takes one hit anyway!" .format(ctx, dueler))
                                player2.take_hit(5)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(15)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        
            #Flurry maneuvers handled.

            #POWER ATTACK:
            if "power attack" in p1_msg.content:
                
                if "left" in p1_msg.content:
                    await ctx.send("{1} throws out a powerful blow from the left!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)                        
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} tries to block, but the blow is too much!" .format(ctx, dueler))
                            player2.take_hit(10)
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too much!" .format(ctx, dueler))
                            player2.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            elif "right" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, dueler))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(10)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))

                elif "right" in p1_msg.content:
                    await ctx.send("{1} throws out a powerful blow from the right!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)                        
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} tries to block, but the blow is too much!" .format(ctx, dueler))
                            player2.take_hit(10)
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too much!" .format(ctx, dueler))
                            player2.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, dueler))
                                player2.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            elif "left" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, dueler))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(10)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                else:
                    await ctx.send("{1} throws out a powerful blow from the top!" .format(ctx, duelee))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p2_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, dueler))
                            player2.take_hit(100)                        
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} tries to block, but the blow is too much!" .format(ctx, dueler))
                            player2.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too much!" .format(ctx, dueler))
                            player2.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content or "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll, but gets slapped anyway!" .format(ctx, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} dodges the blow." .format(ctx, dueler))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, dueler))
                        player2.take_hit(10)
                        await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        
            #All attacks handled. Player 2's attack.
            #It's the exact same code as above. Maybe make it all one function?
            
            
        except asyncio.TimeoutError:
            await ctx.send("{1} does nothing." .format(ctx, duelee))
        if player2.life() == False or player1.life() == False: #Check if either player died during the first turn; otherwise next turn triggers while one player is dead
            break
        await ctx.send("It's {1}'s turn!" .format(ctx, dueler))
        
        try:
            p1_msg = await bot.wait_for("message", timeout=20, check=p2_attack_check)
            
            if "die" in p1_msg.content:
                await ctx.send("{1} screams that {2} will never understand their pain, then slits their wrists!" .format(ctx, dueler, duelee))
                player2.take_hit(100)
                
            if "critical strike" in p1_msg.content:
                
                if "left" in p1_msg.content:
                    await ctx.send("{1} throws out a critical strike from the left!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                        
                        elif "block" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} blocks the strike." .format(ctx, duelee))
                            else:
                                await ctx.send("{1} tries to block, but misses the direction of the blow!" .format(ctx, duelee))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!" .format(ctx, duelee))
                            player1.take_hit(20)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, duelee))
                                player1.take_hit(40)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            elif "right" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, duelee))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(20)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))

                elif "right" in p1_msg.content:
                    await ctx.send("{1} throws out a critical strike from the right!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                        
                        elif "block" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} blocks the strike." .format(ctx, duelee))
                            else:
                                await ctx.send("{1} tries to block, but misses the direction of the blow!" .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!" .format(ctx, duelee))
                            player1.take_hit(20)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, duelee))
                                player1.take_hit(40)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            elif "left" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, duelee))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(20)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                else:
                    await ctx.send("{1} throws out a critical strike from the top!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                          
                        elif "block" in p2_msg.content:
                            if "left" in p2_msg.content or "right" in p2_msg.content:
                                await ctx.send("{1} fails to block the central strike!" .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} blocks the strike." .format(ctx, duelee))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too precisely aimed!" .format(ctx, duelee))
                            player1.take_hit(20)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content or "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll, but gets slapped anyway!" .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} dodges the blow." .format(ctx, duelee))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(20)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))


            #Critical strike handled.
            if "flurry" in p1_msg.content:
            
                if "left" in p1_msg.content:
                    await ctx.send("{1} throws out a flurry of blows from the left!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                          
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} attempts to block the blows, but there's just too many!" .format(ctx, duelee))
                            player1.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "parry" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!" .format(ctx, duelee, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!" .format(ctx, duelee))
                                player1.take_hit(15)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blows!" .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            elif "right" in p2_msg.content:
                                await ctx.send("{1} dodges most of the blows, but takes one across the back!" .format(ctx, duelee))
                                player1.take_hit(5)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(15)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                elif "right" in p1_msg.content:
                    await ctx.send("{1} throws out a flurry of blows from the right!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                          
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} attempts to block the blows, but there's just too many!" .format(ctx, duelee))
                            player1.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "parry" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!" .format(ctx, duelee, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                            else:
                                await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!" .format(ctx, duelee))
                                player1.take_hit(15)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blows!" .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            elif "left" in p2_msg.content:
                                await ctx.send("{1} dodges most of the blows, but takes one across the back!" .format(ctx, duelee))
                                player1.take_hit(5)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(15)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                else:
                    await ctx.send("{1} throws out a flurry of blows from the top!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                          
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} attempts to block the blows, but there's just too many!" .format(ctx, duelee))
                            player1.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "parry" in p2_msg.content:
                            if "left" in p2_msg.content or "right" in p2_msg.content:
                                await ctx.send("{1} tries to parry, but misjudges the direction and gets hit!" .format(ctx, duelee))
                                player1.take_hit(15)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} easily parries the attacks, redirecting them onto {2}!" .format(ctx, duelee, dueler))
                                player2.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, dueler, player2.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content or "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll, but gets slapped anyway!" .format(ctx, duelee))
                                player1.take_hit(15)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} dodges most of the blows, but takes one hit anyway!" .format(ctx, duelee))
                                player1.take_hit(5)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(15)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        
            #Flurries handled.

            if "power attack" in p1_msg.content:
                
                if "left" in p1_msg.content:
                    await ctx.send("{1} throws out a powerful blow from the left!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                          
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} tries to block, but the blow is too much!" .format(ctx, duelee))
                            player1.take_hit(10)
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too much!" .format(ctx, duelee))
                            player1.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            elif "right" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, duelee))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(10)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))

                elif "right" in p1_msg.content:
                    await ctx.send("{1} throws out a powerful blow from the right!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                          
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} tries to block, but the blow is too much!" .format(ctx, duelee))
                            player1.take_hit(10)
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too much!" .format(ctx, duelee))
                            player1.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content:
                                await ctx.send("{1} tries to roll out of the way, but rolls straight into the blow!" .format(ctx, duelee))
                                player1.take_hit(20)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            elif "left" in p2_msg.content:
                                await ctx.send("{1} dodges the blow." .format(ctx, duelee))
                            else:
                                await ctx.send("{1} misses the dodge." .format(ctx, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(10)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))

                else:
                    await ctx.send("{1} throws out a powerful blow from the top!" .format(ctx, dueler))
                    try:
                        p2_msg = await bot.wait_for("message", timeout=atk_time, check=p1_defense_check)
                        if "die" in p2_msg.content:
                            await ctx.send("{1} accepts their fate and allows the blow to split their skull!" .format(ctx, duelee))
                            player1.take_hit(100)                          
                        elif "block" in p2_msg.content:
                            await ctx.send("{1} tries to block, but the blow is too much!" .format(ctx, duelee))
                            player1.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "parry" in p2_msg.content:
                            await ctx.send("{1} attempts to parry, but the blow is too much!" .format(ctx, duelee))
                            player1.take_hit(10)
                            await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        elif "dodge" in p2_msg.content:
                            if "right" in p2_msg.content or "left" in p2_msg.content:
                                await ctx.send("{1} tries to roll, but gets slapped anyway!" .format(ctx, duelee))
                                player1.take_hit(10)
                                await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                            else:
                                await ctx.send("{1} dodges the blow." .format(ctx, duelee))
                    except asyncio.TimeoutError:
                        await ctx.send("{1} doesn't move fast enough, and gets hit!" .format(ctx, duelee))
                        player1.take_hit(10)
                        await ctx.send("{1} 's health is {2}." .format(ctx, duelee, player1.health()))
                        
            #All attacks handled. Player 1's attack.
        except asyncio.TimeoutError:
            await ctx.send("{1} does nothing." .format(ctx, dueler))
    #Someone's dead.
    if player1.life() == False:
        await ctx.send("{1} wins!" .format(ctx, dueler))
    else:
        await ctx.send("{1} wins!" .format(ctx, duelee))