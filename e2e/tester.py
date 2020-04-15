import sys
import time
from datetime import datetime, timedelta
from random import randrange

import requests

if len(sys.argv) != 3:
    print('Arguments for Auctioneer Management API and Auctioneer Authorization API are required')
    exit()

management_api = sys.argv[1]
authorization_api = sys.argv[2]

print("Testing Management API", management_api, "& Authorization API", authorization_api)


def post(endpoint, data=None, headers={}):
    print('Making POST request to ', endpoint)
    r = requests.post(endpoint, json=data, headers=headers)
    try:
        json = r.json()
    except Exception as e:
        return r.text, r.status_code
    return json, r.status_code


def get(endpoint, headers={}):
    print('Making GET request to ', endpoint)
    r = requests.get(endpoint, headers=headers)
    try:
        json = r.json()
    except Exception as e:
        return r.text, r.status_code
    return json, r.status_code


def create_account(username, email, password, country_id, city_name):
    return post(authorization_api + '/register',
                {'username': username, 'password': password, 'email': email, 'country': country_id,
                 'city_name': city_name})


def open_auction(expires_in_seconds, title, ask, token):
    _from_now = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
    return post(management_api + '/auction/new', {
        "expiration_time_utc": _from_now.isoformat() + 'Z',
        "status": "open",
        "ask_amount_currency": "usd",
        "starting_ask_amount": ask,
        "international_delivery": "true",
        "item": {
            "title": title,
            "description": "No description",
            "condition": "new"
        }
    }, {'Authorization': 'Bearer ' + token})


def login(username, password):
    return post(authorization_api + '/login', {'username': username, 'password': password})


def generate_random_credentials():
    name = "account" + str(randrange(100000000))
    return name, name + '@email.com', randrange(100000000)


failures, passes = 0, 0

olgaCredentials = generate_random_credentials()
nickCredentials = generate_random_credentials()
maryCredentials = generate_random_credentials()

print('Created random credentials for Olga =>', olgaCredentials[0])
print('Created random credentials for Nick =>', nickCredentials[0])
print('Created random credentials for Mary =>', maryCredentials[0])

print('\n\nTest 1) Registration')

olga = create_account(olgaCredentials[0], olgaCredentials[1], olgaCredentials[2], 1, 'Test City')
nick = create_account(nickCredentials[0], nickCredentials[1], nickCredentials[2], 1, 'Test City')
mary = create_account(maryCredentials[0], maryCredentials[1], maryCredentials[2], 1, 'Test City')

print('{}: Successfully registered {}, got initial Bearer token {}'.format('Olga', olgaCredentials[0],
                                                                           olga[0]['access_token']))
print('{}: Successfully registered {}, got initial Bearer token {}'.format('Nick', nickCredentials[0],
                                                                           nick[0]['access_token']))
print('{}: Successfully registered {}, got initial Bearer token {}'.format('Mary', maryCredentials[0],
                                                                           mary[0]['access_token']))

if olga[1] != 200 or nick[1] != 200 or mary[1] != 200:
    failures += 1
else:
    passes += 1

print('\n\nTest 2) Login with new accounts')

olga = login(olgaCredentials[0], olgaCredentials[2])
nick = login(nickCredentials[0], nickCredentials[2])
mary = login(maryCredentials[0], maryCredentials[2])

if olga[1] != 200 or nick[1] != 200 or mary[1] != 200:
    failures += 1
else:
    passes += 1

print('{}: Successfully logged in, got session Bearer token {}'.format('Olga', olga[0]['access_token']))
print('{}: Successfully logged in, got session Bearer token {}'.format('Nick', nick[0]['access_token']))
print('{}: Successfully logged in, got session Bearer token {}'.format('Mary', mary[0]['access_token']))

print('\n\nTest 3) Request to authenticated endpoint with no token should fail')

print('Olga requesting member profile...')
res = get(management_api + '/member/account')

