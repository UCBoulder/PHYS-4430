# Use the official Ruby image from the Docker Hub
FROM ruby:2.7

# Install dependencies
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    libpq-dev \
    nodejs \
    pandoc \
    python3-pip

# Install pandoc-xnos filters via pip
RUN pip3 install pandoc-xnos pandoc-fignos pandoc-eqnos pandoc-tablenos pandoc-secnos --user

# Add the user's local bin directory to the PATH
ENV PATH=$PATH:/root/.local/bin

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