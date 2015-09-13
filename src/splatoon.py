#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import web, Workflow, ICON_ERROR
import datetime

ICON_REGULAR = "./regular.png"
ICON_RANKED = "./ranked.png"

def main(wf):
    # Get current maps
    def get_maps():
        try:
            # Get schedule
            response = web.get("http://splatoon.ink/schedule.json")
            if response.status_code == 200:
                # Ensure schedule is ordered correctly
                schedule = sorted(response.json()["schedule"], key=lambda session: session["startTime"])

                # Add map rotations
                for index, session in enumerate(schedule):
                    sessionPrefix = "Current" if index == 0 else datetime.datetime.fromtimestamp(session["startTime"] / 1000).strftime("%I %p").lstrip("0")
                    if session["regular"]: wf.add_item(reduce(lambda m1, m2: m1["nameEN"] + ", " + m2["nameEN"], session["regular"]["maps"]), sessionPrefix + " Turf Maps", valid=False, icon=ICON_REGULAR)
                    if session["ranked"]: wf.add_item(reduce(lambda m1, m2: m1["nameEN"] + ", " + m2["nameEN"], session["ranked"]["maps"]), sessionPrefix + " " + session["ranked"]["rulesEN"] + " Maps", valid=False, icon=ICON_RANKED)
            else:
                wf.add_item("Error getting maps", "Unable to retrieve maps", valid=False, icon=ICON_ERROR)
        except:
            wf.add_item("Error getting maps", "Unable to retrieve maps", valid=False, icon=ICON_ERROR)

    # Perform action type
    type = wf.args[0]
    if type == "maps":
        get_maps()

    # Return results
    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow(
        update_settings={ "github_slug": "flipxfx/alfred-splatoon" },
        help_url="https://github.com/flipxfx/alfred-splatoon#help"
    )
    sys.exit(wf.run(main))
