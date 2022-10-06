# Seminar Project
# Made by: Hanan Ben Shabat
# Email: hanan.ben.shabat@s.afeka.ac.il

from sqlalchemy import create_engine
from tkinter.font import Font
from constants import *
from queries import *
from tkinter import *
import pandas as pd
import ctypes
import sqlite3


def is_empty(string):
    """
    target: Checks if a string is
    empty or blank or contain
    spaces only

    :param str string: The string that
    will be checked
    :return: True if empty or blank or
    contain spaces only
    False otherwise
    :rtype: bool
    """
    if not (string and not string.isspace()):
        return True
    else:
        return False


def is_digit(string):
    """
    target: Checks if a string is
    numeric
    :param str string: The string that
    will be checked
    :return: True if numeric
    False otherwise
    :rtype: bool
    """
    if string == 'None':
        string = '0'
    return string.lstrip('-'). \
        replace('.', '').isdigit()


def dbconn(obj, note, query, button=None):
    """
    target: Connect to the DB and
    execute a query
    :param gui obj: Object containing
    all the widgets
    :param str note: Note explaining
    the query
    :param str query: Sqlite query
    :param bool button: Indication
    weather the entrance to the function
    was via a lambda button click
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    engine = create_engine(SQL_LITE_PATH)
    execute_query(obj,
                  note,
                  query,
                  cur,
                  engine,
                  button=button)
    conn.close()


def execute_query(obj, note, query, cur, engine, button=None):
    """
    target: Executes a query and displays it
    :param gui obj: Object containing
    all the widgets
    :param str note: Note explaining
    the query
    :param str query: Sqlite query
    :param sqlite3.Cursor cur: Cursor
    used for iterating the sqlite query
    :param sqlalchemy.engine.base.Engine engine:
    Sqlite engine
    :param bool button: Indication
    weather the entrance to the function
    was via a lambda button click
    :raises error_empty: if the query is
    empty or blank or contain
    spaces only
    :raises error_not_long: if the length
    of the note is over the max limit
    :raises error_description: if there
    are any sql related errors for the
    query execution
    """
    try:
        if is_empty(query):
            update_selected_text(obj.status,
                                 ERROR_EMPTY)
            obj.status \
                .configure(background=ERROR_BACKGROUND,
                           foreground=ERROR_FOREGROUND)
            obj.input_status_title \
                .configure(background=ERROR_TITLE_BACKGROUND,
                           foreground=ERROR_TITLE_FOREGROUND)
        else:
            cur.execute(query)
            results = cur.fetchall()
            if len(note) > NOTE_MAX_LENGTH:
                update_selected_text(obj.status,
                                     ERROR_NOTE_LONG)
                obj.status \
                    .configure(background=ERROR_BACKGROUND,
                               foreground=ERROR_FOREGROUND)
                obj.input_status_title \
                    .configure(background=ERROR_TITLE_BACKGROUND,
                               foreground=ERROR_TITLE_FOREGROUND)
            else:
                if button:
                    add_query(obj, note, query)
                else:
                    display_with_engine(obj,
                                        results,
                                        query,
                                        cur,
                                        engine)

    except Exception as error_description:

        update_selected_text(obj.status,
                             f'{ERROR}{error_description}')
        obj.status \
            .configure(background=ERROR_BACKGROUND,
                       foreground=ERROR_FOREGROUND)
        obj.input_status_title \
            .configure(background=ERROR_TITLE_BACKGROUND,
                       foreground=ERROR_TITLE_FOREGROUND)


def add_query(obj, note, query):
    """
    target: Adds the query and note
    to the obj widgets
    :param gui obj: Object containing
    all the widgets
    :param str note: Note explaining
    the query
    :param str query: Sqlite query
    """
    QUERIES.append(query)
    NOTES.append(note)
    clear_note_input(obj)
    clear_query_input(obj)
    queries_selection_values(obj)
    combobox_last_index = len(obj.combobox['values']) - 1
    obj.combobox.current(combobox_last_index)
    update_selected_text(obj.status, SUCCESS_IMPORTED)
    obj.status \
        .configure(background=SUCCESS_BACKGROUND,
                   foreground=SUCCESS_FOREGROUND)
    obj.input_status_title \
        .configure(background=SUCCESS_TITLE_BACKGROUND,
                   foreground=SUCCESS_TITLE_FOREGROUND)


def display_with_engine(obj, results, query, cur, engine):
    """
    target: Displays the results
    of a query execution
    :param gui obj: Object containing
    all the widgets
    :param list results: Fetched results
    from the executed query
    :param str query: Sqlite query
    :param sqlite3.Cursor cur: Cursor
    used for iterating the sqlite query
    :param sqlalchemy.engine.base.Engine engine:
    Sqlite engine
    """
    df = pd.DataFrame(results)
    df.columns = [x[0] for x in cur.description]
    row_w = ROW_WIDTH
    if len(df.columns) == 1:
        row_w = int(row_w * 5.048)
    if len(df.columns) == 2:
        row_w *= 2.52
    if len(df.columns) == 3:
        row_w *= 1.69
    if len(df.columns) == 4:
        row_w = int(row_w * 1.26)

    cols = list(range(len(df.columns)))

    obj.results_tree['style'] = 'results_tree.Treeview'
    obj.results_tree['columns'] = cols

    # Configures scrollbar
    obj.results_vertical_scrollbar \
        .config(command=obj.results_tree.yview)
    obj.results_horizontal_scrollbar \
        .config(command=obj.results_tree.xview)

    # Adds headings to the treeview
    for i in range(len(df.columns)):
        obj.results_tree \
            .heading(column=f'{i}',
                     text=f'{df.columns[i]}',
                     anchor='w',
                     command=lambda col=f'{i}':
                     sort_column(obj.results_tree,
                                 col,
                                 False))
        obj.results_tree \
            .column(column=f'{i}',
                    minwidth=0,
                    width=int(row_w),
                    anchor='w',
                    stretch=False)

    # Add values to the treeview
    rs = engine.execute(query)
    for row in rs:
        obj.results_tree \
            .insert('',
                    'end',
                    values=row[0:MAX_COLUMNS])

    obj.results_tree['show'] = 'headings'
    obj.results_tree.grid(row=1,
                          column=0,
                          sticky='nsew')


def get_font(font_size):
    """
    target: Getting a font with
    the default type and the size
    from the input
    :param int font_size: Font size
    :return: Font with the default
    font type and the inserted
    font size
    """
    return Font(family=DEFAULT_FONT_TYPE,
                size=font_size)


def edge_case(num):
    """
    target: Checks for cases
    in a string, where none means 0
    and '-', '_' don't mean anything.
    the main goal is to figure out if
    the string might be a number.
    :param str num: The string input
    that might be a number if the
    edge cases are removed
    :return: The modified input
    after removing the edge cases
    """
    if num == 'None':
        return 0
    if '-' in num:
        num.replace('-', '')
    if '_' in num:
        num.replace('_', '')
    if is_digit(num):
        return float(num)
    return num


#
def sort_column(tree, column, reverse):
    """
    target: Sorts the treeview columns
    upon clicking on the columns headings
    If clicked on the column headings
    again sort the columns reversed
    :param Treeview tree: Treeview table
    containing the results of the selected
    query's execution
    :param str column: Column of the treeview
    :param bool reverse: Indication of the
    sorting type
    """
    li = [(tree.set(k, column), k)
          for k in tree.get_children('')]
    li.sort(key=lambda k: (str(type(edge_case(k[0]))),
                           edge_case(k[0])),
            reverse=reverse)

    for index, (val, k) in enumerate(li):
        tree.move(k, '', index)

    tree.heading(column,
                 command=lambda:
                 sort_column(tree,
                             column,
                             not reverse))


def queries_selection_values(obj):
    """
    target: Gets the queries notes to the
    combobox dropdown selection
    :param gui obj: Object containing
    all the widgets
    """
    queries_length = len(QUERIES)
    digit_range = range(1, 10)
    single_digit_values = \
        ['0' + str(i) + ' - ' + NOTES[i - 1]
         for i in digit_range]
    if queries_length < 10:
        return single_digit_values
    multi_digit_range = range(10, queries_length + 1)
    multi_digit_values = \
        [str(i) + ' - ' + NOTES[i - 1]
         for i in multi_digit_range]
    v = single_digit_values + multi_digit_values
    obj.combobox.configure(values=v)


def update_selected_text(text, updated_text):
    """
    target: sets the text values
    to the updated_text's values
    :param Text text: Selected text
    :param str updated_text: Value to
    change for the selected text
    """
    text.delete('1.0', 'end')
    text.insert('end', updated_text)


def reset_results(obj):
    """
    target: Resets the query
    results display
    :param gui obj: Object containing
    all the widgets
    """
    if obj.combobox.get() != \
            COMBOBOX_DEFAULT:
        for tree_c in \
                obj.results_tree.get_children():
            obj.results_tree.delete(tree_c)

        obj.results_vertical_scrollbar \
            .grid(row=1,
                  column=1,
                  sticky='nsew')
        obj.results_horizontal_scrollbar \
            .grid(row=2,
                  column=0,
                  sticky='nsew')


def reset_font_size(obj):
    """
    target: Set's the font
    size to the default values
    :param gui obj: Object containing
    all the widgets
    """
    obj.title_font['size'] = TITLE_FONT_SIZE
    obj.sub_title_font['size'] = SUB_TITLE_FONT_SIZE
    obj.heading_font['size'] = HEADING_FONT_SIZE
    obj.code_font['size'] = CODE_FONT_SIZE
    obj.row_font['size'] = ROW_FONT_SIZE


def dynamic_font_size(obj):
    """
    target: Set's the font
    size based on the user's
    selected scale size
    :param gui obj: Object containing
    all the widgets
    """
    reset_font_size(obj)

    obj.title_font['size'] = \
        int(obj.title_font['size'] *
            obj.font_scale.get())

    obj.sub_title_font['size'] = \
        int(obj.sub_title_font['size'] *
            obj.font_scale.get())

    obj.heading_font['size'] = \
        int(obj.heading_font['size'] *
            obj.font_scale.get())

    obj.code_font['size'] = \
        int(obj.code_font['size'] *
            obj.font_scale.get())

    obj.row_font['size'] = \
        int(obj.row_font['size'] *
            obj.font_scale.get())


def dynamic_window_size(obj):
    """
    target: Set's the window
    size based on the user's
    selected scale size
    :param gui obj: Object containing
    all the widgets
    """
    screen_width = \
        obj.master.winfo_screenwidth()

    screen_height = \
        obj.master.winfo_screenheight()

    window_width = int(screen_width *
                       obj.window_scale.get())

    window_height = int(screen_height *
                        obj.window_scale.get())

    root_x = (screen_width / 2) - \
             (window_width / 2)

    root_y = (screen_height / 2) - \
             (window_height / 2)

    # Sets the dimensions of
    # the screen and where it is placed
    obj.master.geometry('%dx%d+%d+%d' %
                        (window_width,
                         window_height,
                         root_x,
                         root_y))


def root_dynamic(obj):
    """
    target: Adapts the main window dimensions
    to the user's screen resolution
    :param gui obj: Object containing
    all the widgets
    """
    # Adapts to the OS DPI settings
    ctypes.windll \
        .shcore \
        .SetProcessDpiAwareness(2)

    dynamic_font_size(obj)
    dynamic_window_size(obj)

    # TODO: MAKE DYNAMIC:
    obj.master.minsize(1000, 700)


def root_attributes(obj):
    """
    target: Add attributes to the root
    :param gui obj: Object containing
    all the widgets
    """
    obj.heading_font['weight'] = 'bold'

    obj.title_font['weight'] = 'bold'

    obj.title_font['underline'] = True

    obj.sub_title_font['underline'] = True

    # Applies the title for the window
    obj.master.title(ROOT_TITLE)

    # Applies the icon image
    # for the window icon
    obj.master.iconbitmap(ROOT_ICON_PATH)

    # Window is on top of other windows
    obj.master.wm_attributes('-topmost', 1)

    # Adds the heading font to
    # the combobox dropdown list
    obj.master.option_add('*TCombobox*Listbox*Font',
                          obj.heading_font)


def title_initialize(titleLabel, title, title_background, title_font):
    """
    target: Applies the inserted
    attributes to the input
    label's widgets, along with
    initial values on a 0,0
    grid cell
    :param titleLabel: Input label
    :param title: Text
    :param title_background: Background
    :param title_font: Font
    """
    titleLabel.grid(row=0,
                    column=0,
                    columnspan=2,
                    sticky='nsew')

    titleLabel.configure(background=title_background,
                         font=title_font)

    titleLabel['text'] = title


def titles_initialize(obj):
    """
    target: Initializing all the
    obj titles
    :param gui obj: Object containing
    all the widgets
    """
    # query and note valid examples
    title_initialize(obj.valid_examples_title,
                     VALID_EXAMPLES_TITLE_TEXT,
                     VALID_EXAMPLES_TITLE_BACKGROUND,
                     obj.title_font)

    # query and note invalid examples
    title_initialize(obj.invalid_examples_title,
                     INVALID_EXAMPLES_TITLE_TEXT,
                     INVALID_EXAMPLES_TITLE_BACKGROUND,
                     obj.title_font)

    # Insert a new note
    title_initialize(obj.insert_note_title,
                     INSERT_NOTE_TITLE_TEXT,
                     INSERT_NOTE_TITLE_BACKGROUND,
                     obj.title_font)

    # Insert a new query code
    title_initialize(obj.insert_query_title,
                     INSERT_QUERY_TITLE_TEXT,
                     INSERT_QUERY_TITLE_BACKGROUND,
                     obj.title_font)

    # Status of the submission of the user input
    title_initialize(obj.input_status_title,
                     STATUS_TITLE_TEXT,
                     STATUS_TITLE_BACKGROUND,
                     obj.title_font)

    # Select a query to perform
    title_initialize(obj.select_query_title,
                     SELECT_QUERY_TITLE_TEXT,
                     SELECT_QUERY_TITLE_BACKGROUND,
                     obj.title_font)

    # Font scale
    title_initialize(obj.font_scale_title,
                     FONT_SCALE_TITLE_TEXT,
                     FONT_SCALE_TITLE_BACKGROUND,
                     obj.title_font)
    obj.font_scale_title.grid(columnspan=1)

    # Window scale
    title_initialize(obj.window_scale_title,
                     WINDOW_SCALE_TITLE_TEXT,
                     WINDOW_SCALE_TITLE_BACKGROUND,
                     obj.title_font)
    obj.window_scale_title.grid(column=1,
                                columnspan=1)

    # Selected query code
    title_initialize(obj.selected_code_title,
                     CODE_TITLE_TEXT,
                     CODE_TITLE_BACKGROUND,
                     obj.title_font)

    # Selected query results
    title_initialize(obj.selected_results_title,
                     RESULTS_TITLE_TEXT,
                     RESULTS_TITLE_BACKGROUND,
                     obj.title_font)


def grid_initialize(obj):
    """
    target: Initializing the
    obj's frames grids
    :param gui obj: Object containing
    all the widgets
    """
    # window_frame
    obj.window_frame \
        .grid_propagate(False)
    obj.window_frame \
        .grid_columnconfigure(0,
                              weight=4)
    obj.window_frame \
        .grid_columnconfigure(1,
                              weight=1)
    obj.window_frame \
        .grid_columnconfigure(2,
                              weight=1)
    obj.window_frame \
        .grid_rowconfigure(0,
                           weight=1,
                           minsize=75)
    obj.window_frame \
        .grid_rowconfigure(1,
                           weight=2,
                           minsize=100)
    obj.window_frame \
        .grid_rowconfigure(2,
                           weight=3,
                           minsize=100)
    obj.window_frame \
        .grid_rowconfigure(3,
                           weight=1,
                           minsize=100)
    obj.window_frame \
        .grid_rowconfigure(4,
                           weight=0)

    # valid_examples_frame
    obj.valid_examples_frame \
        .grid_propagate(False)
    obj.valid_examples_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.valid_examples_frame. \
        grid_rowconfigure(1,
                          weight=0)
    obj.valid_examples_frame \
        .grid_rowconfigure(2,
                           weight=1)
    obj.valid_examples_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.valid_examples_frame \
        .grid_columnconfigure(1,
                              weight=1)
    obj.valid_examples_frame \
        .grid_columnconfigure(2,
                              weight=1)
    obj.valid_examples_frame \
        .grid_columnconfigure(3,
                              weight=1)

    # invalid_examples_frame
    obj.invalid_examples_frame \
        .grid_propagate(False)
    obj.invalid_examples_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.invalid_examples_frame \
        .grid_rowconfigure(1,
                           weight=0)
    obj.invalid_examples_frame \
        .grid_rowconfigure(2,
                           weight=1)
    obj.invalid_examples_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.invalid_examples_frame \
        .grid_columnconfigure(1,
                              weight=1)
    obj.invalid_examples_frame \
        .grid_columnconfigure(2,
                              weight=1)
    obj.invalid_examples_frame \
        .grid_columnconfigure(3,
                              weight=1)

    # insert_note_frame
    obj.insert_note_frame \
        .grid_propagate(False)
    obj.insert_note_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.insert_note_frame \
        .grid_rowconfigure(1,
                           weight=1)
    obj.insert_note_frame \
        .grid_rowconfigure(2,
                           weight=0)
    obj.insert_note_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.insert_note_frame \
        .grid_columnconfigure(1,
                              weight=0)

    # insert_query_frame
    obj.insert_query_frame \
        .grid_propagate(False)
    obj.insert_query_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.insert_query_frame \
        .grid_rowconfigure(1,
                           weight=1)
    obj.insert_query_frame \
        .grid_rowconfigure(2,
                           weight=0)
    obj.insert_query_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.insert_query_frame \
        .grid_columnconfigure(1,
                              weight=0)

    # input_status_frame
    obj.input_status_frame \
        .grid_propagate(False)
    obj.input_status_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.input_status_frame \
        .grid_rowconfigure(1,
                           weight=1)
    obj.input_status_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.input_status_frame \
        .grid_columnconfigure(1,
                              weight=0)

    # settings_frame
    obj.settings_frame \
        .grid_propagate(False)
    obj.settings_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.settings_frame \
        .grid_rowconfigure(1,
                           weight=1)
    obj.settings_frame \
        .grid_rowconfigure(2,
                           weight=0)
    obj.settings_frame \
        .grid_rowconfigure(3,
                           weight=1)
    obj.settings_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.settings_frame \
        .grid_columnconfigure(1,
                              weight=1)
    # selection_frame
    obj.selection_frame \
        .grid_propagate(False)
    obj.selection_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.selection_frame \
        .grid_rowconfigure(1,
                           weight=0)
    obj.selection_frame \
        .grid_columnconfigure(0,
                              weight=1)

    # code_frame
    obj.code_frame \
        .grid_propagate(False)
    obj.code_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.code_frame \
        .grid_rowconfigure(1,
                           weight=1)
    obj.code_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.code_frame \
        .grid_columnconfigure(1,
                              weight=0)

    # query_frame
    obj.query_frame \
        .grid_rowconfigure(0,
                           weight=0)
    obj.query_frame \
        .grid_rowconfigure(1,
                           weight=1)
    obj.query_frame \
        .grid_rowconfigure(2,
                           weight=0)
    obj.query_frame \
        .grid_columnconfigure(0,
                              weight=1)
    obj.query_frame \
        .grid_columnconfigure(1,
                              weight=0)


def frame_initialize(obj):
    """
    target: Initializing the
    obj's frames
    :param gui obj: Object containing
    all the widgets
    """
    obj.window_frame['style'] = \
        'window_frame.TFrame'
    obj.valid_examples_frame['style'] = \
        'valid_examples_frame.TFrame'
    obj.invalid_examples_frame['style'] = \
        'invalid_examples_frame.TFrame'
    obj.insert_query_frame['style'] = \
        'insert_query_frame.TFrame'
    obj.insert_note_frame['style'] = \
        'inset_note_frame.TFrame'
    obj.input_status_frame['style'] = \
        'input_status_frame.TFrame'
    obj.selection_frame['style'] = \
        'selection_frame.TFrame'
    obj.code_frame['style'] = \
        'code_frame.TFrame'
    obj.query_frame['style'] = \
        'query_frame.TFrame'

    obj.window_frame.pack(side='right',
                          fill='both',
                          expand=True)

    grid_initialize(obj)

    obj.settings_frame.grid(row=0,
                            column=0,
                            sticky='nsew')
    obj.valid_examples_frame.grid(row=0,
                                  column=1,
                                  sticky='nsew')
    obj.invalid_examples_frame.grid(row=0,
                                    column=2,
                                    sticky='nsew')
    obj.code_frame.grid(row=1,
                        column=0,
                        rowspan=2,
                        sticky='nsew')
    obj.insert_note_frame.grid(row=1,
                               column=1,
                               columnspan=2,
                               sticky='nsew')
    obj.insert_query_frame.grid(row=2,
                                column=1,
                                columnspan=2,
                                sticky='nsew')
    obj.input_status_frame.grid(row=3,
                                column=1,
                                columnspan=2,
                                sticky='nsew')
    obj.selection_frame.grid(row=3,
                             column=0,
                             sticky='nsew')
    obj.query_frame.grid(row=4,
                         column=0,
                         columnspan=3,
                         sticky='nsew')


# Initialize the root
def root_initialize(obj):
    """
    target: Initializing the
    obj's root
    :param gui obj: Object containing
    all the widgets
    """
    root_dynamic(obj)
    root_attributes(obj)


# Initialize the combobox
def combobox_initialize(obj):
    """
    target: Initializing the
    obj's combobox
    :param gui obj: Object containing
    all the widgets
    """
    # Query selection
    # qs is the int variable for the
    # select box combobox of the
    # queries' selection array
    # indicating the selected index
    obj.qs = IntVar()

    # Trace function will be executed
    # when the selected query of the
    # query selection combobox changes
    # The first argument indicates the mode
    # w means write
    # The second argument indicates the
    # traced executed function
    obj.qs.trace('w', obj.on_query_change)

    # Configure the query selection combobox
    obj.combobox. \
        configure(textvar=obj.qs,
                  width=COMBOBOX_WIDTH,
                  font=obj.heading_font,
                  state='readonly')
    queries_selection_values(obj)

    # Setting the default value for the combobox
    obj.combobox.set(COMBOBOX_DEFAULT)

    obj.combobox.grid(row=1,
                      column=0,
                      columnspan=2,
                      sticky='nsew')


def scale_initialize(obj):
    """
    target: Initializing the
    obj's font and window scales
    :param gui obj: Object containing
    all the widgets
    """

    obj.font_scale.bind("<ButtonRelease-1>", obj.font_scale_release)

    obj.window_scale.bind("<ButtonRelease-1>", obj.window_scale_release)

    obj.font_scale \
        .configure(from_=1.5,
                   to=0.5,
                   resolution=0.01,
                   background='light blue',
                   activebackground='light green',
                   orient='horizontal')
    obj.window_scale \
        .configure(from_=1.0,
                   to=0.5,
                   resolution=0.01,
                   background='light blue',
                   activebackground='light green',
                   orient='horizontal')

    obj.font_scale.set(1)

    obj.font_scale.grid(row=1,
                        column=0,
                        sticky='nsew')
    obj.window_scale.grid(row=1,
                          column=1,
                          sticky='nsew')


def insert_query_textbox(obj):
    """
    target: Initializing the
    obj's insert query textbox
    :param gui obj: Object containing
    all the widgets
    """
    obj.insert_query \
        .grid(row=1,
              column=0,
              sticky='nsew')
    obj.insert_query_scrollbar. \
        grid(row=1,
             column=1,
             sticky='nsew')
    obj.insert_query_scrollbar \
        .config(command=obj.insert_query.yview,
                orient='vertical')
    obj.insert_query \
        .configure(yscrollcommand=obj.insert_query_scrollbar.set,
                   font=obj.heading_font,
                   height=5,
                   bd=0,
                   background=INSERT_QUERY_BACKGROUND)


def insert_note_textbox(obj):
    """
    target: Initializing the
    obj's insert note textbox
    :param gui obj: Object containing
    all the widgets
    """
    obj.insert_note \
        .configure(yscrollcommand=obj.insert_note_scrollbar.set,
                   font=obj.heading_font,
                   height=5,
                   bd=0,
                   background=INSERT_NOTE_BACKGROUND)
    obj.clear_note_input \
        .configure(text=CLEAR_BUTTON_TEXT,
                   background=CLEAR_BUTTON_BACKGROUND,
                   activebackground=CLEAR_BUTTON_ACTIVE_BACKGROUND,
                   foreground=CLEAR_BUTTON_FOREGROUND,
                   borderwidth=CLEAR_BUTTON_BORDER_WIDTH,
                   font=obj.heading_font,
                   command=lambda: clear_note_input(obj))
    obj.insert_note \
        .grid(row=1,
              column=0,
              sticky='nsew')
    obj.insert_note_scrollbar \
        .grid(row=1,
              column=1,
              sticky='nsew')
    obj.insert_note_scrollbar \
        .config(command=obj.insert_note.yview,
                orient='vertical')
    obj.clear_note_input \
        .grid(row=2,
              column=0,
              sticky='w')


def clear_note_input(obj):
    """
    target: clearing the
    obj's insert note textbox
    :param gui obj: Object containing
    all the widgets
    """
    update_selected_text(obj.insert_note, '')


def clear_query_input(obj):
    """
    target: clearing the
    obj's insert query textbox
    :param gui obj: Object containing
    all the widgets
    """
    update_selected_text(obj.insert_query, '')


def export_user_input(obj):
    """
    target: Retrieves the user input
    to the obj's widgets
    :param gui obj: Object containing
    all the widgets
    """
    note_input = \
        obj.insert_note.get('1.0',
                            'end-1c')
    query_input = \
        obj.insert_query.get('1.0',
                             'end-1c')

    if is_empty(query_input):
        update_selected_text(obj.status, ERROR_EMPTY)
        obj.status \
            .configure(background=ERROR_BACKGROUND,
                       foreground=ERROR_FOREGROUND)
        obj.input_status_title \
            .configure(background=ERROR_TITLE_BACKGROUND,
                       foreground=ERROR_TITLE_FOREGROUND)
    else:
        if is_empty(note_input):
            note_input = \
                INSERT_NOTE_DEFAULT
        dbconn(obj,
               note_input,
               query_input,
               button=True)


def insert_query_buttons(obj):
    """
    target: initializing the
    obj's submit and clear buttons
    :param gui obj: Object containing
    all the widgets
    """
    obj.clear_query_input \
        .configure(text=CLEAR_BUTTON_TEXT,
                   background=CLEAR_BUTTON_BACKGROUND,
                   activebackground=CLEAR_BUTTON_ACTIVE_BACKGROUND,
                   foreground=CLEAR_BUTTON_FOREGROUND,
                   borderwidth=CLEAR_BUTTON_BORDER_WIDTH,
                   font=obj.heading_font,
                   command=lambda: clear_query_input(obj))
    obj.user_input \
        .configure(text=USER_INPUT_TEXT,
                   background=USER_INPUT_BACKGROUND,
                   activebackground=USER_INPUT_ACTIVE_BACKGROUND,
                   foreground=USER_INPUT_FOREGROUND,
                   activeforeground=USER_INPUT_ACTIVE_FOREGROUND,
                   borderwidth=USER_INPUT_BORDER_WIDTH,
                   font=obj.heading_font,
                   command=lambda: export_user_input(obj))
    obj.clear_query_input.grid(row=2,
                               column=0,
                               sticky='w')
    obj.user_input.grid(row=2,
                        column=0,
                        sticky='n')


def import_example(obj, note, query):
    """
    target: Sets the obj's inserted
    note's and query's text to the
    input's note and query values
    :param gui obj: Object containing
    all the widgets
    :param str note: Note explaining
    the query
    :param str query: Sqlite query
    """
    update_selected_text(obj.insert_note,
                         note)
    update_selected_text(obj.insert_query,
                         query)


def import_example_button(is_button_valid, obj, example_button, example_number):
    """
    target: Initializing an example
    button in the obj
    :param bool is_button_valid: Indicating
    the button's type
    :param gui obj: Object containing
    all the widgets
    :param Button example_button: The button's
    objective
    :param int example_number: The button's
    number
    """
    if is_button_valid:
        imported_example_note = \
            NOTES_VALID_EXAMPLE[example_number]
        imported_example_query = \
            QUERIES_VALID_EXAMPLE[example_number]
        button_background = \
            VALID_EXAMPLE_BUTTON_BACKGROUND
        button_active_background \
            = VALID_EXAMPLE_BUTTON_ACTIVE_BACKGROUND
        button_foreground = \
            VALID_EXAMPLE_BUTTON_FOREGROUND
    else:
        imported_example_note = \
            NOTES_INVALID_EXAMPLE[example_number]
        imported_example_query = \
            QUERIES_INVALID_EXAMPLE[example_number]
        button_background = \
            INVALID_EXAMPLE_BUTTON_BACKGROUND
        button_active_background = \
            INVALID_EXAMPLE_BUTTON_ACTIVE_BACKGROUND
        button_foreground = \
            INVALID_EXAMPLE_BUTTON_FOREGROUND

    example_button \
        .configure(text=example_number + 1,
                   background=button_background,
                   activebackground=button_active_background,
                   foreground=button_foreground,
                   font=obj.heading_font,
                   command=lambda:
                   import_example(obj,
                                  imported_example_note,
                                  imported_example_query))

    example_button \
        .grid(row=2,
              column=example_number % 4,
              columnspan=1,
              sticky='nsew')


def import_all_example_buttons(obj):
    """
    target: Initializing the
    obj's example buttons
    :param gui obj: Object containing
    all the widgets
    """
    obj.valid_examples_title \
        .grid(row=1,
              column=0,
              columnspan=4,
              sticky='nsew')
    obj.invalid_examples_title \
        .grid(row=1,
              column=0,
              columnspan=4,
              sticky='nsew')

    import_example_button(True,
                          obj,
                          obj.valid_example_1,
                          0)
    import_example_button(True,
                          obj,
                          obj.valid_example_2,
                          1)
    import_example_button(True,
                          obj,
                          obj.valid_example_3,
                          2)
    import_example_button(True,
                          obj,
                          obj.valid_example_4,
                          3)

    import_example_button(False,
                          obj,
                          obj.invalid_example_1,
                          0)
    import_example_button(False,
                          obj,
                          obj.invalid_example_2,
                          1)
    import_example_button(False,
                          obj,
                          obj.invalid_example_3,
                          2)
    import_example_button(False,
                          obj,
                          obj.invalid_example_4,
                          3)


def textbox_initialize(obj):
    """
    target: Initializing the
    obj's textboxes
    :param gui obj: Object containing
    all the widgets
    """
    insert_query_textbox(obj)
    insert_note_textbox(obj)
    insert_query_buttons(obj)
    import_all_example_buttons(obj)


def code_initialize(obj):
    """
    target: Initializing the
    obj's query code display
    :param gui obj: Object containing
    all the widgets
    """
    obj.selected_code \
        .grid(row=1,
              column=0,
              sticky='nsew')
    obj.code_vertical_scrollbar \
        .grid(row=1,
              column=1,
              sticky='nsew')
    obj.code_vertical_scrollbar \
        .config(command=obj.selected_code.yview,
                orient='vertical')

    # Configure the code text
    obj.selected_code \
        .configure(yscrollcommand=obj.code_vertical_scrollbar.set,
                   font=obj.code_font,
                   height=50,
                   bd=0,
                   background=CODE_BACKGROUND,
                   foreground=CODE_FOREGROUND)

    obj.selected_code \
        .insert('end',
                CODE_DEFAULT)

    obj.selected_code \
        .bind('<Key>',
              lambda e: 'break')


def status_initialize(obj):
    """
    target: Initializing the
    obj's status
    :param gui obj: Object containing
    all the widgets
    """
    obj.status \
        .grid(row=1,
              column=0,
              sticky='nsew')
    obj.status_vertical_scrollbar \
        .grid(row=1,
              column=1,
              sticky='nsew')
    obj.status_vertical_scrollbar \
        .config(command=obj.selected_code.yview,
                orient='vertical')

    obj.status \
        .configure(yscrollcommand=obj.status_vertical_scrollbar.set,
                   font=obj.sub_title_font,
                   height=5,
                   borderwidth=0,
                   bd=0,
                   background=STATUS_BACKGROUND,
                   foreground=STATUS_FOREGROUND)

    obj.status.insert('end', STATUS_DEFAULT)

    obj.status.bind('<Key>', lambda s: 'break')


def results_display_initialize(obj):
    """
    target: Initialize the
    query results display
    :param gui obj: Object containing
    all the widgets
    """
    # Configure the vertical scrollbar
    obj.results_vertical_scrollbar \
        .configure(orient='vertical',
                   command=obj.results_tree.yview)

    # Configure the horizontal scrollbar
    obj.results_horizontal_scrollbar \
        .configure(orient='horizontal',
                   command=obj.results_tree.xview)

    # Configure the results tree
    obj.results_tree \
        .configure(yscrollcommand=obj.results_vertical_scrollbar.set,
                   xscrollcommand=obj.results_horizontal_scrollbar.set,
                   height=TABLE_HEIGHT,
                   show='headings',
                   selectmode='browse')


def style_initialize(obj):
    """
    target: Initializing the
    obj's style
    :param gui obj: Object containing
    all the widgets
    """
    # Setting the theme of the style
    obj.style.set_theme(STYLE_THEME)

    # **************** Frames ****************
    obj.style \
        .configure('TFrame',
                   relief='sunken')

    obj.style \
        .configure('valid_examples_frame.TFrame',
                   background=VALID_EXAMPLES_FRAME_BACKGROUND)

    obj.style \
        .configure('invalid_examples_frame.TFrame',
                   background=INVALID_EXAMPLES_FRAME_BACKGROUND)

    obj.style \
        .configure('inset_note_frame.TFrame',
                   background=INSERT_NOTE_FRAME_BACKGROUND)

    obj.style \
        .configure('insert_query_frame.TFrame',
                   background=INSERT_QUERY_FRAME_BACKGROUND)

    obj.style \
        .configure('input_status_frame.TFrame',
                   background=STATUS_FRAME_BACKGROUND)

    obj.style \
        .configure('selection_frame.TFrame',
                   background=QUERY_SELECTION_FRAME_BACKGROUND)

    obj.style \
        .configure('code_frame.TFrame',
                   background=CODE_FRAME_BACKGROUND)

    obj.style \
        .configure('query_frame.TFrame')

    # **************** Treeview ****************

    obj.style \
        .configure('results_tree.Treeview',
                   font=obj.row_font,
                   rowheight=20,  #
                   relief='flat')

    obj.style \
        .configure('results_tree.Treeview.Heading',
                   font=obj.heading_font)


def gui_initialize(obj):
    """
    target: Initializing the
    obj's widgets and runs
    the main window
    :param gui obj: Object containing
    all the widgets
    """
    # Initialize the widgets
    style_initialize(obj)
    frame_initialize(obj)
    titles_initialize(obj)
    combobox_initialize(obj)
    scale_initialize(obj)
    textbox_initialize(obj)
    code_initialize(obj)
    status_initialize(obj)
    results_display_initialize(obj)
    root_initialize(obj)

    # Runs the main window
    obj.master.mainloop()
