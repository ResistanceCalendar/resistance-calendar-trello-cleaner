#!/usr/bin/python

import argparse
import distutils.util
import requests
import sys
import webbrowser
from trello import TrelloApi
from local_settings import *

parser = argparse.ArgumentParser(description='Resistance Calendar Trello ETL')
parser.add_argument('--boards', required=True, type=str, nargs='+',
                    help='board names, using single quotes \'My Board\'. Multiple can be defined \'Board a\' \'Board b\'')
parser.add_argument('--dry_run', type=distutils.util.strtobool, default='true',
                    help='when false, logs changes it would make but does not alter data')
args = parser.parse_args()

try:
    trello = TrelloApi(TRELLO_APP_KEY)
except NameError:
    print 'No TRELLO_APP_KEY settings found, please generate via the following URL and place in local_settings.py:'
    print '  - https://trello.com/1/appKey/generate'
    sys.exit()

try:
  trello.set_token(TRELLO_USER_TOKEN)
except NameError:
    print 'No TRELLO_USER_TOKEN settings found, please generate via the following URL and place in local_settings.py:'
    print '  - ' + trello.get_token_url('resistance-calendar-etl', expires='1day', write_access=True)
    sys.exit()

dry_run_prefix = ''
if True == args.dry_run:
    dry_run_prefix = '[dry_run]'

INDEX_NAME_FIELD  = 0
INDEX_EMAIL_FIELD = 1
INDEX_LINK_FIELD  = 2

################################################################################
# Looks thtough the card content and suggests labels as a dict with name and
# color based on string matches
#
def suggest_card_labels(card):
    labels = []
    card_fields = card['desc'].split('\n')
    link = card_fields[INDEX_LINK_FIELD]

    if 'www.facebook.com' in link:
        labels.append({'name':'FACEBOOK','color':'blue'})
    elif 'moveon.org' in link:
        labels.append({'name':'MOVEON', 'color':'blue'})
    elif eventbrite.com in link:
        labels.append({'name':'EVENTBRITE', 'color':'blue'})
    elif meetup.com in link:
        labels.append({'name':'MEETUP', 'color':'blue'})

    return labels

################################################################################
# Looks thtough the card content and suggests labels as a dict with name and
# color based on string matches
#
def suggest_card_name(card):
    card_fields = desc.split('\n')
    return card_fields[INDEX_NAME_FIELD][6:]

member = trello.members.get(TRELLO_MEMBER_NAME)
print ('username: %s with %d board(s) found' % (member['username'], len(member['idBoards'])))

for board_id in member['idBoards']:
    board = trello.boards.get(board_id)
    print ('Investigating Board "%s"' % board['name'])

    if board['name'] not in args.boards:
        print ('Skipping non-whitelisted board "%s"' % board['name'])
        continue

    # NOTE: It would be safer to limit to a list vs query the entire board
    cards = trello.boards.get_card(board_id)
    new_cards = filter(lambda x: x['name'] == 'NEW EVENT', cards)
    print ('%d out of %d cards are named "NEW EVENT"' % (len(new_cards), len(cards)))

    # Eample card as specified in the webflow form emailer action
    # Name: Some event
    # Email: some.email@gmail.com
    # Link: https://www.facebook.com/events/1832911003613719/?acontext=%7B%22source%22%3A5%2C%22page_id_source%22%3A1598182536873570%2C%22action_history%22%3A[%7B%22surface%22%3A%22page%22%2C%22mechanism%22%3A%22main_list%22%2C%22extra_data%22%3A%22%7B%5C%22page_id%5C%22%3A1598182536873570%2C%5C%22tour_id%5C%22%3Anull%7D%22%7D]%2C%22has_source%22%3Atrue%7D

    for new_card in new_cards:
        desc = new_card['desc']
        # TODO: Add safety filter here -- desc.find('liberal snowflake')

        new_name = suggest_card_name(card)
        print '%s converting name %s to %s' % (dry_run_prefix, new_card['name'], new_name)
        if False == args.dry_run:
            trello.cards.update_name(new_card['id'], new_name)

        # This can technically be done on any card, but limiting to
        # new cards for now
        for label in suggest_card_labels(new_card):
            if len(filter(lambda l: l['name'] == label['name'], new_card['labels'])) == 0:
                print('%s labeling with: %s' % (dry_run_prefix, label['name']))
                if False == args.dry_run:
                    # trello API does not work due to a bug, so use HTTP POST
                    requests.post(
                        url  = 'https://api.trello.com/1/cards/%s/labels' % new_card['id'],
                        data = {
                            'name':  label['name'],
                            'color': label['color'],
                            'key':   TRELLO_APP_KEY,
                            'token': TRELLO_USER_TOKEN
                        }
                    )
