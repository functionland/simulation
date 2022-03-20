###
## Simulating the Miner Rewards for the Fula Network
##
## Authors: Nicholas O'Kelley, Jake Cassani
## Organization: Longtail Financial
## Date: March 8th, 2022
## Last Modified: March 19, 2022
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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


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
    """

    curr_miners = len(miners)
    amount_to_increase = round(curr_miners * percent_change)

    for i in range(amount_to_increase):
        storage = random.random() * 10
        mac_address = uuid.uuid4()
        miners.append(Box(mac_address, storage))

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


def display_stats(monthly_reward, monthly_miner_dist, token_value):
    """
    A helper function that can display a few stats on the terminal
    """

    curr_month = 1
    for i in range(len(monthly_reward)):
        tokens = monthly_reward[i]
        miners = monthly_miner_dist[i]
        curr_val = token_value[i]

        print("[Simulation] Current Month: " + str(curr_month))
        print("\t[Simulation] Current Miners: " + str(miners))
        print("\t[Simulation] Current Monthly Reward: " + str(tokens) + " tokens")
        print("\t[Simulation] Current reward value in USD: " + str(tokens * curr_val))
        curr_month += 1


def gen_miners(init_miners, start=0) -> list:
    """
    Generates the initial batch of miners

    Returns:
        The updated miner array
    """

    miners = []

    for _ in range(start, init_miners):
        storage = random.randrange(0, 11)
        miners.append(Box(uuid.uuid4(), storage))

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
    Calculates the amount of storage in the Fula Network
    """
    storage = 0

    for miner in miners:
        storage = storage + miner.storage

    return storage


def calc_daily_rewards(miner):
    # NOTE: A month is consider a 30 day period
    return miner.monthly_rewards[-1] / 30


def create_df(miners):
    """
    Helper function that is mainly utilized to create the Storage breakdown
    dataframe.

    Used on the dashboard mainly.
    """
    storage = []
    mac = []

    for miner in miners:
        mac.append(miner.mac_address)
        storage.append(miner.storage)

    data = zip(mac, storage)
    df = pd.DataFrame(data, columns=["MacAddress", "Storage"])
    val = df["Storage"].value_counts()
    counts = []
    for i in range(0, 11):
        counts.append(val[i])
    index = [i for i in range(0, 11)]

    df = pd.DataFrame(zip(index, counts), columns=["Amnt", "Count"])

    return df


def gen_results(configs: dict = {}):
    """
    Params:
        - configs: a dictionary of simulation configs

    Returns:
        A dictionary with the calculated information
    """

    init_miners = configs["miner_config"]["miner_count"]
    monthly_tokens = configs["miner_config"]["monthly_token_amount"]
    init_token_value = configs["global_params"]["token_value"]
    rate_of_change = configs["miner_config"]["rate_of_change"]

    # month 1 of miners
    miners = gen_miners(init_miners, start=0)
    total_storage = calc_network_storage(miners)

    # An array to track the amount of miners per month (good chart)
    monthly_miner_snapshot = [len(miners)]

    # An array to track amount of network storage per month
    monthly_storage_snapshot = []

    for _ in range(1, 13):

        # Update the snapshot
        monthly_storage_snapshot.append(total_storage)

        # calc reward
        update_monthly_rewards(miners, monthly_tokens, total_storage)

        # increase the miner pool
        miners = monthly_change(miners, rate_of_change)

        # Sum the current storage
        total_storage = calc_network_storage(miners)

        # Readjust the amount of contribution
        update_network_contribution(miners, total_storage)
        monthly_miner_snapshot.append(len(miners))

    # placeholder box
    miner = Box(uuid.uuid4(), random.randrange(0, 11))
    # This can be reduce some how
    for m in miners:
        if m.storage == configs["miner_config"]["storage_provided"]:
            miner = m
            break

    # NOTE: our selected miner / box represents the uers viewing the app
    avg_tokens_per_day = sum(miner.daily_rewards) / 12
    yearly_mined_tokens = sum(miner.monthly_rewards)
    EOY_value = yearly_mined_tokens * configs["global_params"]["token_value"]

    # NOTE: Calc the users costs / savings
    power_cost = configs["user_config"]["avg_power_consumption"] * 12
    cloud_savings = configs["user_config"]["avg_monthly_storage_cost"] * 12

    time_array = [i for i in range(1, 13)]

    current_token_value = configs["global_params"]["token_value"]
    token_value_array = [current_token_value + (i * 0.01) for i in range(0, 12)]

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

    token_value = token_value_array
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

        value = token_value[i]
        usd_reward_balance.append(float(amnt) * value)
        sub_val.append(float(tokens) * current_token_value)

    reward_in_usd_plot = {
        "data": [{"x": time_array, "y": usd_reward_balance, "type": "line"}]
    }

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

    usd_val_tokens_per_month = {
        "data": [{"x": monthly_sub_total, "y": sub_val, "type": "line"}]
    }

    sub_val = [
        monthly_sub_total[i] * token_value[i] for i in range(0, len(token_value))
    ]

    usd_val_inc_1_cent = {
        "data": [{"x": monthly_sub_total, "y": sub_val, "type": "line"}]
    }

    # the final dictionary with all of our calculations
    to_sender = {
        "Time": configs["global_params"]["time_in_months"],
        "Miners": init_miners,
        "Avg_Active_Miners": calc_avg_active_miners(monthly_miner_snapshot),
        "Tokens": monthly_tokens,
        "token_value": current_token_value,
        "rate_of_change": configs["miner_config"]["rate_of_change"],
        "Avg_Miner_stats": {
            "power_cost": power_cost,
            "cloud_storage_savings": cloud_savings,
            "avg_tokens_per_day": avg_tokens_per_day,
            "yearly_mined_tokens": yearly_mined_tokens,
            "end_of_year_value": EOY_value,
            "net_profit": ((EOY_value - power_cost) + cloud_savings),
        },
        "plots": {
            "token_accum_plot": token_accum_plot,
            "network_storage_plot": network_plot,
            "reward_in_usd_plot": reward_in_usd_plot,
            "miner_plot": miner_plot,
            "usd_val_tokens_per_month": usd_val_tokens_per_month,
            "increment_token": usd_val_inc_1_cent,
            "pie_df": create_df(miners).to_json(),
        },
    }

    return to_sender