if res[1] != 401:
    print('Error: Expected 401 error, got ', res[1])
    failures += 1
else:
    passes += 1
    print('Good: Expected invalid credentials 401 error, got {}.'.format(res[1]))

print('\n\nTest 4) Olga should auction something for 1500 USD')

[olgaAuction, code] = open_auction(1200, "Olga's auction", 1500, olga[0]['access_token'])

if code != 200:
    failures += 1
    print('Unable to book Auction', res[0])
else:
    passes += 1
    print('Auction id = {}: {} expiring in {} seconds opened'.format(olgaAuction['auction_id'], "Olga's auction", 1200))

print('\n\nTest 5) Nick should auction something for 1500 USD')

[nickAuction, code] = open_auction(45, "Nick's auction", 1500, nick[0]['access_token'])

if code != 200:
    failures += 1
    print('Unable to book Auction', res[0])
else:
    passes += 1
    print('Auction id = {}: {} expiring in {} seconds opened'.format(nickAuction['auction_id'], "Nick's auction", 45))

print('\n\nTest 6) Mary should auction something for 1500 USD')

[maryAuction, code] = open_auction(30, "Mary's auction", 1500, mary[0]['access_token'])

if code != 200:
    failures += 1
    print('Unable to book Auction', res[0])
else:
    passes += 1
    print('Auction id = {}: {} expiring in {} seconds opened'.format(maryAuction['auction_id'], "Mary's auction", 30))

print('\n\nTest 7) Nick and Olga browse all open auctions')

nickOpenAuctions = get(management_api + '/auction/all?status=open',
                       {'Authorization': 'Bearer ' + nick[0]['access_token']})[0]
olgaOpenAuctions = get(management_api + '/auction/all?status=open',
                       {'Authorization': 'Bearer ' + olga[0]['access_token']})[0]

targets = [maryAuction['auction_id'], olgaAuction['auction_id'], nickAuction['auction_id']]
print('Expecting to find auctions: ', targets)

nickFound = 0
for auction in nickOpenAuctions:
    id = auction['id']
    status = auction['status']
    if status['value'] == 'open' and id in targets:
        nickFound += 1

olgaFound = 0
for auction in olgaOpenAuctions:
    id = auction['id']
    status = auction['status']
    if status['value'] == 'open' and id in targets:
        olgaFound += 1

if olgaFound == nickFound == 3:
    print('Nick and Olga found all new auctions as available for bidding')
    passes += 1
else:
    print('FAILURE!! Not all auctions are available')
    failures += 1

print('\n\nTest 8) Nick and Olga get the details of Mary''s item')

olgaItemDetails = get(management_api + '/auction/{}'.format(maryAuction['auction_id']),
                      {'Authorization': 'Bearer ' + olga[0]['access_token']})[0]

nickItemDetails = get(management_api + '/auction/{}'.format(maryAuction['auction_id']),
                      {'Authorization': 'Bearer ' + nick[0]['access_token']})[0]

if olgaItemDetails['item']['title'] == "Mary's auction" == nickItemDetails['item']['title']:
    passes += 1
    print('Both Nick and Mary fetched details of item with title', olgaItemDetails['item']['title'])
else:
    failures += 1
    print('Names do not match expected', olgaItemDetails['item']['title'], nickItemDetails['item']['title'])

print('\n\nTest 9) Mary should bid for her own item')

[response, code] = post('{}/auction/{}/bid'.format(management_api, maryAuction['auction_id']), {
    "bid_currency": "usd",
    "bid_amount": 4000
}, {'Authorization': 'Bearer ' + mary[0]['access_token']})

if code != 400:
    print('FAIL!!! Mary should not be allowed to bid on her own auctions expected 400 got', code)
    failures += 1
else:
    print('Got 400 error from server, Mary could not bid on her own auction!')
    passes += 1

print('\n\nTest 10) Nick and Olga should bid for Mary''s item')

