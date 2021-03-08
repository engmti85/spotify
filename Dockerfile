# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
WORKDIR /app
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["SpotifyEndpoint.py"]
