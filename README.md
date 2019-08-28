# SMS Demo

## Installation
1. Clone the repo to your server i.e. `git clone <repo>`
1. Move into the created directory i.e. `cd sms_demo`
1. Execute `python3 -m venv venv` to create a virtual environment for the application.
1. Execute `. venv/bin/activate` to activate the virtual environment.
1. Execute `pip3 install -r requirements.txt`
1. Execute `python main.py` to run the program

## Assumptions

1. Phone numbers will be validated accroding to the Kenyan format
1. All costs are in KSh.
1. For asyncronous delivery messages, we will only send the final ones back to the developers, intermediates will be ignored. Differences between the service providers have been harmonized. These are:
   - rejected: Downstream carrier refuses to deliver message
   - buffered: Message has been buffered for later delivery
   - delivered: Message has been delivered
   - failed: Message not delivered
1. the application will run on one server, so no need to have an external database(redis, etc) for storage.
1. deque.append() and deque.popleft() are thread-safe due to GIL
1. CPython implementation is used.