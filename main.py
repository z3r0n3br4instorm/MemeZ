import os
import streamlit as st
from redditEngine import RedditEngine
import threading
import time

# class WhatsappComm:
#     def __init__(self):
#         self.groups = None

#     def login(self):
#         print("Logging in...")
#         os.system("npx mudslide login")

#     def get_groups(self):
#         print("Retrieving groups...")
#         os.system("npx mudslide groups > groups.json")
#         with open("groups.json", "r") as file:
#             groups = json.load(file)
#         return groups

#     def send_message(self, group_id, message):
#         print(f"Sending message to group ID: {group_id}")
#         os.system(f'npx mudslide send "{group_id}" "{message}"')

#     def searchAndRetrieve(self, groupName):
#         self.login()
#         self.groups = self.get_groups()
#         target_group = next((group for group in self.groups if group.get("subject") == groupName), None)
#         if target_group:
#             print(f'Found group: {target_group["subject"]}')
#             group_id = target_group["id"]
#             return group_id
#         else :
#             print("Group not found!")
#             return None


class Interface:
    def __init__(self):
        st.empty()
        self.memeEngine = RedditEngine()
        # self.whatsapp = WhatsappComm()
        if "memeSaves" not in st.session_state:
            st.session_state.memeSaves = []
        if "latestMemes" not in st.session_state:
            st.session_state.latestMemes = []
        if "subredditList" not in st.session_state:
            st.session_state.subredditList = []
            st.session_state.subredditList = [
                "memes",
                "dankmemes",
                "wholesomememes",
                "funny",
            ]
        if "refreshReady" not in st.session_state:
            st.session_state.refreshReady = False
        if "refreshCount" not in st.session_state:
            st.session_state.refreshCount = [0, 0, 0, 0]
        if "refreshThread" not in st.session_state:
            st.session_state.refreshThread = threading.Thread(
                target=self.memeUpdateCheckThread
            )
            time.sleep(2)
            st.session_state.refreshThread.start()

    def memeUpdateCheckThread(self):
        while True:
            newMemes = []
            for subreddit in st.session_state.subredditList:
                self.memeEngine.fetch(subreddit)
                meme = self.memeEngine.getMeme()
                if meme not in st.session_state.memeSaves:
                    newMemes.append(meme)
            for i in len(newMemes):
                if newMemes[i] != st.session_state.latestMemes[i]:
                    st.toast(
                        f"New meme from r/{st.session_state.subredditList[i]}!, refresh pending..."
                    )
                    st.session_state.refreshCount[i] = 1
                if sum(st.session_state.refreshCount) == 4:
                    st.session_state.refreshReady = True
            time.sleep(60)

    def main(self):
        # The Meme Squad - Always Bringing the Heat!
        st.title("MemeZ: Your Daily Meme Drop")
        st.subheader("Every minute, a new meme. Get ready to laugh!")

        while st.session_state.refreshReady:
            with st.spinner("MemeZ Online..."):
                for subreddit in st.session_state.subredditList:
                    st.markdown(f"> **Latest Meme from r/{subreddit}**")
                    self.memeEngine.fetch(f"{subreddit}")
                    meme = self.memeEngine.getMeme()
                    st.session_state.latestMemes.append(meme)
                    print(st.session_state.memeSaves, meme)
                    if meme in st.session_state.memeSaves:
                        meme = None
                        st.info("Duplicate meme detected, skipping...")
                    if meme:
                        # Show the meme, with some style
                        st.image(
                            meme,
                            caption=f"Straight from r/{subreddit}, no cap",
                            use_container_width=True,
                        )
                        st.markdown("Catch this vibe, it's top-tier content!")
                        st.session_state.memeSaves.append(meme)
                    else:
                        st.markdown(
                            "No memes? Nah, just wait for the next round. We gotchu."
                        )
            time.sleep(10)
            st.rerun()


if __name__ == "__main__":
    Interface().main()
