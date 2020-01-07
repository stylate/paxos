## Question 1 - Message Service

The service is created as a Node.js/Express application deployed onto a Docker container. 

### Concept

This application is a simple message service that acts as a key-value store with the key being a SHA256 hash digest and the value being a message that the user sends through a POST request (typically a JSON object). 

### Setup

The dependencies used in this application are: express, crypto (built-in Node), body-parser, jest, and cors. In the docker image, these dependencies should already have been installed. We should have docker, docker-machine, and docker-compose installed as well!

#### Local

However, if you _*are*_ interested in running the code locally, consider the following commands:

```
npm install
npm run start
```
The service's functionality is tested through Jest in the file `message.test.js`, and can be run through `npm run test`. The  test cases in the section *Usage* are meant to test the service through HTTP rather than functionality.

#### Docker

As previously mentioned, we should have docker, docker-machine, and docker-compose installed already. We'll be using a local VM with a docker machine for this service. 

If we already don't have a machine running, run the follow commands to create a default VirtualBox VM.

```
docker-machine create --driver virtualbox default
docker-machine env default
eval "$(docker-machine env default)"
```

We can now run our container! Change your working directory to `message-service` and input the following commands in one terminal window:

```
docker-compose build
docker-compose up
```

Our docker container by default will now be accessible through the following endpoint: `http://192.168.99.100:8080/`. Your machine's IP address/URL may be different, however. You should double check by running `docker-machine ls`. The port `8080` will always be exposed due to the Dockerfile in place.

### Usage

Consider making the following requests through Postman or the terminal - up to you. For this specific scenario, we'll be using `curl` in our terminal.

To make a `POST` request to `/messages`, input the following command:

```
curl -X POST -H "Content-Type: application/json" -d <message> http://192.168.99.100:8080/messages
```

If done correctly, we should get an output similar to the following:

```
$ curl -X POST -H "Content-Type: application/json" -d '{"message": "foo"}' http://192.168.99.100:8080/messages
{"digest":"cbd7ad8022ab50b7b13c4d1027a848ac14d1a4bb8c656f1d0a2d6223fbe387e0"}%
```

To make a `GET` request to `/messages:hash`, such that `hash` is our SHA256 hash digest, input the following command:

```
$ curl http://192.168.99.100:8080/messages/:hash
```

If done correctly, we should get an output similar to the following:

```
$ curl http://192.168.99.100:8080/messages/cbd7ad8022ab50b7b13c4d1027a848ac14d1a4bb8c656f1d0a2d6223fbe387e0

HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: text/html; charset=utf-8
Content-Length: 17
ETag: W/"11-sQyloL4x40yYZGjKm1eSnOGidog"
Date: Tue, 07 Jan 2020 03:41:39 GMT
Connection: keep-alive

{"message":"foo"}%
```

If `hash` is invalid, we instead get the following:

```
$ curl http://192.168.99.100:8080/messages/cbd7ad8022ab50b7b13c4d1027a848ac14d1a4bb8c656f1d0a2d622

HTTP/1.1 404 Not Found
X-Powered-By: Express
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Content-Length: 31
ETag: W/"1f-mbEpO3xcvrkRw5FOKy5nOJE38tg"
Date: Tue, 07 Jan 2020 03:42:46 GMT
Connection: keep-alive

{"err_msg":"Message not found"}%
```

### Scaling

The bottlenecks in my application as I acquire more users would most definitely be involving concurrency. For instance, what if we had an extremely large amount of users who all perform `POST` requests, especially with large messages? Clearly, our current local application would fail at successfully fulfilling all of these requests, especially if these requests contain large messages/JSON objects. This is due to our object `digests` becoming too big (which is represented as a dictionary).

In order to adjust for these worst-case scenarios, the database that stores all of the hashes and original messages should be routed to a NoSQL database, like Redis or DynamoDB. We can also implement an LRU cache in order to evict messages that previously weren't retrieved through a `GET` request if we want to go the extra mile in the scenario that we have _*too*_ many messages being stored. 

Furthermore, if a said message `m` was particularly large in question, say 200 MB+, we could also house the original message in another database (although this is optional). To better illustrate this idea, we have one database that stores the hashes as the key and an encrypted message of length 32 as the value. This value can then be used as a key to access the original message in another database. 

This ensures that our messages are tightly secured (although this extra layer of indirection is _*entirely*_ optional) and that we can account for the hypothesis that a large amount of users would be concurrently sending in messages with extremely large amounts of data. Our NoSQL database(s) would also be presumably ACID compliant.

### Deployment

Currently, how our application is deployed is through a Docker container. But what if we want this application to be maintained in the long term? We can consider placing this application, along with its databases (assuming we scale with NoSQL) and dependencies in a Kubernetes cluster to ensure that this message service stays running for an indefinite period of time. This also guarantees that our service can be self-sufficient; that is, updates are readily available without downtime and recovery is possible in case of failure.