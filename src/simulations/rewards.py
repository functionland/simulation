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
import Box

# Standard imports
import uuid
import random
import pandas as pd

# A constant for the upper bound of storage a user can provide
# Allows for expansion or reduction without repeating ourselves in the code.
STORAGE_BOUND = 10.001


def gen_boxes(total_storage=0.0, boxes=[], storage_user=-1.0) -> list:
    """
    Generates boxes

    Params:
        spawn: the cap of storage
        boxes: an optional list to update

    Returns:
        The updated array
    """

    remaining_storage = total_storage - storage_user
    allocated = 0
    # print("Remaining Storage: " + str(remaining_storage))

    if storage_user != -1.0:
        # Ensure one miner represents the dashboard user
        boxes.append(Box.Box(str(uuid.uuid4()), storage_user))

    if storage_user == 0:
        # Prevent issues with zero division
        boxes.append(Box.Box(str(uuid.uuid4()), 1))
        remaining_storage = remaining_storage - 1

    while remaining_storage > 0.0:
        if remaining_storage < 1.0:
            allocated = remaining_storage
            boxes.append(Box.Box(uuid.uuid4(), allocated))
        elif remaining_storage < 10.0:
            allocated = random.uniform(0.0, remaining_storage)
            boxes.append(Box.Box(uuid.uuid4(), allocated))
        else:
            allocated = random.uniform(0.0, 10.0)
            boxes.append(Box.Box(uuid.uuid4(), allocated))

        remaining_storage = remaining_storage - allocated

    return boxes


def calc_network_storage(boxes: list) -> float:
    """
    Helper function to calculate the amount of storage in the Fula Network
    Params:
        boxes: current list of boxes
    Returns:
        The summed amount of storage provided by all the boxes.
    """
    storage = 0

    for b in boxes:
        storage = storage + b.storage

    return storage


def update_monthly_rewards(boxes, monthly_tokens, total_storage):
    """
    Helper function that updates the rewards of the boxes for the month
    and calculates the average tokens per day.
    Params:
        boxes: list of the boxes in the system
        monthly_tokens: pool of tokens to divide
        total_storage: amount of total storage provided (basis)
    Returns:
        None
    """
    for miner in boxes:
        miner.monthly_rewards.append(
            token_rewards(
                calc_storage_percentage(miner.storage, total_storage),
                monthly_tokens,
            )
        )

        miner.daily_rewards.append(calc_daily_rewards(miner))


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


def calc_daily_rewards(miner):
    """
    Helper function to calculate the daily rewards for a given 30 day period.
    Params:
        boxes: current list of boxes
    Returns:
        The Daily amount of mined rewards
    """

    # NOTE: A month is consider a 30 day period
    return miner.monthly_rewards[-1] / 30


def update_network_contribution(boxes, total_storage):
    """
    Helper function that updates the relative amount of storage provided to the network
    Params:
        boxes: list of the boxes in the system
        total_storage: amount of total storage provided (basis)
    Returns:
        None
    """
    for miner in boxes:
        miner.storage_percent = calc_storage_percentage(miner.storage, total_storage)


def monthly_change(
    current_provided_storage,
    boxes: list,
    percent_change: float,
) -> list:
    """
    Helper function that adds new boxes to the pool
    Params:
        current_provided_storage: amount of stroage currently provided
        boxes: current list of boxes
        percent_change: amount to increase the amount of boxes in the system
    Returns:
        The updated list of boxes in the simulation
    """

    amount_to_increase = round(current_provided_storage * percent_change)
    return gen_boxes(total_storage=amount_to_increase, boxes=boxes)


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

    monthly_sub_total = []
    sub_val = []
    tokens = 0

    # print(len(miner.monthly_rewards))
    for i in range(len(miner.monthly_rewards)):

        amnt = miner.monthly_rewards[i]

        if len(monthly_sub_total) == 0:
            monthly_sub_total.append(amnt)
            tokens = amnt
        else:
            monthly_sub_total.append(monthly_sub_total[i - 1] + amnt)
            tokens = monthly_sub_total[-1]

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

    network_table = {
        "Start of Year Storage (TB)": round(monthly_storage_snapshot[0], 2),
        "End of Year Storage (TB)": round(monthly_storage_snapshot[-1], 2),
        "Monthly % Change in Storage": configs["box_config"]["rate_of_change"],
        "Token Value (USD)": configs["global_params"]["token_value"],
    }

    storage_table = {
        "Mined Token Value (USD)": round(EOY_value, 2),
        "User Cloud Storage Savings (USD)": cloud_savings,
        "Electricity Cost (USD)": 12
        * float(configs["user_config"]["avg_power_consumption"]),
        "Net Profit (USD)": round(((EOY_value - power_cost) + cloud_savings), 2),
        "Yearly Token Reward": round(yearly_mined_tokens, 3),
        "Avg Daily Token Reward": round(avg_tokens_per_day, 3),
    }

    # the final dictionary with all of our calculations
    return {
        "tables": {
            "network_table": network_table,
            "storage_table": storage_table,
        },
        "plots": {
            "token_accum_plot": token_accum_plot,
            "network_storage_plot": network_plot,
            "miner_plot": miner_plot,
        },
    }


def gen_results(configs: dict):
    """
    Params:
        - configs: a dictionary of simulation configs

    Returns:
        A dictionary with the calculated information
    """

    # Some constants to make references easier later
    storage_cap = configs["box_config"]["storage_cap"]
    monthly_tokens = configs["box_config"]["monthly_token_amount"]
    rate_of_change = configs["box_config"]["rate_of_change"]
    storage_provided = configs["box_config"]["storage_provided"]
    time = configs["global_params"]["time_in_months"]

    # Create the initial pool of boxes
    boxes = gen_boxes(storage_cap, storage_user=storage_provided)
    total_storage = calc_network_storage(boxes)
    # print("Starting storage: " + str(round(total_storage, 2)))

    amount_of_boxes = len(boxes)

    # An array to track amount of network storage per month
    monthly_storage_snapshot = []

    monthly_storage_snapshot.append(total_storage)

    # An array to track the amount of boxes per month (good chart)
    monthly_miner_snapshot = [amount_of_boxes]

    for month in range(1, time):

        # print("----- Month " + str(month) + " -----")
        update_monthly_rewards(boxes, monthly_tokens, total_storage)

        # print("\tActive Network Participants: " + str(len(boxes)))
        boxes = monthly_change(total_storage, boxes, rate_of_change)

        total_storage = calc_network_storage(boxes)
        # print("\tCurrent Storage: " + str(round(total_storage, 2)))

        update_network_contribution(boxes, total_storage)
        monthly_storage_snapshot.append(total_storage)
        monthly_miner_snapshot.append(len(boxes))

    update_monthly_rewards(boxes, monthly_tokens, total_storage)

    # print("\n ----- Data Generation Done ----- \n\n")

    to_sender = gen_to_sender(
        boxes, configs, monthly_miner_snapshot, monthly_storage_snapshot
    )

    return to_sender
