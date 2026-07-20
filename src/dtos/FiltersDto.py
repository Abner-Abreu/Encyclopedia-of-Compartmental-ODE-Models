class FiltersDto:
    """
    Data Transfer Object for filter criteria when querying models.

    This DTO encapsulates all possible filter parameters that can be
    applied when searching for models in the encyclopedia. Each field
    represents a specific search criterion, and all fields are optional.

    Filters can be combined to narrow down search results. For example,
    searching for models with a specific name that also contain a
    particular parameter.

    Attributes:
        name_contains (str | None): Filter by model name (partial match).
        parameter_contains (str | None): Filter by parameter name (partial match).
        compartment_contains (str | None): Filter by compartment name (partial match).
        situation_contains (str | None): Filter by situation name (partial match).
        article_contains (str | None): Filter by article name (partial match).
        all_linear (bool | None): If True, only return models where all
            parameters are linear. If False or None, no filter applied.
    """
    def __init__(self, 
                 name_contains:str | None,
                 parameter_contains:str | None,
                 compartment_contains:str | None,
                 situation_contains: str | None,
                 article_contains: str | None,
                 all_linear: bool | None):
        self.name_contains = name_contains
        self.parameter_contains = parameter_contains
        self.compartment_contains = compartment_contains
        self.situation_contains = situation_contains
        self.article_contains = article_contains
        self.all_linear = all_linear