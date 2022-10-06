# **************** Paths *****************
# Path of the db
DB_PATH = '../db/chinook/chinook.db'

# Path of the icon image(.ico)
ROOT_ICON_PATH = '../images/gui.ico'

# Pre path of the SQLite
SQL_LITE_PRE_PATH = 'sqlite:///'

# Path of the SQLite
SQL_LITE_PATH = SQL_LITE_PRE_PATH + DB_PATH

# ****************************************

# Title for the Tk root
ROOT_TITLE = \
    'Seminar Project - Hanan Ben Shabat'

# Style theme from ttkthemes library
STYLE_THEME = 'breeze'

# **************** Status ****************

NOTE_MAX_LENGTH = 60

ERROR = 'ERROR:\n'

# Empty query
ERROR_EMPTY = ERROR + \
              'Query cannot be empty.'

#  Note too long
ERROR_NOTE_LONG = ERROR + \
                  f'Query explanation cannot be ' \
                  f'over {NOTE_MAX_LENGTH} letters.'

SUCCESS = 'SUCCESS:\n'

SUCCESS_IMPORTED = SUCCESS + \
                   'User input imported' \
                   ' successfully.'

# ****************************************

# **************** Style *****************

VALID_EXAMPLES_FRAME_BACKGROUND = 'wheat'

INVALID_EXAMPLES_FRAME_BACKGROUND = 'lightslategrey'

INSERT_NOTE_FRAME_BACKGROUND = 'orchid'

INSERT_QUERY_FRAME_BACKGROUND = 'teal'

STATUS_FRAME_BACKGROUND = 'cornsilk'

QUERY_SELECTION_FRAME_BACKGROUND = 'powderblue'

CODE_FRAME_BACKGROUND = 'darkslateblue'

ERROR_BACKGROUND = 'darkred'
ERROR_FOREGROUND = 'lavenderblush'

SUCCESS_BACKGROUND = 'aquamarine'
SUCCESS_FOREGROUND = 'royalblue'

INSERT_QUERY_BACKGROUND = 'lightseagreen'

INSERT_NOTE_BACKGROUND = 'thistle'

ERROR_TITLE_BACKGROUND = 'red'
ERROR_TITLE_FOREGROUND = 'lavenderblush'

SUCCESS_TITLE_BACKGROUND = 'lime'
SUCCESS_TITLE_FOREGROUND = SUCCESS_FOREGROUND

VALID_EXAMPLES_TITLE_TEXT = 'Valid Examples:'
VALID_EXAMPLES_TITLE_BACKGROUND = 'springgreen'

INVALID_EXAMPLES_TITLE_TEXT = 'Invalid Examples:'
INVALID_EXAMPLES_TITLE_BACKGROUND = 'salmon'

INSERT_NOTE_TITLE_TEXT = 'Insert Query Explanation:'
INSERT_NOTE_TITLE_BACKGROUND = \
    INSERT_NOTE_FRAME_BACKGROUND

INSERT_QUERY_TITLE_TEXT = 'Insert Query:'
INSERT_QUERY_TITLE_BACKGROUND = \
    INSERT_QUERY_FRAME_BACKGROUND

STATUS_TITLE_TEXT = 'Submission Status:'
STATUS_TITLE_BACKGROUND = 'khaki'

SELECT_QUERY_TITLE_TEXT = 'Perform Query:'
SELECT_QUERY_TITLE_BACKGROUND = 'deepskyblue'

FONT_SCALE_TITLE_TEXT = 'Scale Font:'
FONT_SCALE_TITLE_BACKGROUND = 'turquoise'

WINDOW_SCALE_TITLE_TEXT = 'Scale Window:'
WINDOW_SCALE_TITLE_BACKGROUND = 'turquoise'

CODE_TITLE_TEXT = 'Performed Query Code:'
CODE_TITLE_BACKGROUND = 'slateblue'

RESULTS_TITLE_TEXT = 'Performed Query Results:'
RESULTS_TITLE_BACKGROUND = 'gainsboro'

VALID_EXAMPLE_BUTTON_BACKGROUND = 'yellowgreen'
VALID_EXAMPLE_BUTTON_ACTIVE_BACKGROUND = 'olivedrab'
VALID_EXAMPLE_BUTTON_FOREGROUND = 'darkmagenta'

INVALID_EXAMPLE_BUTTON_BACKGROUND = 'tomato'
INVALID_EXAMPLE_BUTTON_ACTIVE_BACKGROUND = 'firebrick'
INVALID_EXAMPLE_BUTTON_FOREGROUND = 'maroon'

CLEAR_BUTTON_TEXT = 'Clear'
CLEAR_BUTTON_BACKGROUND = 'crimson'
CLEAR_BUTTON_ACTIVE_BACKGROUND = 'orangered'
CLEAR_BUTTON_FOREGROUND = 'darkorange'
CLEAR_BUTTON_BORDER_WIDTH = 3

USER_INPUT_TEXT = 'Submit'
USER_INPUT_BACKGROUND = 'lawngreen'
USER_INPUT_ACTIVE_BACKGROUND = 'gold'
USER_INPUT_FOREGROUND = 'indigo'
USER_INPUT_ACTIVE_FOREGROUND = 'mediumblue'
USER_INPUT_BORDER_WIDTH = CLEAR_BUTTON_BORDER_WIDTH

# ****************************************

# **************** Fonts *****************

# Default font of the GUI
DEFAULT_FONT_TYPE = 'Verdana'

DEFAULT_FOT_SIZE = 9

# Size of the font for the
# query results columns rows
ROW_FONT_SIZE = DEFAULT_FOT_SIZE

# Size of the font for the
# code display label
CODE_FONT_SIZE = DEFAULT_FOT_SIZE + 1

# Size of the font for the
# query selection combobox and for the
# query results columns headings
HEADING_FONT_SIZE = DEFAULT_FOT_SIZE + 2

# Size of the font for the
# status text box
SUB_TITLE_FONT_SIZE = DEFAULT_FOT_SIZE + 3

# Size of the font for the
# title labels
TITLE_FONT_SIZE = DEFAULT_FOT_SIZE + 4

# ****************************************

INSERT_NOTE_DEFAULT = \
    'No query explanation inserted'

STATUS_DEFAULT = 'There is no submission.\n' \
                 'Submit a query.'
STATUS_BACKGROUND = \
    STATUS_FRAME_BACKGROUND
STATUS_FOREGROUND = 'sienna'

# Default value of the
# combobox query selection
COMBOBOX_DEFAULT = \
    'Select a query'

CODE_BACKGROUND = CODE_FRAME_BACKGROUND
CODE_FOREGROUND = 'lavender'

CODE_DEFAULT = 'No query selected, ' \
               'Select a query.'


# Width of the combobox
COMBOBOX_WIDTH = 60

# Width of the rows for the
# results treeview table
ROW_WIDTH = 400

# Height of the results
# treeview table
TABLE_HEIGHT = 10

# Max columns allowed for
# queries results display
MAX_COLUMNS = 20
