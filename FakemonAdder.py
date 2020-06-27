import json
from github import Github
import base64

# Getting config
with open("config.json") as f:
    config = json.load(f)
    gUser = config["gUser"]
    gPass = config["gPass"]

# Initializing Github object
g = Github(gUser, gPass)

class FakemonAdder():
    def __init__(self, name, spritesDict, abilitiesDict, learnsetDict, types, eggGroups, baseStats, height, weight, mainColor, evolution="", genderRatioDict={"M": 0.5, "F": 0.5}):
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
        serverRepo = g.get_repo("koreanpanda345/Pokefinium-SD-Server")

        """
        This part onwards is where we edit the code in the server files and commit it to the `bot-add-fakemon` branch.
        """
        # Getting the original content of pokedex.ts
        pokedexContents = serverRepo.get_contents("data/pokedex.ts")
        pokedexSha = pokedexContents.sha
        # Decoding the contents of pokedex.ts
        pokedexContents = base64.b64decode(pokedexContents.content).decode("utf-8")\
        # Updating the content of pokedex.ts
        newContent = f"""    {self.name.lower()}: {{
        num: 1,
        species: \"{self.name}\",
        types: {self.types},
        genderRatio: {self.genderRatio},
        baseStats: {self.baseStats},
        abilities: {self.abilities},
        heightm: {self.height},
        weightkg: {self.weight},
        color: \"{self.color}\",
        evos: {self.evolution},
        eggGroups: {self.eggGroups}
    }},
}};
        """
        print(f"New fakemon: {newContent}")
        pokedexContents = pokedexContents.replace("};", newContent)
        # Committing the updates to the pokedex.ts file
        pokedexCommit = serverRepo.update_file(pokedexContents.path, f"Adding {self.name} as requested by {discordUser}.", pokedexContents, pokedexSha, branch="bot-add-fakemon")["commit"]

        # Getting the original content of learnsets.ts
        learnsetContents = serverRepo.get_contents("data/learnsets.ts")
        learnsetSha = learnsetContents.sha
        # Decoding the contents of learnsets.ts
        learnsetContents = base64.b64decode(learnsetContents.content).decode("utf-8")
        # Updating the content of learnsets.ts
        newContent = f"""    {self.name.lower()}: {{
        learnset: {self.learnset}
    }},
}};
        """
        learnsetContents = learnsetContents.replace("};", newContent)
        # Committing the updates to the learnsets.ts file
        learnsetCommit = serverRepo.update_file(learnsetContents.path, f"Adding {self.name}'s learnset as requested by {discordUser}.", learnsetContents, learnsetSha, branch="bot-add-fakemon")["commit"]

        # Getting the original content of formats-data.ts
        formatsContents = serverRepo.get_contents("data/formats-data.ts")
        formatsSha = formatsContents.sha
        # Decoding the contents of formats-data.ts
        formatsContents = base64.b64decode(formatsContents.content).decode("utf-8")
        # Updating the content of formats-data.ts
        newContent = f"""    {self.name.lower()}: {{
            isNonStandard: \"Cap\",
            tier: \"CAP\"
    }},
}}; 
        """
        formatsContents = formatsContents.replace("};", newContent)
        # Committing the updates to the formats-data.ts file
        formatsCommit = serverRepo.update_file(formatsContents.path, f"Adding {self.name}'s format info as requested by {discordUser}.", formatsContents, formatsSha, branch="bot-add-fakemon")["commit"]

        # Making the Pull Request in the server repository
        title = f"{self.name} - new fakemon. Requested by {discordUser}; updated BY BOT."
        body = f"""THIS PULL REQUEST WAS MADE AUTOMATICALLY IN RESPONSE TO A REQUEST TO ADD {self.name} BY {discordUser}.
        """
        serverPR = serverRepo.create_pull(title=title, body=body, head="bot-add-fakemon", base="master")
        print(f"New PR made: {serverPR.html_url}")

        """
        This part onwards is where we add the sprites to the sprites repository.
        """
        # TODO

#Testing baby let's get it
name = "RickAstley"
spritesDict = {}
abilitiesDict = {
    "0": "Gluttony",
    "1": "Thick Fat",
    "H": "Iron Fist"
}
learnsetDict = {}
types = ["Fire", "Water"]
genderRatioDict = {"M": 0.5, "F": 0.5}
baseStats = {
    "hp": 5,
    "atk": 5,
    "def": 5,
    "spa": 5,
    "spd": 5,
    "spe": 5
}
height = 0.5
weight = 60
mainColor = "Red"
evolution = "Richard Buttockstley"
eggGroups = ["Fat"]
adder = FakemonAdder(name, spritesDict, abilitiesDict, learnsetDict, types, eggGroups, baseStats, height, weight, mainColor, evolution, genderRatioDict)
adder.add("harbar20#9389")