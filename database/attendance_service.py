from datetime import datetime

from database.mongo import attendance_collection


def mark_attendance(name):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    record = attendance_collection.find_one(
        {
            "name": name,
            "date": today
        }
    )

    # CHECK-IN

    if record is None:

        attendance_collection.insert_one(
            {
                "name": name,
                "date": today,
                "checkIn": current_time,
                "checkOut": None,
                "hoursWorked": None
            }
        )

        return f"{name} Checked In at {current_time}"

    # CHECK-OUT

    elif record["checkOut"] is None:

        checkin_time = datetime.strptime(
            record["checkIn"],
            "%H:%M:%S"
        )

        checkout_time = datetime.strptime(
            current_time,
            "%H:%M:%S"
        )

        hours = round(
            (
                checkout_time - checkin_time
            ).total_seconds() / 3600,
            2
        )

        attendance_collection.update_one(
            {
                "_id": record["_id"]
            },
            {
                "$set": {
                    "checkOut": current_time,
                    "hoursWorked": hours
                }
            }
        )

        return f"{name} Checked Out at {current_time}"

    else:

        return "Attendance already completed today"