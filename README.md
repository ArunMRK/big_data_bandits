# Deloton Exercise Bikes

Deloton Exercise Bikes have tasked us with extracting a continuous stream of data coming from their exercise bikes regarding rides and users. 
The incoming data was unstructured and dirty meaning that it had to be cleaned so it could be easily used for the deliverables.

## Data Warehouse
- The data warehouse is stored on AWS RDS and consists of user details and ride details tables. This data is only dumped to the warehouse once a new user appears in the stream, such that all the data stored in the ride details is aggregated and contains useful insights for analysis.
- There exists a local storage within the script that stores the current users ride details such that it can be used for the heart rate alerts.
The data warehouse ingestion script is hosted on AWS EC2 and runs persistently.

## Heart Rate Alerts
- The aim of this deliverable was to send an email (AWS SES) once a users heart rate went outside of their maximum allowed working heart rate, calculated using (220 - age) * 0.85.
- Whenever a new user is spotted in the stream, their maximum allowed heart rate is calculated and used to compare against their current heart rate.
- If the users heart rate exceeds the maximum allowed heart rate 5 consecutive times, then an email is sent, within 15 seconds, to alert that their heart rate has exceeded the allowed limit.
- We implemented a trigger that only allows one email to be sent per ride, with the aim of reducing spam.
- This heart rate alert system runs within the data warehouse ingestion script (AWS EC2) in order to have quick access to the users heart rate.

## Live Dashboard
- We developed a live dashboard containing information about a current user on a ride, and information about ride in the past 12 hours.
- The dashboard is running persistently on AWS EC2.
- Current Ride:
	- The current ride data updates every 15 seconds in order for the user to get the most recent data regarding their ride.
	- The included data is the users demographics, along with their ride statistics, such as their current heart rate and whether it is in the healthy range.
	- Alongside that, their duration is shown along with their mean and total power outputs.
- Recent Rides:
	- The recent rides section updates every 10 minutes (approximately how long each ride is historically), and displays the past 12 hours of ride data.
	- Recent ride data includes the mean total power output, along with the total power output of all rides.
	- Some figures are present that show the age distribution of riders, and gender distributions accross rides and durations.

## Daily Report

- A daily report that sends the past 24 hours worth of data to the CEO of Deloton, at 5pm.
- The report contains average and total values of interesting aggregate data that will be useful to the business, along with some figures to show the gender and age distributions of the rides over a 24 hour period.
- The daily report script runs in a AWS Lambda function that is triggered daily at 5pm - this results in an email being send to the CEO using AWS SES.

## RESTful API

- This RESTful API allows for easy communication between the user and the database hosted on AWS RDS.
- It contains a landing page that lists all functionalities of the API and how to use them.
- The included endpoints are:
	- Get a ride with a specific ID
	- Get rider information with a specific user ID
	- Get all rides for a user with a specific ID
	- Delete a ride with a specific ID
	- Get all daily rides, along with getting all rides for a user-defined date
- This API runs persistently on AWS EC2 and communicates with AWS RDS.

## Tableau Integration

- Tableau integration allows for an easy mean of access to the data warhouse in order to quickly access and analyse data.
- Not only does it have some pre-defined analytics, it allows the user to create their own analytics to suit their needs.

## Developers

- Big Data Bandits:
    - **Justas Bauras** (Project Manager I, Quality Assurance II, Engineer)
     - **Arun Kalia** (Architect I, Project Manager II, Engineer)
    - **Ben Douglas-Griffiths** (Quality Assurance I, Architect II, Engineer)
