# Testing summary
## Unit & integration testing
![Pytest summary](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/tests_run.png)

Almost 200 unit and integration tests have been written to test both the application logic and the functionality of the database. The tests concerning the database can be found in *tests/database* directory, and the integration tests concern mostly the battle loop – class `TestBattleLoops` includes majority of these. In some of the tests, mocked classes (such as `StubEventHandler`) have been used to simulate user input.

### Test coverage
Excluding the user interface layer, the branch coverage for the application testing is 97%.
![Coverage report](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/coverage_report_210516.png)

A few branches have not been covered, some of them being battle action scenarios. In *util.py*, the scaling of images is left untested within the scope of unit tests, but seemed to work when running the application.

Example tests for different scenarios during battle are pictured in the image below.
![Example tests](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/images/test_examples.png)

## System testing

The system testing of the application has been done manually by installing and running the application with different configurations and systems as per the instructions in the [user manual](https://github.com/nuclearkittens/ot-projekti/blob/master/documentation/user_manual.md). All the functionality specified in the specification document has been reviewed, and erroneous input has been tested in different scenarios (keyboard input that does nothing, trying to choose an option in a menu that is not allowed).

The application has only been tested in macOS and Linux environments, so no guarantees on it running on a Windows machine.

## Known issues

The framerate is not always consistent in battle, and I have not found a workaround for scaling the Pygame window (even though window scaling should be disabled – this is apparently a problem with some window managers).
