###
## Entry point for (potentially) many simulations for the
## Fula network
##
## Authors: Nicholas O'Kelley, Jake Cassani
## Organization: Longtail Financial
## Date: March 8th, 2022
###

# Python imports might cause an issue, but our server uses this
# for the data you see on the dashboard app.
from .rewards import gen_results


def test_system_params() -> dict:
    """
    Allows us to supply either an initial config or a fail safe should the one
    supplied be invalid.

    Params:
        None

    Returns:
        A dictionary with simulation configurations
    """
    test_config = {
        "global_params": {
            "time_in_months": 12,
            "token_value": 0.4,
        },
        "user_config": {
            "avg_monthly_storage_cost": 50,
            "avg_power_consumption_cost": 5,
        },
        "miner_config": {
            "rate_of_change": 0.1,
            "hardware_buyin_cost": 30,
            "miner_count": 10000,
            "monthly_token_amount": 10e6,
        },
    }

    return test_config


def simulate(configs: dict = test_system_params()):
    """
    This is the entry point into our simulation(s) for the Fula Network

    Params:
        - configs: dict - A dictionary of possible simulation configurations

    Returns:
        None
    """

    # NOTE: Should more simulations be added in the future, we can simply call their
    #       'simulate' functions here and all the data would be passed back!

    config = configs | test_system_params()

    results = gen_results(config)
    return results
