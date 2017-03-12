## Characters

Characters are made up of several features. These features are described below.


### Character Features

#### Core Aspects

All characters come with three aspects by default. These are: strength, mobility and intelligence.


#### Basic Move

All characters come with a basic move of 5 map cells. This can be modified by aspects.


#### Health Point Pool

Character damage is represented by health points. A character has a certain pool of health poitns representing just how much damage they can take.

Health point pools, unmodified, start with a maximum of 6 for all characters. This is due to how the damage scales with aspect points as defined in the aspects document.


#### Energy Point Pool

Character endurance and execution of combat actions are represented as energy points. A character has a certain pool of energy points representing just how much endurance they can expend in a short period of time (the time of one turn).

Energy point pools, unmodified, start with a maximum of 1 for all characters.


### Aspects

Aspects describe parts of a character. They may include rules and modifiers that apply to the character. All aspects have an aspect point cost that must be paid when acquired. Once acquired, many aspects impart an ability that the character can utilize or an effect that triggers. These effects are all outlined in the rules of the aspect.


#### Aspect Points

Characters are granted a certain number of aspect points at the start of a new game. This pool of points allows a player to customize their characters. The pool of aspect points may be divided amongst a player's characters as the player sees fit with one exception: each character must have at least 1 apsect point invested.

Aspect points are the primary mechanisim for character advancement. They are granted at the start of a new campaign and at important events during the campaign. In addition to important events, game masters are encouraged to reward players by granting additional aspect points.


#### Progression

Throughout a campaign, players will acrew aspect points as part of the party's progression. These points may be spent during downtime. The game master may declare any point during the campaign as downtime. Long rests that the party can take safely almost always qualify but it is up to the game master to say whether or not a rest may be considered downtime.

During downtime, characters may reflect on what they have experienced and learned recently.

#### Upgrading Aspects

With enough use of an aspect, there may come benefits from mastery. During downtime, players may upgrade character aspects that have seen frequent use.

Players may not add new features to an aspect, they may only modify what the aspect grants.

##### Aspect Upgrade Example

During downtime, Claire decides to upgrade her Character, Nala's, Spell Dart aspect. She wants it to have a stronger punch and decides that the spell should do 1d6 in damage instead of 1d4. This change in cost is paid by the player and the aspect is considered upgraded at this point. In this case the cost difference is one aspect point.


#### Acquiring New Aspects

As your characters grow, so should their abilities.

Once a character successfully utilizes a new aspect (see Using Unlearned Aspect Skills), they may then attempt to acquire it during downtime as described in **Progression**. This requires the character to utilize the new aspect successfully during downtime with no negative modifier. Upon failure, the character must wait until the next downtime to attempt to acquire the aspect. Upon success, the player may spend the necessary aspect points and acquire the aspect.


### Core Aspects

Core aspects are character aspects that come with every character created. These are the basis for the primary ability checks a character can make and also represent the three primary physical features of the character.


#### Strength

Strength determines a character's physical presence. A character with a strong strength aspect will be able to last longer and carry more. They may also take less damage when thrown around or when overpowered. Strength is also a primary factor in determining a character's physical endurance and constitution.

Strength is important for characters that will have physically demanding professions or strength oriented ability focuses (melee combat for example).


##### Strength Damage

While a character is subject to a negative strength modifier they must make a strength check against a difficulty of 10 plus the value of the negative modifier. This check must be made every turn unless the character is incapacitated.

Failing this check grants the character the stunned condition until their next turn and renders the character prone if they are not already prone.


#### Intelligence

Intelligence determines a character's ability to both retain information and process complex problems. A character's intelligence also plays a factor in the character's outward ability to communicate. A character with a low intelligence aspect may find it difficult to interact with certain non-player characters and or other characters.

Intelligence also serves as a character's internal voice. Characters with higher intelligence will often have a more rational approach to mind affecting effects. However, the opposite is true for lower intelligence characters in that they can simply chose to ignore the effect.


##### Intelligence Damage

While a character is subject to a negative intelligence modifier they must make an intelligence check against a difficulty of 10 plus the value of the negative modifier. This check must be made every turn unless the character is incapacitated.

Failing this check immediately grants the unconscious condition until their next turn and renders the character prone if they are not already prone.


#### Mobility

Mobility is a core aspect that determines a character's ability to move quickly. Mobility also represents a character’s inherent balance and muscle control – making it important for dodging attacks and environment hazards. A character’s reflexes are dependent on the character’s mobility.

Mobility also plays a direct roll in jumping and scaling obstacles as well as performing maneuvers during movement.


##### Mobility Damage

While a character is subject to a negative mobility modifier they must make a mobility check against a difficulty of 10 plus the value of the negative modifier. This check must be made every turn unless the character is incapacitated.

Failing this check removes the character’s ability to attempt any dodge until their next turn and renders the character prone if they are not already prone.


## Game Mechanics

This section is dedicated to explaining many of the mechanics that make combat work in The Crawl.


### Map Details

The game recommends utilizing a hexagon grid map. When a hexagon grid is not available, a square grid may be used in substitution. When using a square grid, each square may be treated as a position with eight possible directions instead of four by using both the edges and corners of the squares. 

