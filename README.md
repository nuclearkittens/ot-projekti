# (still an) untitled rpg

In this game, you will share an adventure with the main hero in a contemporary environment. The world resembles our own, but in this reality magic and weird monsters exist (I mean, squirrels with human feet? Wouldn't want to encounter them in the city streets).

The game is programmed using Python (v.3.8) and its Pygame library. As the game develops, it will have explorable maps and a turn-based battle system. Currently, the only functionality is a mock-up of the title screen. If you want to check out the art style, take a look at the first character sprites in the [assets](https://github.com/nuclearkittens/ot-projekti/tree/master/src/assets) folder!

This game is developed as a part of the University of Helsinki's *Ohjelmistotekniikka* course.

### documentation

+ [requirement specification](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/requirementspecification.md)
+ [architecture](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/architecture.md)
+ [study log](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/studylog.md)
+ [newest coverage report](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/coverage-report-210413.png)
+ [credits](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/temp-credits.md)

### installation

1) install dependencies using the following command: `poetry install` 
2) run the game: `poetry run invoke start`

### command line tools

+ run the game: `poetry run invoke start`
+ run tests: `poetry run invoke test`
+ generate a test coverage report: `poetry run invoke coverage-report`
  + report can be found in *htmlcov* directory

