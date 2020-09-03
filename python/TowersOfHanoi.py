def intro():
	print("""
Let's play Towers of Hanoi!!
The rules are as follows:
Pick a starting number of disks (3 is recommended to start).
The objective is to move all the disks
from the left stack to the right stack.
|1|	
|2|	
|3|	
|4|    |GOAL|
 L   M   R
When you pick a stack, you move its topmost disk.
You can choose any stack to move the disk to,
they don't have to be sequential...
The number of the disk indicates the disk size --
you cannot stack a disk that is larger than another on top.
Have fun!
	""")

def generate_stacks():
	stacks = {}
	stacks['L'], stacks['M'], stacks['R'] = [], [], []
	return stacks

def show_stacks(stacks):
	print('\n...Current Stacks...')
	for key in stacks.keys():
		print("{} stack: {}".format(key, stacks[key]))

def valid_choice(curr_choice, stacks, prev_choice=False):
	valid_choices = ['L', 'M', 'R']
	curr_choice = curr_choice.upper()
	if curr_choice not in valid_choices:
		return False
	
	#moving origin
	if not prev_choice:
		if stacks[curr_choice] == []:
			print("That stack is empty")
			return False
		else:
			return True
	#moving destination
	else:
		if not stacks[curr_choice]:
			return True
		elif stacks[curr_choice][-1] < stacks[prev_choice.upper()][-1]:
			print("That disk is larger than it's destination disk")
			return False
		else:
			return True

def options_message(to_from):
	message = """
Choose a stack (L,M,R) to move a disk {}! 
(Press s to show all stacks again, 
i for instructions, q to quit the game): """.format(to_from)
	return message

def alternate_options(choice, stacks):
	valid_options = ['q', 's', 'i', 'l', 'm', 'r']

	if choice.lower() == 'q':
		quit()
	elif choice.lower() == 's':
		show_stacks(stacks)
	elif choice.lower() == 'i':
		intro()
	elif choice.lower() not in valid_options:
		print("That doesn't seems to be a valid choice...")

def victory_condition(stacks):
	if not stacks['L'] and not stacks['M']:
		print("Congratulations!! you won!!")
		return True
	return False

def quit():
	print("See you next time!!")
	raise SystemExit

def game_setup():
	game_stacks = generate_stacks()
	num_disks = 0
	num_disks = int(input('\nHow many disks do you want to play with? (3 minimum): '))
	
	while num_disks < 3:	
		if num_disks < 3:
			print()
			num_disks = input("I'm sorry, please pick more than 3... (enter q to quit): ")
			if num_disks == 'q':
				quit()
			num_disks =  int(num_disks)
	
	for i in reversed(range(1, num_disks+1)):
		game_stacks['L'].append(i)

	num_optimal_moves = (2 ** num_disks) - 1
	print("\nThe fastest you can solve this game is in {} moves... Good luck!\n".format(num_optimal_moves))

	return game_stacks

def gameplay(stacks):
	show_stacks(stacks)
	
	while True:
		first_choice = input(options_message("from"))
		if valid_choice(first_choice, stacks):
			break
		alternate_options(first_choice, stacks)
		
	while True:
		second_choice = input(options_message("to"))
		if valid_choice(second_choice, stacks, prev_choice=first_choice):
			break
		alternate_options(second_choice, stacks)	
	
	stacks[second_choice.upper()].append(stacks[first_choice.upper()].pop())

def play():
	intro()
	stacks = game_setup()
	while True:
		while not victory_condition(stacks):
			gameplay(stacks)
		try_again = input("Would you like to play again? ")
		try_again.lower()
		if try_again == 'y':
			stacks = game_setup()
		elif try_again == 'n':
			quit()
		else:
			print("That doesn't seem to be a valid option (press n to quit)")

if __name__ == '__main__':
	play()
