# (still an) untitled rpg

In this game, you will share an adventure with the main hero in a contemporary environment. The world resembles our own, but in this reality magic and weird monsters exist (I mean, squirrels with human feet? Wouldn't want to encounter them in the city streets).

The game is programmed using Python (v.3.8) and its Pygame library. As the game develops, it will have explorable maps and a turn-based battle system. Currently, the only functionality is a never-ending demo battle. The first map is in production, and I have managed to find someone to write an actual storyline script for the game!

In development for probably at least for the next yer or so.

This game is developed as a part of the University of Helsinki's *Ohjelmistotekniikka* course.

### documentation

+ [requirement specification](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/requirementspecification.md)
+ [architecture](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/architecture.md)
+ [user manual](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/user_manual.md) **new! wk6**
+ [study log](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/studylog.md)
+ [newest coverage report](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/coverage_report_210504.png) **updated: wk6**
+ [credits](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/temp-credits.md)

### installation

1) install dependencies using the following command: `poetry install` 
2) run the game: `poetry run invoke start`

### command line tools

+ run the game: `poetry run invoke start`
+ run tests: `poetry run invoke test`
+ generate a test coverage report: `poetry run invoke coverage-report`
  + report can be found in *htmlcov* directory
+ lint: `poetry run invoke lint`

