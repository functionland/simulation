###
## Simulating the Miner Rewards for the Fula Network
##
## Authors: Nicholas O'Kelley, Jake Cassani
## Organization: Longtail Financial
## Date: March 8th, 2022
###


def monthly_change(
    var,
    percent_change,
    upper_bound=12,
) -> list:
    """
    Simulates either 12 months or a specified monthly percent change (delta)

    Params:
        var : the variable that will change
        percent_change : the percent increase or decrease
        upper_bound : the amount of iterations (months) that should pass

    Returns:
        A list with each months values
    """
    payload = []
    payload.append(var)
    for i in range(1, upper_bound):
        payload.append(round(payload[i - 1] + (payload[i - 1] * percent_change)))
    return payload


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


def gen_reward_per_month(miner_dist, monthly_token_amount):
    """
    A helper function that will calculate the token reward each miner will recieve
    for each entry in the miner distribution. This is typically a one year calculation
    based on our work, but it should handle future year expansion

    Params:
      - miner_dist: dictionary of miners each month, for a given time frame
      - monthly_token_amount: the amount of tokens to be mined each month

    Returns:
      A list with the rewards per month

    """
    reward_per_miner_per_month = []
    for miners in miner_dist:
        reward_per_miner_per_month.append(monthly_token_amount / miners)

    return reward_per_miner_per_month


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


def gen_results(configs: dict = {}):
    """
    This is the "meat and potatos" of the simulation. Given a few parameters based
    on the config seen in `main.py`, this function will
    handle calculating the various stats about how much a person would see in
    rewards and offseting this with any costs that come up from joining the
    system.

    Params:
        - configs: a dictionary of simulation configs

    Returns:
        A dictionary with the calculated information
    """

    miners = configs["miner_config"]["miner_count"]
    tokens = configs["miner_config"]["monthly_token_amount"]
    current_token_value = configs["global_params"]["token_value"]

    monthly_miner_dist = monthly_change(
        miners, configs["miner_config"]["rate_of_change"]
    )

    # NOTE: If they want to change rate of price increase, we can modify the 0.01
    # NOTE: and then add another slider on the dashboard
    token_value = [current_token_value + (i * 0.01) for i in range(0, 12)]

    # A list of each months mined tokens
    monthly_reward = gen_reward_per_month(monthly_miner_dist, tokens)

    monthly_balance = [monthly_reward[0]]

    for i in range(1, len(monthly_reward)):
        monthly_balance.append(monthly_balance[i - 1] + monthly_reward[i])

    # The total years cost of power (it's a debt that has to be accounted for)
    yearly_power_cost = configs["user_config"]["avg_power_consumption_cost"] * 12

    # Given the current_token_value, what are the tokens worth
    EOY_value = round(sum(monthly_reward) * current_token_value, 2)

    # This debt is now a savings that can help offset power
    cloud_cost_now_savings = configs["user_config"]["avg_monthly_storage_cost"]

    # A constant array that is used on the dashboard
    months = [i for i in range(1, configs["global_params"]["time_in_months"])]

    # Calcuate the average tokens mined per day for a year
    # total tokens for the year divided by 365
    avg_tokens_per_day = round(monthly_balance[-1] / 365)

    # the final dictionary with all of our calculations
    to_sender = {
        "Miners": miners,
        "Tokens": tokens,
        "Time": configs["global_params"]["time_in_months"],
        "Avg_Active_Miners": calc_avg_active_miners(monthly_miner_dist),
        "rate_of_change": configs["miner_config"]["rate_of_change"],
        "Avg_Miner_stats": {
            "avg_tokens_per_day": avg_tokens_per_day,
            "yearly_mined_tokens": sum(monthly_reward),
            "end_of_year_value": EOY_value,
            "power_cost": yearly_power_cost,
            "cloud_storage_savings": cloud_cost_now_savings,
            "net_profit": ((EOY_value - yearly_power_cost) + cloud_cost_now_savings),
        },
        "monthly_miner_dist": monthly_miner_dist,
        "monthly_rewards_per_miner": monthly_reward,
        "time_array": months,
        "monthly_balance": monthly_balance,
        "token_value_array": token_value,
    }

    # Display results for the CLI
    # Not necessary for a remote call
    print("--- Start Miner Rewards ----")
    display_stats(monthly_balance, monthly_miner_dist, token_value)
    print("--- End Miner Rewards ----")

    return to_sender
