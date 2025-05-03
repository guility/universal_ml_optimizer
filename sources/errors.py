class MissingFeatureError(ValueError):
    def __init__(self, missing_features: list[str]):
        super().__init__(f'Missing features: "{', '.join(missing_features)}"')


class NAError(ValueError):
    def __init__(self, na_features: list[str], na_number: int):
        super().__init__(
            f'Found {na_number} of NAs in columns:'
            f' {", ".join(na_features)}'
            )
