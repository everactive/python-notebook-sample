"""Contains the ApiConnection class that provides an Oauth connection to the
Everactive Data Services API."""

import os
import urllib
from typing import Dict, List, Optional

import oauthlib
import requests
import requests_oauthlib

import everactive_envplus.log as logger
import everactive_envplus.utils as utils

log = logger.get_logger()

EVERACTIVE_API_BASE_URL = "https://api.data.everactive.com/"
DEFAULT_PAGE_SIZE = 500


class ApiConnection:
    """Class to provide API connection to the Everactive Data Services API.

    Typical usage example:
        # Supply API credentials explicitly.
        connection = ApiConnection(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

        # Or initialize and the class attempts to discover credentials from environs.
        connection = ApiConnection()

        connection.get(f"ds/v1/eversensors/{mac_address}/readings/last")
        connection.get_paginated_results("ds/v1/eversensors")
    """

    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ) -> None:
        """Initialize an ApiConnection object and establish connection to the
        Everactive Data Services API.

        If API credentials are not provided as arguments, the object attempts to
        discover the credentials as the EVERACTIVE_CLIENT_ID and
        EVERACTIVE_CLIENT_SECRET environment variables.

        Args:
            client_id: Optional string Everactive API client id credential
            client_secret: Optional string Everactive API client secret credential
        """

        self._base_url = EVERACTIVE_API_BASE_URL

        # Autodiscover credentials from environment variable or constructor.
        self._set_credentials(client_id, client_secret)

        self._create_session()
        self._authenticate()

    def _set_credentials(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ) -> None:
        """Discover and set the client id and client secret Everactive API credentials.

        Args:
            client_id: Optional string Everactive API client id credential
            client_secret: Optional string Everactive API client secret credential

        Raises:
            Exception:
                * If client id is not supplied as an argument or set as the
                  EVERACTIVE_CLIENT_ID environment variable
                * If client secret is not supplied as an argument or set as the
                  EVERACTIVE_CLIENT_SECRET environment variable
        """
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

    def _create_session(self) -> None:
        """Establish an OAuth2 session with the Everactive API."""
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        client = oauthlib.oauth2.BackendApplicationClient(client_id=self._client_id)
        self._session = requests_oauthlib.OAuth2Session(client=client)
        self._session.mount(self._base_url, adapter)

    def _authenticate(self) -> None:
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
        """Retrieve results via HTTP GET for specified Everactive API endpoint.

        Args:
            url: Requested API endpoint URL as string, relative to base API URL
                e.g. ds/v1/eversensors/{eversensor_mac_address}/readings
                    or ds/v1/evergateways/{evergateway_id}

        Returns:
            * If GET is successful and response can be parsed, returns a Dict containing
            response data
            * If GET or response parsing fails, returns bad response object
        """
        request_url = urllib.parse.urljoin(self._base_url, url)

        try:
            response = self._session.request("GET", request_url)
            result = response.json()["data"]
            return result

        except:
            log.error(f"Error requesting url: {request_url}")
            return response

    def get_paginated_results(
        self,
        url: str,
        sort_by: str,
        query_params: Optional[Dict] = {},
        page_size: Optional[int] = DEFAULT_PAGE_SIZE,
    ) -> List[Dict]:
        """Return aggregated paginated GET results from Everactive API endpoint.

        Args:
            url: Requested API endpoint URL as string, relative to base API URL
                e.g. ds/v1/eversensors or ds/v1/evergateways
            sort_by: string name of parameter to sort results by, e.g. serial-number
            query_params: Optional Dict containing string query params, in format:
                {"param-name-1" : "param-value-1", param-name-2" : "param-value-2", ...}
            page_size: Optional int specifying the page size for paginated results

        Returns:
            * If GETs are successful and responses can be parsed, returns aggregated
            response data as List of Dicts
            * If a GET or response parsing fails, returns bad response object
        """
        paginated_results = []
        request_url = urllib.parse.urljoin(self._base_url, url)

        response = self._session.request(
            "GET",
            request_url,
            params={
                "page": 1,
                "page-size": page_size,
                "sort-by": sort_by,
                **query_params,
            },
        )

        try:
            log.debug(f"Requested URL: {response.__dict__['url']}")

            result = response.json()

            if "paginationInfo" in result.keys():
                if (
                    result["paginationInfo"]["totalPages"]
                    >= result["paginationInfo"]["page"]
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
                                **query_params,
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

    def __del__(self) -> None:
        """Close session when object is deleted."""
        if self._session:
            self._session.close()
