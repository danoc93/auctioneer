# Auctioneer System

BBK Cloud Computing Project

You can use the helper [scripts](scripts) folder to setup the application.

It requires [pipenv](https://github.com/pypa/pipenv) to be available as it is the core dependency service.

## Auctioneer

An Auction-As-A-Service service. The project generates an [Open API](https://swagger.io/docs/specification/about/) schema for the API, as well as a Swagger UI documentation explorer under ```/docs```.

OAuth2 is used by the Management API and Authorization Service to ensure the consumer is allowed to access operations.

### Management API

Exposed to manage auctions, bids, and explore available items. Consists of a few DJANGO apps under a single project.

### Authentication

Authentication service to grant the corresponding access tokens.
### Workers

Workers are setup via CRON to execute routine tasks. Currently, the most important worker sets the status of expired auctions as fulfilled.
