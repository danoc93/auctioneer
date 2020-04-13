# Auctioneer

The Auction-As-A-Service service monorepo.

You can use the helper [Makefile](Makefile) commands to manage certain operations in the application.

It requires [pipenv](https://github.com/pypa/pipenv) to be available as it is the core dependency service.

OAuth2 is used by the Management API and Authorization Service to ensure the consumer is allowed to access operations.

## Parts

The current system requires five individual parts working together. While these are maintained as a few apps part of a single Django Project, they could easily be scaled individually as microservices.

### Auctioneer Management API

Exposed to manage auctions, bids, and explore available items. It is structured mainly within the [auctions](auctions) folder.

The API requires bearer tokens to be provided in all non-public operations. These tokens can be obtained via the Auctioneer Authorization API.

Exposed under `/api/v1`

The project generates an [Open API](https://swagger.io/docs/specification/about/) schema for the API, as well as a Swagger UI documentation explorer under ```/api/v1/docs```. This has been chosen given that the Specification is a standardized way of documenting APIs, unlike the built-in DRF generator. This relies on the ```drf-yasg``` schema generating library.

The Documentation explorer is a fully integrated front-end that allows you to interact with the API directly.

### Auctioneer Authorization API

Used as a simple interface to get access tokens and manage accounts for the Auctioneer Management API.

It talks to the Authentication Service via the corresponding API using the configured client credentials.

This requires the following environment variables to be defined:
```
OAUTH_CLIENT_SECRET
OAUTH_CLIENT_ID
OAUTH_TOKEN_URL
OAUTH_TOKEN_REVOKE_URL
```

Exposed under `/api/auth`

### Authentication Service API

Authentication service to grant the corresponding access tokens. Implemented with the oauth2 toolkit under the same project. However, independent from the other APIs, as it could live separately in its own service.

Exposed an api under `/o`

### Workers

Workers are setup via CRON to execute routine tasks. Currently, the most important worker sets the status of expired auctions as fulfilled. In theory this worker could be expended to be more useful, e.g. emailing users with their corresponding bids or setting up auto payments in a production-ready implementation.

### Database

At the core of this project is a database built from the model definition migrations and a single initial metadata script to populate the corresponding tables (country, currency, item_condition, etc).

This uses the default sqlite implementation, however it should be trivial to expose this via a database cluster if desirable.

## Setup

As it stands, this is a single Django project. The migration folders have been generated via ```scripts/prepare.sh``` and committed.

1. Clone this repo.
2. Install ```pipenv``` in your environment and add it to the PATH.
3. Run ```make setup```, this will install dependencies and apply the migrations on the system.
4. Whitelist the required hosts via ```ALLOWED_HOSTS``` in your project settings files.
5. Create the first superuser ```make create-super-user```.
6. Run your server with ```make start-background-server``` and access ``/admin``.
7. Under Applications register your API with the "Resource owner password-based" flow. Copy the client_id and the client_secret before closing it.
8. Kill the server.
9. Start the server (include the actual values for the variables) ```make start-background-server```.
10. Start the workers with ```make start-background-workers```.
11. Run the tester from a different context and give it the desired API endpoints. It should not fail.
12. Validate the Management API docs under ```/api/v1/docs``` is accessible from the outside.

If something breaks, remove the generated DB file and repeat every step from (4) and onwards.

## Testing

A tester file has been provided under ```e2e```. This tester will run against the API endpoints provided as arguments.

This tester generates unique ids to run experiments. Potentially, since it depends on a worker, you may end up with auctions that haven't been marked as fulfilled immediately. 