# CS423

Long Island City Event Syndication


# Long Island City Event Syndication

## Getting Started

- Ensure that python 2 is installed and available in your path
    - It's recommended to use the `pyvenv` utility to manage dependencies separately from other projects.
    - To do this make a folder anywhere on your system to house the environment (I recommend something like `~/syndication_venv`) and run `pyvenv PATH_TO_ENVIRONMENT`

- Install dependencies
    - In the project root run `pip install -r requirements.txt`
        -This will install all dependencies in the folder you configured in the previous step

- Run the app
    - If you are running locally, you must add loopback.pizza to your hosts file, mapped to 127.0.0.1 since Facebook requires requests to come from a domain.
    - In the project root, run runserver.sh script. This script exports all the sensitive variables and runs the server.
    - Navigate to http://loopback.pizza:8000/eventsyndication/ to see the homepage.

- Troubleshoot
    - Make sure you have a mysql database running.
