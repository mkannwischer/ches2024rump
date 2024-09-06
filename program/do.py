#!/usr/bin/env python3
import json

def gettalks(talks):
    objs = []
    for idx, talk in enumerate(talks):
        t = {}
        t['affiliations'] = ""
        t['authors'] = [a.strip() for a in talk[1].split(",")]
        t["id"] = f"talk-{idx}"
        t['title'] = talk[0]
        objs.append(t)
    return objs


def get(talks, start, end, idx, title):
    slot = {}
    slot["starttime"] = start 
    slot["endtime"] = end
    session = {}
    session["id"] = f"rump-session-{idx}"
    session["session_title"] = title
    if talks is not None:
        session["talks"] = gettalks(talks)
    slot["sessions"] = [session]
    return slot



s1 = [
    ("Rump Session Opening", "Matthias Kannwischer, Shivam Bhasin"),
    ("Program Chairs' Report", "Bo-Yin Yang, Francisco Rodriguez"),
    ("General Announcement", "Benedikt Gierlichs"),
    ("Artifact Chair Report & Awards", "Markku-Juhani O. Saarinen"),
    ("CHES Challenge (WhibOx) - Technical Wrap-up and Award", "Aleksei Udovenko")
]

s2 = [
    ("Real Rump Session Opening", "Matthias Kannwischer, Shivam Bhasin"),
    ("Don't hack hardware", "Jasper van Woudenberg"),
    ("tiny simon", "Patrick Schaumont"),
    ("We <3 LEDs", "Marno van der Maas"),
    ("OpenTitan After All (this time)", "Dom Rizzo"),
    ("Side Channel Attacks: Artificial Intelligence Vs Human Intelligence", "Morgane Guerreau"),
    ("Wanted AGAIN: Postdoc(s) and your vote(s)", "Bo-Yin Yang")
]

s3 = [
    ("New Records in Hardware S-Box Gate Count", "Colin O'Flynn"),
    ("Optimist OSE: The Fellowship of the Code", "Dev Manish Mehta, Evan Apinis, Trey Marcantonio"),
    ("Ask your doctor about sec-certs", "Jan Jancar"),
    ("A Game of Visas", "Diego F. Aranha"),
    ("On Non Constant-time Nonces", "Thomas Eisenbarth"),
    ("Hey it's 1999 again", "Markku-Juhani Saarinen, Nicky Mouha"),
    ("PQCrypto 2025", "Ruben Niederhagen"),
    ("EUCLEAK : Story of a Side-Channel Vulnerability", "Victor Lomné"),
    ("Future-proof cryptography", "Antoon Purnal"),
    ("1st Edition of the CASCADE Conference", "Pascal Sasdrich"),
    ("The PhD Student", "Georg Land"),
    ("Rump Session Closing & Awards", "Matthias Kannwischer, Shivam Bhasin")
]

program = {}
program["config"] = {}
program["config"]["default_talk_minutes"] = 4
program["config"]["default_track_locations"] = [{"name" : "Enter a location"}]
program["config"]["timezone"] = {"abbr": "America/Halifax", "name": "America/Halifax", "shortName": "Halifax"}
program["config"]["unassigned_talks"] = [{"id": "category-0", "name": "Uncategorized","talks": []}]
program["config"]["uniqueIDIndex"] = 3329
program["database_id"] = 3329
program["name"] = "CHES 2024 Rump Session"
program["tabbedSessions"]=  False
program["twoSessions"] = False;


day = {}
day["date"] = "2024-09-06"
day["timeslots"] = [
    get(s1, "20:00", "20:45", 1, "Reports & Awards"),
    get(None, "20:45", "21:10", 2, "Break"),
    get(s2, "21:10", "21:40", 3, "Let's get serious"),
    get(None, "21:40", "22:00", 4, "Break"),
    get(s3, "22:00", "22:45", 5, "Let's get more serious")
] 

program["days"] = [day]

with open('rump.json', 'w', encoding ='utf8') as json_file:
    json.dump(program, json_file)