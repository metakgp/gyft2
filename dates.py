from __future__ import print_function

import build_event

# import datetime
# import pytz
# SEM_BEGIN = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
# SEM BEGIN, and MID_TERM_BEGIN are one day before due to weird calculations
SEM_BEGIN = build_event.generateIndiaTime(2025, 1, 2, 0, 0)
MID_TERM_BEGIN = build_event.generateIndiaTime(2025, 2, 15, 0, 0)
MID_TERM_END = build_event.generateIndiaTime(2025, 2, 23, 0, 0)
END_TERM_BEGIN = build_event.generateIndiaTime(2025, 4, 18, 0, 0)

# Sanity check

sanity = [
    SEM_BEGIN < MID_TERM_BEGIN,
    MID_TERM_BEGIN < MID_TERM_END,
    MID_TERM_END < END_TERM_BEGIN,
]

# check if anything is False
sanity_check = [item for item in sanity if not item]

if len(sanity_check) > 0:
    print("Check the dates you have entered")
    print("Note: SEM_BEGIN < MID_TERM_BEGIN < MID_TERM_END < END_TERM_BEGIN")
    import os

    os._exit(1)


def get_dates():
    """
    Returns a list of lists denoting the time periods of working days
    """
    return [[SEM_BEGIN, MID_TERM_BEGIN], [MID_TERM_END, END_TERM_BEGIN]]
