class TeamSimple:
    def __init__(self, key: str, nickname: str, name: str, location: tuple[str, str, str]):
        self.__key = key
        self.__nickname = nickname
        self.__name = name
        self.__location = location

    def get_key(self) -> str:
        return self.__key

    def get_nickname(self) -> str:
        return self.__nickname

    def get_name(self) -> str:
        return self.__name

    def get_location(self) -> tuple[str, str, str]:
        return self.__location

