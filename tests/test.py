import os
import json

def login():
    print("Logging in...")
    os.system("npx mudslide login")

def get_groups():
    print("Retrieving groups...")
    os.system("npx mudslide groups > groups.json")
    with open("groups.json", "r") as file:
        groups = json.load(file)
    return groups

def send_message(group_id, message):
    print(f"Sending message to group ID: {group_id}")
    os.system(f'npx mudslide send "{group_id}" "{message}"')

def main():
    login()

    # Retrieve groups
    groups = get_groups()

    # Search for the group "Kernel Panic"
    target_group = next((group for group in groups if group.get("subject") == "Kernel Panic"), None)

    if target_group:
        print(f'Found group: {target_group["subject"]}')
        group_id = target_group["id"]
        send_message(group_id, "Hello")
    else:
        print("Group 'Kernel Panic' not found!")

if __name__ == "__main__":
    main()