Each cell on a map represents **2 meters**.


#### Range Definitions

There are a number of range definitions to help easily determine distance ranges on a map. All ranges assume that the starting cell is the point of origin, not the cell’s edge. This means that the cell your character is standing in is equivalent to a range of one.


#### Range Classes

##### Personal
Personal range applies only to a target or character. This means that effects targeting personal range do not affect targets considered squeezing in the same map cell.

##### Close
Close range is equal to a radius of 1 cell. This covers 1 map cell in total. This range affects the target cell only.

##### Melee
Melee range is equal to a radius of 2 cells. This covers 7 map cells total. Melee range is also dependent on character abilities and may vary from character to character.

##### Short
Short range is equal to a radius of 7 cells or a total of 14 meters.

##### Medium
Medium range is equal to a radius of 15 cells or a total of 30 meters.

##### Long
Long range is equal to a radius of 30 cells or a total of 60 meters.

##### Extreme
Extreme range is equal to a radius of 60 cells or a total of 120 meters.


#### Range Penalty

Using an aspect on a target outside of it's range incurs a negative to the skill check associated with the aspect - attack or otherwise. This negative is equal to the number of range classes the target is beyond the aspect's range.

Any target beyond extreme range may have a negative modifier assigned to it at the game master's discretion.

##### Examples

A character targeting an enemy at medium range with an attack that's only effective at short range gives the character a -1 modifier to their attack.

A character targeting an enemy at extreme range with an attack that's only effective at short range gives the character a -3 modifier to their attack.

A character targeting an enemy far beyond extreme range with an attack that's only effective at short range may be given a -5 modifier by the game master.


#### Area Effects

Because area effects fill entire map cells, targeted characters may not make dodge attempts to avoid the area effect. Because of this, many area attacks will include a check that characters may make to potentially mitigate some or all of the effects.


#### Rough Terrain

Character movement speed is halved when the character steps into any significantly damaged or disturbed terrain. Rough terrain may also prevent certain combat maneuvers and also grants a -2 modifier to any mobility check of any character standing on it.

Stepping in or out of rough terrain immedieately incurs this penalty.


### Object and Character Size Modifiers

By default all characters are treated as a 1.7 meter (~5 1/2 feet) tall humanoid. Deviations from this may be added to an aspect to modify a character's overall size. Object sizes must source their relative costs from this modifier.

* Size -4
    * Macroscopic or Insect
* Size -3
    * 0.0 meters - 0.3 meters
* Size -2
    * 0.3 meters - 1.0 meters
* Size -1
    * 1.0 meters - 1.5 meters
* Size 0
    * 1.5 meters - 2.0 meters
* Size 1
    * 2.0 meters - 2.5 meters
* Size 2
    * 2.5 meters - 3.5 meters
* Size 3
    * 3.5 meters - 5.0 meters
* Size 4
    * Gargantuan or Dinosaur


### Equipment

Characters may have equipment. Weight is optional but trackable. Most items will require a slot to be equipped.

#### Using Shields

Unless a character has a defense aspect that allows the use of a shield, the shield may only provide it's DR modifiers to the character. Certain aspects may allow shields to be used to completely block an incoming attack or defend against an attack that targets a near by ally.

#### Lightweight Items

Lightweight items are items that may be worn without changing the available equipment slots on the character. They are, as their name implies, lightweight and therefore on their own do not generally affect the use of the limb they are worn on.

However, lightweight items can add up!

Stacking more than 2 lightweight items in the same equipment slot incurs a stacking -1 modifier to the character's mobility. This negative modifier stacks both if the character has more than one overloaded equipment or has overloaded a single slot with more than 2 lightweight items.

#### Slots

Certain items may require a character to equip it to a specific slot. The available slots are listed below.

* Head
    * The head slot covers not just the character's head but also their neck.
* Arms
    * Items and armor that slot for a character's arms must take into consideration both arms. Lightweight items that are slotted for the arms may specify if they fit on both or on one arm.
* Torso
    * A character's torso is the largest single hit location.
* Legs
    * Items and armor that slot for a character's legs must take into consideration both legs. Lightweight items that are slotted for the legs may specify if they fit on both or on one leg.

#### Max Weight

**Note: This is an optional rule.**

Characters are able to carry a base weight of 25kg (~55lb). For each positive strength modifier, this limit increases according to the table below:

|Modifier|Weight Capacity|
|---|---|
|+1 Core Strength|50kg|
|+2 Core Strength|80kg|
|+3 Core Strength|110kg|
|+4 Core Strength|170kg|
|+5 Core Strength|260kg|
|+6 Core Strength|410kg|
|+7 Core Strength|650kg|
|+8 Core Strength|1040kg|
|+9 Core Strength|1670kg|
|+10 Core Strength|2690kg|

#### Weight Encumberance

**Note: This is an optional rule.**

Characters that are carrying more than their weight capacity are subject to negative mobility modifiers.

