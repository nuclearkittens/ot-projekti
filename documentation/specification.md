# Specification

The application is a demo version of the turn-based battle system for Fractured Loop (working title), an RPG that has developed into a bit of a passion project for me. The aim is simple: defeat the enemies before they defeat you. As I definitely bit more than I can chew, that is all the application does at the moment (but if you are curious, be my guest and check the [original plan](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/og_specification.md) for the project).

## UI diagram

![ui diagram](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/ui_diagram.png)

## Functionality

### Title screen

The title screen is displayed when the application is opened, and again when a battle ends. The user can:

+ Browse throught the three-item menu
+ Choose to try their luck in battle
+ Check the controls by choosing the help menu
+ Quit the application by either choosing the **quit** option or closing the window

### Battle

It's a turn-based battle! Against some weird squirrels with human feet, but okay, I'll roll with it.

+ Attack the opponent by, well, attacking. The Witch knows a few spells, too.
+ Usable items
+ Possibility to pause the game
+ Information displayed on a separate panel
+ The characters take damage from attacks and can heal using items
+ Pause and game over screens
+ Idle and hurt animation

### Database

A SQLite database is used to gather the character information.

### Planned additions

+ Explorable maps
+ More monsters! Boss fights!
+ Better damage formula
+ Saving game data to a separate file
+ and more!
