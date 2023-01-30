"""Contains the ColorPalette class that defines the Everactive data visualization
color palette."""

from typing import Optional

DEFAULT_INTENSITY = 100

VIOLET = {
    "violet_20": "#EAD1F1",
    "violet_25": "#E4C5ED",
    "violet_33": "#DCB3E7",
    "violet_40": "#D5A3E2",
    "violet_50": "#CA8CDB",
    "violet_60": "#BF75D4",
    "violet_67": "#B865CF",
    "violet_75": "#AF52C9",
    "violet_80": "#AA47C5",
    "violet_100": "#9519B7",
}

SKY = {
    "sky_20": "#CCF4FF",
    "sky_25": "#BFF1FF",
    "sky_33": "#ABEDFF",
    "sky_40": "#99E9FF",
    "sky_50": "#80E3FF",
    "sky_60": "#66DEFF",
    "sky_67": "#54DAFF",
    "sky_75": "#40D5FF",
    "sky_80": "#33D3FF",
    "sky_100": "#00C8FF",
}

MIDNIGHT = {
    "midnight_20": "#D7D6E4",
    "midnight_25": "#CDCBDD",
    "midnight_33": "#BDBBD2",
    "midnight_40": "#AFADC9",
    "midnight_50": "#9B98BB",
    "midnight_60": "#8783AD",
    "midnight_67": "#7975A4",
    "midnight_75": "#696499",
    "midnight_80": "#5F5A92",
    "midnight_100": "#373177",
}

CHARTREUSE = {
    "chartreuse_20": "#EDF7D0",
    "chartreuse_25": "#E8F5C5",
    "chartreuse_33": "#E1F2B2",
    "chartreuse_40": "#DBF0A2",
    "chartreuse_50": "#D2EC8A",
    "chartreuse_60": "#C9E873",
    "chartreuse_67": "#C2E563",
    "chartreuse_75": "#BBE250",
    "chartreuse_80": "#B7E044",
    "chartreuse_100": "#A4D916",
}

DARK_TEAL = {
    "dark_teal_20": "#CDE1E8",
    "dark_teal_25": "#C0DAE2",
    "dark_teal_33": "#ACCED9",
    "dark_teal_40": "#9BC4D1",
    "dark_teal_50": "#82B5C5",
    "dark_teal_60": "#69A6BA",
    "dark_teal_67": "#579CB1",
    "dark_teal_75": "#4390A8",
    "dark_teal_80": "#3688A2",
    "dark_teal_100": "#046B8B",
}

SAND = {
    "sand_20": "#EDE1C8",
    "sand_25": "#E4D7BB",
    "sand_33": "#DACCAF",
    "sand_40": "#D4C4A1",
    "sand_50": "#D2C5A9",
    "sand_60": "#BFAF90",
    "sand_67": "#BFB5A1",
    "sand_75": "#BFAF90",
    "sand_80": "#B7AD9A",
    "sand_100": "#A89E88",
}

CHARCOAL = {
    "charcoal_20": "#D2D2D2",
    "charcoal_25": "#C7C7C7",
    "charcoal_33": "#B5B5B5",
    "charcoal_40": "#A5A5A5",
    "charcoal_50": "#8F8F8F",
    "charcoal_60": "#797979",
    "charcoal_67": "#696969",
    "charcoal_75": "#575757",
    "charcoal_80": "#4C4C4C",
    "charcoal_100": "#1F1F1F",
}

APRICOT = {
    "apricot_20": "#FBEBDD",
    "apricot_25": "#F9E6D4",
    "apricot_33": "#F8DEC6",
    "apricot_40": "#F6D7BA",
    "apricot_50": "#F4CDA9",
    "apricot_60": "#F2C498",
    "apricot_67": "#F0BD8C",
    "apricot_75": "#EEB57E",
    "apricot_80": "#EDB075",
    "apricot_100": "#E99C53",
}

COLOR_PALETTE = {
    **VIOLET,
    **SKY,
    **MIDNIGHT,
    **CHARTREUSE,
    **DARK_TEAL,
    **SAND,
    **CHARCOAL,
    **APRICOT,
}


class ColorPalette:
    """Helper class to store and serve the Everactive data visualization color palette.

    Typical usage example:
        palette = ColorPalette()
        palette.violet()    # Hex code for violet at 100% intensity
        palette.violet(50)  # Hex code for violet at 50% intensity
    """

    def violet(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for violet at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("violet", intensity)

    def sky(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for sky at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("sky", intensity)

    def midnight(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for midnight at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("midnight", intensity)

    def chartreuse(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for chartreuse at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("chartreuse", intensity)

    def dark_teal(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for dark teal at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("dark_teal", intensity)

    def sand(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for sand at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("sand", intensity)

    def charcoal(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for charcoal at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("charcoal", intensity)

    def apricot(self, intensity: Optional[int] = None) -> str:
        """Return string hex code for apricot at specified int intensity.
        Defaults to 100(%) intensity."""
        return self._get_color_hex("apricot", intensity)

    def _get_color_hex(
        self, color: str, intensity: Optional[int] = DEFAULT_INTENSITY
    ) -> str:
        """Return the string hex code for the requested color at the requested
        intensity level.

        Args:
            color: String name of palette color (e.g. sky, dark_teal, apricot..)
            intensity: Optional int to specify the intensity percentage level of the
                requested color. Valid intensity levels are:
                    20, 25, 33, 40, 50, 60, 67, 75, 80, 100
        """
        if intensity is None:
            intensity = DEFAULT_INTENSITY

        color_key = f"{color}_{intensity}"

        if color_key not in COLOR_PALETTE:
            raise KeyError(
                f"Color {color} at intensity {intensity} does not exist in palette"
            )

        return COLOR_PALETTE[color_key]