|Modifier|Weight Capacity|
|---|---|
| Up to **20kg** | -1 Core Mobility |
| Up to **45kg** | -2 Core Mobility |
| Up to **70kg** | -3 Core Mobility |
| Up to **100kg** | -4 Core Mobility |
| Up to **130kg** | -5 Core Mobility |
| Greater than **130kg** | **Character is Immobile** |

### Initiative

All characters are required to roll for initiative when combat begins. Initative controls which characters go when and in what order. All initiative rolls are a d20. Additional modifiers specific to the character may apply after the roll.

Combat follows initiative order. The character with the highest value for initiative receives their turn next. Once the character completes their turn, the next turn is granted to the character with the next highest value for initiative.

    For example: characters A, B, and C roll for initiative.
    
    * Character A rolls a 2.
    * Character B rolls a 5.
    * Character C rolls a 2.
    
    Character C has a +1 modifier which, when applied, puts their initiative total at a 3.
    
    The initiative is then ordered with character B going first, character C going second and character A going last.
    
    B recieves their turn.
    C recieves their turn after B.
    A recieves their turn after A.
    
    B recieves their next turn.
    C recieves their turn after B.
    A recieves their turn after A.
    
    ...


### Turn Duration

Turns in the crawl last for only a moment. There is no exact interval given here to avoid players attempting to rationalize for or against an action that may not fit. General rules for what fits in a moment follow:

**A moment is long enough to...**

* Execute an attack.
* Open a door.
* Pull out something from your traveler's pack.
* Speak a short sentence to another character and recieve an equally short reply.


### Effort

Certain character actions cost effort in the form of energy points. During the beginning of a character's turn, the character recieves 1 energy point. Energy points may be saved for future turns to pay for more powerful or complex actions.

Characters may save energy points according to their own aspects.

Characters may have aspects that grant additional energy points under certain circumstances. Certain equipment and magic may also grant use of additional energy points.


#### Maximum Effort

A character may choose to spend health points and convert them into an energy points in times of dire need. This loss of health points counts as damage to the character and is treated the same. Aspects and effects may modify this rule.

Maximum effort may only be used in the following circumstances:

* **Attacks**
    * A character may choose to spend **2 Health Points** to perform one final attack on their turn. This may only be used at the end of the character's turn and only if the character has exhausted all their energy points.
* **Defense**
    * A character may choose to spend **2 Health Points** to perform a defense. As long as the character has a positive amount of healh points, the character may spend them to perform additional defenses. To clarify, a character may not use maximum effort if they have less than 0 health points in their health pool or if by using maximum effort the character would then have less than 0 health points.


#### Using Aspect Skills

Aspects may grant skills that define how they are used. Many skills require a skill check: a roll using a d20. The outcome of this roll is used to determine success of the skill and the degree of success or failure and degree of failure. Skill checks have a failure chance that represent the relative difficulty of performing the skill correctly. This difficulty is represented as a number that must be overcome by the character's roll for the character to be considered successful.

This roll may be modified from several sources including: magic, equipment and other aspects.

Lastly, all skills have an energy point cost associated with them.

Only when characters are in initiative do energy point costs matter. Outside of initiative, all skills may be utilized with the energy point cost becoming a guide to how long it may take the character - this is at the game masters discretion!


#### Using Unlearned Aspect Skills

If a character meets all the requirements of an aspect, they may attempt to use the aspect without having learned it. The skill roll is subject to a -5 modifier. The game master is encouraged to raise the modifier up to -20, if the situation, or difficulty of execution of the new aspect warrants it.


### Skill Check Difficulty

Certain game actions are represented as a skill check: a challenge that a character must attempt to defeat with a roll. Each check must either be related to an acquired aspect or to one of the three core character aspects.

The difficulty of a check is the number that the player must roll at or above to have been considered successful.

For example: a character is attempting to unlock a door with a lock pick. The character makes a lockpicking check against the difficulty of the lock using all of the character’s relevant modifiers.

In this case, the game master has decided that the lock is moderately strong and therefore chooses a difficulty of 16. If the player’s check is equal to or higher than 16, then the lock clicks free and the door opens.


#### Uncontested Skill Retries

Failed skill rolls that are uncontested may be retried by the character: e.g. a rogue trying to pick a lock while the party waits safely around them. This costs the character time. The game master is encouraged to pick a time using the energy point cost of the skill as a guide if present. This time is doubled for further attempts.

For example: a character fails their roll and it took them 1 minute to make the attempt. They then fail their second roll which took them 2 minutes this time around. The third roll finally succeeds, this attempt taking 4 minutes. The character therefore spent a total of 7 minutes.


#### Opposed Checks

Many aspects that affect a target may offer the target an opposing check. For example: attacking a character allows the character the ability to make an opposed check - a defense role, to mitigate the attack.

Opposed skill checks, like certain skilled attacks, require your character to beat a difficulty to even be considered successful in their execution. For example, even if a defender fails to defend by failing their skill check, or chooses not to defend, your character's attack may still not land.


#### Attacking

Many aspects grant attacks. Despite having different damages, effects and or other modifiers; all attacks follow the rules below.

##### Default Hit Location

Unless specified by the player with a **Targeted Attack** all attacks aim and strike for the target's torso.

##### Executing an Attack

