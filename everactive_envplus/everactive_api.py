from typing import Dict, Optional, Union

import pandas as pd

import everactive_envplus.connection as connection

DEFAULT_OUTPUT_FORMAT = "json"


class EveractiveApi:
    def __init__(self, api_connection: connection.ApiConnection):
        self._api = api_connection

    def _format_results(
        self, results: Dict, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ):
        if output_format not in ["json", "pandas"]:
            raise ValueError("output_format must be either 'json' or 'pandas'")

        if output_format == "pandas":
            return pd.json_normalize(results, sep="_")

        return results

    def get_all_eversensors(
        self, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:
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

        results = self._api.get(
            f"ds/v1/eversensors/{mac_address}/readings?start-time={start_time}&end-time={end_time}"
        )

        return self._format_results(results, output_format)

    def get_eversensor_last_reading(
        self, mac_address: str, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:

        results = self._api.get(f"ds/v1/eversensors/{mac_address}/readings/last")

        return self._format_results(results, output_format)

    def get_all_evergateways(
        self, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:
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
        results = self._api.get(f"ds/v1/evergateways/{gateway_identifier}")

        return self._format_results(results, output_format)
