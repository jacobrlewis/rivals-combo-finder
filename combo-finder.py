import os

# replay directory
REPLAYS = os.path.expanduser("~") + '/AppData/Local/RivalsofAether/replays'
# REPLAYS = os.path.curdir + '/tmp'

# interval in frames (60 fps)
INTERVAL = 15 * 60

# set to True to edit your replay files and star them to find them easily in-game
ADD_STARS = True

def main():
    stars = []
    for name in os.listdir((REPLAYS)):
        if not name.endswith(".roa"):
            continue

        contents: str = ''
        with open(os.path.join(REPLAYS, name)) as f:
            try:
                lines = f.readlines()
            except UnicodeDecodeError as e: 
                print(f"{name} error while decoding unicode")
                print(e.reason)
                continue

            if len(lines) < 9:
                print(f"{name} missing lines")
                continue

            # read line 9, exclude first (match duration) and last (newline/whitespace)
            nums = lines[8].split(',')[1:-1]

            players = {}

            for i in range(0, len(nums), 2):
                player, death = nums[i], int(nums[i+1])

                # game starts moving after the frame counter starts, so use 120 as starting point
                last_death = players.get(player, 120)
                time_alive = death - last_death

                if time_alive < INTERVAL:
                    stars.append(name)
                    # read contents after first character (star/unstar character)
                    f.seek(1)
                    contents = f.read()
                    break

                players[player] = death

        if ADD_STARS and len(contents) > 0:
            with open(os.path.join(REPLAYS, name), 'w') as w:
                w.write('1' + contents)

    print(stars)
    print(f'{len(stars)} replays starred')

if __name__ == '__main__':
    main()
