import collections

END_OF_FILE_GROUP = 'end_of_file'

NEW_LINE_GROUP = 'new_line'
WHITE_SPACE_GROUP = 'white_space'
STRING_GROUP = 'string'
DICT_OPEN_GROUP = 'dict_open'
DICT_CLOSE_GROUP = 'dict_close'
LIST_OPEN_GROUP = 'list_open'
LIST_CLOSE_GROUP = 'list_close'
NUMBER_GROUP = 'number'
COLON_GROUP = 'colon'
COMMA_GROUP = 'comma'

NEW_LINE_REGEX = r'[\n]+'
WHITE_SPACE_REGEX = r'[ \t]+'
STRING_REGEX = r'"(?:\\.|[^"\\])*?"'
DICT_OPEN_REGEX = r'\{'
DICT_CLOSE_REGEX = r'\}'
LIST_OPEN_REGEX = r'\['
LIST_CLOSE_REGEX = r'\]'
NUMBER_REGEX = r'\d+(\.\d*)?'
COLON_REGEX = r':'
COMMA_REGEX = r','


REGEX_DICT = {
    NEW_LINE_GROUP: NEW_LINE_REGEX,
    WHITE_SPACE_GROUP: WHITE_SPACE_REGEX,
    STRING_GROUP: STRING_REGEX,
    DICT_OPEN_GROUP: DICT_OPEN_REGEX,
    DICT_CLOSE_GROUP: DICT_CLOSE_REGEX,
    LIST_OPEN_GROUP: LIST_OPEN_REGEX,
    LIST_CLOSE_GROUP: LIST_CLOSE_REGEX,
    NUMBER_GROUP: NUMBER_REGEX,
    COLON_GROUP: COLON_REGEX,
    COMMA_GROUP: COMMA_REGEX,
}

Token = collections.namedtuple('Token', ['group', 'value', 'line', 'column'])
