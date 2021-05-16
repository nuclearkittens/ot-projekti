# User manual
Download the source code of the [latest release](https://github.com/nuclearkittens/ot-projekti/releases) (found under *assets*).

## Configuration
The name of the database used, as well as some in-game constants are specified in an *.env* file and, as a back-up, in [config.py](https://github.com/nuclearkittens/ot-projekti/blob/master/src/config.py). If running the application on a massive display (especially 4K), changing the scale to `SCALE=2` is recommended, as the Pygame window should not be scalable on itself. The scaling variable is found in the .env file on line 13.

## Installation & starting the application
Before trying to run the game, install dependencies using the command `poetry install`. Now you should be able to run the game by using the command `poetry run invoke start`.

### User input
As of now, only keyboard input is supported. The application opens up the title menu. Use the **up and down arrow keys** to move through the menu options.

![title screen](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual1.png)

If you want to check the controls, choose the **help** option in the main menu. The keyboard input is not configurable at the moment, but hopefully will be in the future.

![help screen](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual2.png)

By choosing battle, the battle screen is displayed. When the player's turn is reached, the main battle menu will become active – you'll know this is the case when the info panel says *Physical damage to a single target*.

![main battle menu](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual3.png)

An action can be chosen by pressing **enter (also known as return)**. The chosen action should be highlighted, as shown below. When a menu action is chosen, the target selector cursor appears. Move the cursor by pressing **left or right arrow key**, and select the target by pressing **enter**.

![chosen action](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual4.png)

When choosing a menu option other than attack, a submenu opens and becomes active. If the character does not have any magic or skills, the submenu will be empty. Returning to the parent menu can be done by pressing **backspace**.

![battle submenu](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual5.png)

The battle can be paused by pressing **P**, and unpaused by pressing **P** again. While paused, a pause menu is displayed.

![paused battle](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual6.png)

After either dying or defeating all enemies, a game over screen is displayed – returning to the the title screen can be done by pressing **return**.

![game over](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual7.png)

To quit the application, simply close the Pygame window (or choose quit in the main menu, both work).

