import os
import time
from redditEngine import RedditEngine
import threading
import datetime
import json
import random

global groupName
groupName = "MemeZ"


class WhatsappComm:
    def __init__(self):
        self.groups = None

    def login(self):
        print("Logging in...")
        os.system("npx mudslide@latest login")

    def get_groups(self):
        print("Retrieving groups...")
        os.system("npx mudslide@latest groups > groups.json")
        groups = open("groups.json", "r")
        return groups

    def send_message(self, group_id, image, cap):
        print(f"Sending message to group ID: {group_id}")
        os.system(
            f'npx mudslide@latest send-image --caption {cap} "{group_id}" "{image}"'
        )

    def searchAndRetrieve(self, groupName):
        self.groups = self.get_groups()
        for line in self.groups:
            if groupName in line:
                group_id = (
                    line.split(":")[1]
                    .replace(",", "")
                    .replace('"', "")
                    .replace(" subject", "")
                    .strip()
                )
                print(group_id)
                return group_id
        target_group = next((group_id), None)
        if target_group:
            print(f'Found group: {target_group["subject"]}')
            group_id = target_group["id"]
            return group_id
        else:
            print("Group not found!")
            return None


class MemeEngine:
    def __init__(self):
        self.memeEngine = RedditEngine()
        self.whatsapp = WhatsappComm()
        self.memeSaves = []
        self.latestMemes = ["", "", "", ""]
        self.subredditList = ["memes", "dankmemes", "wholesomememes", "funny"]
        self.refreshReady = False
        self.refreshCount = [0, 0, 0, 0]
        self.refreshThread = threading.Thread(target=self.memeUpdateCheckThread)
        self.sendMemesThread = threading.Thread(target=self.sendMemes)
        self.sentMemes = set()  # Track sent memes
        # time.sleep(2)
        self.refreshThread.start()
        self.sendMemesThread.start()

    def log(self, text):
        print(
            f"[MEMEZ-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {text}"
        )

    def memeUpdateCheckThread(self):
        i = 0
        while True:
            try:
                newMemes = []
                for subreddit in self.subredditList:
                    self.memeEngine.fetch(subreddit)
                    meme = self.memeEngine.getMeme()
                    meme_basename = os.path.basename(meme)
                    if meme_basename not in self.sentMemes:  # Avoid repeating sent memes
                        newMemes.append(meme)
                for i in range(0, len(newMemes)):
                    if newMemes[i] != self.latestMemes[i]:
                        self.log(
                            f"New meme from r/{self.subredditList[i]}!, refresh pending..."
                        )
                        self.refreshCount[i] = 1
                    if sum(self.refreshCount) >= 2:
                        self.log("Refresh Ready !")
                        self.refreshReady = True
                if i == 0:
                    time.sleep(120)
                else:
                    time.sleep(random.randint(60, 200))
                if i == 5000:
                    i = 0
                i += 1
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(2)
                self.log("Retrying...")
    def sendMemes(self):
        whatsappEngine = WhatsappComm()
        while True:
            try:
                if self.refreshReady:
                    self.refreshReady = False
                    self.log(f"Meme Memmory Status : {self.memeSaves}")
                    for i in range(0, len(self.subredditList)):
                        if self.refreshCount[i] == 1:
                            self.memeEngine.fetch(self.subredditList[i])
                            self.log(os.path.basename(self.memeEngine.getMeme()))
                            meme_basename = os.path.basename(self.memeEngine.getMeme())
                            # Check if the meme was already sent
                            if meme_basename in self.sentMemes:
                                self.log("Meme already sent, skipping...")
                                self.latestMemes[i] = "MemeSkip"
                            else:
                                self.latestMemes[i] = self.memeEngine.getMeme()
                                os.system(
                                    f"wget {self.latestMemes[i]}"
                                )  # Download the meme
                                self.sentMemes.add(meme_basename)  # Mark meme as sent

                            self.refreshCount[i] = 0

                    # Send memes
                    for i in range(0, len(self.latestMemes)):
                        if (
                            self.latestMemes[i] != "MemeSkip"
                            and self.latestMemes[i] not in self.memeSaves
                        ):
                            WhatsappComm().send_message(
                                whatsappEngine.searchAndRetrieve(groupName),
                                os.path.basename(self.latestMemes[i]),
                                f"'HELL YEAH, Straight From :r/{self.subredditList[i]}'",
                            )
                            self.log(f"Sent meme: {self.latestMemes[i]}")
                        else:
                            self.log("Meme skipped due to duplication")
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(2)
                self.log("Retrying...")


if __name__ == "__main__":
    whatsappEngine = WhatsappComm()
    os.system("rm *jpeg*")
    while True:
        print("MemeZ Server v0.1")
        input = str(input("Enter command: "))
        if input == "exit":
            break
        elif input == "send":
            memeEngine = MemeEngine()
            memeEngine.sendMemes()
        elif input == "login":
            whatsappEngine.login()
        elif input == "logout":
            os.system("npx mudslide@latest logout")
        elif input == "group":
            groupName = input("Enter group name: ")
