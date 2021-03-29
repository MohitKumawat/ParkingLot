Use Case:
    Create Sample Parking Lot

Initial Setup:
    Install Python 3 and django

Commands to test the code:
    1. python manage.py shell
    2. from testing_lot.testing import test_parking_lot
    3. test_parking_lot('testing_lot\input.txt')
    4. quit()

Output will be shown on the terminal screen.

Things taken into consideration:
    Support for multiple parking lots
    Support for col and rows in parking, where distance is calculated using row, col
    Multiple strategies could be added, as strategy is loosely coupled

Possible Enhancements:
    Support for taking input from different sources
    Access/use parking lots using numbers from commands/inputs
    Rebuild elements(like heap) used in strategy, in case server restarts
