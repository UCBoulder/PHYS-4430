# Use the official Ruby image from the Docker Hub
FROM ruby:3.3.4

# Install dependencies
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    libpq-dev \
    nodejs \
    pandoc \
    python3-pip \
    python3-venv \
    dos2unix

# Create a virtual environment and install pandoc-xnos filters via pip
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install pandoc-xnos pandoc-fignos pandoc-eqnos pandoc-tablenos pandoc-secnos

# Update RubyGems to a compatible version
RUN gem update --system 3.3.22

# Set the working directory
WORKDIR /usr/src/app

# Copy the Gemfile and Gemfile.lock into the image
COPY Gemfile* ./

# Install the gems specified in the Gemfile
RUN gem install bundler:2.4.17 && bundle install

# Copy the rest of the application code into the image
COPY . .

# Expose port 4000 to the host
EXPOSE 4000