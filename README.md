# Simulation

### Fula Blockchain Simulation

## Motivation

To develop a simulation model for the Mining rewards portion of the Functionland
project.

## Basic Concept:

A user would assess their current position financially and then make a decision
on whether or not to purchase the Functionland box. If they choose to purchase the
box, then we analyze the trade potential cost difference (and earnings!) that a user
would experience.

Some key parameters being utilized:

- Cloud savings
- Hardware buy in cost
- Power consumption cost
- Tokens earned per end user

These will then influence the modeling the rewards (money earned) from
mining the token over the course of a year.

## Development

### Requirements:

- Python >= 3.8
- A virtual environment
  - Currently using [VirtualFish](https://virtualfish.readthedocs.io/en/latest/install.html)
- Jupyter Labs or Jupyter notebook
  - Download or use an extension inside of VScode
- `ipykernel`

### Project Execution

To run the Jupyter Notebook (and eventually python script files):

1. Enable your virtual environment

```
vf new functionland

pip install requirements.txt

```

Then you will need to add the kernel to the notebook if you want the virtual environment
to work properly:

```
python -m ipykernel install --user --name=functionland
```

Do note that the environment name of `functionland` can be replaced with anything else,
just remember to stay consistent otherwise errors may arise.

Once we have the script files, those can be executed with the python run time without
the need to load in that extra kernel (woo!).

### Progress:

- [x] Setup the initial system parameters
- [x] Show the token price at $0.04
- [x] Allow the graph to adjust for price up to $5
- [x] Show the rewards for those who mined over the course of year as the token value increases.
- [x] Show the break even point (explicitly)
- [ ] Build the models in Python scripts (Working on this)
- [ ] Integrate with dashboard service
- [x] Build out the UI of the dashboard
- [ ] Deliver link

### Issues / Bugs:

At this time, no known bugs are present.
