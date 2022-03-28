###
## Simulating the Miner Rewards for the Fula Network
##
## Authors: Nicholas O'Kelley, Jake Cassani
## Organization: Longtail Financial
## Date: March 8th, 2022
## Last Modified: March 26, 2022
###

# NOTE:
# Python imports might cause an issue, but our server uses this
# for the data you see on the dashboard app.
# from .Box import Box

# NOTE: python 3.8+ on the command line
# import Box
from Box import Box

# Standard imports
import uuid
import random
import pandas as pd

# A constant for the upper bound of storage a user can provide
# Allows for expansion or reduction without repeating ourselves in the code.
STORAGE_BOUND = 10.001


def calc_storage_percentage(storage, total_storage):
    """
    Calcualates the percentage for the amount of storage provided to the network.

    Params:
        - storage: Amount provided to the network
        - total_storage: total storage in the network

    Returns:
        The percentage of contribution

    """
    return storage / total_storage


def token_rewards(reward_percent: float, monthly_tokens: float) -> float:
    """
    Calculates the monthly reward based on the current storage provided and the
    tokens allocated for the month.

    Params:
        - reward_percent : percentage of network contribution
        - monthly_tokens : tokens allocated for the monthly rewards

    Returns:
        The monthly reward

    """
    return monthly_tokens * reward_percent


def monthly_change(
    miners: list,
    percent_change: float,
) -> list:
    """
    Helper function that adds new miners to the pool

    Params:
        miners: current list of miners
        percent_change: amount to increase the amount of miners in the system

    Returns:
        The updated list of miners in the simulation
    """

    curr_miners = len(miners)
    amount_to_increase = round(curr_miners * percent_change)

    for _ in range(amount_to_increase):
        storage = round(random.uniform(0, STORAGE_BOUND), 2)
        mac_address = uuid.uuid4()
        miners.append(Box(str(mac_address), storage))

    return miners


def calc_avg_active_miners(monthly_miner_dist: list) -> float:
    """
    Calculates the average active miners for the year

    Params:
        monthly_miner_dist: a list of miners each month

    Returns:
        A float value representing the average
    """
    avg = 0

    for i in monthly_miner_dist:
        avg += i

    return round(avg / len(monthly_miner_dist), 1)


def gen_miners(spawn=0, start=0, boxes=[], storage=None) -> list:
    """
    Generates the initial batch of miners

    Params:
        spawn: the number of miners to spawn
        miners: an optional list to update

    Returns:
        The updated miner array
    """

    miners = []

    # Ensure one miner represents the dashboard user
    if storage is not None:
        print("Added custom miner")
        miners.append(Box(str(uuid.uuid4()), storage))

    # We subtract one from our upper bound to account for previous step
    for i in range(start, spawn - 1):
        if i % 200 == 0:
            print("Spawned " + str(i) + " miners...")

        storage = round(random.uniform(0, STORAGE_BOUND), 2)
        miners.append(Box(str(uuid.uuid4()), storage))

    print("Created a total of " + str(len(miners)) + " miners.")
    return miners


def update_monthly_rewards(miners, monthly_tokens, total_storage):
    """
    Helper function that updates the rewards of the miners for the month
    and calculates the average tokens per day.

    Params:
        miners: list of the miners in the system
        monthly_tokens: pool of tokens to divide
        total_storage: amount of total storage provided (basis)

    Returns:
        None
    """
    for miner in miners:
        miner.monthly_rewards.append(
            token_rewards(
                calc_storage_percentage(miner.storage, total_storage),
                monthly_tokens,
            )
        )

        miner.daily_rewards.append(calc_daily_rewards(miner))


def update_network_contribution(miners, total_storage):
    """
    Helper function that updates the relative amount of storage provided to the network

    Params:
        miners: list of the miners in the system
        total_storage: amount of total storage provided (basis)

    Returns:
        None
    """
    for miner in miners:
        miner.storage_percent = calc_storage_percentage(miner.storage, total_storage)


