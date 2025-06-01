import constants

# Question 3 user interaction - the user inputs source and destination stops
# And the system prints the path between these stops
# This is repeated until the user inserts the cancellation token (`cancel`)
def provide_path_for_user(all_paths : dict[str, dict[str, str]]):
    
    print(f"For your convenience, possible stops:\n{sorted(list(all_paths.keys()))}")

    while True:
        source_stop = input(f"Please provide a source stop (insert '{constants.CANCELLATION_KEYWORD}' to exit):  ")
        if (source_stop == constants.CANCELLATION_KEYWORD):
            break
        if (source_stop not in all_paths):
            print(f"No such station: '{source_stop}'")
            continue

        destination_stop = input(f"Please provide a destination stop (insert '{constants.CANCELLATION_KEYWORD}' to exit):  ")
        if (destination_stop == constants.CANCELLATION_KEYWORD):
            break
        if (destination_stop not in all_paths):
            print(f"No such station: '{destination_stop}'")
            continue

        if (destination_stop in all_paths[source_stop]):
            print(f"Path from {source_stop} to {destination_stop} is: {all_paths[source_stop][destination_stop]}")
        else:
            print(f"No path from {source_stop} to {destination_stop}, sorry.")