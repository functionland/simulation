There is more comprehensive machinations simulations, which includes both mining and torage rewards: https://github.com/functionland/simulation/blob/2a33dc9a07f47a3ae2b337c42587f5fec19e6d9d/Simulation%20FULA%20-%20final%20version.mp4

# Simulation

This is Python simulation for mining part.

### Fula Blockchain Simulation

## Motivation

To develop a simulation model for the Mining rewards portion of the
Functionland project.

## Basic Concept:

A user would assess their current position financially and then make a decision
on whether or not to purchase the Functionland box. If they choose to purchase
the box, then we analyze the trade potential cost difference (and earnings!)
that a user would experience.

Some key parameters being utilized:

- Time (defaults to 1 year)
- Cloud savings (Is derived from the amount not spent on the cloud storage
  solutions)
- Hardware buy in cost (A one time cost associated with getting the mining
  device)
- Power consumption cost (An additional cost, though not much, per month)
- Tokens earned per end user (The reward earned by mining per user)
  - Amount depends on the number of miners in the system
  - Example: 50,000 miners a month and the reward is 200 tokens a month

These will then influence the modeling the rewards (money earned) from mining
the token over the course of a year.

### Key Insights

- We noticed on the default settings (after we had set miners to default to 1100) that the token rewards at the end of the year vs miners starts to cross
  after 1 year.
  - This was different from the relatively low margin of tokens mined at 10,000
    miners and could be a good indicator of when people would want to join the
    network.

## Development

### Requirements:

- Python >= 3.10
- A virtual environment
  - Currently using
    [VirtualFish](https://virtualfish.readthedocs.io/en/latest/install.html)
- Jupyter Labs or Jupyter notebook
  - Download or use an extension inside of VScode
- `ipykernel`

### Project Execution

To run the Jupyter Notebook (and eventually python script files):

1. Enable your virtual environment

```vf new functionland

pip install requirements.txt

```

Then you will need to add the kernel to the notebook if you want the virtual
environment to work properly:

`python -m ipykernel install --user --name=functionland`

Do note that the environment name of `functionland` can be replaced with
anything else, just remember to stay consistent otherwise errors may arise.

Once we have the script files, those can be executed with the python run time
without the need to load in that extra kernel (woo!).

#### Running the Python Simulation

This was developed with Python 3.8 as the version so the way to run it on the
CLI should follow:

`python3 src/simulations/__init__.py`

If you use VScode (or similar) it should be a very similar execution step once
you are able to locate `main.py` or the `__init__.py` module.

### Progress:

- [x] Setup the initial system parameters
- [x] Show the token price at $0.04
- [x] Show the rewards for those who mined over the course of year as the token
      value increases.
- [x] Show the break even point (explicitly)
- [x] Build the models in Python scripts
- [x] Integrate with dashboard service
- [x] Build out the UI of the dashboard

### Issues / Bugs:

At this time, no known bugs are present.
