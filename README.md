## Components

- Poller that invokes the btc api and hydrates the dynamo table with the bitcoin prices
    - montecarlo/producer/lambda_function.py
- API Handler that serves requests
    - montecarlo/lambda/api_request_handler.py
- Metric Gatherer with business logic to obtain the information requested by the api.
    - montecarlo/lambda/metric_gatherer.py
- Spins up a cdk stack with the data in us-east-2
    - [montecarlo_stack py](montecarlo_stack.py)

## Features implemented

- The app will query data from a publicly available source at least every 1 minute (try https://docs.cryptowat.ch/rest-api/ to get cryptocurrency quotes, 
- The app has a REST API to enable the following user experience (you do not need to implement the user interface):
  obtain metrics for a given id, and its rank.
- The app will log an alert whenever a metric exceeds 3x the value of its average in the last 1 hour. 

## API Endpoint to test with:
https://q74w4ov0i6.execute-api.us-east-2.amazonaws.com/prod

## API endpoints

    curl {API_ENDPOINT}/prod/metrics
        Gets available coins

    curl {API_ENDPOINT}/prod/metrics/dogeusd
    curl {API_ENDPOINT}/prod/rank/dogeusd
    curl {API_ENDPOINT}/prod/metrics/btcusd
    curl {API_ENDPOINT}/prod/rank/btcusd
    curl {API_ENDPOINT}/prod/metrics/ltcusd
    curl {API_ENDPOINT}/prod/rank/ltcusd

## Alerts

    - Emits an alert of format: ("Alert " + coin_price + " " + coin_name) when price exceeds 3 * mean
    - Future steps: 
        - Set up an SES email integration based off this log message: custom meric filter -> SES to be asynchronous while handling this alert.
        - The values in the db could be prefixed with the timestamp in case the hydrator for the values (poller
          component) crashes. Right now, we rely on those values being present and the poller never crashing.

### CDK Details

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

```
source aws creds
```
