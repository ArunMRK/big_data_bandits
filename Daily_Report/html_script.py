from typing import NoReturn
import datetime

TODAY = datetime.datetime.now()


def gender_list(genders: dict) -> str:
    """Creates a HTML list element that contains the genders and how many riders are of that gender
    """
    html_code = """<ul> <h2>Genders</h2>"""

    for gender in genders.keys():
        html_code += f"{gender[0].upper() + gender[1:]}: <b>{genders[gender]}</b> <br>"
    html_code += "</li>"

    return html_code


def make_html_report(
    num_of_rides: int, ages: dict, genders: dict, averages: dict, totals: dict
) -> NoReturn:
    """Makes a html file based on the daily data"""
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Daily Report</title>
    </head>
    <h1 style="text-align: center;">Deloton Daily Report for {TODAY.year}-{TODAY.month}-{TODAY.day}</h1>
    <hr>
    <div style="display: flex;">
        <div style="flex: 25%; text-align: center; padding: 5px;">
            <ul>
                <h2>Total Values</h2>
                Total Rides: <b>{num_of_rides}</b> <br>
                Total Duration:<b>{round(totals["total_duration"])} s</b> <br>
                Total Power: <b>{round(totals["total_power"], 2)}</b> <br>
            </ul>
        </div>

        <div style="flex: 25%; text-align: center; padding: 5px;">
            <ul>
                <h2>Average Values</h2>
                Average Duration: <b>{round(averages["avg_duration"], 2)} s</b> <br>
                Average RPM: <b>{round(averages["avg_rpm"], 2)}</b> <br>
                Average Power: <b>{round(averages["avg_power"], 2)}</b> <br>
                Average Resistance: <b>{round(averages["avg_resistance"], 2)}</b> <br>
                Average Heart Rate: <b>{round(averages["avg_heart_rate"], 2)} bpm</b> <br>
            </ul>
        </div>

        <div style="flex: 25%; text-align: center; padding: 5px;">
            <ul>
                <h2>Ages</h2>
                <18: <b>{ages["<18"]}</b> <br>
                18-24: <b>{ages["18-24"]}</b> <br>
                25-34: <b>{ages["25-34"]}</b> <br>
                35-44: <b>{ages["35-44"]}</b> <br>
                45-54: <b>{ages["45-54"]}</b> <br>
                55-64: <b>{ages["55-64"]}</b> <br>
                65+: <b>{ages["65+"]}</b> <br>
            </ul>
        </div>

        <div style="flex: 25%; text-align: center; padding: 5px;">
            {gender_list(genders)}
        </div>
    </div>
    </html>
    """

    with open(f"/tmp/report.html", "w") as f:
        f.write(html)
