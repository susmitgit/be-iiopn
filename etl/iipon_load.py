import os

from pymongo import MongoClient

collection_schedule = 'schedule'
collection_business = 'business'

dbCon = None


# Helpers methods
# Business name extract from the read line string
def extract_business_name(line):
    return line.split("\",\"")[0].lstrip('"').rstrip('"')


# Transform time string to searchable form
def time_str(dt_str, meridian=None):
    # Last two bits handle:
    if ':' in dt_str:
        last_two_bit = dt_str.split(":")[1]
        if len(last_two_bit) <= 1:
            dt_str = dt_str.split(":")[0] + ':' + str(int(last_two_bit) * 10)
    else:
        if int(dt_str) > 23:
            raise Exception('InValid ! Greater than 23!')
        dt_str = dt_str + ':' + '00'

    int_str = int(dt_str.replace(":", ""))

    # Convert every 1/2 digit to 4 digit
    if len(dt_str) <= 2:
        int_str = int_str * 100

    # If no meridian sent
    if not meridian:
        meridian = 'pm' if int_str > 1200 else 'am'

    # AM Handlers
    if meridian == 'am':
        if int_str > 1159:
            return int_str - 1200
    else:
        # PM Handlers
        if int_str >= 1200:
            return int_str
        if int_str < 1200:
            int_str += 1200

    return int_str


# Transform Days to number and number to day
def transform_day_number(day, reverse=None):
    data_day = None
    day_map = {'mon': 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
    reverse_day_map = {0: 'mon', 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat", 6: "sun"}
    if reverse:
        return reverse_day_map[day]
    if 'mon' in day.lower():
        data_day = day_map['mon']
    if 'tue' in day.lower():
        data_day = day_map['tue']
    if 'wed' in day.lower():
        data_day = day_map['wed']
    if 'thu' in day.lower():
        data_day = day_map['thu']
    if 'fri' in day.lower():
        data_day = day_map['fri']
    if 'sat' in day.lower():
        data_day = day_map['sat']
    if 'sun' in day.lower():
        data_day = day_map['sun']
    return data_day


# Extract business operation time Open / Close
def extract_operation_time(b_time: str = None, data_day: str = None, line: str = None):
    b_time.lower().replace(transform_day_number(day=data_day, reverse=True), "")
    # Time - time break up
    times = b_time.split("-")

    business_open = None
    business_close = None

    # Open Time Analysis
    open_time = times[0].lower()

    if 'am' in open_time:
        am_time = open_time.split('am')[0].lstrip(' ').rstrip(' ')
        business_open = time_str(dt_str=am_time, meridian='am')
    if 'pm' in open_time:
        pm_time = open_time.split('pm')[0].lstrip(' ').rstrip(' ')
        business_open = time_str(dt_str=pm_time, meridian='pm')

    # Close time analysis
    close_time = times[1].lower()

    if 'am' in close_time:
        am_time = close_time.split('am')[0].lstrip(' ').rstrip(' ')
        business_close = time_str(dt_str=am_time, meridian='am')
        # print(f"Day {data_day} AM - {business_close}")
    if 'pm' in close_time:
        pm_time = close_time.split('pm')[0].lstrip(' ').rstrip(' ')
        business_close = time_str(dt_str=pm_time, meridian='pm')
        # print(f"Day {data_day} PM - {business_close}")

    # Catch error in transforming
    if not business_open and business_open != 0 or not business_close and business_close != 0:
        print(f"Investigate data - {line}")
    return business_open, business_close


def get_raw_schedule_from_line(line: str = None):
    return line.split("\",\"")[1].lstrip('"').rstrip('"')


def insert_business_schedule(line: str = None, business_id: str = None):
    # Business Schedule part from the given line
    business_time = get_raw_schedule_from_line(line=line)
    options = business_time.split('/')

    for opt in options:
        days = opt.split(",")
        # Time analysis
        business_open, business_close = \
            extract_operation_time(b_time=days[-1].lower().replace(
                transform_day_number(day=transform_day_number(days[-1]), reverse=True), ""),
                data_day=transform_day_number(days[-1]), line=line)

        for day in days:
            data_day = transform_day_number(day)

            # Next Day Adjusted time for next day - Considering next day close will not be passed the open time
            if business_open > business_close:
                cur_update_obj = {
                    'b_id': business_id,
                    'b_day': data_day,
                    'b_open': business_open,
                    'b_close': 2359}
                insert_data(data=cur_update_obj, collection=collection_schedule)
                nxt_update_obj = {
                    'b_id': business_id,
                    'b_day': data_day + 1 if data_day + 1 < 7 else data_day + 1 - 7,
                    'b_open': 0000,
                    'b_close': business_close}
                insert_data(data=nxt_update_obj, collection=collection_schedule)
            else:
                update_obj = {
                    'b_id': business_id,
                    'b_day': data_day,
                    'b_open': business_open,
                    'b_close': business_close}
                insert_data(data=update_obj, collection=collection_schedule)
    return True


def db_connect():
    global dbCon
    try:
        if not dbCon:
            client = MongoClient(os.getenv('DATABASE_URI'), tlsAllowInvalidCertificates=True)
            db = client[os.getenv('DATABASE_NAME', 'test')]
            dbCon = db
        return dbCon
    except Exception as e:
        print(f"Error in DB Connection {str(e)}")
        return None


def insert_data(data: object = {}, collection: object = None) -> object:
    connection = db_connect()
    try:
        inserted = connection[collection].insert_one(data)
        return inserted.inserted_id
    except Exception as e:
        print(f"Error in Insert() {str(e)}")


def select_data(statement: object = {}, collection=None):
    connection = db_connect()
    try:
        data = connection[collection].find_one(statement)
        return data
    except Exception as e:
        print(f"Error in select {str(e)}")


def insert_business_name(b_name: str = None, raw_schedule: str = None):
    if b_name:
        # If business already present return the business_id instead of inserting
        data = select_data(statement={"name": b_name}, collection=collection_business)
        if data and data.get('_id', None):
            b_id = str(data['_id'])
            return b_id
        else:
            data = insert_data(data={'name': b_name, 'raw_schedule': raw_schedule}, collection=collection_business)
            return data


def main():
    # Main program
    raw_file = 'transformed_hours.csv'
    {}
    all_business_names = []
    duplicate_business = []

    try:
        # Read the transformed data line by line
        with open(raw_file, 'r') as f:
            for line in f:
                business_name = extract_business_name(line)
                if business_name not in all_business_names:
                    all_business_names.append(business_name)
                else:
                    # Identify the duplicate business names in the Data - Just for analysis
                    duplicate_business.append(business_name)

                # Creating 'business' collection
                b_id = insert_business_name(b_name=business_name, raw_schedule=get_raw_schedule_from_line(line=line))
                insert_business_schedule(line, business_id=str(b_id))

    except Exception as error:
        print("Failed to insert record into mobile table", error)

    finally:
        pass

    print(duplicate_business)


if __name__ == "__main__":
    main()
    print("End of program")
