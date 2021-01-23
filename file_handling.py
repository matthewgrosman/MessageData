import json
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup


def get_facebook_messages() -> (dict, str):
    name = input("Enter the name of the person/conversation: ")

    try:
        filepath = Path(f"/Users/matthew/Documents/Message Data/{name}")
        conversation = defaultdict(list)
        for item in list(filepath.iterdir()):
            if item.is_file() and item.suffix == ".json":
                with open(item, "r") as f:
                    new_json = json.load(f)
                    if conversation == {}:
                        conversation = new_json
                    else:
                        conversation['messages'] += new_json["messages"]
        return conversation, name

    except FileNotFoundError:
        return {"messages": []}, name


def get_imessage(name: str) -> BeautifulSoup:
    try:
        filepath = Path(f"/Users/matthew/Documents/Message Data/{name}/{name}.html")
        return BeautifulSoup(open(filepath), 'html.parser')

    except FileNotFoundError:
        return BeautifulSoup()
