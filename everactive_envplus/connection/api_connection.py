import os
import urllib
from typing import Dict, Optional

import oauthlib
import requests
import requests_oauthlib

import everactive_envplus.log as logger
import everactive_envplus.utils as utils

log = logger.get_logger()

EVERACTIVE_API_BASE_URL = "https://api.data.everactive.com/"
DEFAULT_PAGE_SIZE = 500


class ApiConnection:
    """Class to provide API connection to the Everactive Edge API."""

    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        """Construct an ApiConnection object.

        Args:
            client_id:
            client_secret
        """

        self._base_url = EVERACTIVE_API_BASE_URL

        # Autodiscover credentials from environment variable or constructor.
        self._set_credentials(client_id, client_secret)

        self._create_session()
        self._authenticate()

    def _set_credentials(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):

        self._client_id = utils.coalesce([client_id, os.getenv("EVERACTIVE_CLIENT_ID")])

        if self._client_id is None:
            raise Exception(
                f"Client id not found. Please supply client_id to the ApiConnection() constructor, "
                f"or set as environment variable EVERACTIVE_CLIENT_ID."
            )

        self._client_secret = utils.coalesce(
            [client_secret, os.getenv("EVERACTIVE_CLIENT_SECRET")]
        )

        if self._client_secret is None:
            raise Exception(
                f"Client secret not found. Please supply client_secret to the ApiConnection() constructor, "
                f"or set as environment variable EVERACTIVE_CLIENT_SECRET."
            )

    def _create_session(self):
        """Establish an Oauth2 session with the Everactive API."""

        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        client = oauthlib.oauth2.BackendApplicationClient(client_id=self._client_id)
        self._session = requests_oauthlib.OAuth2Session(client=client)
        self._session.mount(self._base_url, adapter)

    def _authenticate(self):
        """Authenticate to the Everactive API."""
        token_url = urllib.parse.urljoin(self._base_url, "auth/token")
        log.debug(f"Fetching oauth token from: {token_url}")
        self._session.fetch_token(
            token_url=token_url,
            client_id=self._client_id,
            client_secret=self._client_secret,
            include_client_id=True,
        )

        log.info("Authenticated to the Everactive API")

    def get(self, url: str) -> Dict:

        request_url = urllib.parse.urljoin(self._base_url, url)

        try:
            response = self._session.request("GET", request_url)
            result = response.json()["data"]
            return result

        except:
            log.error(f"Error requesting url: {request_url}")
            return response

    def get_paginated_results(
        self, url: str, sort_by: str, page_size: int = DEFAULT_PAGE_SIZE
    ):
        """Aggregate paginated GET results from Everactive API endpoints."""
        paginated_results = []
        request_url = urllib.parse.urljoin(self._base_url, url)

        response = self._session.request(
            "GET",
            request_url,
            params={"page": 1, "page-size": page_size, "sort-by": sort_by},
        )

        try:
            result = response.json()

            if "paginationInfo" in result.keys():
                if (
                    result["paginationInfo"]["totalPages"]
                    > result["paginationInfo"]["page"]
                ):
                    log.debug(
                        f"Page: {result['paginationInfo']['page']}/"
                        f"{result['paginationInfo']['totalPages']}, "
                        f"Total Items: {result['paginationInfo']['totalItems']}"
                    )

                    total_pages = result["paginationInfo"]["totalPages"]
                    paginated_results.extend(result["data"])

                    for page in range(2, total_pages + 1):
                        page_response = self._session.request(
                            "GET",
                            request_url,
                            params={
                                "page": page,
                                "page-size": page_size,
                                "sort-by": sort_by,
                            },
                        )
                        page_result = page_response.json()

                        log.debug(
                            f"Page: {page_result['paginationInfo']['page']}/"
                            f"{page_result['paginationInfo']['totalPages']}"
                        )

                        paginated_results.extend(page_result["data"])

            return paginated_results

        except:
            log.error(f"Error requesting url: {request_url}")
            return response

    def __del__(self):
        """Close session when object is deleted."""
        if self._session:
            self._session.close()
