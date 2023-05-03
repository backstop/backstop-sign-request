#!/usr/bin/env python3


# (c) 2021 Backstop Solutions Group, LLC. 
# Licensed under the MIT license: https://opensource.org/licenses/mit-license.php


import argparse
import base64
import os
import requests


import cryptography as cryptography  # project page: https://github.com/pyca/cryptography
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


from email.utils import formatdate
from time import time


SIGNATURE_ALGORITHM = 'SHA256withRSA'
TIME_TO_LIVE = 120  # seconds
API_MIME_TYPE = 'application/vnd.api+json'


def create_signature(private_key, message):
    # This is the same as "SHA256withRSA" in Java
    signature = private_key.sign(
        message.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature)


def create_time_string():
    return format_time_string(int(time()))


def format_time_string(signature_time):
    # Returns the date formatted as RFC1123
    return formatdate(
        timeval=signature_time,
        localtime=False,
        usegmt=True
    )


def get_private_key_from_file(p12_file_name, store_pass):
    try:
        p12_file = open(p12_file_name, 'rb')
        p12_data = cryptography.hazmat.primitives.serialization.pkcs12.load_key_and_certificates(
            p12_file.read(),
            store_pass.encode())
        p12_file.close()
        private_key = p12_data[0]
    except OSError as oe:
        print("Can't open keyfile: " + request_body_file_name + ', Reason: ' + oe.strerror)
        exit(oe.errno)
    except ValueError as ve:
        print("Can't read keyfile: " + request_body_file_name + ', Reason: ' + ve.args[0])
        exit(1)
    return private_key


def get_post_body_text_from_file(request_body_file_name):
    try:
        request_body_file = open(request_body_file_name, 'r')
        request_body_file_text = request_body_file.read()
        request_body_file.close()
    except OSError as oe:
        print("Can't open datafile: " + request_body_file_name + ', Reason: ' + oe.strerror)
        exit(oe.errno)
    return request_body_file_text


def test_us():
    print(create_time_string())
    time_string = format_time_string(1610609694)
    print(time_string == 'Thu, 14 Jan 2021 07:34:54 GMT')
    url = 'http://localhost:8080/backstop/api/bulk-system-users'
    request_body_file_text = get_post_body_text_from_file('sample_datafile.json')
    message = url + time_string + request_body_file_text
    private_key = get_private_key_from_file('backstop3.p12', 'asdf')
    encoded_signature = create_signature(private_key, message)
    print(encoded_signature == b'EC5Y8cIRtidyhAqCQBikmHcRXUOhIGeF7TXp4GlfgFv+Xv/cux7fotdd/xg+qaKJ+QBh2av6VFhuZcTnTHOaga3Djv2XEMbq849wzcTG5M83R1cMdzpXQ54dwaRtw83Ca7AZFjppMcgj5B5bFAQ1WKpp//XdJixx0rJWJmtJ4ymbT/UVAwJBxY4//SGKCTB7/Dof6gJNo4FcdIBI9fBBFozDKQPB/efNG6HpNWzKMgg6QWtBY8W6bwG9EPXV5wNq4wjW9OqPMO2ZtZquUKEMY+uzFGkwai3eV6JuaH2e2GEbHneYJSlwovnvhLn9JNQHfGfgWyPDU8P47W9gD0GIjw==')


####


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--datafile', required=True, help='POST data file name')
parser.add_argument('-k', '--keyfile', required=True, help='private key file name')
parser.add_argument('-p', '--password', required=True, help='private key file password')
parser.add_argument('-u', '--url', required=True, help='Backstop URL')
parser.add_argument('-n', '--username', required=True, help='Backstop username')
parser.add_argument('-t', '--token', required=True, help='Backstop API token')

args = parser.parse_args()

request_body_file_name = args.datafile
p12_file_name = args.keyfile
store_pass = args.password
url = args.url
username = args.username
api_token = args.token

time_string = create_time_string()
request_body_file_text = get_post_body_text_from_file(request_body_file_name)

# For an http GET request, message_to_sign = url + time_string
message_to_sign = url + time_string + request_body_file_text

private_key = get_private_key_from_file(p12_file_name, store_pass)
encoded_signature = create_signature(private_key, message_to_sign)

key_id = os.path.splitext(os.path.basename(p12_file_name))[0]

signature_header = 'keyId:' + key_id \
                   + ', algorithm:' + SIGNATURE_ALGORITHM \
                   + ', timeToLive:' + str(TIME_TO_LIVE) \
                   + ', signature:' + encoded_signature.decode('ascii')

response = requests.post(url,
                         auth=(username, api_token),
                         data=request_body_file_text,
                         headers={
                             'token': 'true',
                             'Content-Type': API_MIME_TYPE,
                             'Accept': API_MIME_TYPE,
                             'X-Signature': signature_header,
                             'Date': time_string
                         })

print(response.text)
