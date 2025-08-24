Note: Used P4 Template with major changes

# autoHTN.py
- Create methods, actions from data
- Added Heuristic:
    - Only plan to accuse the actual culprit
    - Can't repeatedly search/question the same object

# mystery_elements.py
- define items, states, characters
- randomize the murder weapon, victim, culprit, and motive each time the planner is called
- randomly place items accross characters and searchable objects
- EDITABLE: lines 10-33 can be edited for new characters, motives, murder weapons, and searchable locations

# mystery.txt
- Contains output of autoHTN.py 
- MYSTERY: outlines overall mystery
- CHARACTERS + PERSONALITIES: contains each character's personality, to keep the characters consistent accross playthroughs
- CHARACTERS + MOTIVES: contains each character and the motive for why they may be the killer
- LOCATIONS + OBJECTS: describes where each object can be found (not all objects may be used in the plan)
- PLAN: Outlines plan for solving the mystery 
- Note: red herrings added for increased suspence 

