# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /streamlit

# Copy the current directory contents into the container at /streamlit
COPY . /streamlit

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit will run on
EXPOSE 8501

# Define the command to run Streamlit when the container starts
CMD ["streamlit", "run", "streamlit_view.py"]
