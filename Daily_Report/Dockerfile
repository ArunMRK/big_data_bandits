# base image to be used
FROM public.ecr.aws/lambda/python:3.9

# add requirements file to dir
COPY requirements.txt "${LAMBDA_TASK_ROOT}"

# install requirments
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# add necessary files
COPY  .env "${LAMBDA_TASK_ROOT}"
COPY daily_reports.py "${LAMBDA_TASK_ROOT}"
COPY data_extraction.py "${LAMBDA_TASK_ROOT}"
COPY sqlwrapper.py "${LAMBDA_TASK_ROOT}"
COPY html_script.py "${LAMBDA_TASK_ROOT}"

CMD [ "daily_reports.lambda_handler" ]