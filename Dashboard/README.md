# Dashboard

- This folder contains all necessary scripts for running the live dashboard

## Running Locally

- Download entire <code>Dashboard/</code> folder
- Install required libraries
  - <code>pip3 install -r requirements.txt</code>
- Run Dash app
  - <code>python3 app.py</code>

## Running on AWS

- Download entire <code>Dashboard/</code> folder
- Create an AWS EC2 instance, _making sure to choose **Auto-assign public IP** in network settings while launching_
- Secure copy all the files from your local machines into your EC2 instance (.pem key will be needed)
  - <code>scp -i path/to/key/key.pem path/to/directory/Dashboard/\* ec2-user@<YOUR_Public_IPv4_DNS_EC2>:.</code>
- NOTE: folders cannot be copied using scp; you will have to individually move the files around once they are copied into EC2
- Connect to your EC2 instance's terminal and install requirements
  - <code>pip3 install -r requirements.txt</code>
- Make a window such that the EC2 instance can run persistently
  - <code>sudo yum install tmux</code>
  - <code>tmux new -s dahsboard_window</code>
- Move into your newly created window
  - <code>tmux a -t dashboard_window</code>
- Run the Dash app
  - <code>python3 app.py</code>
- Navigate to the instance's IP address in your browser to see the dashboard (under Public IPv4 address when you click on your instance in the AWS EC2 dashboard)
