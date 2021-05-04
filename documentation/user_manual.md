## user manual
Download the source code of the [latest release](https://github.com/nuclearkittens/ot-projekti/releases) (found under *assets*).

### starting the application
Before trying to run the game, install dependencies using the command `poetry install`. Now you should be able to run the game by using the command `poetry run invoke start`.

### user input
As of now, only keyboard input is supported. Use the **up and down arrow keys** to move through the menu options.

![main battle menu](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual01.png)

An action can be chosen by pressing **enter (also known as return)**. The chosen action should be highlighted, as shown below.

![chosen action](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual02.png)

If the character does not have any magic or skills, the submenu will be empty (pictured below). Returning to the parent menu can be done by pressing **backspace**.

![empty submenu](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual03.png)

When a menu action is chosen, the target selector cursor appears. Move the cursor by pressing **left or right arrow key**, and select the target by pressing **enter**. Once an action has been chosen, it cannot be cancelled and you have to select a target.
![target selection screen](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/manual04.png)

Currently, the game does not check for a game over, so it will be running forever unless the user closes the Pygame window. Working on it, though.