def calc_network_storage(miners):
    """
    Helper function to calculate the amount of storage in the Fula Network

    Params:
        miners: current list of miners

    Returns:
        The summed amount of storage provided by all the miners.
    """
    storage = 0

    for miner in miners:
        storage = storage + miner.storage

    return storage


def calc_daily_rewards(miner):
    """
    Helper function to calculate the daily rewards for a given 30 day period.

    Params:
        miners: current list of miners

    Returns:
        The Daily amount of mined rewards

    """

    # NOTE: A month is consider a 30 day period
    return miner.monthly_rewards[-1] / 30


def create_network_table(miners):
    """
    Helper function that is mainly utilized to create the Storage breakdown
    dataframe.

    Used on the dashboard mainly.

    Params:
        miners: current list of miners

    Returns:
        A dataframe with the counts for the amount of miners providing
        zero through ten TB of storage to the network.
    """

    storage = []
    mac = []

    for miner in miners:
        mac.append(miner.mac_address)
        storage.append(miner.storage)

    df = pd.DataFrame(zip(mac, storage), columns=["MacAddress", "Storage"])
    sorted_df = df.sort_values(by="Storage")
    # print(sorted_df)

    if sorted_df is not None:
        return sorted_df.to_dict()
    else:
        return df


def gen_to_sender(
    miners: list,
    configs: dict,
    monthly_miner_snapshot: list,
    monthly_storage_snapshot: list,
):
    """
    A helper function that processes the data from the simulation and then returns
    a dictionary containing useful charts and data.

    Params:
        miners: a list of the miners in the system
        configs: the simulation configs passed in originally
        monthly_miner_snapshot: list of the amount of miners per month
        monthly_storage_snapshot: list of the storage in the network per month

    Returns:
        A dictionary of useful data
    """
    # Our simulation runner miner.
    miner = miners[0]

    # NOTE: our selected miner / box represents the uers viewing the app
    avg_tokens_per_day = sum(miner.daily_rewards) / 12
    yearly_mined_tokens = sum(miner.monthly_rewards)
    EOY_value = yearly_mined_tokens * configs["global_params"]["token_value"]

    # NOTE: Calc the users costs / savings
    power_cost = configs["user_config"]["avg_power_consumption"] * 12
    cloud_savings = configs["user_config"]["avg_monthly_storage_cost"] * 12

    current_token_value = configs["global_params"]["token_value"]
    token_value_array = [current_token_value + (i * 0.01) for i in range(0, 12)]

    # An array to model the X-axis on a few graphs
    time_array = [i for i in range(1, 13)]

    # Shows the amount of miners for each month
    miner_plot = {
        "data": [
            {
                "x": time_array,
                "y": monthly_miner_snapshot,
                "name": "Miners",
                "type": "line",
            }
        ]
    }

    usd_reward_balance = []
    monthly_sub_total = []
    sub_val = []
    tokens = 0

    for i in range(len(miner.monthly_rewards)):
        amnt = miner.monthly_rewards[i]

        if len(monthly_sub_total) == 0:
            monthly_sub_total.append(amnt)
            tokens = amnt
        else:
            monthly_sub_total.append(monthly_sub_total[i - 1] + amnt)
            tokens = monthly_sub_total[-1]

        usd_reward_balance.append(float(amnt) * token_value_array[i])
        sub_val.append(float(tokens) * current_token_value)

    # A plot that shows as miners increase, tokens rewarded per miner (based
    # on amount of storage the individual provides)
    token_accum_plot = {
        "data": [
            {
                "x": time_array,
                "y": miner.monthly_rewards,
                "type": "line",
                "name": "Mined Rewards",
            },
            {
                "x": time_array,
                "y": monthly_sub_total,
                "type": "line",
                "name": "Accumulated Tokens",
            },
        ]
    }

    # Shows the increase in monthly storage increase
    network_plot = {
        "data": [
            {
                "x": time_array,
                "y": monthly_storage_snapshot,
                "type": "line",
                "labels": {"x": " Months", "y": "Monthly Network Storage"},
            }
        ]
    }

    # Char to show the value of the tokens for the year if price is constant
    usd_val_tokens_per_month = {
        "data": [{"x": monthly_sub_total, "y": sub_val, "type": "line"}]
    }

    # Array of token values for the accumulated tokens
    sub_val = [
        monthly_sub_total[i] * token_value_array[i]
        for i in range(0, len(token_value_array))
    ]

    # Chart to show each months Accumulated tokens value
    usd_val_inc_1_cent = {
        "data": [{"x": monthly_sub_total, "y": sub_val, "type": "line"}]
    }

    network_table = {
        "Start of Year Storage": round(monthly_storage_snapshot[0], 2),
        "End of Year Storage": round(monthly_storage_snapshot[-1], 2),
        "Initial Token Value": configs["global_params"]["token_value"],
        "End of Year Value": current_token_value,
    }

    miner_table = {
        "Start of Year Miners": configs["miner_config"]["miner_count"],
        "End of Year Active Miners": calc_avg_active_miners(monthly_miner_snapshot),
        "Monthly % Change in miners": configs["miner_config"]["rate_of_change"],
        "Avg Daily Token Reward": round(avg_tokens_per_day, 3),
        "Yearly Token Reward": round(yearly_mined_tokens, 3),
        "Mined token USD Value": round(EOY_value, 2),
        "User Cloud Storage Savings": cloud_savings,
        "Net Profit": round(((EOY_value - power_cost) + cloud_savings), 2),
    }

    # the final dictionary with all of our calculations
    to_sender = {
        "tables": {
            "network_table": network_table,
            "miner_table": miner_table,
            "network_storage_table": create_network_table(miners),
        },
        "plots": {
            "token_accum_plot": token_accum_plot,
            "network_storage_plot": network_plot,
            "miner_plot": miner_plot,
            "usd_val_tokens_per_month": usd_val_tokens_per_month,
            "increment_token": usd_val_inc_1_cent,
        },
    }
    return to_sender


