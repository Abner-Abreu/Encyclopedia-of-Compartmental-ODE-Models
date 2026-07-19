class FiltersDto:
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