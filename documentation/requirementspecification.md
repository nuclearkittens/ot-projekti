# Requirement specification

A turn-based rpg(/dungeon crawler), set in a world not too unlike ours. 
This version will most likely act as a demo, consisting of only one explorable map 
and few different functionalities, hopefully expanding to a full-sized world with 
an exciting storyline in the future.

## UI draft

![UI sketch v.1](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/uisketch.png)

## Demo / Basic functionality

### Exploration

The player can move around the map(s) freely, finding items and encountering enemies.

+ Tiled maps
+ Random encounters
+ Interacting with surroundings
+ Keyboard and mouse input

### Battle

Turn-based battle system

+ Battle menu 
	+ Physical and magical attacks 
	+ Possibility to flee the battle 
	+ Use items
+ Health point system 
+ Defeating enemies gives experience points
+ Boss fights (only one will be provided in the demo version)

### Main menu

See your party's stats and view inventory

+ Simple, one screen menu
+ Not accessible from the battle screen

### Save file

For the time being, saving the game in demo mode is not possible. However, a save file 
will be created, keeping track of the player's stats and experience.

## Planned additions

After the demo version is finished, more functionalities will be added, for example:

+ Nicer graphics
+ NPCs, party members, monsters
+ Actual storyline
+ World expansion: more explorable maps and dungeons
+ Treasures, equipment, items
+ More complex main menu (changing party formation, equipment, using items/skills)
+ Saving: save your progress in a save file (possibly multiple saves?)
+ Level up/skill system
+ Algorithms/RNG for battles, random encounters, loot etc.
