
import math
import random as rand

culprit = None
victim = None
murder_weapon = None
motive = None

data = {
 "Items": [
   "key",
   "password",
   "screwdriver",
   "evidence",
   "red_herring"
 ],
 "States": [
   "desk_unlocked",
   "safe_unlocked",
   "fireplace_unlocked",
   "steven_questioned",
   "conrad_questioned",
   "jeremiah_questioned",
   "taylor_questioned",
   "belly_questioned"
 ],
 "Murder Weapons":[
   "knife",
   "poison",
   "fire_poker",
   "broken_bottle",
   "pushed_down_stairs",
   "drowning",
   "jeremiah's blue eyed stare"
 ],
  "Characters": {
   "Steven": {
    "Motive": None,
    "Personality": "Unserious"
   },
   "Conrad": {
     "Motive": None,
     "Personality": "Caring"
   },
   "Jeremiah": {
     "Motive": None,
     "Personality": "Selfish"
   },
   "Taylor": {
     "Motive": None,
     "Personality": "Headstrong"
   },
   "Belly": {
     "Motive": None,
     "Personality": "Naive"
   }
  },
 "Initial": {
   "Culprit": culprit,
   "Victim": victim,
   "Motive": motive,
   "Murder Weapon": murder_weapon
 },
 "Goal": {
  "mystery_solved": 1
 },
 "Recipes": {
   "accuse Belly for mystery solved": {
     "Produces": {
       "mystery solved": 1
     },
     "Requires": {
       "culprit": "Belly",
       "evidence": 3
     }
   },
   "accuse Jeremiah for mystery solved": {
     "Produces": {
       "mystery solved": 1
     },
     "Requires": {
       "culprit": "Jeremiah",
       "evidence": 2
     }
   },
   "accuse Conrad for mystery solved": {
     "Produces": {
       "mystery solved": 1
     },
     "Requires": {
       "culprit": "Conrad",
       "evidence": 2
     }
   },
   "accuse Steven for mystery solved": {
     "Produces": {
       "mystery solved": 1
     },
     "Requires": {
       "culprit": "Steven",
       "evidence": 2
     }
   },
   "accuse Taylor for mystery solved": {
     "Produces": {
       "mystery solved": 1
     },
     "Requires": {
       "culprit": "Taylor",
       "evidence": 2
     }
   },
 }
}

def randomize():
    global culprit, victim, murder_weapon, motive
    characters = list(data["Characters"].keys())
    culprit = rand.choice(characters)
    
    # Ensure victim is different from culprit
    possible_victims = [c for c in characters if c != culprit]
    victim = rand.choice(possible_victims)
    
    murder_weapon = rand.choice(data["Murder Weapons"])
    
    # Update the Initial dictionary
    data["Initial"]["Culprit"] = culprit
    data["Initial"]["Victim"] = victim
    data["Initial"]["Murder Weapon"] = murder_weapon
    
    randomize_motives()

def randomize_motives():
    motives = {
        "Steven": [
            "accidental_prank_gone_wrong",
            "drunken_mistake",
            "jealousy_over_friendship",
            "protecting_another_secret"
        ],
        "Conrad": [
            "protecting_someone",
            "mercy_killing",
            "guilt_over_past_action",
            "temporary_rage"
        ],
        "Jeremiah": [
            "inheritance_money",
            "status_power",
            "jealousy_in_relationship",
            "covering_up_scandal"
        ],
        "Taylor": [
            "revenge_for_betrayal",
            "defending_reputation",
            "extreme_competitiveness",
            "blackmail_gone_wrong"
        ],
        "Belly": [
            "manipulated_into_it",
            "mistaken_identity",
            "false_confession",
            "unrequited_love_turned_deadly"
        ]
    }
    
    # Assign random motive to each character
    for character in data["Characters"]:
        if character in motives:
            data["Characters"][character]["Motive"] = rand.choice(motives[character])
    
    # Special case: Assign the actual culprit's motive to the mystery
    global culprit, motive
    if culprit in data["Characters"]:
        motive = data["Characters"][culprit]["Motive"]
        data["Initial"]["Motive"] = motive  # Update the global data

def randomize():
    global culprit, victim, murder_weapon, motive
    characters = list(data["Characters"].keys())
    culprit = rand.choice(characters)
    
    # Ensure victim is different from culprit
    possible_victims = [c for c in characters if c != culprit]
    victim = rand.choice(possible_victims)
    
    murder_weapon = rand.choice(data["Murder Weapons"])
    
    # Update the Initial dictionary
    data["Initial"]["Culprit"] = culprit
    data["Initial"]["Victim"] = victim
    data["Initial"]["Murder Weapon"] = murder_weapon
    
    # Assign motives after culprit is chosen
    randomize_motives()

def print_mystery():
    print(data["Initial"])

def get_data():
    randomize()
    return data