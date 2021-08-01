@staticmethod
def transform_raw_schedule(raw_schedule: object = {}):
    if raw_schedule and raw_schedule.get('raw_schedule', None):
        return raw_schedule.get('raw_schedule').title()
    return raw_schedule
