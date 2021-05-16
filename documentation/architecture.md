# Architecture

## Pattern

The structure of the application is more or less three-tiered, as shown in the image below.

![Structure](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/arch.png)

The *ui* package includes the graphic user interface (for example menus) and the `EventHandler` class that checks for user input. The application logic is contained in three separate packages, *core*, *combat*, and *entities*. All reading and writing data (apart from images) is handled by the *database* package.

## User Interface

The user interface consits mainly of different menus that the user can browse through using their keyboard. Mouse input (other than closing the window) nor other controllers are currently not supported.

The different menu and button classes are used both in the title and battle state, as they are mostly general components. The [EventHandler](https://github.com/nuclearkittens/ot-projekti/blob/master/src/ui/event_handler.py) class is responsible for converting the player's keyboard input in to events that are handled by the application, and the [Renderer](https://github.com/nuclearkittens/ot-projekti/blob/master/src/ui/renderer.py) class handles displaying graphics on the game window.

The title view includes the title menu and a static help screen. Classes purely for title screen are [TitleScreen](https://github.com/nuclearkittens/ot-projekti/blob/master/src/ui/title.py) and [HelpScreen](https://github.com/nuclearkittens/ot-projekti/blob/master/src/ui/help_screen.py), which display the title screen menu and help information respectively.

In battle, the player has their main menu, and choosing actions are divided into their own submenus. The battle state also includes three different static screens depending on the current state of the battle. [BattleMenu](https://github.com/nuclearkittens/ot-projekti/blob/master/src/ui/battle_menu.py), a subclass of `Menu`, is the main component responsible for player input. In addition, an info panel displays information for the player, and `DamageText` buttons are also considered to be a part of the interface.

Application logic and user interface could have been separated even more, as some of classes grouped here check for sprite collisions.

## Application Logic

The application logic is divided into three packages: characters, skills, and such are contained in *entities*, battle loops and actions in *combat*, and the main demo (plus some preparatory methods and functions) in *core*.

As the main functionality of this application is to be a turn-based battle demo, the [combat](https://github.com/nuclearkittens/ot-projekti/blob/master/src/combat) package playes a major role. However,`Character`entities (and its subclasses `Monster`and `PartyMember`) contain most functionality for single (battle) actions and checking the characters' stats. The diagram below shows the dependencies between the different classes and objects.

![Class diagram](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/package_diagram.png)

## Database

As of now, the application does not utilise reading and writing data in a very thorough level. A SQlite database is used to store information on characters' stats, inventories and information, but the application does not write anything in the database – plan is to use cvs or json files for saving, if I ever get to the point where a save file is needed.

A [script](https://github.com/nuclearkittens/ot-projekti/blob/master/src/assets/db/init_commands.sql) initialising the database is provided as the database is emptied every time when the application is closed.

## Main Functionality

*WIP, add some sequence diagrams or idk gifs of the main functionalities, like the player action in battle or sth*

## Known Issues

As mentioned before, the application logic and UI are not separated as well as they could be. The data reading functions need some work, too, as a workaround has been implemented in the character subclasses to avoid circular imports. Named tuples might also not be the best way to contain character data in the future, as I had several problems replacing values in them
