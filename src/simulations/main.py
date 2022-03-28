###
## Entry point for (potentially) many simulations for the
## Fula network
##
## Authors: Nicholas O'Kelley, Jake Cassani
## Organization: Longtail Financial
## Date: March 8th, 2022
## Last Modified: March 26, 2022
###

import json

# NOTE:
# Python imports might cause an issue, but our server uses this
# for the data you see on the dashboard app.
# from .rewards import gen_results

# NOTE: python 3.8+ on the command line
import rewards


def test_system_params() -> dict:
    """
    Allows us to supply either an initial config or a fail safe should the one
    supplied be invalid.

    Params:
        None

    Returns:
        A dictionary with sample simulation configurations
    """
    test_config = {
        "global_params": {
            "time_in_months": 12,
            "token_value": 0.04,
        },
        "user_config": {
            "avg_monthly_storage_cost": 50,
            "avg_power_consumption": 5,
        },
        "miner_config": {
            "rate_of_change": 0.05,
            "miner_count": 23000,
            "storage_provided": 5,
            "monthly_token_amount": 10e6,
        },
    }

    return test_config


def display_stats(results):
    """
    Neatly displays the final dictionary as a JSON dump
    """
    result = json.dumps(results, indent=2)
    print(result)


def simulate(configs: dict = test_system_params()):
    """
    This is the entry point into our simulation(s) for the Fula Network

    NOTE: Should more simulations be added in the future, we can simply call their
    'simulate' functions here and all the data would be passed back!

    Params:
        - configs: dict - A dictionary of possible simulation configurations

    Returns:
        Final simulation results dictionary
    """

    config = configs or test_system_params()

    print("---- Fula Network Simulation ----")

    # NOTE: Python 3.8+ on the command line
    results = rewards.gen_results(config)
    # NOTE: Python 3.10 and remote request
    # results = gen_results(config)

    # display_stats(results)
    display_stats(results["tables"]["network_table"])
    display_stats(results["tables"]["miner_table"])
    # display_stats(results["tables"]["network_storage_table"])

    print("---- End of Simulation ----")

    return results
