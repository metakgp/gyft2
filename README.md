# gyft

Get Your Freaking Timetable

## About

Gets your timetable from ERP and gives you an **ICS file** which you can add in any common calendar application (such as Google Calendar).

**Note:** Please use this utility with `python3`.

## How to use the program?

- **Step 1:** Get your timetable from ERP:

Log in to ERP portal, and visit [https://erp.iitkgp.ernet.in/Acad/student/view_stud_time_table.jsp](https://erp.iitkgp.ernet.in/Acad/student/view_stud_time_table.jsp).

Save this page in the Directory using `Ctrl+S` on any browser (Use Only HTML)

Now run the gyft script

  ```sh
  $ python3 gyft.py
  ```

Your timetable will be saved in `data.txt`. Make any changes required appropriately in `data.txt`.

- **Step 2:** Decide whether you want to add the events to Google Calendar or
    generate an ICS file from the data.

    Adding to Google Calendar requires an Internet connection

    ICS files are compatible with almost all Calendar applications (including
    the iOS calendar application, Sunrise etc)

- **Step 2:** To generate an ICS file:

    - **Step (i):** Run the command:

        ```sh
        $ python3 generate_ics.py
        # or for windows
        > python generate_ics.py
        ```

        ```sh
        # you can provide input and output file path to this python script
        $ python3 generate_ics.py --input d.txt --output t.ics
        # or for windows
        > python3 generate_ics.py --input d.txt --output t.ics
        ```

    - **Step (ii):** Open your calendar application and import this ICS file
        into it. For Google Calendar You can follow [this guide](https://support.google.com/calendar/answer/37118?hl=en).

## License

GPLv3.
