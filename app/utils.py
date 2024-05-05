
import pandas as pd
from app.models import Store, PollData, BusinessHours, Report
from app import db
from datetime import datetime, timedelta
from pytz import timezone
from collections import defaultdict
import uuid
from dateutil import parser

from pytz import timezone

def generate_report():
    poll_data = pd.read_csv('data/poll_data.csv', dtype={'store_id': str})
    business_hours = pd.read_csv('data/business_hours.csv', dtype={'store_id': str})
    timezones = pd.read_csv('data/timezones.csv', dtype={'store_id': str})
    report_id = str(uuid.uuid4())
    # Get the current UTC timestamp
    current_timestamp_utc = datetime.utcnow()

    # Store data into database
    for _, row in timezones.iterrows():
        store = Store(store_id=int(row['store_id']), timezone=row.get('timezone_str', 'America/Chicago'))
        db.session.add(store)
    db.session.commit()

    for _, row in business_hours.iterrows():
        business_hour = BusinessHours(store_id=int(row['store_id']), day_of_week=row['day'], 
                                      start_time_local=row['start_time_local'], end_time_local=row['end_time_local'])
        db.session.add(business_hour)
    db.session.commit()

    # Dictionary to store uptime and downtime for each store
    store_uptime = defaultdict(int)
    store_downtime = defaultdict(int)

    for _, row in poll_data.iterrows():
        # Convert string timestamp_utc to datetime object
        timestamp_utc = datetime.strptime(row['timestamp_utc'], '%Y-%m-%d %H:%M:%S.%f %Z')

        store = Store.query.filter_by(store_id=row['store_id']).first()
        if store:
            # Check if the store is within business hours
            business_hour = BusinessHours.query.filter_by(store_id=store.store_id, day_of_week=timestamp_utc.weekday()).first()
            # business_hour = BusinessHours.query.filter_by(store_id=store.store_id).first()
            if business_hour:
                # Convert timestamp_utc to the local time zone of the store
                store_timezone = timezone(store.timezone)
                timestamp_local = timestamp_utc.astimezone(store_timezone)

                # Check if the timestamp is within business hours
                business_start = datetime.strptime(business_hour.start_time_local, '%H:%M:%S')
                business_end = datetime.strptime(business_hour.end_time_local, '%H:%M:%S')
                if business_start.time() <= timestamp_local.time() <= business_end.time():
                    # Store the poll data in the database
                    poll = PollData(store_id=int(row['store_id']), timestamp_utc=timestamp_utc, status=row['status'])
                    db.session.add(poll)
                    # Update uptime/downtime counts
                    if row['status'] == 'active':
                        store_uptime[int(row['store_id'])] += 1
                    else:
                        store_downtime[int(row['store_id'])] += 1

    db.session.commit()
    # Now, generate the report for each store
    for store_id in store_uptime.keys():
        uptime_last_hour = store_uptime[store_id]
        downtime_last_hour = store_downtime[store_id]
        # Placeholder logic to calculate uptime and downtime for the last day and last week
        uptime_last_day = uptime_last_week = downtime_last_day = downtime_last_week = 0

        # Save the report in the database
        report_id = str(uuid.uuid4())  # Generate a unique report_id
        report = Report(
            report_id=report_id,
            store_id=store_id,
            uptime_last_hour=uptime_last_hour,
            uptime_last_day=uptime_last_day,
            uptime_last_week=uptime_last_week,
            downtime_last_hour=downtime_last_hour,
            downtime_last_day=downtime_last_day,
            downtime_last_week=downtime_last_week
        )
        db.session.add(report)

    db.session.commit()

    return report_id
