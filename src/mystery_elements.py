
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
   "mystery_solved",
   "desk_unlocked",
   "safe_unlocked",
   "fireplace_unlocked",
   "desk_searched",
   "safe_searched",
   "fireplace_searched",
   "steven_questioned",
   "conrad_questioned",
   "jeremiah_questioned",
   "taylor_questioned",
   "belly_questioned",
   "Culprit",
   "Victim",
   "Motive",
   "Murder Weapon"
 ],
 "Murder Weapons":[
   "knife",
   "poison",
   "golf_cart",
   "broken_bottle",
   "pushed_down_stairs",
   "drowning"
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
   # ACCUSE TO SOLVE
   "accuse Belly for mystery solved": {
     "Produces": {
       "mystery_solved": 1
     },
     "Requires": {
       "Culprit": "Belly",
       "evidence": 3
     }
   },
   "accuse Jeremiah for mystery solved": {
     "Produces": {
       "mystery_solved": 1
     },
     "Requires": {
       "Culprit": "Jeremiah",
       "evidence": 2
     }
   },
   "accuse Conrad for mystery solved": {
     "Produces": {
       "mystery_solved": 1
     },
     "Requires": {
       "Culprit": "Conrad",
       "evidence": 2
     }
   },
   "accuse Steven for mystery solved": {
     "Produces": {
       "mystery_solved": 1
     },
     "Requires": {
       "Culprit": "Steven",
       "evidence": 2
     }
   },
   "accuse Taylor for mystery solved": {
     "Produces": {
       "mystery_solved": 1
     },
     "Requires": {
       "Culprit": "Taylor",
       "evidence": 2
     }
   }, # SEARCH FOR EVIDENCE
   "search desk for evidence": {
      "Produces": {
        "evidence": 1,
        "desk_searched": 1
        
      },
      "Requires": {
        "desk_unlocked": 1,
      }
    },
   "search safe for evidence": {
      "Produces": {
        "evidence": 1,
        "safe_searched": 1    
      },
      "Requires": {
        "safe_unlocked": 1,
      }
    },
    "search fireplace for evidence": {
        "Produces": {
          "evidence": 1,
          "fireplace_searched": 1
          
        },
        "Requires": {
          "fireplace_unlocked": 1
        }
      }, # QUESTION CHARACTERS
    "question Steven for evidence": {
      "Produces": {
        "password": 1,
        "steven_questioned": 1
        
      },
      "Requires": {
        "steven_questioned": 0
      }
    },
    "question Conrad for evidence": {
      "Produces": {
        "key": 1,
        "conrad_questioned": 1
        
      },
      "Requires": {
         "conrad_questioned": 0

      }
    },
    "question Jeremiah for evidence": {
      "Produces": {
        "screwdriver": 1,
        "jeremiah_questioned": 1
      },
      "Requires": {
         "jeremiah_questioned": 0
      }
    },
    "question Taylor for evidence": {
      "Produces": {
        "taylor_questioned": 1
        
      },
      "Requires": {
        "taylor_questioned": 0
      }
    },
    "question Belly for evidence": {
      "Produces": {
        "belly_questioned": 1
        
      },
      "Requires": {
        "belly_questioned": 0
      }
    }, # UNLOCK ITEMS
    "unlock desk for search desk": {
      "Produces": {
        "desk_unlocked": 1
      },
      "Requires": {
        "key": 1,
      },
      "Consumes": {
        "key": 1
      }
    },
    "unlock safe for search safe": {
      "Produces": {
        "safe_unlocked": 1
      },
      "Requires": {
        "password": 1,
      },
      "Consumes": {
        "password": 1
      }
    },
    "unlock fireplace for search fireplace": {
      "Produces": {
        "fireplace_unlocked": 1
      },
      "Requires": {
        "screwdriver": 1
      },
      "Consumes": {
        "screwdriver": 1
      }
    }
 }
}

def randomize_motives():
    motives = {
        "Steven": ["accidental_prank_gone_wrong", "drunken_mistake", "jealousy_over_friendship", "protecting_another_secret"],
        "Conrad": ["protecting_someone", "mercy_killing", "guilt_over_past_action", "temporary_rage"],
        "Jeremiah": ["inheritance_money", "status_power", "jealousy_in_relationship", "covering_up_scandal"],
        "Taylor": ["revenge_for_betrayal", "defending_reputation", "extreme_competitiveness", "blackmail_gone_wrong"],
        "Belly": ["manipulated_into_it", "mistaken_identity", "false_confession", "unrequited_love_turned_deadly"]
    }
    
    for character in data["Characters"]:
        if character in motives:
            data["Characters"][character]["Motive"] = rand.choice(motives[character])
    
    global culprit, motive
    if culprit in data["Characters"]:
        motive = data["Characters"][culprit]["Motive"]
        data["Initial"]["Motive"] = motive



def randomize():
    global culprit, victim, murder_weapon, motive
    characters = list(data["Characters"].keys())
    culprit = rand.choice(characters)
    victim = rand.choice([c for c in characters if c != culprit])    
    murder_weapon = rand.choice(data["Murder Weapons"])
    
    data["Initial"].update({
        "Culprit": culprit,
        "Victim": victim,
        "Murder Weapon": murder_weapon
    })
    
    data["Recipes"].pop(f"question {victim} for evidence")
    data["Recipes"].pop(f"accuse {victim} for mystery solved")
    
    randomize_motives()

def print_mystery():
    print("Current Mystery:")
    print(data["Initial"])
    # print(f"Victim: {data['Initial']['Victim']}")
    # print(f"Murder Weapon: {data['Initial']['Murder Weapon']}")
    # possible_culprits = list(data['Characters'].keys())
    # possible_culprits.remove(victim)
    # print(f"Possible Culprits: {possible_culprits} ({culprit})")
    # print(f"Required Evidence: {2 if data['Initial']['Culprit'] != 'Belly' else 3}")

def get_data():
    randomize()
    return data