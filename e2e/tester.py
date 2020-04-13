import sys

if len(sys.argv) != 3:
    print('Arguments for Auctioneer Management API and Auctioneer Authorization API are required')
    exit()

management_api = sys.argv[1]
authorization_api = sys.argv[2]

print("Testing Management API", management_api, "& Authorization API", authorization_api)