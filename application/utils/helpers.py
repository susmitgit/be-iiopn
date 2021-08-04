@staticmethod
def transform_raw_schedule(raw_schedule: object = {}):
    if raw_schedule and raw_schedule.get('raw_schedule', None):
        data = {**raw_schedule, **{'b_id': str(raw_schedule['_id']), 'raw_schedule': raw_schedule.get('raw_schedule').title()}}
        return exclude_mongo_id(data)
    return raw_schedule


def exclude_mongo_id(data=None):

    if type(data) == list:
        for d in data:
            if d and d.get('_id', None):
                d['id'] = str(d['_id'])
                del d['_id']
    else:
        if data and data.get('_id', None):
            data['id'] = str(data['_id'])
            del data['_id']
    return data


def escape_search_special_chars(val):
    escape_chars = ['$', '#', '.', '@', '>', '/', '^', '~']
    for each_char in escape_chars:
        val = val.replace(each_char, f"\{each_char}", -1)
    return val

