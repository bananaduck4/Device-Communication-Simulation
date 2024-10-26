from pathlib import Path
from Device_Manager import  DEVICE_MANAGER

def _read_input_file_path() -> list | None:
    """Reads the input file path from the standard input"""
    try:
        file = Path(input())
        file = open(file)
        data = file.readlines()
        file.close()

    except FileNotFoundError:
        print('FILE NOT FOUND')
        return

    else:
        # Get all the rules of the simulations
        data = [i.rstrip('\n') for i in data if i != '\n' and i[0] != '#']
        # Sort the information based on device number and putting the length last
        data.sort(key = lambda x: x.split()[0])  # sort alphabetically
        data.sort(key = lambda x: x.startswith('LENGTH'))  # put length last
        return data

def main() -> None:
    """Runs the simulation program in its entirety"""
    rules = _read_input_file_path()

    if rules:
        sim = DEVICE_MANAGER(rules)
        sim.run() #Run the sims

if __name__ == '__main__':
    main()
