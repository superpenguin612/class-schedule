import datetime
import re
import math

STUDENT_DATA = {
    "blue": {
        "lunch": "D",
        "classes": {
            "Block 1": "AP Physics 1",
            "Block 2": "Honors Pre-Calc/Trig",
            "Block 3": "New Edition",
            "Block 4": "AP Computer Science A",
        },
    },
    "gold": {
        "lunch": "B",
        "classes": {
            "Block 1": "Honors Chemistry",
            "Block 2": "SRT",
            "Block 3": "AP Seminar",
            "Block 4": "Spanish III",
        },
    },
    "enable_block_naming": True,
}

SCHOOL_DATA = {
    "times": {
        "regular": {
            "A": {
                "09:05": "Block 1 starts in ",
                "10:35": "Block 1 ends in ",
                "10:45": "Block 2 starts in ",
                "12:15": "Block 2 ends in ",
                "12:48": "Lunch ends in ",
                "12:55": "Block 3 starts in ",
                "14:25": "Block 3 ends in ",
                "14:35": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
            "B": {
                "09:05": "Block 1 starts in ",
                "10:35": "Block 1 ends in ",
                "10:45": "Block 2 starts in ",
                "12:15": "Block 2 ends in ",
                "12:25": "Block 3 (before lunch) starts in ",
                "12:51": "Block 3 (before lunch) ends in ",
                "13:21": "Lunch ends in ",
                "13:26": "Block 3 (after lunch) starts in ",
                "14:25": "Block 3 (after lunch) ends in ",
                "14:35": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
            "C": {
                "09:05": "Block 1 starts in ",
                "10:35": "Block 1 ends in ",
                "10:45": "Block 2 starts in ",
                "12:15": "Block 2 ends in ",
                "12:25": "Block 3 (before lunch) starts in ",
                "13:24": "Block 3 (before lunch) ends in ",
                "13:54": "Lunch ends in ",
                "13:59": "Block 3 (after lunch) starts in ",
                "14:25": "Block 3 (after lunch) ends in ",
                "14:35": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
            "D": {
                "09:05": "Block 1 starts in ",
                "10:35": "Block 1 ends in ",
                "10:45": "Block 2 starts in ",
                "12:15": "Block 2 ends in ",
                "12:25": "Block 3 starts in ",
                "13:55": "Block 3 ends in ",
                "14:25": "Lunch ends in ",
                "14:35": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
        },
        "late": {
            "A": {
                "09:45": "Block 1 starts in ",
                "11:01": "Block 1 ends in ",
                "11:11": "Block 2 starts in ",
                "12:28": "Block 2 ends in ",
                "13:01": "Lunch ends in ",
                "13:08": "Block 3 starts in ",
                "14:38": "Block 3 ends in ",
                "14:48": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
            "B": {
                "09:45": "Block 1 starts in ",
                "11:01": "Block 1 ends in ",
                "11:11": "Block 2 starts in ",
                "12:28": "Block 2 ends in ",
                "12:38": "Block 3 (before lunch) starts in ",
                "13:04": "Block 3 (before lunch) ends in ",
                "13:34": "Lunch ends in ",
                "13:39": "Block 3 (after lunch) starts in ",
                "14:38": "Block 3 (after lunch) ends in ",
                "14:48": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
            "C": {
                "09:45": "Block 1 starts in ",
                "11:01": "Block 1 ends in ",
                "11:11": "Block 2 starts in ",
                "12:28": "Block 2 ends in ",
                "12:38": "Block 3 (before lunch) starts in ",
                "13:37": "Block 3 (before lunch) ends in ",
                "14:07": "Lunch ends in ",
                "14:12": "Block 3 (after lunch) starts in ",
                "14:38": "Block 3 (after lunch) ends in ",
                "14:48": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
            "D": {
                "09:45": "Block 1 starts in ",
                "11:01": "Block 1 ends in ",
                "11:11": "Block 2 starts in ",
                "12:28": "Block 2 ends in ",
                "12:38": "Block 3 starts in ",
                "14:08": "Block 3 ends in ",
                "14:38": "Lunch ends in ",
                "14:48": "Block 4 starts in ",
                "16:05": "Block 4 ends in ",
            },
        },
    },
    "overview": {
        "regular": {
            "A": {
                "09:05": "Block 1 (9:05 AM to 10:35 AM)",
                "10:45": "Block 2 (10:45 AM to 12:15 PM)",
                "12:15": "Lunch (12:15 PM to 12:48 PM)",
                "12:55": "Block 3 (12:55 PM to 2:25 PM)",
                "14:35": "Block 4 (2:35 PM to 4:05 PM)",
            },
            "B": {
                "09:05": "Block 1 (9:05 AM to 10:35 AM)",
                "10:45": "Block 2 (10:45 AM to 12:15 PM)",
                "12:25": "Block 3 (before lunch) (12:25 PM to 12:51 PM)",
                "12:51": "Lunch (12:51 PM to 1:21 PM)",
                "13:26": "Block 3 (after lunch) (1:26 PM to 2:25 PM)",
                "14:35": "Block 4 (2:35 PM to 4:05 PM)",
            },
            "C": {
                "09:05": "Block 1 (9:05 AM to 10:35 AM)",
                "10:45": "Block 2 (10:45 AM to 12:15 PM)",
                "12:25": "Block 3 (before lunch) (12:25 PM to 1:24 PM)",
                "13:24": "Lunch (1:24 PM to 1:54 PM)",
                "13:59": "Block 3 (after lunch) (1:59 PM to 2:25 PM)",
                "14:35": "Block 4 (2:35 PM to 4:05 PM)",
            },
            "D": {
                "09:05": "Block 1 (9:05 AM to 10:35 AM)",
                "10:45": "Block 2 (10:45 AM to 12:15 PM)",
                "12:25": "Block 3 (12:25 PM to 1:55 PM)",
                "13:55": "Lunch (1:55 PM to 2:25 PM)",
                "14:35": "Block 4 (2:35 PM to 4:05 PM)",
            },
        },
        "late": {
            "A": {
                "09:45": "Block 1 (9:45 AM to 11:01 AM)",
                "11:11": "Block 2 (11:11 AM to 12:28 PM)",
                "12:28": "Lunch (12:28 PM to 1:01 PM)",
                "13:08": "Block 3 (1:08 PM to 2:38 PM)",
                "14:48": "Block 4 (2:48 PM to 4:05 PM)",
            },
            "B": {
                "09:45": "Block 1 (9:45 AM to 11:01 AM)",
                "11:11": "Block 2 (11:11 AM to 12:28 PM)",
                "12:38": "Block 3 (before lunch) (12:38 PM to 1:04 PM)",
                "13:04": "Lunch (1:04 PM to 1:34 PM)",
                "13:39": "Block 3 (after lunch) (1:39 PM to 2:38 PM)",
                "14:48": "Block 4 (2:48 PM to 4:05 PM)",
            },
            "C": {
                "09:45": "Block 1 (9:45 AM to 11:01 AM)",
                "11:11": "Block 2 (11:11 AM to 12:28 PM)",
                "12:38": "Block 3 (before lunch) (12:38 PM to 1:37 PM)",
                "13:37": "Lunch (1:37 PM to 2:07 PM)",
                "14:12": "Block 3 (after lunch) (2:12 PM to 2:38 PM)",
                "14:48": "Block 4 (2:48 PM to 4:05 PM)",
            },
            "D": {
                "09:45": "Block 1 (9:45 AM to 11:01 AM)",
                "11:11": "Block 2 (11:11 AM to 12:28 PM)",
                "12:38": "Block 3 (12:38 PM to 2:08 PM)",
                "14:08": "Lunch (2:08 PM to 2:38 PM)",
                "14:48": "Block 4 (2:48 PM to 4:05 PM)",
            },
        },
    },
    "days": {
        "08/12/2021": "Blue Day",
        "08/13/2021": "Gold Day",
        "08/14/2021": "Weekend",
        "08/15/2021": "Weekend",
        "08/16/2021": "Blue Day",
        "08/17/2021": "Gold Day",
        "08/18/2021": "Blue Day",
        "08/19/2021": "Gold Day",
        "08/20/2021": "Blue Day",
        "08/21/2021": "Weekend",
        "08/22/2021": "Weekend",
        "08/23/2021": "Gold Day",
        "08/24/2021": "Blue Day",
        "08/25/2021": "Gold Day, Late Start",
        "08/26/2021": "Blue Day",
        "08/27/2021": "Gold Day",
        "08/28/2021": "Weekend",
        "08/29/2021": "Weekend",
        "08/30/2021": "Blue Day",
        "08/31/2021": "Gold Day",
        "09/01/2021": "Blue Day",
        "09/02/2021": "Gold Day",
        "09/03/2021": "Blue Day",
        "09/04/2021": "Weekend",
        "09/05/2021": "Weekend",
        "09/06/2021": "Labor Day",
        "09/07/2021": "Gold Day",
        "09/08/2021": "Blue Day, Late Start",
        "09/09/2021": "Gold Day",
        "09/10/2021": "Blue Day",
        "09/11/2021": "Weekend",
        "09/12/2021": "Weekend",
        "09/13/2021": "Gold Day",
        "09/14/2021": "Blue Day",
        "09/15/2021": "Gold Day",
        "09/16/2021": "Blue Day",
        "09/17/2021": "Gold Day",
        "09/18/2021": "Weekend",
        "09/19/2021": "Weekend",
        "09/20/2021": "Blue Day",
        "09/21/2021": "Gold Day",
        "09/22/2021": "Blue Day, Late Start",
        "09/23/2021": "Gold Day",
        "09/24/2021": "Homecoming",
        "09/25/2021": "Weekend",
        "09/26/2021": "Weekend",
        "09/27/2021": "Blue Day",
        "09/28/2021": "Gold Day",
        "09/29/2021": "Blue Day",
        "09/30/2021": "Gold Day",
        "10/01/2021": "Blue Day",
        "10/02/2021": "Weekend",
        "10/03/2021": "Weekend",
        "10/04/2021": "Gold Day",
        "10/05/2021": "Blue Day",
        "10/06/2021": "Gold Day, Late Start",
        "10/07/2021": "Blue Day",
        "10/08/2021": "Gold Day",
        "10/09/2021": "Weekend",
        "10/10/2021": "Weekend",
        "10/11/2021": "Blue Day",
        "10/12/2021": "Gold Day",
        "10/13/2021": "Blue Day, Midterms",
        "10/14/2021": "Fall Break",
        "10/15/2021": "Fall Break",
        "10/16/2021": "Weekend",
        "10/17/2021": "Weekend",
        "10/18/2021": "Gold Day",
        "10/19/2021": "Blue Day",
        "10/20/2021": "Gold Day, Late Start",
        "10/21/2021": "Blue Day",
        "10/22/2021": "Gold Day",
        "10/23/2021": "Weekend",
        "10/24/2021": "Weekend",
        "10/25/2021": "Blue Day",
        "10/26/2021": "PSAT Testing",
        "10/27/2021": "Gold Day",
        "10/28/2021": "Blue Day",
        "10/29/2021": "Gold Day",
        "10/30/2021": "Weekend",
        "10/31/2021": "Weekend",
        "11/01/2021": "Blue Day",
        "11/02/2021": "Gold Day",
        "11/03/2021": "Blue Day, Late Start",
        "11/04/2021": "Gold Day",
        "11/05/2021": "Blue Day",
        "11/06/2021": "Weekend",
        "11/07/2021": "Weekend",
        "11/08/2021": "Gold Day",
        "11/09/2021": "Blue Day",
        "11/10/2021": "Gold Day",
        "11/11/2021": "Blue Day",
        "11/12/2021": "Gold Day",
        "11/13/2021": "Weekend",
        "11/14/2021": "Weekend",
        "11/15/2021": "Blue Day",
        "11/16/2021": "Gold Day",
        "11/17/2021": "Blue Day, Late Start",
        "11/18/2021": "Gold Day",
        "11/19/2021": "Blue Day",
        "11/20/2021": "Weekend",
        "11/21/2021": "Weekend",
        "11/22/2021": "Gold Day",
        "11/23/2021": "Blue Day",
        "11/24/2021": "Thanksgiving Break",
        "11/25/2021": "Thanksgiving Break",
        "11/26/2021": "Thanksgiving Break",
        "11/27/2021": "Weekend",
        "11/28/2021": "Weekend",
        "11/29/2021": "Gold Day",
        "11/30/2021": "Blue Day",
        "12/01/2021": "Gold Day, Late Start",
        "12/02/2021": "Blue Day",
        "12/03/2021": "Gold Day",
        "12/04/2021": "Weekend",
        "12/05/2021": "Weekend",
        "12/06/2021": "Blue Day",
        "12/07/2021": "Gold Day",
        "12/08/2021": "Blue Day",
        "12/09/2021": "Gold Day",
        "12/10/2021": "Blue Day",
        "12/11/2021": "Weekend",
        "12/12/2021": "Weekend",
        "12/13/2021": "Gold Day",
        "12/14/2021": "Blue Day",
        "12/15/2021": "Gold Day",
        "12/16/2021": "Blue Day",
        "12/17/2021": "Gold Day, End of Semester",
        "12/18/2021": "Weekend",
        "12/19/2021": "Weekend",
        "12/20/2021": "Winter Break",
        "12/21/2021": "Winter Break",
        "12/22/2021": "Winter Break",
        "12/23/2021": "Winter Break",
        "12/24/2021": "Winter Break",
        "12/25/2021": "Weekend",
        "12/26/2021": "Weekend",
        "12/27/2021": "Winter Break",
        "12/28/2021": "Winter Break",
        "12/29/2021": "Winter Break",
        "12/30/2021": "Winter Break",
        "12/31/2021": "Winter Break",
        "01/01/2022": "Weekend",
        "01/02/2022": "Weekend",
        "01/03/2022": "Teacher Contract Day",
        "01/04/2022": "Blue Day",
        "01/05/2022": "Gold Day",
        "01/06/2022": "Blue Day",
        "01/07/2022": "Gold Day",
        "01/08/2022": "Weekend",
        "01/09/2022": "Weekend",
        "01/10/2022": "Blue Day",
        "01/11/2022": "Gold Day",
        "01/12/2022": "Blue Day, Late Start",
        "01/13/2022": "Gold Day",
        "01/14/2022": "Blue Day",
        "01/15/2022": "Weekend",
        "01/16/2022": "Weekend",
        "01/17/2022": "Martin Luther King Jr. Day",
        "01/18/2022": "Gold Day",
        "01/19/2022": "Blue Day",
        "01/20/2022": "Gold Day",
        "01/21/2022": "Blue Day",
        "01/22/2022": "Weekend",
        "01/23/2022": "Weekend",
        "01/24/2022": "Gold Day",
        "01/25/2022": "Blue Day",
        "01/26/2022": "Gold Day, Late Start",
        "01/27/2022": "Blue Day",
        "01/28/2022": "Gold Day",
        "01/29/2022": "Weekend",
        "01/30/2022": "Weekend",
        "01/31/2022": "Blue Day",
        "02/01/2022": "Gold Day",
        "02/02/2022": "Blue Day",
        "02/03/2022": "Gold Day",
        "02/04/2022": "Blue Day",
        "02/05/2022": "Weekend",
        "02/06/2022": "Weekend",
        "02/07/2022": "Gold Day",
        "02/08/2022": "Blue Day",
        "02/09/2022": "Gold Day, Late Start",
        "02/10/2022": "Blue Day",
        "02/11/2022": "Gold Day",
        "02/12/2022": "Weekend",
        "02/13/2022": "Weekend",
        "02/14/2022": "Blue Day",
        "02/15/2022": "Gold Day",
        "02/16/2022": "Blue Day",
        "02/17/2022": "Gold Day",
        "02/18/2022": "Blue Day",
        "02/19/2022": "Weekend",
        "02/20/2022": "Weekend",
        "02/21/2022": "President's Day",
        "02/22/2022": "Gold Day",
        "02/23/2022": "Blue Day, Late Start",
        "02/24/2022": "Gold Day",
        "02/25/2022": "Blue Day",
        "02/26/2022": "Weekend",
        "02/27/2022": "Weekend",
        "02/28/2022": "Gold Day",
        "03/01/2022": "Blue Day",
        "03/02/2022": "SAT Testing",
        "03/03/2022": "Gold Day",
        "03/04/2022": "Blue Day",
        "03/05/2022": "Weekend",
        "03/06/2022": "Weekend",
        "03/07/2022": "Gold Day",
        "03/08/2022": "Blue Day",
        "03/09/2022": "Gold Day, Late Start",
        "03/10/2022": "Blue Day",
        "03/11/2022": "Gold Day, Midterms",
        "03/12/2022": "Weekend",
        "03/13/2022": "Weekend",
        "03/14/2022": "Blue Day",
        "03/15/2022": "Gold Day",
        "03/16/2022": "Blue Day",
        "03/17/2022": "Gold Day",
        "03/18/2022": "Blue Day",
        "03/19/2022": "Weekend",
        "03/20/2022": "Weekend",
        "03/21/2022": "Gold Day",
        "03/22/2022": "Blue Day",
        "03/23/2022": "Gold Day, Late Start",
        "03/24/2022": "Blue Day",
        "03/25/2022": "Gold Day",
        "03/26/2022": "Weekend",
        "03/27/2022": "Weekend",
        "03/28/2022": "Blue Day",
        "03/29/2022": "Gold Day",
        "03/30/2022": "Blue Day",
        "03/31/2022": "Gold Day",
        "04/01/2022": "Spring Break",
        "04/02/2022": "Weekend",
        "04/03/2022": "Weekend",
        "04/04/2022": "Spring Break",
        "04/05/2022": "Spring Break",
        "04/06/2022": "Spring Break",
        "04/07/2022": "Spring Break",
        "04/08/2022": "Spring Break",
        "04/09/2022": "Weekend",
        "04/10/2022": "Weekend",
        "04/11/2022": "Blue Day",
        "04/12/2022": "Gold Day",
        "04/13/2022": "Blue Day, Late Start",
        "04/14/2022": "Gold Day",
        "04/15/2022": "Blue Day",
        "04/16/2022": "Weekend",
        "04/17/2022": "Weekend",
        "04/18/2022": "Gold Day",
        "04/19/2022": "Blue Day",
        "04/20/2022": "Gold Day",
        "04/21/2022": "Blue Day",
        "04/22/2022": "Gold Day",
        "04/23/2022": "Weekend",
        "04/24/2022": "Weekend",
        "04/25/2022": "Blue Day",
        "04/26/2022": "Gold Day",
        "04/27/2022": "Blue Day, Late Start",
        "04/28/2022": "Gold Day",
        "04/29/2022": "Blue Day",
        "04/30/2022": "Weekend",
        "05/01/2022": "Weekend",
        "05/02/2022": "Gold Day",
        "05/03/2022": "Blue Day",
        "05/04/2022": "Gold Day",
        "05/05/2022": "Blue Day",
        "05/06/2022": "Gold Day",
        "05/07/2022": "Weekend",
        "05/08/2022": "Weekend",
        "05/09/2022": "Blue Day",
        "05/10/2022": "Gold Day",
        "05/11/2022": "Blue Day, Late Start",
        "05/12/2022": "Gold Day",
        "05/13/2022": "Blue Day",
        "05/14/2022": "Weekend",
        "05/15/2022": "Weekend",
        "05/16/2022": "Gold Day",
        "05/17/2022": "Blue Day",
        "05/18/2022": "Gold Day",
        "05/19/2022": "Blue Day",
        "05/20/2022": "Gold Day",
        "05/21/2022": "Weekend",
        "05/22/2022": "Weekend",
        "05/23/2022": "Blue Day",
        "05/24/2022": "Gold Day",
        "05/25/2022": "Blue Day, End of Semester",
    },
}


class Day:
    day_name: str
    is_school_day: bool
    classes: dict
    lunch: str
    day_type: str
    school_over: bool

    def __init__(self):
        pass


current_day = Day()


def _set_day_information() -> None:
    formatted_date = datetime.datetime.strftime(datetime.datetime.now(), "%m/%d/%Y")
    current_day.day_name = SCHOOL_DATA["days"][formatted_date]
    search_result = re.search("(Blue|Gold)", current_day.day_name).group()
    if search_result:
        current_day.is_school_day = True
        current_day.lunch = STUDENT_DATA[search_result.lower()]["lunch"]
        current_day.classes = STUDENT_DATA[search_result.lower()]["classes"]
        current_day.day_type = "late" if "Late" in current_day.day_name else "regular"

    else:
        current_day.is_school_day = False


def create_day_result() -> str:
    formatted_date = datetime.datetime.strftime(
        datetime.datetime.now(), "%A, %B %d, %Y"
    )
    return f"Today is {formatted_date} ({current_day.day_name})."


def _rename_block(to_rename: str) -> str:
    if STUDENT_DATA["enable_block_naming"]:
        match = re.search("(Block\s[0-9])", to_rename)
        if match:
            class_to_sub = current_day.classes[match.group()]
            renamed = re.sub("(Block\s[0-9])", class_to_sub, to_rename)
        else:
            renamed = to_rename
        return renamed


def create_block_result() -> str:
    if current_day.is_school_day:
        block_result = ""
        for time in sorted(
            SCHOOL_DATA["times"][current_day.day_type][current_day.lunch].keys()
        ):
            if not block_result:
                class_time_difference = (
                    datetime.datetime.combine(
                        datetime.datetime.now().date(),
                        datetime.datetime.strptime(time, "%H:%M").time(),
                    )
                    - datetime.datetime.now()
                )
                if class_time_difference > datetime.timedelta():
                    block_name = SCHOOL_DATA["times"][current_day.day_type][
                        current_day.lunch
                    ][time]
                    minute_type = "minute" if class_time_difference == 1 else "minutes"
                    formatted_time = datetime.datetime.strptime(time, "%H:%M").strftime(
                        "%I:%M %p"
                    )
                    block_result = f"{block_name}{math.floor(class_time_difference.seconds / 60)} {minute_type} ({formatted_time})."
        if not block_result:
            block_result = "There are no more classes today."
            current_day.school_over = True
    else:
        block_result = "There is no school today."
    return _rename_block(block_result)


def create_day_overview_result() -> str:
    if current_day.is_school_day:
        day_overview_blocks = []
        for time in sorted(
            SCHOOL_DATA["overview"][current_day.day_type][current_day.lunch].keys()
        ):
            class_time_difference = (
                datetime.datetime.combine(
                    datetime.datetime.now().date(),
                    datetime.datetime.strptime(time, "%H:%M").time(),
                )
                - datetime.datetime.now()
            )
            if class_time_difference > datetime.timedelta():
                day_overview_blocks.append(
                    _rename_block(
                        SCHOOL_DATA["overview"][current_day.day_type][
                            current_day.lunch
                        ][time]
                    )
                )

        day_overview_result = (
            "\n".join(day_overview_blocks) if day_overview_blocks else None
        )
        if not day_overview_result:
            day_overview_result = "There are no more classes today."
            current_day.school_over = True
    else:
        day_overview_result = "There is no school today."
    return day_overview_result


def create_week_overview_result() -> str:
    week_overview_result = []
    for i in range(7):
        date = datetime.datetime.now() + datetime.timedelta(days=i + 1)
        week_overview_result.append(
            f"{date.strftime('%a, %b %d, %Y')}: {SCHOOL_DATA['days'][date.strftime('%m/%d/%Y')]}"
        )
    return "\n".join(week_overview_result)


def main():
    _set_day_information()
    print(
        f"""🗓 Date 🗓
{create_day_result()}

📖 Current Class 📖
{create_block_result()}

📚 Day Overview 📚
{create_day_overview_result()}

📋 Week Overview 📋
{create_week_overview_result()}
"""
    )
    pass


if __name__ == "__main__":
    main()
