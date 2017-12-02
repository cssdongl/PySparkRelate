import random


def chose(N, rechoose=False):
    global actually_valid_times
    global right_direction_times
    for i in range(10000):
        directions = list(range(N))
        leave_direction = random.choice(directions)
        first_chose = random.choice(directions)

        temp_directions = directions[:]
        temp_directions.remove(first_chose)

        host_chose = random.choice(temp_directions)

        if host_chose == leave_direction:
            continue

        if first_chose != leave_direction and rechoose:
            directions.remove(first_chose)
            directions.remove(host_chose)
            first_chose = random.choice(directions)
            actually_valid_times = actually_valid_times + 1

            if first_chose == leave_direction:
                right_direction_times = right_direction_times + 1

if __name__ == "__main__":
    price = 1000000
    times = 10000
    N = 4

    actually_valid_times = 0
    right_direction_times = 0

    chose(N)
    print(right_direction_times)
    print(actually_valid_times)
    print(float(right_direction_times) / float(actually_valid_times))

    actually_valid_times = 0
    right_direction_times = 0
    chose(N, True)
    print(right_direction_times)
    print(actually_valid_times)
    print(float(right_direction_times) / float(actually_valid_times))

