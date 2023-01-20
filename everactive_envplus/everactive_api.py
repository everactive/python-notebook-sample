from typing import Dict, Optional, Union

import pandas as pd

import everactive_envplus.connection as connection

DEFAULT_OUTPUT_FORMAT = "json"


class EveractiveApi:
    def __init__(self, api_connection: connection.ApiConnection):
        self._api = api_connection

    def _format_as_pandas(self, data: Dict) -> pd.DataFrame:
        return pd.json_normalize(data, sep="_")

    def get_all_eversensors(
        self, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:
        results = self._api.get_paginated_results(
            "ds/v1/eversensors", sort_by="mac-address"
        )

        if output_format == "pandas":
            return self._format_as_pandas(results)

        return results

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

        if output_format == "pandas":
            return self._format_as_pandas(results)

        return results

    def get_eversensor_last_reading(
        self, mac_address: str, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:

        results = self._api.get(f"ds/v1/eversensors/{mac_address}/readings/last")

        if output_format == "pandas":
            return self._format_as_pandas(results)

        return results

    def get_all_evergateways(
        self, *, output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT
    ) -> Union[Dict, pd.DataFrame]:
        results = self._api.get_paginated_results(
            f"ds/v1/evergateways", sort_by="serial-number"
        )

        if output_format == "pandas":
            return self._format_as_pandas(results)

        return results

    def get_evergateway(
        self,
        gateway_identifier: str,
        *,
        output_format: Optional[str] = DEFAULT_OUTPUT_FORMAT,
    ) -> Union[Dict, pd.DataFrame]:
        results = self._api.get(f"ds/v1/evergateways/{gateway_identifier}")

        if output_format == "pandas":
            return self._format_as_pandas(results)

        return results
