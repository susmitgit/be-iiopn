from itertools import cycle


# Helpers
# Transform From date - to date into comma seperated days in a cyclic order
def from_to_day_gen(from_day, to_day):
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    pool = cycle(days)
    start = None
    ret_days = []
    for dy in pool:
        if dy == from_day:
            start = True
        if dy == to_day and start:
            start = None
            ret_days.append(dy)
            break
        if start:
            ret_days.append(dy)
    return ', '.join(ret_days)


# Generate all possible combinations of From-To days
def generate_combination():
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    ends_with = days[-1]
    chain_days = days
    combinations = {}
    from_day = chain_days[0]

    while ends_with != from_day:
        from_day = chain_days[0]
        for index, day in enumerate(chain_days):
            if from_day != day:
                combinations = {**combinations, **{f'{from_day} - {day}': from_to_day_gen(from_day, day)}}
        chain_days.append(chain_days.pop(0))
    return combinations


def main():

    # Main
    raw_file = 'hours_actual.csv'
    transform_file = 'transformed_hours.csv'
    transformed_business = {}

    # exclusive Patterns map for transformation
    transform_extrafields = {'tues': 'tue', 'weds': 'wed', 'thurs': 'thu'}

    # Open raw file context
    with open(raw_file, 'r') as f:
        for line in f:
            # Identify Business name and Business schedule segment
            business_name = line.split('","')[0]
            business_time = line.split('","')[1]

            # Modifying the exclusive patterns in business time segment
            for ek, ev in transform_extrafields.items():
                if ek in business_time.lower():
                    business_time = business_time.lower().replace(ek, ev)

            # Re generate the line after modification
            line = business_name + '","' + business_time.lower()

            # Writing the modified form in another file 'transformed_hours.csv'
            with open(transform_file, 'a') as ft:
                # Generate each combinations of From-To day possible and iterate, as we don't want to deal
                # with the different From-To possible combinations
                for k, v in generate_combination().items():
                    business_name = line.split('","')[0]
                    business_time = line.split('","')[1]
                    # If a combination matched with the current From-To day then transform it to comma seperated days
                    if k in line.lower() or k.replace(' ', '') in line.lower():
                        line = business_name + '","' + business_time.lower().replace(k, v).replace(k.replace(' ', ''), v)
                ft.write(line)
    print(transformed_business)


if __name__ == "__main__":
    main()
    print("End of program")