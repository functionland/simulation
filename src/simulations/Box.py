###
## Model of the Box for the Fula network
##
## Authors: Nicholas O'Kelley, Jake Cassani
## Organization: Longtail Financial
##
## Date: March 19th, 2022
## Last Modified: March 19, 2022
###


class Box:
    def __init__(self, mac, storage_provided):
        self.mac_address = mac  # UUID
        self.storage = storage_provided  # float | int
        self.storage_percent = 0.0
        self.monthly_rewards = []
        self.daily_rewards = []

    def display(self):
        return (
            "Box UUID: "
            + str(self.mac_address)
            + " Storage Provided: "
            + str(self.storage)
        )