All attacks begin with a d20 roll from the attacker and target the torso.

This roll represents the attacker's attempt to hit a target. If the attack has a skill check then this roll also represents their skill check roll.

For example: a character may use an attack that has a skill check roll with a difficulty of 12. The attacking character rolls an 11 and fails the skill check, therefore their attack fails and the defending character need not defend.

A character's attack roll may be modified from several sources including: magic, equipment and aspects.

An attack is considered successful if the target's defense is less than or equal to the attacker's roll. This means that if both attacker and defender roll a total of 15, the attack is successful. If successful, the attack lands and its associated effects (including damage) then apply. If the defender can not defend themselves either by their will or by some other mechanic such as a desire to conserve energy points, then the attack is considered successful automatically.

Many attack aspects will require a skill check roll despite the defender's lack of defense. Aspects such as these might include magic where the caster's success is determined by their attack roll. For example, a fire spell aspect may have a difficulty of 10. If the defender is unable to defend but the caster rolls a 9, then the spell fails and the defender is unaffected.


#### Defending

Manay aspects grant denfenses. Despite having different effects and or other modifiers; all defenses follow the rules below.

##### Executing a Defense

Characters, unless otherwise affected, may defend themselves when being attacked.

All defenses begin with a d20 roll from the defender. This action represents the character attempting to dodge, parry, block, or otherwise interrupt the incoming attack. A character may choose not to defend against an attack, in which case the attack is considered to be successful.

An attack is considered defeated only if the defender's defense roll is greater than the attacker's attack roll. 


#### Critical Hits

Rolling a 20 on an attack roll is considered a **critical hit**. This attack does its normal damage plus an additional modifier from the critical table. The effect is determined by a d20 roll by the attacker.

If the defender has a defense they can utilize, they may attempt to defend against the critical hit but at a **-10** modifier to their roll.


#### Critical Failure

Rolling a 1 on an attack roll is considered a **critical failure**. This attack does no damage plus an additional modifier from the critical table. The effect is determined by a d20 roll by the attacker.


#### Critical Hit Table

| Roll Range | Result |
| ---------- | ------ |
| 1 | Wound to Vital Organs - Take Bleed Damage for 1d4 Turns |
| 2 - 4 | Left Leg Incapacitated |
| 5 - 7 | Right Leg Incapacitated |
| 8 - 10 | Right Arm Incapacitated |
| 11 - 13 | Left Arm Incapacitated |
| 14 - 16 | Bleeding Torso Wound - Take 1d4 Bleed Damage |
| 17 - 19 | Face Strike - Damaged Senses for 1d6 Turns |
| 20 | Bleeding Neck Wound - Take 1d4 Bleed Damage - Attacker does x2 Damage |


#### Critical Failure Table

| Roll Range | Result |
| ---------- | ------ |
| 1 | Vital Organ Wound - Take Bleed Damage for 1d4 Turns |
| 2 - 4 | Left Leg Incapacitated |
| 5 - 7 | Right Leg Incapacitated |
| 8 - 10 | Right Arm Incapacitated |
| 11 - 13 | Left Arm Incapacitated |
| 14 - 16 | Bleeding Torso Wound - Take 1d4 Bleed Damage |
| 17 - 19 | Face Strike - Damaged Senses for 1d6 Turns |
| 20 | Bleeding Neck Wound - Take Bleed Damage for 1d4 Turns |


#### Critical Skill Success

Rolling a 20 on a d20 skill check is considered a **critical success**. The results of a critical success on a skill check is determined by the game master.


#### Critical Success Range Modifiers

The range for critical success on any check including attack rolls, may be modified by aspects. However, no one check may have a critical range modifier of greater than **+5**.


#### Damage

Characters may take damage over time during the game. Damage types are listed below.

* Fire
* Kinetic
* Electric
* Cold
* Meta


#### Armor

##### Encumberance

Some armors may restrict movement and therefore come with a negative mobility check modifier. Some heavier armors may also require a certain strength check modifier from the character.

Lastly, some armors may include an energy point cost representing the amount of effort required to equip or unequip it.


#### Attacking from Behind

Characters being attacked from behind are subject to a -2 modifier to any defense roll they attempt.


#### Surprise Attack

Characters unaware of the presence of an enemy force may be subject to a surprise attack. In a surprise attack, the attacking force has the advantage. Initiative is rolled for combat as normal. However, during the first turn, only the attackers may act.


#### Targeted Attacks

The game master may allow a character to target a specific piece of armor in order to reduce the DR that applies to an attack to only that which the piece of armor gives. This however should incur a hefty penalty of at least a -10 modifier to the character's attack roll, or greater at the game master's discretion.

Characters may defend themselves not just with actions but with equipment. Armor imparts a function called **damage resistance**. The damage resistance of an armor is given as a number to reduce damage taken by - this damage must apply to an energy type. For example, an Iron Chestplate imparts **6 DR Kinetic**. This value means that the armor will reduce any incoming kinetic damage to the character by 6.


#### Ready Actions

A character may choose to ready an action of any type. The action will execute when a specific set of conditions are met. If the conditions are not met by the character's next turn, the action is not executed but the energy points are still spent.

