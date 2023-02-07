# Data Warehouse and Heart Rate Alerts
- This folder contains all necessary scripts for data ingestion and loading to the data warehouse, along with the script that runs the heart rate alerts whenever the heart rate surpasses a threshold for a number of consecutive readings.
## Running Locally
- Download entire <code>Database/</code> folder
- Install required libraries
  - <code>pip3 install -r requirements.txt</code>
- Run ingestion script
  - <code>python3 ingestion.py</code>
## Running on AWS
- Download entire <code>Database/</code> folder
- Create an AWS EC2 instance, along with an AWS RDS database and AWS SES email service
- Secure copy all the files from your local machines into your EC2 instance (.pem key will be needed)
  - <code>scp -i path/to/key/key.pem path/to/directory/Database/* ec2-user@<YOUR_Public_IPv4_DNS_EC2>:.</code>
- NOTE: folders cannot be copied using scp; you will have to individually move the files around once they are copied into EC2
- Connect to your EC2 instance's terminal and install requirements
  - <code>pip3 install -r requirements.txt</code>
- Make a windows such that the EC2 instance can run persistently
  - <code>sudo yum install tmux</code>
  - <code>tmux new -s ingestion_window</code>
- Move into your newly created window
  - <code>tmux a -t ingestion_window</code>
- Run the ingestion script
  - <code>python3 ingestion.py</code>
