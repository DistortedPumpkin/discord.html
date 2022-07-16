class InvalidHTML(ValueError):
    pass


class MissingData(InvalidHTML):
    def __init__(self, missing: str):
        super().__init__(f"The html passed is missing a data attribute: {missing}")


class CommandParsingError(InvalidHTML):
    pass


class CommandMissingData(CommandParsingError):
    def __init__(self, tag: str, missing: str):
        super().__init__(f"The data attribute '{missing}' is missing for the command with the following tag:\n{tag}")


class CommandActionMissingType(CommandParsingError):
    def __init__(self, tag: str):
        super().__init__(f"The action type for the following action was either missing or invalid:\n{tag}")


class CommandActionMissingData(CommandParsingError):
    def __init__(self, tag: str):
        super().__init__(f"content was not passed to the following action but was required:\n{tag}")


class UserInputError(ValueError):
    pass


class MissingRequiredArgument(UserInputError):
    def __init__(self, argument: str):
        super().__init__(f"{argument} is a required argument that is missing")