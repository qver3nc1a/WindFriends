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