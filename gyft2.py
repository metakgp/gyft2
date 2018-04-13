from bs4 import BeautifulSoup as bs
import json
import generate_ics
from sys import exit
import os.path
from Query_yn import query_yes_no

# Input the file
if os.path.isfile('view_stud_time_table.html'):
    with open('view_stud_time_table.html', 'r') as myfile:
        r = myfile.read()
elif os.path.isfile('Time Table View.html'):
    with open('Time Table View.html', 'r') as myfile:
        r = myfile.read()
else:
    print("HTML file not found")
    exit()

# print(r)
soup = bs(r, 'html.parser')
rows_head = soup.findAll('table')[2]
rows = rows_head.findAll('tr')
times = []

# Delete the rows that doesn't have tableheader, basically without a weekday
del_rows = []
for i in range(1, len(rows)):
    HeaderRows = rows[i].findAll("td", {"class": "tableheader"})
    # print(HeaderRows)
    if len(HeaderRows) is 0:
        del_rows.append(i)

# print(del_rows)

for index_del in sorted(del_rows, reverse=True):
    del rows[index_del]

# for row in rows:
#     print(row)

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


with open('data.txt', 'w+') as outfile:
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
