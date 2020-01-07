# Paxos Coding Challenge

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

## Question 2 - Gift Purchasing

### Concept

Given a gift card with a set balance `b`, we want to _*maximize*_ its usage by spending as much as possible on two separate gifts for two separate friends. Given an input file containing a sorted list of unique identifiers and their balances, we can produce an efficient O(n) algorithm that outputs the most expensive gifts that can be purchased with our gift card.

### Usage

All inputs should go in the `gift/inputs` folder. The rest of the code is as follows in `gift`. It is assumed that the user has python3 installed. All libraries used (`sys`, `unittest`) are built-in. Set the working directory as `gift` and run the following command:

```
python solution.py <input file> <balance>
```

Our first parameter should be a .txt file and be well-formed, the second parameter being a positive integer, an example being as follows:

```
Candy Bar, 500
Paperback Book, 700
Detergent, 1000
Headphones, 1400
Earmuffs, 2000
Bluetooth Stereo, 6000
```

An example input should be `python solution.py inputs/prices.txt 10000`. An example output would appear as:

```
Earmuffs 2000, Bluetooth Stereo 6000
```

For testing, run `test_solution.py` by entering the command `python test_solution.py`. 

### Algorithm

Our following assumptions are as follows:

- Every item is unique in its identifier (prices can be non-unique).
- Our input list is sorted by price.
- We can only buy one of each item.
- An item's price is a strictly positive integer.
- Our input file is well-formed (each line follows the structure "(Unique Identifier), (Price)").

Recall that our list is sorted by price, and that we want to maximize the balance given in our gift card. To do this, we use a two-pointer approach with the pointers `left` and `right` such that `left` points to the first index and `right` points to the last index of our array `prices`. For *simplicity* of explanation, consider `prices` to be an array of item costs (without keeping in mind of the unique identifier). In order to retrieve the _*optimal*_ output, we set a variable `min_diff` to infinity. This will be explained in the next paragraph.

We thus approach this problem in a case-by-case analysis. Let `sum_prices` be the sum of our "left" item's price and our "right" item's price. In technical terms, we set `sum_prices = prices[left] + prices[right]`, and our balance `b`. We enter one of the three following cases until our two pointers meet:

- Case 1: `sum_prices < b`. We would have some balance leftover if we were to purchase the items pointed by `left` and `right`. However, we are not so sure if this is our _*best*_ option. Let our variable `leftover` be `b - sum_prices`. Recall that we have the variable `min_diff`. The smaller the difference, the more we used up of our gift card. This is our ideal situation, so we check if `leftover < min_diff`. If so, then we have a currently optimal combination of gifts.
- Case 2: `sum_prices == b`. We can immediately end our algorithm in this scenario; we have fully maximized our gift card balance with the current left and right items. This is what we should get for our two friends with the gift card.
- Case 3: `sum_prices > b`. Decrement the right pointer by one. In the next iteration, `sum_prices` may decrease as a result of the sorted property in `prices`.

By the time the while loop ends (the two points meet), we would have had our optimal combination of gifts (or no combination).

### Analysis

Our algorithm, entitled `find_gifts` in the python code, contains one `while` loop such that it ends only if case 2 is reached or if the two pointers meet. Given that `left` increments by 1, and `right` decrements by 1, our pointers will eventually meet. In the worst-case scenario, our `left` pointer iterates through the entire array forwards, or vice versa for our `right` pointer. The operations that are ran during this iteration all are ran in O(1) time, since they are simply math operations (comparisons, addition/subtraction). `find_gifts` is therefore a linear scan through `prices`, so our total runtime is O(n).

The algorithm's proof of correctedness is mainly discussed in the previous section--but in short, it has to do with the sorted property that `prices` contains by assumption. This allows our two-pointer implementation to make small adjustments towards maximizing the gift card balance, whether we increase or decrease `sum_prices` in the next iteration. 

### Possible Extensions

1. If we were to pick 3 gifts for 3 friends, we can adjust the algorithm by perhaps iterating through the `prices` array from index `0` to `len(prices) - 2` and running `find_gifts` on the entire list (without the current item `prices[i]` and the balance `b - prices[i]`). We add the result of `find_gifts` and `prices[i]` together. By the end of this algorithm, we should have the most optimal set of 3 gifts. The use of complements in this algorithm and adjusting for the 3-gift solution would thus increase our runtime from linear to quadratic in the worst-case scenario.
2. If we were not hypothetically able to load the file into memory, what we can do instead is use buffers in order to load parts of the file at a time while performing the same algorithm (with two pointers `left` and `right`, of course). Implementing this would be especially more difficult due to having to keep track of byte offsets as parts of the file get loaded into the buffers.