### backstop-sign-request

Example script to call a signed Backstop API request.

## Setup Instructions

Requires:

Python 3

pipenv. If you don't have pipenv, install it: 
`pip3 install --user pipenv`
On Windows, you might want to add pipenv to your path, see https://www.jetbrains.com/help/pycharm/pipenv.html

Use pipenv to install the dependencies:
`pipenv install`

## Setup
* The user who calls the API must have a Security Admin license, and no other licences.
* Your API allowance must be configured.

## Run:
* datafile or -d, contains the POST payload data
* keyfile.p12 or -k, is an API Signing Key downloaded from your Backstop User Profile page
* password or -p. is the API signing key file password you set when you created the API signing key. If you forget your password, you must generate a new signing key
* url or -u, is the full URL to the API, example: https://mysite.backstopsolutions.com/backstop/api/bulk-system-users
* username or -n,  is your Backstop username.
* token or -t, is your Backstop API token, which you can change on your Backstop User Profile page. The apitoken needs to be enclosed in single quotes.


On MacOS:
`pipenv run python3 BackstopSignRequest.py -d datafile.json -k keyfile.p12 -p password -u backstopurl -n username -t 'apitoken'`


On Windows:
`pipenv run python BackstopSignRequest.py -d datafile.json -k keyfile.p12 -p password -u backstopurl -n username -t apitoken`


or, use the sample script: 
MacOS:`backstop-sign-request.sh`
Windows:`backstop-sign-request.cmd`
