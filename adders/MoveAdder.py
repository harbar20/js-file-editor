import json
from github import github
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

class MoveAdder():
    def __init__(self, accuracy, basePower, category, description, shortDesc, name, pp, priority, secondary, target, moveType, zMove, flags={}):
        self.accuracy = accuracy
        self.bp = basePower
        self.category = category
        self.desc = description
        self.shortDesc = shortDesc
        self.name = name
        self.pp = pp
        self.priority = priority
        self.secondary = secondary
        self.target = target
        self.type = moveType
        self.zMove = zMove
        self.flags = flags
    
    def add(discordUser):
        """
        This function is used to add the fakemon's info to the server and client.
        """
        # Getting the Pokefinium Pokemon Showdown Server repository
        serverRepo = g.get_repo("koreanpanda345/Pokefinium-PS-Server")
        with open("currentMoveNum.txt") as f: currentNum = f.read()

        """
        This part onwards is where we edit the code in the server files and commit it to the `bot-add-move` branch.
        """
        # Getting the original content of moves.ts
        movesSha = getSHA("data/moves.ts")
        movesBlob = serverRepo.get_git_blob(movesSha)
        # Decoding the contents of moves.ts
        movesContents = base64.b64decode(movesBlob.content).decode("utf-8")
        # Updating the contents of moves.ts
        newContent = f"""   {self.name.lower().join()}: {{
        num: {currentNum},
        accuracy: {self.accuracy},
        basePower: {self.bp},
        category: {self.category},
        desc: {self.desc},
        shortDesc: {self.shortDesc},
        name: {self.name},
        pp: {self.pp},
        priority: {self.priority},
        flags: {self.flags},
        secondary: {self.secondary},
        target: {self.target},
        type: {self.type},
        zMove: {self.zMove}
    }}
}};
        """
        movesContents = movesContents.replace("};", newContent)
        # Updating the current number for the next Pokemon
        with open("../currentNum/currentMoveNum.txt", "w") as f: f.write(currentNum+1)

        # Making the Pull Request in the server repository
        title = f"{self.name} - new fake move. Requested by {discordUser}; updated BY BOT."
        body = f"""THIS PULL REQUEST WAS MADE AUTOMATICALLY IN RESPONSE TO A REQUEST TO ADD {self.name} BY {discordUser}.
        """
        # Committing the updates to the moves.ts file
        movesCommit = serverRepo.update_file("data/moves.ts", f"Adding {self.name} as requested by {discordUser}.", movesContents, movesSha, branch="bot-add-move")["commit"]
        # Making the PR
        serverPR = serverRepo.create_pull(title=title, body=body, head="bot-add-move", base="master")
        print(f"New PR made: {serverPR.html_url}")