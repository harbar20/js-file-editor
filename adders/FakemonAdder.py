import json
from github import Github
import base64
import requests

# Getting config
with open("config.json") as f:
    config = json.load(f)
    gUser = config["gUser"]
    gPass = config["gPass"]

# Initializing Github object
g = Github(gUser, gPass)

# Gets the SHA-1 value of a given filepath in the server repo
def getSHA(filepath):
    tree = requests.get("https://api.github.com/repos/koreanpanda345/Pokefinium-PS-Server/git/trees/bot-add-fakemon").json()
    firstDir = filepath.split("/")[0]
    # Finding the file sha
    for path in tree["tree"]:
        if (path["path"] == firstDir):
            firstUrl = path["url"]
            firstDirTree = requests.get(firstUrl).json()
            targetFile = filepath.split("/")[1]
            for path2 in firstDirTree["tree"]:
                if (path2["path"] == targetFile):
                    return path2["sha"]

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
        serverRepo = g.get_repo("koreanpanda345/Pokefinium-PS-Server")
        with open("../currentNum/currentPokeNum.txt") as f: currentNum = f.read()

        """
        This part onwards is where we edit the code in the server files and commit it to the `bot-add-fakemon` branch.
        """
        # Getting the original content of pokedex.ts
        pokedexSha = getSHA("data/pokedex.ts")
        pokedexBlob = serverRepo.get_git_blob(pokedexSha)
        # Decoding the contents of pokedex.ts
        pokedexContents = base64.b64decode(pokedexBlob.content).decode("utf-8")
        # Updating the content of pokedex.ts
        newContent = f"""    {self.name.lower()}: {{
        num: {currentNum},
        name: \"{self.name.lower()}\",
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
        pokedexContents = pokedexContents.replace("};", newContent)
        # Updating the current number for the next Pokemon
        with open("../currentNum/currentPokeNum.txt", "w") as f: f.write(currentNum+1)

        # Getting the original content of learnsets.ts
        learnsetsSha = getSHA("data/learnsets.ts")
        learnsetsBlob = serverRepo.get_git_blob(learnsetsSha)
        # Decoding the contents of pokedex.ts
        learnsetsContents = base64.b64decode(learnsetsBlob.content).decode("utf-8")
        # Updating the content of learnsets.ts
        newContent = f"""    {self.name.lower()}: {{
        learnset: {self.learnset}
    }},
}};
        """
        learnsetsContents = learnsetsContents.replace("};", newContent)

        # Getting the original content of formats-data.ts
        formatsSha = getSHA("data/formats-data.ts")
        formatsBlob = serverRepo.get_git_blob(formatsSha)
        # Decoding the contents of pokedex.ts
        formatsContents = base64.b64decode(formatsBlob.content).decode("utf-8")
        # Updating the content of formats-data.ts
        newContent = f"""    {self.name.lower()}: {{
            isNonstandard: \"Custom\",
            tier: \"CAP\"
    }},
}}; 
        """
        formatsContents = formatsContents.replace("};", newContent)

        # Making the Pull Request in the server repository
        title = f"{self.name} - new fakemon. Requested by {discordUser}; updated BY BOT."
        body = f"""THIS PULL REQUEST WAS MADE AUTOMATICALLY IN RESPONSE TO A REQUEST TO ADD {self.name} BY {discordUser}.
        """
        # Committing the updates to the learnsets.ts file
        learnsetCommit = serverRepo.update_file("data/learnsets.ts", f"Adding {self.name}'s learnset as requested by {discordUser}.", learnsetsContents, learnsetsSha, branch="bot-add-fakemon")["commit"]
        # Committing the updates to the formats-data.ts file
        formatsCommit = serverRepo.update_file("data/formats-data.ts", f"Adding {self.name}'s format info as requested by {discordUser}.", formatsContents, formatsSha, branch="bot-add-fakemon")["commit"]
        # Committing the updates to the pokedex.ts file
        pokedexCommit = serverRepo.update_file("data/pokedex.ts", f"Adding {self.name} as requested by {discordUser}.", pokedexContents, pokedexSha, branch="bot-add-fakemon")["commit"]
        # Making the PR
        serverPR = serverRepo.create_pull(title=title, body=body, head="bot-add-fakemon", base="master")
        print(f"New PR made: {serverPR.html_url}")

        """
        This part onwards is where we add the sprites to the sprites repository.
        """
        # TODO

#Testing baby let's get it
name = "Gorouchu"
spritesDict = {}
abilitiesDict = {
    "0": "Static",
    "1": "Volt Absorb",
    "H": "Inner Focus"
}
learnsetDict = {}
types = ["Electric", "Fighting"]
genderRatioDict = {"M": 0.5, "F": 0.5}
baseStats = {
    "hp": 60,
    "atk": 105,
    "def": 55,
    "spa": 80,
    "spd": 85,
    "spe": 110
}
height = 1
weight = 40
mainColor = "Orange"
evolution = ""
eggGroups = ["Field", "Fairy"]
adder = FakemonAdder(name, spritesDict, abilitiesDict, learnsetDict, types, eggGroups, baseStats, height, weight, mainColor, evolution, genderRatioDict)
adder.add("xSilas#9434")