def gen_results(configs: dict):
    """
    Params:
        - configs: a dictionary of simulation configs

    Returns:
        A dictionary with the calculated information
    """

    # Some constants to make references easier later
    init_miners = configs["miner_config"]["miner_count"]
    monthly_tokens = configs["miner_config"]["monthly_token_amount"]
    rate_of_change = configs["miner_config"]["rate_of_change"]
    storage_provided = configs["miner_config"]["storage_provided"]

    # Create the initial pool of miners/ boxes
    miners = gen_miners(spawn=init_miners, start=0, storage=storage_provided)

    # A variable to help track the current total storage provided
    total_storage = calc_network_storage(miners)

    # An array to track amount of network storage per month
    monthly_storage_snapshot = []

    # An array to track the amount of miners per month (good chart)
    monthly_miner_snapshot = [len(miners)]

    for month in range(1, 13):

        print("\n ----- Month " + str(month) + " -----")
        # Update the snapshot
        monthly_storage_snapshot.append(total_storage)
        # calc reward
        update_monthly_rewards(miners, monthly_tokens, total_storage)

        # increase the miner pool
        print("\tActive Network Participants: " + str(len(miners)))
        miners = monthly_change(miners, rate_of_change)

        # Update the sum of current storage
        total_storage = calc_network_storage(miners)
        print("\tCurrent Storage: " + str(total_storage))

        # Readjust the amount of contribution
        update_network_contribution(miners, total_storage)

        # Create the months miner snapshot
        monthly_miner_snapshot.append(len(miners))

    print("\n ----- Data Generation Done ----- \n\n")

    to_sender = gen_to_sender(
        miners, configs, monthly_miner_snapshot, monthly_storage_snapshot
    )

    return to_sender
