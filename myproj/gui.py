# Seminar Project
# Made by: Hanan Ben Shabat

from wrapping_label import WrappingLabel
from ttkthemes import ThemedStyle
from tkinter import ttk
from func import *


class GUI:
    def __init__(self):
        # Create a root window
        self.master = Tk()

        self.title_font = \
            get_font(TITLE_FONT_SIZE)

        self.sub_title_font = \
            get_font(SUB_TITLE_FONT_SIZE)

        self.heading_font = \
            get_font(HEADING_FONT_SIZE)

        self.code_font = \
            get_font(CODE_FONT_SIZE)

        self.row_font = \
            get_font(ROW_FONT_SIZE)

        # ****************** Frames ******************

        # Create a frame for containing the frames
        self.window_frame = \
            ttk.Frame(self.master)

        self.valid_examples_frame = \
            ttk.Frame(self.window_frame)

        self.invalid_examples_frame = \
            ttk.Frame(self.window_frame)

        self.insert_note_frame = \
            ttk.Frame(self.window_frame)

        self.insert_query_frame = \
            ttk.Frame(self.window_frame)

        self.input_status_frame = \
            ttk.Frame(self.window_frame)

        self.settings_frame = \
            ttk.Frame(self.window_frame)

        self.code_frame = \
            ttk.Frame(self.window_frame)

        self.selection_frame = \
            ttk.Frame(self.window_frame)

        self.query_frame = \
            ttk.Frame(self.window_frame)

        # ********************************************

        # Create a style for the gui
        self.style = \
            ThemedStyle(self.window_frame)

        # Combobox creation
        self.combobox = \
            ttk.Combobox(self.selection_frame)

        # Create a Treeview that will contain
        # the results of the executed query
        self.results_tree = \
            ttk.Treeview(self.query_frame)

        # ****************** Scales ******************

        self.font_scale = Scale(self.settings_frame)

        self.window_scale = Scale(self.settings_frame)

        # ********************************************

        # ****************** Labels ******************

        self.valid_examples_title = \
            WrappingLabel(self.valid_examples_frame)

        self.invalid_examples_title = \
            WrappingLabel(self.invalid_examples_frame)

        self.insert_query_title = \
            WrappingLabel(self.insert_query_frame)

        self.insert_note_title = \
            WrappingLabel(self.insert_note_frame)

        self.input_status_title = \
            WrappingLabel(self.input_status_frame)

        self.select_query_title = \
            WrappingLabel(self.selection_frame)

        self.font_scale_title = \
            WrappingLabel(self.settings_frame)

        self.window_scale_title = \
            WrappingLabel(self.settings_frame)

        self.selected_code_title = \
            WrappingLabel(self.code_frame)

        self.selected_results_title = \
            WrappingLabel(self.query_frame)

        # ********************************************

        # ***************** Buttons ******************

        self.valid_example_1 = \
            Button(self.valid_examples_frame)

        self.valid_example_2 = \
            Button(self.valid_examples_frame)

        self.valid_example_3 = \
            Button(self.valid_examples_frame)

        self.valid_example_4 = \
            Button(self.valid_examples_frame)

        self.invalid_example_1 = \
            Button(self.invalid_examples_frame)

        self.invalid_example_2 = \
            Button(self.invalid_examples_frame)

        self.invalid_example_3 = \
            Button(self.invalid_examples_frame)

        self.invalid_example_4 = \
            Button(self.invalid_examples_frame)

        self.clear_note_input = \
            Button(self.insert_note_frame)

        self.clear_query_input = \
            Button(self.insert_query_frame)

        self.user_input = \
            Button(self.insert_query_frame)

        # ********************************************

        # ****************** Texts *******************

        self.insert_query = \
            Text(self.insert_query_frame)

        self.insert_note = \
            Text(self.insert_note_frame)

        self.selected_code = \
            Text(self.code_frame)

        self.status = \
            Text(self.input_status_frame)

        # ********************************************

        # **************** Scrollbars ****************

        # insert query
        self.insert_query_scrollbar = \
            ttk.Scrollbar(self.insert_query_frame)

        # insert note
        self.insert_note_scrollbar = \
            ttk.Scrollbar(self.insert_note_frame)

        # query code
        self.code_vertical_scrollbar = \
            ttk.Scrollbar(self.code_frame)

        # status
        self.status_vertical_scrollbar = \
            ttk.Scrollbar(self.input_status_frame)

        # query results
        self.results_vertical_scrollbar = \
            ttk.Scrollbar(self.query_frame)

        self.results_horizontal_scrollbar = \
            ttk.Scrollbar(self.query_frame)

        # ********************************************

        gui_initialize(self)

    # noinspection PyUnusedLocal
    def font_scale_release(self, event):
        """
        target: Scales the font size
        after changing the font scale
        :param event:
        """
        dynamic_font_size(self)

    # noinspection PyUnusedLocal
    def window_scale_release(self, event):
        """
        target: Scales the window size
        after changing the window scale
        :param event:
        """
        dynamic_window_size(self)

    # noinspection PyUnusedLocal
    def on_query_change(self, index, value, op):
        """
        target: When the combobox selection changes:
        Deletes the previous query results,
        code and widgets
        Displays the query results,
        code and widgets of the selected query
        :param str index:
        :param str value:
        :param str op:
        """
        reset_results(self)
        if self.combobox.get() != COMBOBOX_DEFAULT:
            selected_index = self.combobox['values'] \
                .index(self.combobox.get())
            selected_query = QUERIES[selected_index]
            selected_note = NOTES[selected_index]
            update_selected_text(self.selected_code,
                                 selected_query)
            dbconn(self,
                   selected_note,
                   selected_query)