In order to ready an action, the character must first be able to satisfy the action’s point cost. The character then specifies the conditions necessary for the action to execute. The complexity of the conditions is subject to the discretion of the game master.


#### Turn Holding

In addition to readying an action, a character may choose to hold their turn. In order to hold their turn, the character may not spend any energy points and must declare that they are holding their turn. The character’s turn will execute either after every other character turn has ended, or when the character opts to rejoin the combat initiative order.

When rejoining, the character must wait for the current character’s turn to end before executing their own turn. This means that holding a turn may not interrupt another character’s turn.

If one or more characters hold their turns and wait for all other characters to exhaust their turns, the characters with the highest combat initiative modifiers execute their turns first. If two or more characters share the same combat initiative modifier then they are required to perform a collective d20 roll-off to determine the order in which their turns execute. The order in which these turns execute represent the new combat initiative order that should be followed until otherwise modified.

Characters may not hold their turn twice in the same turn.


#### Character Threat

Characters are constantly aware of their immediate surroundings and may threaten a number of map cells. These threatened cells are treated differently when enemies perform certain actions or attempt to retreat.

An enemy leaving a threatened map cell is subject to any oportunistic actions of the threatening character.


#### Flanking Enemies

Two or more characters may who threaten the same enemy may attempt to flank this enemy for a stacking modifier to their attack rolls. This modifier to attacks is equal to the number of characters flanking an enemy. Therefore, two characters flanking the same enemy receive a +2 modifier to their attacks.

To be considered flanking, the two attackers must be able to draw a line between the map cells they occupy that intersects a map cell that the enemy occupies. This line must be drawn from the center of the map cells that the attackers occupy.


#### Reactionary Actions

Some aspects may grant actions which can happen at any point during a turn. These are called reactionary actions and may only be used if their critera for use are met. For example, a counter spell aspect is a reactionary action that may be used any time magic is used within medium range of the character.


#### Opportunistic Actions

Many aspects grant actions that have the opportunistic modifier. These actions may be executed when an enemy attempts to leave one of the character’s threatened map cells or executes an action that triggers opportunistic actions.


#### Physical Cover

A character hiding behind physical cover receives added protection from attackers equal to the percent of their body obscured. This percentage is subject to environment constraints (some cover may provide a lower coverage percentage than other available options) and gamemaster discretion.

An attacker attempting to attack a target hidden by cover must make a percent roll (2d10 or d100) higher than the percent coverage the target is receiving. If the attacker rolls less than the character’s cover percentage, the attack impacts and does damage to the physical cover instead.

Cover may be mitigated by acquiring full line of sight on a target.


#### Pyhsical Cover Types

Cover may be destroyed and targeted specifically. Cover has a health point value equal to its material hardness. Common materials are given below. Gamemasters are encouraged to base their own game's materials off of the suggestions.

* Packed Mud/Sand - 5
* Wood - 10
* Sandstone - 15
* Granite/Concrete - 20
* Iron/Unrefined Alloy - 25
* Steel/Refined Alloy - 30


#### Kinetic Damage

Kinetic damage is a core game-play mechanic and many aspects, effects and equipment will utilize it.

Kinetic damage is a specific classification of damage that encompass most damage incurred from a kinetic source. This includes falling, being thrown against a surface and being blasted by raw gravitational energy. The amount of kinetic damage the character sustains is directly related to the amount of kinetic potential the character is subject to.

Kinetic potential is measured in progressions of 5: every 5 points of kinetic potential adds an additional 1d6 worth of kinetic damage. For example, if a character is subject to 25 points of kinetic potential, then they are also subject to 5d6 points worth of kinetic damage.

Your typical punch to the face is equal to five points of kinetic potential and therefore worth 1d6 points of damage.


#### Forced Movement

If an enemy target is subject to a strong push, they must make a strength check to resist being moved. In order to resist being moved by any amount the character's strength check must exceed the kinetic potential of the push. For example, if a character is subject to a push worth 15 points of kinetic potential, then their strength check must be greater than 15 to avoid being forcibly moved.

If the target fails to beat the kinetic potential of the push with their strength check, they are then subject to forced movement. The amount by which the character fails represents the amount of kinetic potential they are subject to.

The character is moved 1 meter for every point of unmitigated kinetic potential in the direction of the force applied. If the character is subject to more than 5 points of kinetic potential then normal kinetic damage rules apply.


#### Stacking Kinetic Damage

If an enemy target is thrown into another target, the second target must make a strength check against the kinetic potential of the throw. For example, if a character is subject to 15 points of kinetic potential then they must make a strength check greater than 15.

If the second target fails their strength check they are subject to half the kinetic damage to be applied to the first target. If the second target passes their strength check, they take no damage and halt the movement of the first target.

Targets thrown against immovable objects and surfaces are subject to an additional 1d6 of kinetic damage.

In both circumstances, the first target receives full kinetic damage and the second target stops the further movement from the kinetic potential. This restriction may be lifted by equipment, items or abilities.


#### Falling Damage

