from typing import NoReturn
import datetime

TODAY = datetime.datetime.now()


def gender_list(genders: dict) -> str:
    """Creates a HTML list element that contains the genders and how many riders are of that gender
    """
    html_code = """<ul style="list-style-type:square;"> <h2>Genders</h2>"""

    for gender in genders.keys():
        html_code += f"<li>{gender[0].upper() + gender[1:]}: {genders[gender]}</li>"
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
        <body>
                <ul style="list-style-type:square;">
                    <h2>Total Values</h2>
                    <li>Total Rides: {num_of_rides}</li>
                    <li>Total Duration: {round(totals["total_duration"])} s</li>
                    <li>Total Power: {round(totals["total_power"], 2)}</li>
                </ul>
            <ul style="list-style-type:square;">
                <h2>Average Values</h2>   
                <li>Average Duration: {round(averages["avg_duration"], 2)} s</li>
                <li>Average RPM: {round(averages["avg_rpm"], 2)}</li>
                <li>Average Power: {round(averages["avg_power"], 2)}</li>
                <li>Average Resistance: {round(averages["avg_resistance"], 2)}</li>
                <li>Average Heart Rate: {round(averages["avg_heart_rate"], 2)} bpm</li>
            </ul>
            
            <ul style="list-style-type:square;">
                <h2>Ages</h2>
                <li><18: {ages["<18"]}</li>
                <li>18-24: {ages["18-24"]}</li>
                <li>25-34: {ages["25-34"]}</li>
                <li>35-44: {ages["35-44"]}</li>
                <li>45-54: {ages["45-54"]}</li>
                <li>55-64: {ages["55-64"]}</li>
                <li>65+: {ages["65+"]}</li>
            </ul>
            {gender_list(genders)}
        </body>
    </div>
        <div style="display: table-row">
            <img src="Data/age_distribution.png" alt="age_distribution" />
            <img src="Data/gender_distribution.png" alt="gender_distribution" />
        </div>
    </html>
    """

    with open("report.html", "w") as f:
        f.write(html)
