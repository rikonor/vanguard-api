Vanguard API
===

This is a working proof-of-concept web-scraping based API for a [personal investor account][1] on [The Vanguard Group][2].

This is to serve as a possible starting point for a highly-usable API for investment bots and as a learning exercise on how to programmatically interact with a website from which we'd like to extract information and/or induce some user action.

Architecture
---

#### 1. User facing API

Our desired product is an API with a pre-defined set of operations the user can perform. The user has access to these operations using a standard RESTful service.

Prior to initial use, the user may register with the service and enroll in the Vanguard service (notice additional services can be added in the future, e.g. Fidelity, Schwab, etc).

Post-registration, the user may make any requests he desires to receive the relevant information regarding his account, this includes **Total Assets**, **Current Holdings**, **Open Orders**, etc.

The user should also be able to perform destructive operations if he desires to do so, such as **Place Order**, **Transfer Funds**, etc.

#### 2. Vanguard facing API (Selenium-based)

Once a user makes a request to the API, we start a selenium session in the background in order to perform the requested operation.

Operations are implemented by using the Selenium API to manipulate the webpage until the desired effect is achieved (finding information, filling out forms, clicking buttons, etc).

This means that any operation we perform is going to happen by literally browsing the site and parsing it's content. Although this is slow and may render this project unusable for certain use-cases - it still allows us to programmatically interact with a resource to which we had no such access before.

Usage
---

#### 1. Installation using `docker-compose`

Use `docker-compose` to run everything locally.  
The included `docker-copose.yml` file defines a local stack comprising of a:

1. `mongodb` instance to hold all user data.
2. A single `selenium` node with Chrome.
3. The API running at port 5000.

To start it in the background, run `docker-compose up -d`.  
View the logs with `docker-compose logs`.

#### 2. Registering and enrolling in services

```
# Register User
$ curl -X POST --data '{"username":"<username>","email":"<email>","password":"<password>"}' http://localhost:5000/register

# Enroll in Service (Vanguard)
$ curl -X POST --data '{"username":"<username>","password":"<password>","service_info":{"service_name":"vanguard","username":"<username>","password":"<password>"}}' http://localhost:5000/enroll

# Submit Security Q&A
$ curl -X POST --data '{"username":"<username>","password":"<password>","service_info":{"service_name":"vanguard","question":"<question>","answer":"<answer>"}}' http://localhost:5000/register_security_answer
```

#### 3. Querying Operations

```
# My Details
$ curl --data '{"username":"<username>","password":"<password>"}' http://localhost:5000/my_details

# Total Assets
$ curl --data '{"username":"<username>","password":"<password>"}' http://localhost:5000/vanguard/total_assets

# Current Holdings
$ curl --data '{"username":"<username>","password":"<password>"}' http://localhost:5000/vanguard/current_holdings
```

Testing
---

The largest concern with an independent API which relies on an external service (in this case Vanguard's online dashboards) is making sure that breaking changes which are made to the external service are detected in a quick manner. It may be enough that an HTML element's id attribute is changed to break a certain API. Therefore integration tests should be run on a regular basis so we can detect when breakage has happened.

IMPORTANT NOTICE: Under no circumstance should an integration test have the goal of causing some change. Tests should be merely querying operations that theoretically should do no harm.

#### Configuring credentials for tests

The tests require that you provide your own account credentials under `seleniumapis/vanguard/tests_config.py`. This requires a `username`, `password` and your `security Q&As`.

#### Running the tests

Tests at the moment are implemented using the native `unittest` module and can be run using `nose` with `nosetests`.

Contributing
---

If you would like to contribute please consider opening an issue or a pull request. I am happy to collaborate and open to discussions about this project.

Resources
---
1. [Selenium Python][4]
2. [Docker Compose][3]
3. [Flask][5]


[1]: https://investor.vanguard.com/home "Vanguard Personal Investors"
[2]: https://en.wikipedia.org/wiki/The_Vanguard_Group "The Vanguard Group"
[3]: https://docs.docker.com/compose "Docker Compose"
[4]: http://selenium-python.readthedocs.org "Selenium Python docs"
[5]: http://flask.pocoo.org "Flask"