Fall damage is ignored for the first 4 meters a character falls, however landing the fall may still require a mobility check. If a character falls further then the character is subject to five points of kinetic potential for every two meters they fall beyond four meters.


#### Resting Weight Crushing Damage

Characters pinned underneath extremely heavy objects or weights may be subject to crushing damage. Crushing damage is calculated as kinetic potential. This potential equal to the total weight of the object in tons multiplied by five. This kinetic potential is then converted to damage die via the kinetic damage progression rules.


#### Movement

All characters start with a base ‘fit’ movement speed of 5 map cells or 10 meters. This speed represents the amount of distance the character can move utilizing one movement action.

A character may move through map cells occupied by a friendly character or entity with no penalty.


#### Speaking During Combat

Speaking to another character during combat may be done as an action during the character's turn. This action costs no points but what is said, including the target's reply, must fit within the definitions of a turn's time duration.

Anything spoken aloud may be heard by any other character within listening range. If the character is out of range, a perception check may be attempted to hear the conversation.


#### Grab

Any enemy in a character’s melee threat range may be grabbed. Grabbing a character requires an opposed mobility check to determine which character is faster. Grabbing an item from a character gives the target character a positive modifier of 5 to the opposed mobility check.

Grabbing a target removes the character's threat, meaning that they may not act on opportunity until they break from the grab.

A grab is an attack skill that costs 1 energy point.

Characters that are grabbed may not move from away from their oppressor until they win an opposed strength check. In addition, the game master may add additional restrictions to the character when using a weapon or item held in the hand of a grabbed arm.


#### Charging

Any character with a melee attack may perform a special combat maneuver called a charge. A charge is an a special attack action that grants the attacking character their full run speed (double movement). This comes at the cost of 1 energy point.

A charge can only be performed when there are no obstacles between the attacking character and their target. There must also be at least 2 map cells of distance between the character and their target, otherwise the character is considered unable to get enough of a running start to enhance the force of their attack.

The charging character receives a bonus of +2 on their attack. Note, the character must also pay the energy point cost of the attack in addition to the energy point cost of the charge.

After the attack, the character must suffer a -2 to any defense rolls they attempt until the start of their next turn. Consecutive charges stack only the **the -2 defense modifier** - for example a character that has charged twice in the same turn is subject to a **-4 defense modifier**.


#### Climbing and Scaling

When a character wishes to climb or scale obstacles, they must make a mobility check against the difficulty of the obstacle. A character has two options when choosing to make this mobility check:

* The character may spend 1 energy point to climb or scale an obstacle. By spending an energy point, they receive a +10 modifier to their mobility check.

* The character may instead choose to climb or scale an obstacle without spending an energy point. Doing so incurs no penalty but grants no positive modifier either.

Obstacle difficulty begins at 5. Difficulty raises by 5 for every meter of difference between the surface the character is on and the distance the character is attempting to scale.

A two meter obstacle will, therefore, require a mobility check greater than 15 to pass successfully.

Upon failure, if the character has spent an energy point to attempt the climb they simply fall back down to where they had attempted the climb without additional effect. However, if the character did not spend an energy point then their current turn ends and they fall back to where they had attempted the climb. In addition, the character is now considered prone.

Note, falling may have additional consequences regardless of whether or not the character chose to spend a movement action on the check. See falling damage for more information.


#### Two-Meter Step

A character may make a special movement action that costs 1 energy point called a two-meter step. As the name implies, a character may take a two meter step or a step equal to one map cell without incuring opportunistic actions.

**Optional Rule**

After a character takes a two-meter step they may not take any further action and their turn ends.


#### Standing Vertical Jump

A character may make a standing jump vertically in meters equal to half their strength modifier.

A standing jump requires 1 energy point and may be preformed as part of an ongoing movement action. For example, a character may move their entire movement to reach an obstacle. They may then choose to attempt to jump up onto the obstacle at the cost of 1 energy point.

The character may attempt a higher jump by performing a strength check. The strength check has a difficulty equal to the number of meters the character is attempting to jump over their standing vertical jump maximum multiplied by 10.

For example, a character with a strength modifier of +2 can safely jump vertically 1 meter without making a check. If the character needs to make a standing vertical jump of 3 meters, they must successfully roll a strength check higher than 20 – 2 meters over the character’s maximum of 1 meter times 10.


#### Standing Forward Jump

A character may make a standing jump forward in meters equal to half their strength modifier.

A standing jump requires 1 energy point and may be performed as part of an ongoing movement action. For example, a character may move their entire movement to reach an obstacle. They may then choose to attempt to jump over the obstacle at the cost of 1 energy point.

The character may attempt a longer jump by performing a strength check. The strength check has a difficulty equal to the number of meters the character is attempting to jump over their standing forward jump maximum multiplied by 5.

For example, a character with a strength modifier of +2 can safely jump 1 meters without making a check. If the character needs to make a standing forward jump of 3 meters, they must successfully roll a strength check higher than 10 – 2 meters over the character’s maximum of 1 times 5.


#### Running Jump

A character may make a running jump in meters equal to their strength modifier combined with their mobility modifier. A running jump costs 1 energy point. In addition, a running jump requires 2 map cells of movement and may be performed as part of an ongoing movement action.

