import os
import time
import threading
import datetime
import random
import asyncio
import json
from redditEngine import RedditEngine

# Global variable for group name
global groupName
groupName = "MemeZ"


class WhatsappComm:
    def __init__(self):
        self.groups = None

    async def login(self):
        print("Logging in...")
        os.system("npx mudslide@latest login")

    async def get_groups(self):
        print("Retrieving groups...")
        os.system("npx mudslide@latest groups > groups.json")
        groups = open("groups.json", "r")
        return groups

    async def send_message(self, group_id, image, cap):
        print(f"Sending message to group ID: {group_id}")
        os.system(f'npx mudslide@latest send-image --caption {cap} "{group_id}" "{image}"')

    async def searchAndRetrieve(self, groupName):
        self.groups = await self.get_groups()
        for line in self.groups:
            if groupName in line:
                group_id = line.split(":")[1].replace(",", "").replace('"', "").replace(" subject", "").strip()
                print(group_id)
                return group_id
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
        self.sentMemes = set()  # Track sent memes
        self.refreshThread = threading.Thread(target=self.memeUpdateCheckThread)
        self.sendMemesThread = threading.Thread(target=self.sendMemes)
        self.refreshThread.start()
        self.sendMemesThread.start()

    def log(self, text):
        print(f"[MEMEZ-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {text}")

    def memeUpdateCheckThread(self):
        t = 0
        while True:
            try:
                if t == 500:
                    t = 0
                newMemes = []
                for subreddit in self.subredditList:
                    self.memeEngine.fetch(subreddit)
                    meme = self.memeEngine.getMeme()
                    meme_basename = os.path.basename(meme)
                    if meme_basename not in self.sentMemes:  # Avoid repeating sent memes
                        newMemes.append(meme)
                for i in range(len(newMemes)):
                    if newMemes[i] != self.latestMemes[i]:
                        self.log(f"New meme from r/{self.subredditList[i]}!, refresh pending...")
                        self.refreshCount[i] = 1
                    if sum(self.refreshCount) >= 2:
                        self.log("Refresh Ready!")
                        self.refreshReady = True

                time.sleep(1800)  # Increased sleep time for reduced frequency
                if t == 100:
                    os.system("rm *jpeg*")
                t+= 1
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(10)
                self.log("Retrying...")

    async def sendMemes(self):
        whatsappEngine = WhatsappComm()
        while True:
            try:
                if self.refreshReady:
                    self.refreshReady = False
                    self.log(f"Meme Memory Status: {self.memeSaves}")
                    for i in range(len(self.subredditList)):
                        if self.refreshCount[i] == 1:
                            self.memeEngine.fetch(self.subredditList[i])
                            meme_basename = os.path.basename(self.memeEngine.getMeme())
                            # Check if meme is already sent
                            if meme_basename in self.sentMemes:
                                self.log("Meme already sent, skipping...")
                                self.latestMemes[i] = "MemeSkip"
                            else:
                                self.latestMemes[i] = self.memeEngine.getMeme()
                                os.system(f"wget {self.latestMemes[i]} -O {meme_basename}")  # Save image to disk
                                self.sentMemes.add(meme_basename)

                            self.refreshCount[i] = 0

                    # Send memes if not skipped
                    for i in range(len(self.latestMemes)):
                        if self.latestMemes[i] != "MemeSkip" and self.latestMemes[i] not in self.memeSaves:
                            await self.whatsapp.send_message(
                                await self.whatsapp.searchAndRetrieve(groupName),
                                os.path.basename(self.latestMemes[i]),
                                f"'HELL YEAH, Straight From :r/{self.subredditList[i]}'"
                            )
                            self.log(f"Sent meme: {self.latestMemes[i]}")
                        else:
                            self.log("Meme skipped due to duplication")
                await asyncio.sleep(500)  # Sleep for a short time between checks
            except Exception as e:
                self.log(f"Error: {e}")
                await asyncio.sleep(2)
                self.log("Retrying...")

# Main entry point
async def main():
    whatsappEngine = WhatsappComm()
    os.system("rm *jpeg*")
    while True:
        print("MemeZ Server v0.1")
        user_input = str(input("Enter command: "))
        if user_input == "exit":
            break
        elif user_input == "send":
            memeEngine = MemeEngine()
            await memeEngine.sendMemes()
        elif user_input == "login":
            await whatsappEngine.login()
        elif user_input == "logout":
            os.system("npx mudslide@latest logout")
        elif user_input == "group":
            groupName = input("Enter group name: ")

# Run the program
if __name__ == "__main__":
    asyncio.run(main())
