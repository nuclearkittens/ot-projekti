# Turn-based battle demo

In Fractured Loop (working title), you will share an adventure with the main hero in a contemporary environment. The world resembles our own, but in this reality magic and weird monsters exist (I mean, squirrels with human feet? Wouldn't want to encounter them in the city streets).

Excited? Yeah, me too, but unfortunately that is not the reality yet. This application is just the demo version for turn-based battle mechanics.

The turn-based battle demo is programmed using Python (v.3.8) and its Pygame library. As the game develops, it will have explorable maps and more monsters to fight. Currently, the only functionality is a demo battle. The first map is in production, and there are plans for an actual storyline for the game!

In development for probably at least for the next year or so.

This game is developed as a part of the University of Helsinki's *Ohjelmistotekniikka* course.

### Documentation

+ [original plan](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/og_specification.md)
+ [specification](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/specification.md)
+ [architecture](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/architecture.md)
+ [testing summary](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/testing.md)
+ [user manual](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/user_manual.md)
+ [study log](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/studylog.md)
+ [credits & references](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/credits.md)

### Installation

1) install dependencies using the following command: `poetry install` 
2) run the game: `poetry run invoke start`

### Command line tools

+ install dependencies: `poetry install`
+ run the game: `poetry run invoke start`
+ run tests: `poetry run invoke test`
+ generate a test coverage report: `poetry run invoke coverage-report`
  + report can be found in *htmlcov* directory
+ lint: `poetry run invoke lint`

