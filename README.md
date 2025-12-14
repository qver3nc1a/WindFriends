# WindFriends

Find other wind lovers and meet up!

## Overview
WindFriends is a web application built with Python Flask that helps users who love windsurfing discover like-minded people, meet up and catch the best wind gusts together

## Features
- Accounts: users can create an account
- Suggest a meeting: suggest a time and place, tell them which gear you prefer and briefly explain what you'd like to do. Feel free to edit the details later
- View meetings: check out what others have suggested

## Installation guide
### Install Flask
```
$ pip install flask
```
### Initialize a new database
```
$ sqlite3 database.db < schema.sql
```
### Run the application
```
$ flask run
```

## How to test
- Register a new user, then log in
- Create a meeting, optionally add tags
- View the meeting; edit or delete it (only creator can)
- Search by keyword and by tags on the Search page
- Ask the meeting organizer a question

## Security notes
- Passwords are hashed
- Forms use CSRF tokens on modifying actions
- SQL queries use parameters (no string concatenation)

## Large dataset performance
To test usability with large datasets, you can seed the database using `seed.py`

### seed.py
This script inserts:
- 1,000 users
- 100,000 meetings (with minimal defaults and randomized titles/gear)
- 1,000,000 messages

Run seeding from the project root:
```
$ python seed.py
```

### Indexes
schema.sql defines indexes to speed up common queries:
- `idx_meetings_date` on `meetings(date)` (for sorting/filtering by date)
- `idx_meetings_user` on `meetings(user_id)` (for filtering by creator)
- `idx_messages_meeting` on `messages(meeting_id)` (for loading messages for meetings)

## Large dataset test
I validated the app on a seeded database with 1 000 users, 100 000 meetings, and 1 000 000 messages

### My observations

- App booted normally
- Meetings page loaded well
- Meetings view with messages worked properly
- Keyword search returned results within a reasonable time

### Note!
Seeding took some time due to single-row inserts, so run seed.py once and reuse for testing