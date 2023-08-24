#!/usr/bin/env python3

from app.backend.prepare_excel import prepare_excel
from app.frontend.window import Window
from gi import require_versions

require_versions({"Gtk": "4.0", "Adw": "1"})
from gi.repository import Gtk, Adw, Gdk

import pyclip
from app.backend.magnitudes import Magnitudes
from app.frontend.ui import ui, css

entries = []

formats = {
    "latex": {
        "SI": {"scientific", "numeric", "hybrid"},
        "num": {"scientific", "numeric", "hybrid"},
    },
    "raw": "",
}


class Application(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        # load css
        provider = Gtk.CssProvider()
        provider.load_from_data(css(), len(css()))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # BUILDER
        builder = Gtk.Builder()
        builder.add_from_string(ui())

        # WIDGETS
        self.execute_button = builder.get_object("execute_button")
        self.auto_update_switch = builder.get_object("auto_update_switch")
        self.clipboard_button = builder.get_object("clipboard_button")
        self.first_and_last_columns_only_switch = builder.get_object(
            "first_and_last_columns_only_switch"
        )
        self.force_error_switch = builder.get_object("force_error_switch")
        self.error_entry = builder.get_object("error_entry")
        self.per_column_error_switch = builder.get_object("per_column_error_switch")
        self.multi_error_box = builder.get_object("multi_error_box")
        self.textview = builder.get_object("textview")

        # input textview
        self.custom_input_switch = builder.get_object("custom_input_switch")
        self.input_scrolled_window = builder.get_object("input_scrolled_window")
        self.input_textview = builder.get_object("input_textview")

        self.custom_input_switch.connect("state-set", self.toggle_input_scrolled_window)

        self.input_textview.get_buffer().connect("changed", self.auto_update_textview)

        # format comboboxes and entry
        self.format0_combobox = builder.get_object("format0_combobox")
        self.format1_combobox = builder.get_object("format1_combobox")
        self.format2_combobox = builder.get_object("format2_combobox")
        self.hybrid_entry = builder.get_object("hybrid_entry")

        self.hybrid_entry.connect("changed", self.auto_update_textview)

        self.connect_comboboxes()
        self.set_format_combobox_from_values(0, ["latex", "raw"])
        self.set_format_comboboxes_from_list(["latex", "SI", "scientific"])

        # update textview on options change
        self.first_and_last_columns_only_switch.connect(
            "state-set", self.auto_update_textview
        )
        self.force_error_switch.connect("state-set", self.auto_update_textview)
        self.execute_button.connect("clicked", self.update_textview)
        self.error_entry.connect(
            "changed",
            lambda *args: self.auto_update_textview(),  # update only if switch is on
        )

        # create error column
        self.per_column_error_switch.connect("state-set", self.create_error_column)

        # copy to clipboard
        self.clipboard_button.connect("clicked", self.copy_to_clipboard)

        # WINDOW
        self.win = builder.get_object("main_window")
        self.win.set_application(self)
        self.win.present()

        # update textview on start
        self.update_textview(self.execute_button)

    # execute main.py and update textview with the output
    def update_textview(self, *args):
        # get options
        options = self.get_options()

        # call script and show output
        buffer = self.textview.get_buffer()
        magnitudes = Magnitudes(**options)
        output = magnitudes.print()

        # update textview
        buffer.set_text(output)

    def auto_update_textview(self, *args):
        if self.auto_update_switch.get_active():
            self.update_textview()

    def copy_to_clipboard(self, *args):
        buffer = self.textview.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True)
        pyclip.copy(text)

    def toggle_input_scrolled_window(self, *args):
        if self.custom_input_switch.get_active():
            self.input_scrolled_window.show()
        else:
            self.input_scrolled_window.hide()

    def get_options(self):
        use_custom_input = self.custom_input_switch.get_active()
        return {
            "format": self.create_format(),
            "first_and_last_columns_only": self.first_and_last_columns_only_switch.get_active(),
            "force_error": self.force_error_switch.get_active(),
            "error": str(
                self.error_entry.get_text() or self.error_entry.get_placeholder_text()
            ).replace(",", "."),
            "per_column_error": self.per_column_error_switch.get_active(),
            "error_columns": self.read_error_columns(),
            "clipboard": self.input_textview.get_buffer().get_text(
                self.input_textview.get_buffer().get_start_iter(),
                self.input_textview.get_buffer().get_end_iter(),
                True,
            )
            if use_custom_input
            else pyclip.paste().decode("utf-8"),
        }

    def update_format_comboboxes(self, widget):
        """
        Updates the format comboboxes based on the changed widget
        """
        self.disconnect_comboboxes()
        format0_active = self.format0_combobox.get_active_text()
        format1_active = self.format1_combobox.get_active_text()
        format2_active = self.format2_combobox.get_active_text()

        entry = self.hybrid_entry
        hybrid_entry_placeholder = entry.get_placeholder_text()
        hybrid_entry_text = entry.get_text()

        match widget:
            case self.format0_combobox:
                try:
                    format1_items = formats[format0_active].keys()
                except AttributeError:
                    format1_items = formats[format0_active]
                except (TypeError, KeyError):
                    format1_items = []
                self.set_format_combobox_from_values(1, format1_items)
                try:
                    format1_active = self.format1_combobox.get_active_text()
                except AttributeError:
                    format1_active = None

                try:
                    format2_items = formats[format0_active][format1_active].keys()
                except AttributeError:
                    format2_items = formats[format0_active][format1_active]
                except (TypeError, KeyError):
                    format2_items = []
                self.set_format_combobox_from_values(2, format2_items)
                try:
                    format1_active = self.format2_combobox.get_active_text()
                except AttributeError:
                    format1_active = None

                if format0_active == "hybrid":
                    entry.set_sensitive(True)
                    entry.set_text(hybrid_entry_placeholder)
            case self.format1_combobox:
                try:
                    format2_items = formats[format0_active][format1_active]
                except (TypeError, KeyError):
                    format2_items = []
                self.set_format_combobox_from_values(2, format2_items)
                if format1_active == "hybrid":
                    entry.set_sensitive(True)
                    entry.set_text(hybrid_entry_placeholder)
            case self.format2_combobox:
                if format2_active == "hybrid":
                    entry.set_sensitive(True)
                    entry.set_text(hybrid_entry_placeholder)
                else:
                    entry.set_sensitive(False)
                    entry.set_text(hybrid_entry_placeholder)
            case _:
                return

        self.connect_comboboxes()
        self.auto_update_textview()
        return

    def set_format_combobox_from_values(self, idx, values: list[str]):
        """
        Sets the combobox from a list of values and enables/disables it
        """
        combobox = getattr(self, f"format{idx}_combobox")
        combobox.remove_all()
        if len(values) == 0:
            combobox.set_sensitive(False)
            return
        combobox.set_sensitive(True)
        for i, value in enumerate(values):
            combobox.append(str(i), value)
        combobox.set_active_id("0")

    def set_format_comboboxes_from_list(self, format: list):
        """
        Sets the format comboboxes based on the selected options
        """
        num_comboboxes = min(len(format), 3)
        for i in range(num_comboboxes):
            combobox = getattr(self, f"format{i}_combobox")
            combobox.set_active_id("0")
        if len(format) > 3:
            self.hybrid_entry.get_text()

    def create_format(self, *args):
        """
        Creates a format dictionary from the selected options

        Example output:
            {"latex", "SI", "scientific"}
        or
            {"latex", "SI", "hybrid/1.25e3"}
        """
        format2_active = self.format2_combobox.get_active_text()
        text = (
            "hybrid/" + self.hybrid_entry.get_text()
            if not ""
            else self.hybrid_entry.get_placeholder_text()
        )

        format = [
            self.format0_combobox.get_active_text(),
            self.format1_combobox.get_active_text(),
            format2_active if format2_active != "hybrid" else text,
        ]
        print(format)
        return format

    def connect_comboboxes(self):
        self.format0_combobox.connect("changed", self.update_format_comboboxes)
        self.format1_combobox.connect("changed", self.update_format_comboboxes)
        self.format2_combobox.connect("changed", self.update_format_comboboxes)

    def disconnect_comboboxes(self):
        self.format0_combobox.disconnect_by_func(self.update_format_comboboxes)
        self.format1_combobox.disconnect_by_func(self.update_format_comboboxes)
        self.format2_combobox.disconnect_by_func(self.update_format_comboboxes)

    def create_error_column(self, *args):
        """
        Creates an entry for each column
        """
        per_column_error = self.per_column_error_switch.get_active()
        error_box = self.multi_error_box
        if not per_column_error:
            for entry in entries:
                self.multi_error_box.remove(entry)
            entries.clear()
            return

        use_custom_input = self.custom_input_switch.get_active()
        clipboard = (
            self.input_textview.get_buffer().get_text(
                self.input_textview.get_buffer().get_start_iter(),
                self.input_textview.get_buffer().get_end_iter(),
                True,
            )
            if use_custom_input
            else pyclip.paste().decode("utf-8")
        )
        columns = prepare_excel(clipboard)

        for i in range(len(columns)):
            entry = Gtk.Entry()
            entries.append(entry)
            entry.set_name(f"error_entry_{i}")
            entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
            entry.set_placeholder_text("0.10")
            entry.connect("changed", self.auto_update_textview)
            error_box.append(entry)

    def read_error_columns(self):
        """
        Reads the error columns from the entries
        """
        error_columns = []
        for entry in entries:
            text = entry.get_text() or entry.get_placeholder_text()
            error_columns.append(text)
        return error_columns
