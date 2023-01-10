# Architectural Design Comments

## Fly React Fly or Running To Stand Still

React doesn't want to live in a node process on a kubernetes cluster; React wants ultimately to live inside a user's browser, delivered there ideally in a static asset bundle with a bunch of minimized node modules packaged alongside.

Even if during this exercize we won't be implementing sending the whole app to a CDN, we can still package a static build, for practice.

We can see that our Progressive Web App implementation right now relies on the processes' `NODE_ENV`, which won't work the same in our static bundling.  We assume that the conversation concluded to the mutual satisfaction of all parties that PWA might be temporarily suspended as we figure out how exactly to re-enable it.

## Localhost and CORS

Front-end can't use localhost any more, since we are headed towards production.

Signing TLS/SSL certs isn't something we want to tangle with, so we'll see if we can alter our queries in a reasonable way.

## API Gateway <3's OpenAPI

Since we know that we'll be in the business of producing OpenAPI endpoints, basically every cloud provider has a good capability to deliver a CDN that can also perform routing _at least_, and can even do some authentication and authorization screens for us.

We also won't do that here, but we'll make sure the steps we do take are compatible.

## Connection Service needs help

Our Connection Service currently performs the following:

1. Loads a list of location data for a person
1. Loads all people into memory
1. For each location data item, queries the database for closeby location activity from persons
1. Combines the results of the people lookup and location data together to form the output

At scale, this will be a performance hotspot in more than one way.  Loading all people into object graph memory is going to be a problem; local heap is not where you want this residing in RAM.

Further, we have a hard binding now regarding PostGIS and the specifics of location checkin.  It would be reasonable to use our work on the Location object to begin sending that over the wire in order to power our solution.

## Location service can be internal

Our front-end is currently calling people and connections.  That is fine with us!  We can keep our location service internal.
