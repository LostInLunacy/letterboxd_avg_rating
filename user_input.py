from time import sleep 

quit_list = ('q', 'quit', 'exit')
no_list = ('n', 'no', 'cancel')
yes_list = ('y', 'yes')

def yn(inp=None, yes_list=yes_list, no_list=no_list, quit_list=quit_list):
    """ While user's response is not in no/yes list, keeps prompting
    if in yes_list -> True
    elif in no_list -> False. """
    pre_string = "y/n:\n> "
    string = f"{inp} {pre_string}" if inp else pre_string
    while True:
        user_response = input(string)
        if user_response in quit_list:
            print("Exiting program")
            sleep(1)
            quit()
        if user_response in yes_list:
            return True
        elif user_response in no_list:
            return False
        print("Sorry, I didn't understand your response!")