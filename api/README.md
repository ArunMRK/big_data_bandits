# API

- This folder contains all the files needed to run the API. The API queries from a postgres RDS database found on RDS. The API has the following end points, returning the data in a JSON format:

  - GET <code>/ride/:id</code>
    - Get a ride with a specific ID
  - GET <code>/rider/:user_id</code>
    - Get rider information (e.g. name, gender, age, avg. heart rate, number of rides)
  - GET <code>/rider/:user_id/rides</code>
    - Get all rides for a rider with a specific ID
  - DELETE <code>/ride/:id</code>
    - Delete a with a specific ID
  - GET <code>/daily</code>
    - Get all of the rides in the current day
  - GET <code>/daily?date=01-01-2020</code>
    - Get all rides for a specific date

## Running Locally

- Download the folder.
- In your terminal, run the following commands:
  - Install requirements: <code>pip3 install -r requirements.txt</code>
  - <code>export FLASK_APP=app.py</code>
  - <code>export FLASK_DEBUG=1</code>
  - <code>flask run --host=0.0.0.0 --port=8080</code>

This will allow you to view the API on your local browser.

## Running on AWS

Create an AWS EC2 instance with all the security groups you wish to open.Ensure your IAM user has the required permissions:

- S3fullaccess
- EC2fullaccess
- RDSfullaccess
- Secure copy all the files from your local machines into your EC2 instance (.pem key will be needed)

- <code>scp -i path/to/key/key.pem path/to/directory/API/\* ec2-user@<YOUR_Public_IPv4_DNS_EC2>:.</code>

- NOTE: folders cannot be copied using scp; you will have to individually move the files around once they are copied into EC2

- Connect to your EC2 instance's terminal and install requirements
  - <code>pip3 install -r requirements.txt</code>
- Make a window such that the EC2 instance can run persistently
  - <code>sudo yum install tmux</code>
  - <code>tmux new -s api_window</code>
- Move into your newly created window
  - <code>tmux a -t api_window</code>
- Run the api script
  - <code>export FLASK_APP=app.py</code>
  - <code>export FLASK_DEBUG=1</code>
  - <code>flask run --host=0.0.0.0 --port=8080</code>
    The app will be running on your EC2 instance’s public IP
