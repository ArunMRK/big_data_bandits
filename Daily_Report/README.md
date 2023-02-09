# Daily Report
- This folder contains all necessary scripts for the daily report script. The aim of this deliverable is to trigger an event that sends an email of the summary information for the last 24 hours, at a specific time of day (5pm in our case).
## Running on AWS
- Download <code>Daily_Report/</code> directory
- Build the Dockerfile
	- <code>DOCKER_BUILDKIT=0 docker build --platform x86_64 -t daily_reports:latest .</code>
	- NOTE: need to specify <code>--platform x86_64</code> as ARM processors are not widely used on AWS
- Create an AWS ECR repository where you will store the image
- Tag the Docker image
		- <code>docker tag daily_reports:latest <ECR_URI>/<REPO_NAME>:<IMAGE_TAG></code>
- Push the Docker image to ECR
	- <code>docker push <ECR_URI>/<REPO_NAME>:<IMAGE_TAG></code>
- Launch a AWS Lambda function and load the newly created image to it
- Create an AWS EventBridge trigger that activates the Lambda function at a given time (5pm in our case)
