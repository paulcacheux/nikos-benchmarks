import sys
from pathlib import Path
from dataclasses import dataclass

root = Path(sys.argv[1])


@dataclass
class Entry:
    ref: str
    stats: list[(str, str)]


entries = []
for name in root.glob("**/output.txt"):
    inserting = False
    entry = Entry(ref="", stats=[])
    with open(name) as output:
        for index, line in enumerate(output):
            line = line.strip()
            if index == 0:
                entry.ref = line

            if line.startswith("Command being timed"):
                inserting = True
                continue

            if not inserting:
                continue

            [before, after] = line.rsplit(": ", maxsplit=1)
            entry.stats.append((before, after))
    entries.append(entry)

print("|" + " | ".join(["Stat"] + [entry.ref for entry in entries]) + "|")
print("|" + "|".join(["-"] * (len(entries) + 1)) + "|")
for i in range(len(entries[0].stats)):
    print(
        "| "
        + " | ".join(
            [entries[0].stats[i][0]] + [entry.stats[i][1] for entry in entries]
        )
        + " |"
    )
