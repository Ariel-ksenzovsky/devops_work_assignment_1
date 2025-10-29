FROM python:3.7
# Copy the python script into the container
COPY ynet.py /app/ynet.py

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV RSS_URL=https://www.ynet.co.il/Integration/StoryRss2.xml

# Run app when the container launches
CMD ["python", "/app/ynet.py"]
