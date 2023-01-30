"""Contains the EveractiveApi class that provides a wrapper around Everactive Data
Services API endpoints."""

from typing import Dict, List, Optional, Union

import pandas as pd

import everactive_envplus.connection as connection

DEFAULT_OUTPUT_FORMAT = "json"


class EveractiveApi:
    """Class to provide a wrapper/client library around Everactive Data Services API
    endpoints.

    Typical usage example:
        api = EveractiveApi(
            api_connection=ApiConnection(
                client_id=CLIENT_ID, client_secret=CLIENT_SECRET
            )
        )

        api.get_all_eversensors()
        api.api.get_eversensor_readings(
            sensor_mac_address, start_time, end_time,
            output_format="pandas"
        )
    """

    def __init__(self, api_connection: connection.ApiConnection) -> None:
        """Initialize an EveractiveApi object.

        Args:
            api_connection: ApiConnection object
        """
        self._api = api_connection

    def _format_results(
        self,
        results: Union[List[Dict], Dict],
        output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT,
    ) -> Union[List[Dict], Dict, pd.DataFrame]:
        """(Re)format supplied results as requested output format.

        Args:
            results: Data to format, as a Dict or List of Dicts
            output_format: Desired string name output format, either "json" or "pandas".
                Defaults to "json".

        Returns:
            Reformatted results, as Dict, List of Dicts, or pandas DataFrame, depending
            on requested output_format
        """

        if output_format not in ["json", "pandas"]:
            raise ValueError("output_format must be either 'json' or 'pandas'")

        if output_format == "pandas":
            return pd.json_normalize(results, sep="_")

        return results

    def get_all_eversensors(
        self, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:
        """Return all Eversensors associated with user API credentials.

        Args:
            output_format: String specifying output format, either "json" or "pandas"
        """

        results = self._api.get_paginated_results(
            "ds/v1/eversensors",
            sort_by="mac-address",
            query_params={"devkitBundled": True, "type": "Environmental"},
        )

        return self._format_results(results, output_format)

    def get_eversensor_readings(
        self,
        mac_address: str,
        start_time: int,
        end_time: int,
        *,
        output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT,
    ) -> Union[Dict, pd.DataFrame]:
        """Return readings for requested Eversensor over requested time period.

        A max of 24 hours of Eversensor readings can be retrieved with a single call.

        Args:
            mac_address: String mac address of requested Eversensor
            start_time: Start time of requested readings period, as unix timestamp
            end_time: End time of requested readings period, as unix timestamp
            output_format: String specifying output format, either "json" or "pandas"
        """
        results = self._api.get(
            f"ds/v1/eversensors/{mac_address}/readings?start-time={start_time}&end-time={end_time}"
        )

        return self._format_results(results, output_format)

    def get_eversensor_last_reading(
        self, mac_address: str, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:
        """Return most recent reading for requested Eversensor.

        Args:
            mac_address: String mac address of requested Eversensor
            output_format: String specifying output format, either "json" or "pandas"
        """
        results = self._api.get(f"ds/v1/eversensors/{mac_address}/readings/last")

        return self._format_results(results, output_format)

    def get_all_evergateways(
        self, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:
        """Return all Evergateways associated with user API credentials.

        Args:
            output_format: String specifying output format, either "json" or "pandas"
        """
        results = self._api.get_paginated_results(
            f"ds/v1/evergateways", sort_by="serial-number"
        )

        return self._format_results(results, output_format)

    def get_evergateway(
        self,
        gateway_identifier: str,
        *,
        output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT,
    ) -> Union[Dict, pd.DataFrame]:
        """Return metadata of requested Evergateway.

        Args:
            gateway_identifier: String identifier of Evergateway
            output_format: String specifying output format, either "json" or "pandas"
        """
        results = self._api.get(f"ds/v1/evergateways/{gateway_identifier}")

        return self._format_results(results, output_format)