For example, a character may move to reach an obstacle. They may then choose to attempt to perform a running jump over the obstacle at the cost of 1 aciton point.

The character may attempt a longer running jump by performing a mobility check. The mobility check has a difficulty equal to the number of meters they are attempting to jump over their running jump maximum multiplied by 5.

For example, a character with a strength modifier of +2 and a mobility modifier of +2 can safely make a running jump of 4 meters without making a check. If the character needs to make a running jump of 6 meters, they must successfully roll a mobility check higher than 10 – 2 meters over the character’s maximum of 4 times 5.


#### Perception

A character, out of combat, may make a perception check at any time to observe their surroundings. In combat, a character may make a perception check as a movement action. Without the perception aspect, this check must be performed unskilled.

The character’s perception check represents how many details they are able to observe and how fine grained that detail is. This is considered an essential activity to look out for traps, hidden secrets and other important aspects about a character’s surroundings.


#### Perception and Stealth

Any character may make a perception check to attempt to reveal enemies in stealth only by acquiring an aspect. This may be done only on targets in stealth that the character has line of sight on.

Shared character vision may qualify as line of sight.


#### Stealth

A character with the stealth aspect may utilize it when no known enemies have line of sight on the character. The value of this stealth check represents the difficulty of the perception check required to identify the character.

A character in stealth may ignore enemy opportunistic actions in the case where the enemy is unable to detect them. In addition, any enemy targeted from stealth is subject to a -10 modifier for any attempted defense roll.

Once in stealth, a character may maintain their stealth if they make no action that reveals them. Maintaining stealth costs a character no action but requires the character to re-roll their stealth check.

Unless otherwise stated by the aspect, only attacks and defenses will reveal a character in stealth.


### Character Health and Status

#### Health Points

All characters have a health point value that represents the amount of damage they may sustain before dying. A character at 0 HP is considered wounded enough to potentially fall unconscious. The moment a character reaches 0 HP must roll a strength check (failure chance of 8). If the character succeeds the check they are still conscious. The character need not roll for consciousness unless they take further damage. Further damage immediately invokes another strength check.

A character is considered dead when they receive damage equal to twice their health point pool.

For example:
    A character with 50 HP is potentially unconscious at 0 HP and dead at -50 HP.

A character’s body may be destroyed once the character is dead as a matter of action - there is no further damage needed. Once a character's body has been destroyed, they may not be revived.


#### Healing

Healing happens over time in most circumstances. Certain medical supplies may contain agents and compounds that impart an immediate health boost as well as repair damage over time. Magic also may make healing far faster than nature can muster.


#### Demeanor

Demeanor is a very rough representation of a character’s disposition towards another. Disposition is represented on a scale of 0 to 50.

A character with zero disposition towards another character is considered hostile. Conversely, a character with a disposition of 40 towards another character is considers friendly.

Demeanor is effective in determining how one character views another and how swayed they maybe. The effectiveness of persuasion relies on a targets demeanor towards the character attempting the persuasion.


#### Persuasion

Persuasion of characters may be attempted by performing a persuasion skill check. Persuasion is modified by a character’s demeanor – a feature that embodies the attention and perhaps command the character carries over others through their charismatic features. These features may include physical beauty, a silk tongue as well as many others.

When persuading a target, whether it be for diplomacy or to haggle, the character makes a presence check to represent their overall position and impact to the targets demeanor. The target makes an opposed intuition check.

The amount that the character’s persuade check beats the target’s intuition check is then added to the target’s current disposition towards the character.

Depending on how much disposition the target already has, this may make the target more friendly or indeed convince them to see it your way.


#### Physical Strength

A character’s physical strength represents how much force they can impart with only their body. A physical strength check for a character is determined by rolling a d20 and then adding both the character’s strength modifier plus any additional modifiers they may have that target physical strength specifically.

A character’s physical strength is easily enhanced and affects many character attributes and abilities.


#### Endurance

A character’s endurance represents how much internal fortitude their body has. This check is essential for resisting many effects, abilities and poisons. An endurance check for a character is determined by rolling a d20 and then adding the character’s strength modifier.

A character’s endurance may only be enhanced by increasing the character’s strength aspect.


#### Poison

A character may be poisoned only if the poison has a vector for entering the target’s body. In combat, this requires that the character take health point damage. If an attack causes no health point damage, then it is considered stopped by the target’s defenses.

Poisons may cause ability damage but must target one or more of the core character aspects. A poison may attack multiple character aspects with varying difficulties. Poisons may also impart negative attributes for the duration of the poison.

All poisons must contain a medical check difficulty for removal. Poisons may also require a specific compound in addition to the medical check.


#### Disease

A disease may impart a single negative character attribute for as long as the character carries the disease. Diseases must include a difficulty for removal equal to 5 plus a modifier that represents the strength of the disease. Removal requires the healing of all health point damage first. Once fully-healed, only then may the difficulty of the disease be challenged.

Disease counter-agents may be created by performing a successful medical check greater than the removal difficulty of the disease. Certain material components may be required when creating counter-agents.


#### Addiction

