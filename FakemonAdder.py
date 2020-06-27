import json
from github import Github

# Getting config
with open("config.json") as f:
    config = json.load(f)
    gUser = config["gUser"]
    gPass = config["gPass"]

# Initializing Github object
g = Github(gUser, gPass)

class FakemonAdder():
    def __init__(self, name, spritesDict, abilitiesDict, learnsetDict, types, genderRatioDict, baseStats, height, weight, mainColor, evolution="", eggGroups):
        self.name = name
        self.sprites = spritesDict
        self.abilities = abilitiesDict
        self.learnset = learnsetDict
        self.types = types
        self.genderRatio = genderRatioDict
        self.baseStats = baseStats
        self.height = height
        self.weight = weight
        self.color = mainColor
        self.evolution = [evolution]
        self.eggGroups = eggGroups

    def add(self, discordUser):
        """
        This function is used to add the fakemon's info to the server and client.
        """
        # Getting the Pokefinium Pokemon Showdown Server repository
        repo = g.get_repo("koreanpanda345/Pokefinium-PS-Server")

        """
        This part onwards is where we edit the code in the server files and commit it to the `bot-add-fakemon` branch.
        """


        """
        This part onwards is where we edit the code in the client files and commit it to the `bot-add-fakemon` branch.
        """
        

        # Making the Pull Request
        body = f"""
        THIS PULL REQUEST WAS MADE AUTOMATICALLY IN RESPONSE TO A REQUEST TO ADD {self.name} BY {discordUser}.
        """
        pr = repo.create_pull() # TODO


