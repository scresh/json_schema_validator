from consts import (
    REGEX_DICT,
    NEW_LINE_GROUP,
    END_OF_FILE_GROUP,
    Token,
)
import re


class TokenGenerator:
    def __init__(self, input_string):
        self._input_string = input_string

        self._line_number = 1
        self._current_position = 0
        self._line_start = 0

        self._match_token_func = self._get_match_token_func(REGEX_DICT)

    def __call__(self):
        match = self._match_token_func(self._input_string)
        while match:
            token_value, token_group, = self._get_token_value_and_group(match)

            if token_group == NEW_LINE_GROUP:
                self.switch_new_line()
            self.switch_current_position(match)

            yield Token(token_group, token_value, self._line_number, match.start() - self._line_start)
            match = self._match_token_func(self._input_string, self._current_position)

        if self._current_position != len(self._input_string):
            raise InvalidCharacterException(self._input_string[self._current_position], self._line_number)

        yield Token(END_OF_FILE_GROUP, '', self._line_number, self._current_position - self._line_start)

    @staticmethod
    def _get_token_value_and_group(match):
        token_group = match.lastgroup
        token_value = match.group(token_group)

        return token_value, token_group

    def switch_new_line(self):
        self._line_start = self._current_position
        self._line_number += 1

    def switch_current_position(self, match):
        self._current_position = match.end()

    @staticmethod
    def _get_match_token_func(tokens_dict):
        tokens_regex = '|'.join(f'(?P<{k}>{v})' for k, v in tokens_dict.items())
        return re.compile(tokens_regex).match


class InvalidCharacterException(Exception):
    def __init__(self, character, line_number):
        super().__init__(f'Invalid character {character} on line {line_number}')
