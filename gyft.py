from bs4 import BeautifulSoup as bs
import json
import generate_ics

import sys


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


with open('view_stud_time_table.html', 'r') as myfile:
    r = myfile.read()
# print(r)
soup = bs(r, 'html.parser')
rows_head = soup.findAll('table')[2]
rows = rows_head.findAll('tr')
times = []

# Delete the rows that have less elements
# this is done because the erp does some shit
del_rows = []
for o in range(len(rows)):
    # print(o, len(rows[o]))
    if len(rows[o]) < 5:
        del_rows.append(o)

for index_del in del_rows:
    del rows[index_del]

# for row in rows:
#     print(len(row))
# #### For timings

for a in rows[0].findAll('td'):
    if ('AM' in a.text or 'PM' in a.text):
        times.append(a.text)

# ### For timings end
days = {}
# ### For day
days[1] = "Monday"
days[2] = "Tuesday"
days[3] = "Wednesday"
days[4] = "Thursday"
days[5] = "Friday"
days[6] = "Saturday"
# ### For day end

timetable_dict = {}

for i in range(1, len(rows)):
    timetable_dict[days[i]] = {}
    tds = rows[i].findAll('td')
    time = 0
    for a in range(1, len(tds)):
        txt = tds[a].find('b').text.strip()
        if (len(txt) >= 7):
            timetable_dict[days[i]][times[time]] = list(
                (
                    tds[a].find('b').text[:7],
                    tds[a].find('b').text[7:],
                    int(tds[a]._attr_value_as_string('colspan'))
                )
            )
        time = time + int(tds[a]._attr_value_as_string('colspan'))


def merge_slots(in_dict):
    for a in in_dict:
        in_dict[a] = sorted(in_dict[a])
        for i in range(len(in_dict[a]) - 1, 0, -1):
            if (in_dict[a][i][0] == in_dict[a][i-1][0] + in_dict[a][i-1][1]):
                in_dict[a][i-1][1] = in_dict[a][i][1] + in_dict[a][i-1][1]
                in_dict[a].remove(in_dict[a][i])
        in_dict[a] = in_dict[a][0]
    return (in_dict)


for day in timetable_dict.keys():
    subject_timings = {}
    for time in timetable_dict[day]:
        flattened_time = int(time[:time.find(':')])
        if (flattened_time < 6):
            flattened_time += 12
        if (not timetable_dict[day][time][0] in subject_timings.keys()):
            subject_timings[timetable_dict[day][time][0]] = []
        subject_timings[timetable_dict[day][time][0]].append(
            [flattened_time, timetable_dict[day][time][2]]
        )
    subject_timings = merge_slots(subject_timings)
    for time in list(timetable_dict[day].keys()):
        flattened_time = int(time[:time.find(':')])
        if (flattened_time < 6):
            flattened_time += 12
        if (
            not flattened_time == subject_timings[
                timetable_dict[day][time][0]
            ][0]
        ):
                del (timetable_dict[day][time])
        else:
            timetable_dict[day][time][2] = subject_timings[
                    timetable_dict[day][time][0]
                ][1]


with open('data.txt', 'w') as outfile:
    json.dump(timetable_dict, outfile, indent=4, ensure_ascii=False)

print(
    '''
    Timetable saved to data.txt file. Be sure to edit this file,
    to have desired names of subjects rather than subject codes.
    '''
)

if query_yes_no("Do you want to generate ICS file too?"):
    generate_ics.main()
else:
    print("You can Generate ICS later using generate_ics.py")
