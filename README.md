## Components

- 

## Features implemented

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

Emits an alert of format: 
    ("Alert " + coin_price + " " + coin_name)
when price exceeds 3 * mean

Future steps: 
    Set up an SES email integration based off this log message: custom meric filter -> SES to be asynchronous while
    handling this alert.

[#](#) CDK Details

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
