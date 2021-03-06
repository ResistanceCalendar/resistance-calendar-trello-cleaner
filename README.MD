# Resistance Calendar Trello Cleaner

## Background

The intent is to assist curators in cleaning trello boards of auto generated content set to it by webflow

It is based on the the [trello python library](https://pythonhosted.org/trello/index.html)

In order to run, update create a local_settings.py file with the following fields:
```
TRELLO_MEMBER_NAME  = [VALUE]
TRELLO_APP_KEY      = [VALUE]
TRELLO_USER_TOKEN   = [VALUE]
```

**TRELLO_APP_KEY** can be generated via https://trello.com/1/appKey/generate

**TRELLO_USER_TOKEN** can be generated via https://trello.com/1/authorize?key=[TRELLO_APP_KEY]&name=resistence-calendar-etl&expiration=1day&response_type=token&scope=read,write

## Installation

pip install -r requirements.txt

## Running

Application runs in dry model by default, see documentation below to enable

Usage available via python trello_cleaner.py --help

```
resistance-calendar-etl $> python trello_cleaner.py --help
usage: trello-cleaner.py [-h] --boards BOARDS [BOARDS ...] [--dry_run DRY_RUN]

Resistance Calendar Trello ETL

optional arguments:
  -h, --help            show this help message and exit
  --boards BOARDS [BOARDS ...]
                        board names, using single quotes 'My Board'. Multiple
                        can be defined 'Board a' 'Board b'
  --dry_run DRY_RUN     when false, logs changes it would make but does not
                        alter data
```

## Examples

Whitelisting skips other boards
```
resistance-calendar-etl $> python trello_cleaner.py --boards '*Tutorial Board (Start Here!)'
Investigating Board "*Tutorial Board (Start Here!)"
0 out of 6 cards are named "NEW EVENT"
[dry_run] Investigating Board "Example Board"
[dry_run] Skipping non-whitelisted board "Example Board"
```

Turning off dry_run
```
resistance-calendar-etl $> python trello_cleaner.py --boards '*Tutorial Board (Start Here!)' --dry_run=False
username: XXXXXXX with 2 board(s) found
Investigating Board "*Tutorial Board (Start Here!)"
Skipping non-whitelisted board "*Tutorial Board (Start Here!)"
Investigating Board "Example Board"
300 out of 2034 cards are named "NEW EVENT"
converting name NEW EVENT to Some event
labeling with: FACEBOOK
```