print('Nick is bidding 4000 USD')
[nicksBid, _] = post('{}/auction/{}/bid'.format(management_api, maryAuction['auction_id']), {
    "bid_currency": "usd",
    "bid_amount": 4000
}, {'Authorization': 'Bearer ' + nick[0]['access_token']})

print('Olga is bidding 2500 USD')
[olgasBid, __] = post('{}/auction/{}/bid'.format(management_api, maryAuction['auction_id']), {
    "bid_currency": "usd",
    "bid_amount": 2500
}, {'Authorization': 'Bearer ' + olga[0]['access_token']})

if _ != 200 or __ != 200:
    failures += 1
    print('Unable to successfully bid, got', _, __)
else:
    print('Nick has a new bid id {}, Olga has a new bid id {}'.format(nicksBid['bid_id'], olgasBid['bid_id']))
    passes += 1

print('\n\nTest 11) The highest bidder should have won the auction')
print('Sleeping for 60 seconds to ensure the auction has been fulfilled by the worker and the winning bid assigned')
time.sleep(60)
marysAuctionStatus = get(management_api + '/auction/{}'.format(maryAuction['auction_id']),
                         {'Authorization': 'Bearer ' + mary[0]['access_token']})[0]

if marysAuctionStatus['status']['value'] != 'fulfilled':
    print('FAIL!! The auction has not been fulfilled, is the worker running? Status:',
          marysAuctionStatus['status']['value'])
    failures += 1
elif marysAuctionStatus['winning_bid']['id'] != nicksBid['bid_id']:
    print('FAIL!! Winning bid is not the highest bid')
else:
    print('Auction is fulfilled, bids can no longer happen.')
    print('Winning bid is highest bid.', nicksBid['bid_id'])
    passes += 1

print('\n\nTest 12) Olga browses all the items sold')

olgaFulfilledAuctions = get(management_api + '/auction/all?status=fulfilled',
                            {'Authorization': 'Bearer ' + olga[0]['access_token']})[0]

print('Expecting to find Mary''s auction in the list')

nickFound = 0
for auction in olgaFulfilledAuctions:
    id = auction['id']
    if id == maryAuction['auction_id']:
        nickFound = 1
        break

if nickFound:
    passes += 1
    print('Auction found as fulfilled!')
else:
    failures += 1
    print('Auction is not in the list of fulfilled things!')

print('\n\nTest 12) Mary queries for the history of bids in her auction')

[bidsOnMarysAuction, status] = get('{}/auction/{}/bids'.format(management_api, maryAuction['auction_id']),
                                   {'Authorization': 'Bearer ' + mary[0]['access_token']})

print('Should have a total of two bids')

if len(bidsOnMarysAuction['bids']) == 2:
    passes += 1
    print('Two bids were found in the element with ids', bidsOnMarysAuction['bids'][0]['id'],
          bidsOnMarysAuction['bids'][1]['id'])
elif status != 200:
    failures += 1
    print('FAIL!! The auction is possibly still open, history unavailable'.format(len(bidsOnMarysAuction['bids'])))
else:
    failures += 1
    print('FAIL!! Found {} bids!'.format(len(bidsOnMarysAuction)))

print('\n\nTest 13) Bidding less than the requested amount should trigger an error')

print('Olga is bidding 5 USD on Nick''s Auction (requested min 1500 USD)')
[olgasBid, __] = post('{}/auction/{}/bid'.format(management_api, nickAuction['auction_id']), {
    "bid_currency": "usd",
    "bid_amount": 5
}, {'Authorization': 'Bearer ' + olga[0]['access_token']})

if _ != 200 or __ != 200:
    passes += 1
    print('As expected, Olga is unable to bid, got HTTP ', __)
else:
    print('Olga should not have been allowed to bid bit got HTTP ', __)
    failures += 1

print('\n\nPASSES {}/{} FAILURES {}/{}\n\n'.format(passes, passes + failures, failures, passes + failures))
