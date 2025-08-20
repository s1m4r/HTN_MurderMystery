import pyhop
import json
import mystery_elements

def check_enough (state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough (state, ID, item, num):
	return [('produce', ID, item), ('have_enough', ID, item, num)]

pyhop.declare_methods ('have_enough', check_enough, produce_enough)

def produce (state, ID, item):
	return [('produce_{}'.format(item), ID)]

pyhop.declare_methods ('produce', produce)

def make_method (name, rule):
	def method (state, ID):
		# --------------- your code here ---------------
		tasks = []
  
		if 'Consumes' in rule.keys():
			for consumed, amount in rule['Consumes'].items():
				tasks.append(('have_enough', ID, consumed, amount))

		if 'Requires' in rule.keys():
			for requirement, amount in rule['Requires'].items():
				tasks.append(('have_enough', ID, requirement, amount))
	
		op_name = 'op_{}'.format(name.replace(' ', '_'))
		tasks.append((op_name, ID))

		return tasks
		# ----------------------------------------------

	return method

def declare_methods (data):
	# some recipes are faster than others for the same product even though they might require extra tools
	# sort the recipes so that faster recipes go first

	# --------------- your code here ---------------
	# hint: call make_method, then declare the method to pyhop using pyhop.declare_methods('foo', m1, m2, ..., mk)
	recipes = data['Recipes']
	methods = {}
	for action, rules in recipes.items():
		product_name = list(rules['Produces'].keys())[0] # i.e. 'wood'

		method_name = 'produce_{}'.format(product_name) # i.e. 'produce_wood'

		if product_name not in methods:
			methods[product_name] = []
		
		new_method = make_method(action, rules)
		new_method.__name__ = action.replace(' ', '_')
		methods[product_name].append((action, new_method)) # i.e. ('produce_wood' :('punch_for_wood', method), ('axe_for_wood', method)))
	
	for item_name, method_list in methods.items(): # i.e. item_name = 'produce_wood', method_list = [('punch_for_wood', method), ('axe_for_wood', method)]
	# 	if len(method_list) > 1:
	# 		# sort by time, ascending
	# 		method_list.sort(key=lambda x: recipes[x[0]]['Time'], reverse=False)

		pyhop.declare_methods('produce_{}'.format(item_name), *[m for _, m in method_list])
	# ------------------------------------------------
	return
				

def make_operator (rule):
	def operator (state, ID):
		# --------------- your code here ---------------
		# CHECK if the operator can be applied
		if 'Requires' in rule.keys():  # REQUIREMENTS CHECK
			for item,amount in rule['Requires'].items():
				if getattr(state, item)[ID] < amount:
					print(f"Not enough {item} to apply operator.")
					return False
		if 'Consumes' in rule.keys():
			for item, amount in rule['Consumes'].items(): # CONSUMES CHECK
				if getattr(state, item)[ID] < amount:
					print(f"Not enough {item} to apply operator.")
					return False
	
		# APPLY the operator
		if 'Produces' in rule.keys(): # PRODUCE ITEMS
			for item, amount in rule['Produces'].items():
				getattr(state, item)[ID] += amount
		if 'Consumes' in rule.keys(): # CONSUME ITEMS
			for item, amount in rule['Consumes'].items():
				getattr(state, item)[ID] -= amount

		return state
		# ----------------------------------------------
	return operator

def declare_operators (data):
	# your code here
	# hint: call make_operator, then declare the operator to pyhop using pyhop.declare_operators(o1, o2, ..., ok)
	for name, rule in data['Recipes'].items():
		operator = make_operator(rule)
		operator.__name__ = 'op_{}'.format(name.replace(' ', '_'))
		pyhop.declare_operators(operator)
	return

def add_heuristic(data, ID):
    
    def heuristic1(state, curr_task, tasks, plan, depth, calling_stack):
        if curr_task[0] == 'have_enough':
            item = curr_task[2]
            num_needed = curr_task[3]
            current_amount = getattr(state, item)[ID]
            if item == 'Culprit':
                if num_needed != mystery_elements.culprit:
                    print(f"Error: Culprit is {mystery_elements.culprit}, not {num_needed}.")
                    return True
        
        return False
    
    def heuristic2(state, curr_task, tasks, plan, depth, calling_stack):
    # Check if current task is a search action
        print(f"Current task: {curr_task}")
        if isinstance(curr_task, tuple) and curr_task[0].startswith('have_enough'):
            print(f"Checking search action: {curr_task[0]}")
            search_action = curr_task[2]
            
            # Extract location from action name (e.g., "safe" from "op_search_safe_for_evidence")
            location = search_action.split('_')[0]  # Gets 'safe' from 'op_search_safe_for_evidence'

            # Check if this location has already been searched
            searched_state = f"{location}_searched"
            if hasattr(state, searched_state) and getattr(state, searched_state).get('agent', 0) >= 1:
                # Location already searched - prune this branch
                return True  # Return True to indicate this path should be pruned

 
        
        return False  # Don't prune this path
    


        
              
    def heuristic3(state, curr_task, tasks, plan, depth, calling_stack):

        return False


    pyhop.add_check(heuristic1)
    pyhop.add_check(heuristic2)
    pyhop.add_check(heuristic3)

def set_up_state (data, ID):
	state = pyhop.State('state')

	for item in data['Items']:
		setattr(state, item, {ID: 0})

	for item in data['States']:
		setattr(state, item, {ID: 0})

	for item, num in data['Initial'].items():
		setattr(state, item, {ID: num})

	return state

def set_up_goals (data, ID):
	goals = []
	for item, num in data['Goal'].items():
		goals.append(('have_enough', ID, item, num))

	return goals

if __name__ == '__main__':
	# rules_filename = 'crafting.json'

	# with open(rules_filename) as f:
	# 	data = json.load(f)

	data = mystery_elements.get_data()
	mystery_elements.print_mystery()

	state = set_up_state(data, 'agent') # allot time here
	goals = set_up_goals(data, 'agent')

	declare_operators(data)
	declare_methods(data)
	add_heuristic(data, 'agent')

	pyhop.print_operators()
	pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long
 
	pyhop.pyhop(state, goals, verbose=3)
 
	# pyhop.pyhop(state, [('have_enough', 'agent', 'wood', 12)], verbose=3)
	# pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)