Certain consumable items and poisons may impart an addiction to a character. An addictive substance must have an addictiveness modifier and a craving interval specified. Craving intervals are measured in hours and must be longer one hour.

When subject to an addictive substance, the character must make an intelligence check with a difficulty equal to 5 plus the addictiveness modifier of the substance.

A substance addiction may be removed by a medical check with a difficulty equal to 10 plus the addictiveness modifier.

While addicted to a substance, the character must consume it at a rate defined by the substance’s craving interval. If a character misses consuming the substance before their next craving, they become subject to a negative modifier that affects **all rolls**. For every interval missed, this negative modifier stacks by 1 to a maximum of -5.

Consuming the substance resets all negative morale modifiers from the associated addiction back to 0.


#### Consuming Food

Consuming food may restore up to 12 points over a time period of 8 hours. This may be done out of combat to bring character health back up gradually. Certain types of food may restore more or less of a character’s health but may not restore more than 12 per hour.


#### Hunger and Thirst

A character that has gone without food, fuel or water for a significant period of time may acquire the malnourished condition. While malnourished, the character receives a negative modifier to **all rolls** equal to the number of days affected.

For example, a character that has gone malnourished for two days is subject to a -2 modifier to **all rolls** they make.

The malnourished condition may be removed by consuming food, fuel or drink.


#### Ability Damage

The most common forms of ability damage target the three core character aspects: strength, intelligence and mobility. These character aspects have unique consequences when reduced to negative values.

Other ability checks may receive damage but their effect when disabled is left to GM discretion.

Ability damage may be mitigated by healing only while the modifier is greater than or equal to 0. Healing removes one point of ability damage per 10 points of health points healed. If the character’s health points have been refilled but they still suffer ability damage, they may still be healed for ability damage at double the rate, or 2 points of ability damage healed per 10 health points healed.

If the character has sustained ability damage to the extent that they’re now subject to a negative modifier, a medical check is required. The medical check has a difficulty of 5 multiplied by the value of the negative modifier the character is currently subject to; 4 points of ability damage that takes the check modifier to a -4 has a difficulty of 20 to remove.

If the medical check is passed, the character may heal their ability damage normally. If the check fails then the character will be unable to heal their ability damage until the check can be attempted again.

For example, a character sustains ability damage that gives then a strength modifier of -4. A party member makes a medical check of 24 which is greater than the 20 required to begin healing the ability damage. They then heal the character for 20 health points, giving them 2 positive points to their negative strength modifier while refilling all of their hit points.

The next round of healing deals 23 points of health to the character, healing an additional 4 points of strength now that they are fully healed.

This brings the character back to a positive strength modifier of 2 and has removed the remainder of the ability damage the character suffered.


### Effects

Throughout the game a character may be subject to a number of effects. The most common are listed below.

#### Prone

The character is laying on the ground. While in this position, the following effects apply to the character:

* Movement is limited to one map cell per move action.
* Ranged attacks receive a +2 modifier.
* Melee attacks receive a -2 modifier.
* Defense rolls receive a -2 modifier.


##### Rising from a Prone Position

A character may rise from a prone position for one energy point. Aspects may modify or negate this cost.

##### Falling Prone

A character may fall to a prone position safely for one energy point. Aspects may modify or negate this cost.

#### Stunned

The character is incapacitated to a certain degree. While stunned, the following effects apply to the character:

* While stunned, the character is unable to save energy points.
* Defense rolls are capped at a maximum of 10.
* Speaking requires an energy point.


#### Slowed

A character that has the slowed status must pay 1 energy point or forfeit their turn. In addition, the slowed character incurs -2 modifier for every dodge attempt made until the condition is removed.


#### Blindness

A character that has lost more than eighty percent of their vision is rendered blind. A character that is blind loses their ability to see in any meaningful capacity. While blind, the character is at a -10 against all attacks made against them. Removing blindness requires a medical item, aspect or magic.


#### Grappled

A character that is grappled is unable to take any action or aspect that requires willful control of the character's body.

The grappled character may spend an energy point to attempt escape. Escape is an opposed strength check between the character and their attacker. Upon escape, the character’s ability to move freely is regained. The character is released in the same map cell as their attacker and is considered squeezing with them.


#### Sickened

The sickened condition grants a character a negative modifier of two for every d20 roll the character makes. Sickened conditions may stack. Removing this condition requires the character to heal at least 1 health point of damage.

All stacked negative modifiers for this condition are removed immediately when the character is healed.


#### Squeezing

When a character is forced to occupy fifty percent or less of a map cell, they are considered squeezed. A character, while squeezed, is subject to a -2 modifier to all checks made. If there are more than two characters squeezed in the same map cell, this modifier stacks to a negative -4 and will continue to stack for a total squeezing modifier of -6.


#### Staggered

A character that has a health point value of less than one fourth their health point total is considered staggered. A staggered character that receives further damage is subject to a fate roll.

If the target character rolls **[ ]** or **[+]** then they may continue their turn normally. However, if the target character rolls **[-]**, they must lose an energy point or forfeit their turn.

This condition’s effects may be mitigated by equipment, items and abilities.
