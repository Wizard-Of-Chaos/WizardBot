README FOR WIZBOT 1.0

COMMAND PREFIX: ~

USING WIZBOT (CMSC280 ONLY):

Get Discord and create a server with it (easy to do).
Add WizardBot to your server with the following link in a browser - https://discordapp.com/api/oauth2/authorize?client_id=643534536734670858&permissions=0&scope=bot 
Install the discord.py library, as well as any supporting libraries it might need.
Run "wizbot.py" (python3 wizbot.py).

NOTICE FOR DR BLAHETA: 
The wizbot.py file includes a token down at the bottom in the bot.run() command.
This is what allows WizardBot to "log in" to its own account and start running. It's kind of the password to the account.
Theoretically, you could modify the code to do whatever you want, using the bot account, so this is a little insecure for the final project, but there aren't any other options that allow you, personally, to run the code.
We'll be changing the token in a month or two so that this won't happen, but as soon as you look at the code, run WizardBot, and are done with it, please let us (Sandy and Grant) know so we can change the token. Sandy plans to continue using and updating the bot for his own purposes post-CMSC280.

EVENTS:
startup - will print out "wizardbot has connected to discord" in terminal
EAT THAT HORSE! - upon seeing this message, it will print a horse emoji

COMMANDS:

~hello - prints out "Hello, World!"

~slap [argument] - slaps who or whatever the argument is

~echo [argument] - will cause the bot to print out whatever you just said, use quotation marks for more than one word

~up [argument] - turns whatever you typed to uppercase

~roll [argument] - will roll a random number with the given argument. So ~roll 20 will be a random number between 1 and 20

TEST SUBFUNCTIONS:

~test - base command, prints out INVALID

~test highfive - prints "Up top!"

GAMES:

~game - Starts up a monster fighting game.
Player picks either health or damage as a starting buff.
Can block, dodge, or attack when a monster attacks it.
The player has the monster's SPEED - printed out - in seconds to react.

BLOCKING - Will stop all damage, provided the player has the requisite shield type (physical or magical). Uses one durability point.
DODGING - Reduces some of the damage taken.
ATTACK - Take extra damage, but make an attack on the monster.
DIE - Ends game immediately.

On the monster's attack, you can attack back.
Will drop either healing, damage, a shield or nothing on death.
Game ends when player dies.

~duel [argument] - Challenges another user on the server to a duel.
If they type "Accept" within 20 seconds, the duel begins. (Decline or no response will stop the command)

Players may enter in any text string that includes the phrases "critical strike", "power attack", or "flurry" (case sensitive) as their attack, and including an optional "left" or "right" (defaults to middle).
USAGE:
WizardBot: It's Cuban#5305's turn to attack.
Cuban: critical strike left
WizardBot: Cuban#5305 throws out a critical strike from the left!

The response from the enemy player is any text string that includes "dodge", "block", or "parry", as well as a direction (again left or right, defaulting to middle).
USAGE FROM ABOVE EXAMPLE:
Wizard of Chaos: block left
WizardBot: Wizard of Chaos#2459 blocks the strike.
WizardBot: It's Wizard of Chaos#2459's turn to attack.
Wizard of Chaos: i'm gonna power attack him from the right
WizardBot: Wizard of Chaos#2459 throws out a powerful blow from the right!
Cuban: right dodge!
WizardBot: Cuban#5305 tries to roll out of the way, but rolls straight into the blow!
WizardBot: Cuban#5305 's health is 80.
WizardBot: It's Cuban#5305's turn to attack.


CRITICAL STRIKE: Must be blocked from the same direction it came from (left, right, or none). Parries fail. Dodge works on opposite direction.
FLURRY: Can be parried from same direction it came from. Cannot be blocked. Can be dodged, opposite direction, for reduced damage.
POWER ATTACK: Cannot be blocked or parried. Must be dodged in opposite direction.

The game ends when one player's health goes to 0 or below. Each player starts out at 100 health.

ALL ERROR MESSAGES ARE PRINTED OUT IN THE TERMINAL WINDOW
THE BOT WILL CONTINUE RUNNING EVEN IF IT ENCOUNTERS AN EXCEPTION
