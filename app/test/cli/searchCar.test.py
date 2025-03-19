import pytest_qt
from car_db import CarSearchCLI

@pytest.mark.qt
def test_search_car_cli():
    cli = CarSearchCLI()

    # Test the CLI's ability to handle valid input
    output = cli.search("Toyota Corolla")
    assert "Toyota Corolla" in output

    # Test the CLI's ability to handle invalid input
    with pytest.raises(SystemExit):
        cli.search("Invalid search term")

    # Test the CLI's help message
    output = cli.help()
    assert "Usage: car_db <search_term>" in output
