from typing import NoReturn
from data_extraction import *
from html_script import make_html_report
import boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def load_to_s3() -> NoReturn:
    """Loads daily report data to an s3 bucket"""
    s3 = boto3.resource("s3")
    bucket = "big-data-bandits"
    directory = f"daily-reports/report_{TODAY.year}_{TODAY.month}_{TODAY.day}"

    s3.Bucket(bucket).upload_file(
        "/tmp/report.html", f"{directory}/report.html")
    s3.Bucket(bucket).upload_file("/tmp/age_distribution.jpg",
                                  f"{directory}/age_distribution.jpg")
    s3.Bucket(bucket).upload_file("/tmp/gender_distribution.jpg",
                                  f"{directory}/gender_distribution.jpg")


def send_email_with_attachment() -> NoReturn:
    """Creates the email that will be send to the recipient - contains code that allows for attaching files (in this case, it attaches the daily report along with 2 figures)
    """
    msg = MIMEMultipart()
    msg["Subject"] = f"Deloton Daily Report {TODAY.date()}"
    msg["From"] = "big.data.bandits@gmail.com"
    msg["To"] = "bicycle-ceo@sigmalabs.co.uk"

    body = MIMEText(
        f"To whom it may concern, \n\nPlease find attached the daily report and figures for {LAST_DAY.date()} to {TODAY.date()}. \nAll previous reports can be viewed at the following S3 URI: s3://big-data-bandits/daily-reports/ \n\nRegards,\nBig Data Bandits", "plain")
    msg.attach(body)

    # email attachments
    with open("/tmp/report.html", "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename="/tmp/report.html")
    msg.attach(part)

    with open("/tmp/age_distribution.jpg", "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename="/tmp/age_distribution.jpg")
    msg.attach(part)

    with open("/tmp/gender_distribution.jpg", "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename="/tmp/gender_distribution.jpg")
    msg.attach(part)

    ses_client = boto3.client("ses", region_name="eu-west-2")
    ses_client.send_raw_email(
        Source=msg["From"],
        Destinations=[msg["To"]],
        RawMessage={"Data": msg.as_string()}
    )


def lambda_handler(event: dict, context: dict) -> NoReturn:
    """Lambda handler function to be used with AWS Lambda"""
    rides = extract_last_day_data(LAST_DAY)
    num_of_rides = rides.shape[0]
    users = extract_last_day_users(rides)
    ages = extract_ages(users)
    genders = gender_distribution(users)
    gender_plot(genders)
    age_plot(ages)
    averages = extract_averages(rides)
    totals = extract_total(rides)
    print("Generating report...")
    make_html_report(num_of_rides, ages, genders, averages, totals)
    load_to_s3()
    try:
        send_email_with_attachment()
    except:
        print("Email unsuccessful")