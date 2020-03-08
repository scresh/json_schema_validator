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
    LIST_CLOSE_GROUP,
    EXPECTED_GROUPS,
)


class Parser:
    def __init__(self, token_generator):
        self._token_generator = token_generator()
        self.current_token = None

    def update_current_token(self, expected_token_groups):
        self.current_token = next(self._token_generator)
        while self.current_token.group in (NEW_LINE_GROUP, WHITE_SPACE_GROUP):
            self.current_token = next(self._token_generator)

        if self.current_token.group not in expected_token_groups:
            self.print_error(expected_token_groups)

    def start(self):
        self.update_current_token((DICT_OPEN_GROUP,))
        self.parse_dict()
        self.update_current_token((END_OF_FILE_GROUP,))

    def parse_list(self):
        list_start = (self.current_token.line, self.current_token.column)

        self.update_current_token((STRING_GROUP, NUMBER_GROUP, DICT_OPEN_GROUP, LIST_CLOSE_GROUP, LIST_CLOSE_GROUP))

        while self.current_token.group != LIST_CLOSE_GROUP:
            if self.current_token.group == DICT_OPEN_GROUP:
                self.parse_dict()
            elif self.current_token.group == LIST_OPEN_GROUP:
                self.parse_list()

            self.update_current_token((COMMA_GROUP, LIST_CLOSE_GROUP))
            if self.current_token.group == COMMA_GROUP:
                self.update_current_token(
                    (STRING_GROUP, NUMBER_GROUP, DICT_OPEN_GROUP, LIST_CLOSE_GROUP, LIST_CLOSE_GROUP))

        list_end = (self.current_token.line, self.current_token.column)
        print(f"[OK] DICT [{list_start} - {list_end}]")

    def parse_dict_value(self, dict_key):
        expected_groups = EXPECTED_GROUPS.get(
            dict_key, (STRING_GROUP, NUMBER_GROUP, DICT_OPEN_GROUP, LIST_OPEN_GROUP)
        )

        self.update_current_token(expected_groups)
        if self.current_token.group == DICT_OPEN_GROUP:
            self.parse_dict()
        elif self.current_token.group == LIST_OPEN_GROUP:
            self.parse_list()

    def parse_dict(self):
        dict_start = (self.current_token.line, self.current_token.column)
        self.update_current_token((STRING_GROUP, NUMBER_GROUP, DICT_CLOSE_GROUP))

        while self.current_token.group != DICT_CLOSE_GROUP:
            self.parse_dict_item()
            self.update_current_token((COMMA_GROUP, DICT_CLOSE_GROUP))

            if self.current_token.group == COMMA_GROUP:
                self.update_current_token((STRING_GROUP, NUMBER_GROUP, DICT_CLOSE_GROUP))

        dict_end = (self.current_token.line, self.current_token.column)
        print(f"[OK] DICT [{dict_start} - {dict_end}]")

    def parse_dict_item(self):
        dict_key = self.current_token.value
        self.update_current_token((COLON_GROUP,))
        self.parse_dict_value(dict_key)

    def print_error(self, expected_token_groups):
        group, value, line, column = self.current_token
        expected_token_groups_string = " or ".join(expected_token_groups)

        exit(
            f'Invalid token group: {value} at {(line, column)}. '
            f'Expected {expected_token_groups_string} but got {group}.'
        )
