from consts import (
    END_OF_FILE_GROUP,
    DICT_OPEN_GROUP,
    STRING_GROUP,
    COLON_GROUP,
    NEW_LINE_GROUP,
    WHITE_SPACE_GROUP,
    NUMBER_GROUP,
    LIST_OPEN_GROUP,
    DICT_CLOSE_GROUP,
    COMMA_GROUP,
    LIST_CLOSE_GROUP)

EXPECTED_GROUPS = {}


class Parser:
    def __init__(self, token_generator):
        self._token_generator = token_generator()
        self.current_token = None

    def update_current_token(self, expected_token_groups):
        self.current_token = next(self._token_generator)
        while self.current_token.group in (NEW_LINE_GROUP, WHITE_SPACE_GROUP):
            self.current_token = next(self._token_generator)

        if self.current_token.group not in expected_token_groups:
            self.error(f"Token {self.current_token} is not instance of {expected_token_groups} groups")

    def error(self, msg):
        raise RuntimeError(msg)

    def start(self):
        self.update_current_token((DICT_OPEN_GROUP,))
        self.parse_dict()
        self.update_current_token((END_OF_FILE_GROUP,))

    def parse_list(self):
        self.update_current_token((STRING_GROUP, NUMBER_GROUP, DICT_OPEN_GROUP, LIST_CLOSE_GROUP, LIST_CLOSE_GROUP))

        while self.current_token.group != LIST_CLOSE_GROUP:
            if self.current_token.group == DICT_OPEN_GROUP:
                self.parse_dict()
            elif self.current_token.group == LIST_OPEN_GROUP:
                self.parse_list()

            self.update_current_token((COMMA_GROUP, LIST_CLOSE_GROUP))
            if self.current_token.group == COMMA_GROUP:
                self.update_current_token((STRING_GROUP, NUMBER_GROUP, DICT_OPEN_GROUP, LIST_CLOSE_GROUP, LIST_CLOSE_GROUP))

        print(f"[OK] list {self.current_token}")

    def parse_dict_value(self, dict_key):
        expected_groups = EXPECTED_GROUPS.get(
            dict_key, (STRING_GROUP, NUMBER_GROUP, DICT_OPEN_GROUP, LIST_OPEN_GROUP))

        self.update_current_token(expected_groups)
        if self.current_token.group == DICT_OPEN_GROUP:
            self.parse_dict()
        elif self.current_token.group == LIST_OPEN_GROUP:
            self.parse_list()

    def parse_dict(self):
        self.update_current_token((STRING_GROUP, NUMBER_GROUP, DICT_CLOSE_GROUP))

        while self.current_token.group != DICT_CLOSE_GROUP:
            self.parse_dict_item()
            self.update_current_token((COMMA_GROUP, DICT_CLOSE_GROUP))

            if self.current_token.group == COMMA_GROUP:
                self.update_current_token((STRING_GROUP, NUMBER_GROUP, DICT_CLOSE_GROUP))

        print(f"[OK] dict {self.current_token}")

    def parse_dict_item(self):
        dict_key = self.current_token.value
        self.update_current_token((COLON_GROUP,))
        self.parse_dict_value(dict_key)