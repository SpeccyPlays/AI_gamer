import json
from collections import Counter

with open("saved_actions/2026-09-2714_56_46save.json", "r") as f:
    data = json.load(f)

actions = Counter(item["action"] for item in data)

print("Total frames:", len(data))
print()

for action, count in actions.items():
    print(f"{action}: {count}")