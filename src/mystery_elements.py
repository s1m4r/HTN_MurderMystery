
import math
import random as rand

culprit = None
victim = None
murder_weapon = None
motive = None

# ------ DEFINE THE CHARACTERS AND THEIR PERSONALITIES ------
#   You can change the Characters names, but make sure to update it in Personalities and Motives as well
#   Note: if adding new personality  --> go to randomize_motives() to add possible motives for each new personality
# ------------------------------------------------------------
Characters = ["Steven", "Conrad", "Jeremiah", "Taylor", "Belly"]
Motives = {"Steven": None, "Conrad": None, "Jeremiah": None, "Taylor": None, "Belly": None}
Personalities = {"Steven": "Unserious", "Conrad": "Caring", "Jeremiah": "Selfish", "Taylor": "Headstrong", "Belly": "Naive"}

# ------ DEFINE THE OBJECTS AND LOCATIONS ------
#   You can change the Searchable_Locations names, but make sure to update it in Required_Unlocker as well
#   ALWAYS KEEP 3 EVIDENCE & ONE RED HERRING
#   make sure number of objects to hide matches the number of characters to question + number of locations to search
# ------------------------------------------------
Searchable_Locations = ["desk", "safe", "fireplace"]
Required_Unlocker = {"desk": "key", "safe": "password", "fireplace": "screwdriver"}
objects_to_hide = ["key", "password", "screwdriver", "evidence", "evidence", "evidence", "red_herring", "red_herring"]

# -------- POSSIBLE MURDER WEAPONS --------
#   Add/Remove murder weapons if needed
# -----------------------------------------
Murder_Weapons = ["knife", "poison", "golf_cart", "heartbreak", "pushed_down_stairs", "drowning"]

# WORLD STATE KEEPS TRACK OF WHERE EACH OBJECT IS HIDDEN
World_State = {"Steven": None, "Conrad": None, "Jeremiah": None, "Taylor": None, "Belly": None, "desk": None, "safe": None, "fireplace": None}

data = {
 "Items": [
   "evidence",
   "red_herring"
 ],
 "States": [
   "mystery_solved",
   "Culprit",
   "Victim",
   "Motive",
   "Murder Weapon"
 ],
 "Initial": {
   "Culprit": culprit,
   "Victim": victim,
   "Motive": motive,
   "Murder Weapon": murder_weapon
 },
 "Goal": {
   "red_herring": 1,
  "mystery_solved": 1
 },
 "Recipes": { 
    # ACCUSE CHARACTERS
    # QUESTION CHARACTERS
    # UNLOCK OBJECTS
    # SEARCH OBJECTS FOR EVIDENCE
    
    # implemented automatucally in functions defined below
 }
}

def create_search_recipe(location): 
    data["States"].append(f"{location}_searched")
    while True:
      found_item = rand.choice(objects_to_hide)
      if (found_item != Required_Unlocker[location] or len(objects_to_hide) == 1):
        break

    objects_to_hide.remove(found_item)
    World_State[location] = found_item
    return [{
        "Produces": {
            found_item: 1,
            f"{location}_searched": 1
        },
        "Requires": {
            f"{location}_unlocked": 1
        }
    }, found_item]

def update_search_recipes():
    for location in Searchable_Locations:
        recipe = create_search_recipe(location)
        recipe_name = f"search {location} for {recipe[1]}"
        data["Recipes"][recipe_name] = recipe[0]

def create_unlock_recipe(location):
    data["States"].append(f"{location}_unlocked")
    
    required_item = Required_Unlocker[location]
    data["Items"].append(required_item)
    
    return {
        "Produces": {
            f"{location}_unlocked": 1
        },
        "Requires": {
            required_item: 1
        },
        "Consumes": {
            required_item: 1
        }
    }

def update_unlock_recipes():
    for location in Searchable_Locations:
        recipe_name = f"unlock {location} for search {location}"
        data["Recipes"][recipe_name] = create_unlock_recipe(location)

def create_question_recipe(character):
    data["States"].append(f"{character.lower()}_questioned")
    found_item = rand.choice(objects_to_hide)
    objects_to_hide.remove(found_item)
    World_State[character] = found_item
    return [{
        "Produces": {
            found_item: 1,
            f"{character.lower()}_questioned": 1
        },
        "Requires": {
            f"{character.lower()}_questioned": 0
        }
    }, found_item]

def update_question_recipes():
    for character in Characters:
      if character != victim:
        recipe = create_question_recipe(character)
        recipe_name = f"question {character} for {recipe[1]}"
        data["Recipes"][recipe_name] = recipe[0]

def create_accuse_recipe(character):
    return {
        "Produces": {
            "mystery_solved": 1
        },
        "Requires": {
            "Culprit": character,
            "evidence": 3
        }
    }

def update_accuse_recipes():
    for character in Characters:
      if character != victim:
        recipe_name = f"accuse {character} for mystery solved"
        data["Recipes"][recipe_name] = create_accuse_recipe(character)

def randomize_motives():
    motives = {
        "Unserious": ["accidental_prank_gone_wrong", "drunken_mistake", "jealousy_over_friendship", "protecting_another_secret"],
        "Caring": ["protecting_someone", "mercy_killing", "guilt_over_past_action", "temporary_rage"],
        "Selfish": ["inheritance_money", "status_power", "jealousy_in_relationship", "covering_up_scandal"],
        "Headstrong": ["revenge_for_betrayal", "defending_reputation", "extreme_competitiveness", "blackmail_gone_wrong"],
        "Naive": ["manipulated_into_it", "mistaken_identity", "false_confession", "unrequited_love_turned_deadly"]
    }
    
    for character in Characters:
        possible_motives = motives[Personalities[character]]
        Motives[character] = rand.choice(possible_motives)
    
    global culprit, motive
    motive = Motives[culprit]
    data["Initial"]["Motive"] = motive

def randomize():
    global culprit, victim, murder_weapon, motive
    culprit = rand.choice(Characters)
    victim = rand.choice([c for c in Characters if c != culprit])    
    murder_weapon = rand.choice(Murder_Weapons)
    
    data["Initial"].update({
        "Culprit": culprit,
        "Victim": victim,
        "Murder Weapon": murder_weapon
    })
    
    # data["Recipes"].pop(f"question {victim} for evidence")
    # data["Recipes"].pop(f"accuse {victim} for mystery solved")
    
    randomize_motives()
    

def print_mystery():
    print("Current Mystery:")
    print(data["Initial"])

def get_data():
    update_accuse_recipes()
    update_question_recipes()
    update_unlock_recipes()
    update_search_recipes()
    randomize()
    return data