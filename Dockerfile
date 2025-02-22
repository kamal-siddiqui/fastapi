# Use AWS Lambda's official Python image as the base image
FROM public.ecr.aws/lambda/python:3.9

# Set the working directory inside the container
WORKDIR /var/task

# Copy the FastAPI app and other necessary files
COPY main.py .

# Install necessary dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Uvicorn (ASGI server) to run the app
RUN pip install uvicorn

# Install Mangum to run FastAPI on AWS Lambda
RUN pip install mangum

# Define the entry point for Lambda
CMD ["lambda_function.lambda_handler"]
