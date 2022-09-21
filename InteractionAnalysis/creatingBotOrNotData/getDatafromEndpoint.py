from unittest import skip
import requests
from twarc import expansions  # copy expansions.py
from time import sleep
import json
import pandas as pd


def from_Twitter(query={}, strEndpointURL="", hasexpansions=True):
    BEARER_TOKEN = "KEY" # Insert Twitter API key here

    def create_headers(bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def connect_to_endpoint(url, headers, params):
        response = requests.request("GET", url, headers=headers,
                                    params=params,  timeout=5)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def get_tweets(hasexpansions, query):
        """
        Pull tweets and and put them in a text file.
        :return: None
        """

        headers = create_headers(BEARER_TOKEN)
        json_response = connect_to_endpoint(strEndpointURL, headers, query)
        try:
            data_main = expansions.ensure_flattened(json_response)
        except:
            pass
        counter = 1
        if hasexpansions:
            while "next_token" in json_response["meta"]:
                query["next_token"] = json_response["meta"]["next_token"]

                json_response = connect_to_endpoint(
                    strEndpointURL, headers, query)
                counter = counter+1
                sleep(1)

                data_current = expansions.ensure_flattened(json_response)
                data_main.extend(data_current)
                json_response = data_main
        return json_response

    return get_tweets(hasexpansions, query=query)
