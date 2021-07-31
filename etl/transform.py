from itertools import cycle


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
            break;
        if start:
            ret_days.append(dy)
    return ', '.join(ret_days)


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

raw_file = '../../f-beiiopn/be-iiopn/etl/hours_actual.csv'
transform_file = '../../f-beiiopn/be-iiopn/etl/transform_hours.csv'
transformed_business = {}
transform_extrafields = {'tues': 'tue', 'weds': 'wed', 'thurs': 'thu'}
with open(raw_file, 'r') as f:
    for line in f:
        business_name = line.split('","')[0]
        busines_time = line.split('","')[1]
        for ek, ev in transform_extrafields.items():
            if ek in busines_time.lower():
                busines_time = busines_time.lower().replace(ek, ev)

        line = business_name + '","' + busines_time.lower()

        with open(transform_file, 'a') as ft:
            for k, v in generate_combination().items():
                business_name = line.split('","')[0]
                busines_time = line.split('","')[1]
                if k in line.lower() or k.replace(' ', '') in line.lower():
                    # try:
                    #     transformed_business[business_name] = transformed_business[business_name] + 1
                    # except:
                    #     transformed_business[business_name] = 1
                    line = business_name + '","' + busines_time.lower().replace(k, v).replace(k.replace(' ', ''), v)
            ft.write(line)
    # else:
    #     ft.write(business_name + '","' + busines_time.lower())
print(transformed_business)