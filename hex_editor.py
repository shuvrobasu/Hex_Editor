#Hex editor v2.3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import os
import struct
import hashlib
import datetime
import json
import tkinter.font as tkfont
import zlib


# Constants and Theme Colors
BYTES_PER_ROW = 16
ASCII_FONT = ("Segoe UI", 11)
HEX_FONT = ("Terminal", 11)
ROW_H = 22
CELL_W = 34
ASCII_W = 15
LINE_NUM_COL_W = 90

LIGHT_THEME_COLORS = {
    "BG": "#f0f0f0", "FG": "#333333", "PANEL_BG": "#e9e9e9", "PANEL_FG": "#1a1a1a",
    "STATUS_BG": "#d0d0d0", "STATUS_FG": "#000000", "OFFSET_BG": "#e0e0e0", "OFFSET_COLOR": "#007bff",
    "HEX_CELL_EVEN_BG": "#fcfcfc", "HEX_CELL_ODD_BG": "#f5f5f5", "HEX_CELL_OUTLINE": "#cccccc",
    "HEX_VALUE_COLOR": "#222222", "ASCII_BG": "#000000", "ACCENT": "#28a745",
    "HEX_SEL_COLOR": "#d8f51b", "CURSOR_COLOR": "#ffc107", "EDIT_BG": "#ffffff", "EDIT_FG": "#000000",
    "EDIT_CURSOR": "#dc3545", "BUTTON_BG": "#e0e0e0", "BUTTON_FG": "#333333",
    "BUTTON_ACTIVE_BG": "#d5d5d5", "RANGE_SEL_COLOR": "#99ccff", "THEME_NAME": "Light"
}

PYTHONPLUS_THEME_COLORS = {
    "BG": "#0d1b2a", "FG": "#e0e0e0", "PANEL_BG": "#1b263b", "PANEL_FG": "#e0e0e0",
    "STATUS_BG": "#0d1b2a", "STATUS_FG": "#ffffff", "OFFSET_BG": "#2e4a6a", "OFFSET_COLOR": "#7aa0ff",
    "HEX_CELL_EVEN_BG": "#233857", "HEX_CELL_ODD_BG": "#2a4266", "HEX_CELL_OUTLINE": "#4a6c9c",
    "HEX_VALUE_COLOR": "#ffffff", "ASCII_BG": "#0d1b2a", "ACCENT": "#4dd2ff",
    "HEX_SEL_COLOR": "#6aa2ff", "CURSOR_COLOR": "#ffdb58", "EDIT_BG": "#3e527d", "EDIT_FG": "#ffffff",
    "EDIT_CURSOR": "#00ff00", "BUTTON_BG": "#2e4a6a", "BUTTON_FG": "#e0e0e0",
    "BUTTON_ACTIVE_BG": "#3f5d88", "RANGE_SEL_COLOR": "#5588ff", "THEME_NAME": "PythonPlus Dark Blue"
}

DARKAMBER1_THEME_COLORS = {
    "BG": "#2b2b2b", "FG": "#f0f0f0", "PANEL_BG": "#3c3c3c", "PANEL_FG": "#f0f0f0",
    "STATUS_BG": "#2b2b2b", "STATUS_FG": "#f0f0f0", "OFFSET_BG": "#4a4a4a", "OFFSET_COLOR": "#ffcc00",
    "HEX_CELL_EVEN_BG": "#333333", "HEX_CELL_ODD_BG": "#3a3a3a", "HEX_CELL_OUTLINE": "#555555",
    "HEX_VALUE_COLOR": "#e0e0e0", "ASCII_BG": "#2b2b2b", "ACCENT": "#ffa500",
    "HEX_SEL_COLOR": "#888800", "CURSOR_COLOR": "#ffff00", "EDIT_BG": "#4a4a4a", "EDIT_FG": "#f0f0f0",
    "EDIT_CURSOR": "#00ff00", "BUTTON_BG": "#4a4a4a", "BUTTON_FG": "#f0f0f0",
    "BUTTON_ACTIVE_BG": "#5c5c5c", "RANGE_SEL_COLOR": "#ccaa00", "THEME_NAME": "Dark Amber"
}

COLORFUL_THEME_COLORS = {
    "BG": "#1f2a36", "FG": "#e0e0e0", "PANEL_BG": "#2a394a", "PANEL_FG": "#ffffff",
    "STATUS_BG": "#1f2a36", "STATUS_FG": "#ffffff", "OFFSET_BG": "#3c506e", "OFFSET_COLOR": "#ff5733",
    "HEX_CELL_EVEN_BG": "#314258", "HEX_CELL_ODD_BG": "#3a4c62", "HEX_CELL_OUTLINE": "#556f8f",
    "HEX_VALUE_COLOR": "#e0e0e0", "ASCII_BG": "#1f2a36", "ACCENT": "#33ff57",
    "HEX_SEL_COLOR": "#66b3ff", "CURSOR_COLOR": "#00ffff", "EDIT_BG": "#4a6385", "EDIT_FG": "#ffffff",
    "EDIT_CURSOR": "#ff00ff", "BUTTON_BG": "#3c506e", "BUTTON_FG": "#e0e0e0",
    "BUTTON_ACTIVE_BG": "#4a6385", "RANGE_SEL_COLOR": "#a279f5", "THEME_NAME": "Colorful Dark"
}




# --- End Monkey Patch ---

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = 0
        self.y = 0
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        "Display text in tooltip window"
        if self.tip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tip_window, text=self.text, background="#FFFFEA", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None


class HexTable(tk.Canvas):
    def __init__(self, master, app_instance, **kwargs):
        super().__init__(master, bd=0, highlightthickness=0, **kwargs)
        self.app_instance = app_instance
        self.file_data = bytearray()
        self.total_rows = 0
        self.selected = None
        self.selection_start_offset = None
        self.selection_end_offset = None
        self._drag_start_offset = None
        self.edit_entry = None
        self.editing = False
        self.blink_on = True
        self.match_length = 1
        self.last_modified_range = None
        self.highlight_timer_id = None
        # Inside HexTable.__init__(self, master, app_instance, **kwargs):
        # ... (other initializations) ...
        self.selected_encoding = "latin-1"  # Default encoding
        # ...
        self.header_height = ROW_H
        self.visible_data_rows = 0
        self.current_display_offset = 0

        self.colors = LIGHT_THEME_COLORS # Default, will be overridden

        self.bind("<Button-1>", self._on_mouse_down)
        self.bind("<B1-Motion>", self._on_mouse_drag)
        self.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.bind("<Button-3>", self._on_right_click)
        self.bind("<Double-Button-1>", self._on_double_click)
        self.bind("<Configure>", lambda e: self._on_canvas_configure())
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel)
        self.bind("<Button-5>", self._on_mousewheel)
        self.bind("<Key>", self._on_key_press)

        # self._redraw() # Called by apply_theme or configure

    def _highlight_changed_bytes(self, start_offset, end_offset):
        if self.last_modified_range:
            self.delete("highlight")
        self.last_modified_range = (start_offset, end_offset)
        self._redraw()
        if self.highlight_timer_id:
            self.after_cancel(self.highlight_timer_id)
        self.highlight_timer_id = self.after(5000, self._remove_highlight)

    def _remove_highlight(self):
        if self.last_modified_range:
            self.last_modified_range = None
            self._redraw()
        self.highlight_timer_id = None

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        if w == 1 and h == 1:  # Canvas might not be sized yet
            return

        line_col_x0 = 0
        offset_col_x0 = LINE_NUM_COL_W
        hex_col_x0 = offset_col_x0 + 90  # Width of offset column
        ascii_col_x0 = hex_col_x0 + BYTES_PER_ROW * CELL_W + 16  # Gap before ASCII

        # --- Draw Header ---
        # Line Number Header
        self.create_rectangle(line_col_x0, 0, offset_col_x0, self.header_height, fill=self.colors["OFFSET_BG"],
                              outline=self.colors["HEX_CELL_OUTLINE"], width=1)
        self.create_text(line_col_x0 + (offset_col_x0 - line_col_x0) / 2, self.header_height // 2, text="Line",
                         anchor="center", fill=self.colors["OFFSET_COLOR"],
                         font=("Consolas", 10, "bold"))

        # Offset Header
        self.create_rectangle(offset_col_x0, 0, hex_col_x0, self.header_height, fill=self.colors["OFFSET_BG"],
                              outline=self.colors["HEX_CELL_OUTLINE"], width=1)
        self.create_text(offset_col_x0 + (hex_col_x0 - offset_col_x0) / 2, self.header_height // 2, text="Offset",
                         anchor="center", fill=self.colors["OFFSET_COLOR"],
                         font=("Consolas", 10, "bold"))

        # Hex Column Headers (0-F)
        for col in range(BYTES_PER_ROW):
            cell_x = hex_col_x0 + col * CELL_W
            self.create_text(cell_x + CELL_W // 2, self.header_height // 2, text=f"{col:X}",
                             font=("Consolas", 10, "bold"), fill=self.colors["HEX_VALUE_COLOR"])

        # ASCII Header
        self.create_text(ascii_col_x0 + (BYTES_PER_ROW * ASCII_W) // 2, self.header_height // 2, text="ASCII",
                         anchor="center",
                         font=("Consolas", 10, "bold"), fill=self.colors["ACCENT"])

        # Header Bottom Line
        self.create_line(0, self.header_height - 1, w, self.header_height - 1, fill=self.colors["HEX_CELL_OUTLINE"],
                         width=1)

        # --- Draw Data Rows ---
        if not self.file_data and self.total_rows == 0:  # No data to draw
            # Optionally draw a "No file loaded" message or similar
            if self.visible_data_rows > 0:
                y_center_data_area = self.header_height + (self.visible_data_rows * ROW_H) / 2
                self.create_text(w / 2, y_center_data_area, text="No data loaded.",
                                 font=ASCII_FONT, fill=self.colors.get("FG_DISABLED", "#aaaaaa"), anchor="center")
            return  # Nothing more to draw

        start_logical_row_to_display = self.current_display_offset // BYTES_PER_ROW

        for row_on_page_idx in range(self.visible_data_rows):
            global_logical_row = start_logical_row_to_display + row_on_page_idx

            if global_logical_row >= self.total_rows:  # Past the end of actual data rows
                break

            y_on_canvas = (row_on_page_idx * ROW_H) + self.header_height
            data_byte_offset_for_row = global_logical_row * BYTES_PER_ROW

            # Line Number Column
            self.create_rectangle(line_col_x0, y_on_canvas, offset_col_x0, y_on_canvas + ROW_H,
                                  fill=self.colors["OFFSET_BG"],
                                  outline=self.colors["HEX_CELL_OUTLINE"], width=1)
            self.create_text(offset_col_x0 - 8, y_on_canvas + ROW_H // 2, text=f"{global_logical_row}", anchor="e",
                             fill=self.colors["OFFSET_COLOR"], font=HEX_FONT)

            # Offset Column
            self.create_rectangle(offset_col_x0, y_on_canvas, hex_col_x0, y_on_canvas + ROW_H,
                                  fill=self.colors["OFFSET_BG"],
                                  outline=self.colors["HEX_CELL_OUTLINE"], width=1)
            self.create_text(hex_col_x0 - 8, y_on_canvas + ROW_H // 2, text=f"{data_byte_offset_for_row:08X}",
                             anchor="e",
                             fill=self.colors["OFFSET_COLOR"], font=HEX_FONT)

            # Hex Data Columns
            for col_idx in range(BYTES_PER_ROW):
                cell_x = hex_col_x0 + col_idx * CELL_W
                current_byte_global_idx = data_byte_offset_for_row + col_idx

                hex_text_val = ""
                byte_val_int = None
                if current_byte_global_idx < len(self.file_data):
                    byte_val_int = self.file_data[current_byte_global_idx]
                    hex_text_val = f"{byte_val_int:02X}"
                # else: hex_text_val remains "" for bytes beyond EOF on the last line

                bg_color_hex = self.colors["HEX_CELL_EVEN_BG"] if (global_logical_row + col_idx) % 2 == 0 else \
                    self.colors["HEX_CELL_ODD_BG"]

                is_in_range_selection = False
                if self.selection_start_offset is not None and self.selection_end_offset is not None and \
                        current_byte_global_idx < len(self.file_data):  # Only select existing bytes
                    if self.selection_start_offset <= current_byte_global_idx <= self.selection_end_offset:
                        is_in_range_selection = True

                is_selected_hex_single = (self.selected == (global_logical_row, col_idx, "hex"))

                current_bg_color = bg_color_hex
                if is_in_range_selection:
                    current_bg_color = self.colors["RANGE_SEL_COLOR"]
                elif is_selected_hex_single and not self.editing:
                    current_bg_color = self.colors["HEX_SEL_COLOR"]

                self.create_rectangle(cell_x, y_on_canvas, cell_x + CELL_W, y_on_canvas + ROW_H, fill=current_bg_color,
                                      outline=self.colors["HEX_CELL_OUTLINE"], width=1)
                if hex_text_val:  # Only draw text if there's a value
                    self.create_text(cell_x + CELL_W // 2, y_on_canvas + ROW_H // 2, text=hex_text_val, font=HEX_FONT,
                                     fill=self.colors["HEX_VALUE_COLOR"])

            # ASCII Data Columns
            for col_idx in range(BYTES_PER_ROW):
                current_byte_global_idx = data_byte_offset_for_row + col_idx
                ascii_char = " "  # Default to blank space for beyond EOF
                byte_val_int = None

                if current_byte_global_idx < len(self.file_data):
                    byte_val_int = self.file_data[current_byte_global_idx]
                    ascii_char = "."  # Default for non-decodable or control chars
                    single_byte_data = bytes([byte_val_int])
                    try:
                        if self.selected_encoding == "utf-8":
                            if 0x20 <= byte_val_int <= 0x7E: ascii_char = chr(byte_val_int)
                        elif self.selected_encoding == "ascii":
                            if 0x20 <= byte_val_int <= 0x7E: ascii_char = chr(byte_val_int)
                        else:
                            decoded_char = single_byte_data.decode(self.selected_encoding, errors='replace')
                            if decoded_char == '\ufffd':
                                ascii_char = '.'
                            elif not decoded_char.isprintable() and ord(decoded_char) > 127:
                                if not (0x20 <= ord(decoded_char) <= 0x7E or 0xA0 <= ord(decoded_char) <= 0xFF):
                                    ascii_char = "."
                                else:
                                    ascii_char = decoded_char  # Use decoded if it's in extended printable
                            elif 0 <= ord(decoded_char) <= 31 or ord(decoded_char) == 127:
                                ascii_char = "."
                            else:
                                ascii_char = decoded_char
                    except:  # Broad except for any decoding issue
                        ascii_char = "."

                bg_color_ascii_default = self.colors["ASCII_BG"]
                is_in_range_selection_ascii = False
                if self.selection_start_offset is not None and self.selection_end_offset is not None and \
                        current_byte_global_idx < len(self.file_data):
                    if self.selection_start_offset <= current_byte_global_idx <= self.selection_end_offset:
                        is_in_range_selection_ascii = True

                is_selected_ascii_single = (self.selected == (global_logical_row, col_idx, "ascii"))
                # Also highlight ASCII if corresponding hex is selected (and not a range)
                is_corresponding_hex_selected_single = (
                            self.selected == (global_logical_row, col_idx, "hex") and not is_in_range_selection_ascii)

                current_ascii_bg = bg_color_ascii_default
                if is_in_range_selection_ascii:
                    current_ascii_bg = self.colors["RANGE_SEL_COLOR"]
                elif (is_selected_ascii_single or is_corresponding_hex_selected_single) and not self.editing:
                    current_ascii_bg = self.colors["HEX_SEL_COLOR"]

                self.create_rectangle(ascii_col_x0 + col_idx * ASCII_W, y_on_canvas,
                                      ascii_col_x0 + (col_idx + 1) * ASCII_W, y_on_canvas + ROW_H,
                                      fill=current_ascii_bg, outline=self.colors["HEX_CELL_OUTLINE"], width=1)
                self.create_text(ascii_col_x0 + col_idx * ASCII_W + ASCII_W // 2, y_on_canvas + ROW_H // 2,
                                 text=ascii_char,
                                 font=ASCII_FONT, fill=self.colors["ACCENT"])

        # --- Draw Edit Cursor / Highlight ---
        if self.editing and self.selected and self.blink_on:
            row, col, kind = self.selected
            bbox = self._calculate_drawn_cell_bbox(row, col, kind)
            if bbox:  # Ensure bbox is valid (cell is visible)
                self.create_rectangle(bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3],
                                      outline=self.colors["CURSOR_COLOR"], width=2, tags="edit_cursor")

        # Vertical line separating Hex and ASCII
        self.create_line(ascii_col_x0 - 8, self.header_height, ascii_col_x0 - 8, h,
                         fill=self.colors["HEX_CELL_OUTLINE"], width=2)

        # --- Draw Modification Highlight ---
        if self.last_modified_range:
            mod_start_offset, mod_end_offset = self.last_modified_range
            for r_idx in range(self.visible_data_rows):
                g_row = start_logical_row_to_display + r_idx
                if g_row >= self.total_rows: break
                y_canv = (r_idx * ROW_H) + self.header_height
                d_offset_row = g_row * BYTES_PER_ROW

                for c_idx in range(BYTES_PER_ROW):
                    curr_byte_g_idx = d_offset_row + c_idx
                    if curr_byte_g_idx > mod_end_offset: break  # Optimization
                    if mod_start_offset <= curr_byte_g_idx <= mod_end_offset:
                        if curr_byte_g_idx < len(self.file_data):  # Ensure byte exists
                            cell_x_hl = hex_col_x0 + c_idx * CELL_W
                            # Draw semi-transparent yellow overlay for hex part
                            self.create_rectangle(cell_x_hl, y_canv, cell_x_hl + CELL_W, y_canv + ROW_H,
                                                  # fill="yellow", stipple="gray50", # Example stipple
                                                  outline=self.colors.get("MODIFIED_OUTLINE", "orange"),
                                                  # Use a specific color
                                                  width=1, tags="highlight")
                            # Optionally highlight ASCII part too
                            # ascii_x_hl = ascii_col_x0 + c_idx * ASCII_W
                            # self.create_rectangle(ascii_x_hl, y_canv, ascii_x_hl + ASCII_W, y_canv + ROW_H,
                            #                     outline=self.colors.get("MODIFIED_OUTLINE", "orange"),
                            #                     width=1, tags="highlight")


    def _on_mouse_down(self, event):
        if self.editing:
            self._close_edit(save=True)
            return

        clicked_offset, clicked_kind = self._get_offset_from_event(event)

        if clicked_offset is not None:
            self._drag_start_offset = clicked_offset
            self.selected = (clicked_offset // BYTES_PER_ROW, clicked_offset % BYTES_PER_ROW, clicked_kind)
            self.selection_start_offset = clicked_offset
            self.selection_end_offset = clicked_offset
            self._redraw()
            self.app_instance.root.event_generate("<<HexSelection>>")
        else:
            self._select_none()
            self.app_instance.status_bar.config(text="Clicked outside data area.")

    def _on_mouse_drag(self, event):
        if self._drag_start_offset is None or not self.file_data:
            return

        current_offset_under_mouse, _ = self._get_offset_from_event(event)

        if current_offset_under_mouse is not None:
            self.selection_start_offset = min(self._drag_start_offset, current_offset_under_mouse)
            self.selection_end_offset = max(self._drag_start_offset, current_offset_under_mouse)
            # Update self.selected to reflect the end of the drag for cursor positioning if needed
            # For range selection, the start/end offsets are primary
            # If you want the single 'selected' cell to be where the mouse is:
            selected_row = current_offset_under_mouse // BYTES_PER_ROW
            selected_col = current_offset_under_mouse % BYTES_PER_ROW
            # Determine kind based on mouse position, or default to 'hex'
            _, kind_under_mouse = self._get_offset_from_event(event) # Re-evaluate kind for accuracy
            self.selected = (selected_row, selected_col, kind_under_mouse if kind_under_mouse else 'hex')

            self._redraw()
            self.app_instance.root.event_generate("<<HexSelection>>")

    def _on_mouse_up(self, event):
        self._drag_start_offset = None
        # self.selected might still be the last cell under drag, which is fine for range selection
        # If you want single selection to revert to the start of the drag on mouse_up without movement:
        # if self.selection_start_offset == self.selection_end_offset and self.selection_start_offset is not None:
        #     offset = self.selection_start_offset
        #     self.selected = (offset // BYTES_PER_ROW, offset % BYTES_PER_ROW, 'hex') # Or determine kind
        self.app_instance.root.event_generate("<<HexSelection>>")

    def _on_double_click(self, event):
        if self.editing:
            self._close_edit(save=True) # Save current edit before starting new one

        clicked_offset, clicked_kind = self._get_offset_from_event(event)

        if clicked_offset is not None:
            self.selected = (clicked_offset // BYTES_PER_ROW, clicked_offset % BYTES_PER_ROW, clicked_kind)
            self.selection_start_offset = clicked_offset # For double-click, select only this byte
            self.selection_end_offset = clicked_offset
            self._start_edit(self.selected[0], self.selected[1], self.selected[2])
            self.app_instance.status_bar.config(text=f"Editing byte at 0x{clicked_offset:08X}.")
            return # Important to return after starting edit
        else:
            self.app_instance.status_bar.config(text="Cannot edit outside data area.")

    def _on_right_click(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        # Apply theme to the context menu itself if app_instance has the method
        if hasattr(self.app_instance, '_apply_menu_theme'):
            self.app_instance._apply_menu_theme(context_menu)

        clicked_offset, clicked_kind = self._get_offset_from_event(event)
        is_click_within_current_range = False
        if self.selection_start_offset is not None and self.selection_end_offset is not None and clicked_offset is not None:
            if self.selection_start_offset <= clicked_offset <= self.selection_end_offset:
                is_click_within_current_range = True

        if clicked_offset is not None:
            if not is_click_within_current_range or (self.selection_start_offset == self.selection_end_offset):
                self.selected = (clicked_offset // BYTES_PER_ROW, clicked_offset % BYTES_PER_ROW, "hex")
                self.selection_start_offset = clicked_offset
                self.selection_end_offset = clicked_offset
            elif self.selected is None:
                self.selected = (clicked_offset // BYTES_PER_ROW, clicked_offset % BYTES_PER_ROW, "hex")
            self._redraw()
            self.app_instance.root.event_generate("<<HexSelection>>")
        else:
            if not (self.selection_start_offset is not None and self.selection_end_offset is not None):
                self._select_none()
            self.app_instance.status_bar.config(text="No byte selected for context actions.")

        is_data_loaded = bool(self.file_data)
        is_selected_range = (self.selection_start_offset is not None and self.selection_end_offset is not None)
        is_clipboard_available = True
        try:
            self.app_instance.root.clipboard_get()  # Check main root for clipboard
        except tk.TclError:
            is_clipboard_available = False

        context_menu.add_command(label="Select All", command=self._select_all,
                                 state=tk.NORMAL if is_data_loaded else tk.DISABLED)
        context_menu.add_command(label="Select None", command=self._select_none,
                                 state=tk.NORMAL if is_selected_range or self.selected else tk.DISABLED)  # Enable if any selection
        context_menu.add_separator()

        context_menu.add_command(label="Copy", command=self.app_instance.copy_selection,
                                 state=tk.NORMAL if is_selected_range else tk.DISABLED)
        context_menu.add_command(label="Cut", command=self.app_instance.cut_selection,
                                 state=tk.NORMAL if is_selected_range else tk.DISABLED)

        # Determine paste target: clicked offset if valid, or current cursor if click was outside
        paste_target_offset = clicked_offset
        if paste_target_offset is None and self.selected:
            paste_target_offset = self.selected[0] * BYTES_PER_ROW + self.selected[1]
        elif paste_target_offset is None and len(self.file_data) == 0:  # Empty file, paste at 0
            paste_target_offset = 0

        paste_enabled = (is_clipboard_available and
                         (is_data_loaded or len(self.file_data) == 0) and  # Must have data or be empty file
                         (paste_target_offset is not None))  # Must have a valid target offset

        context_menu.add_command(label="Paste",
                                 command=lambda: self.app_instance.paste_at_offset(target_offset=paste_target_offset),
                                 state=tk.NORMAL if paste_enabled else tk.DISABLED)
        context_menu.add_separator()

        context_menu.add_command(label="Fill selected bytes...", command=self.app_instance.fill_selection,
                                 state=tk.NORMAL if is_selected_range else tk.DISABLED)
        context_menu.add_separator()

        insert_target_offset_val = clicked_offset
        if clicked_offset is None:
            if self.selected:
                insert_target_offset_val = self.selected[0] * BYTES_PER_ROW + self.selected[1]
            elif len(self.file_data) > 0:
                insert_target_offset_val = len(self.file_data)
            else:
                insert_target_offset_val = 0
        insert_enabled_ctx = (is_data_loaded or len(self.file_data) == 0)

        context_menu.add_command(label="Insert bytes here...",
                                 command=lambda off=insert_target_offset_val: self._insert_bytes(off),
                                 state=tk.NORMAL if insert_enabled_ctx else tk.DISABLED)

        delete_enabled = is_selected_range
        context_menu.add_command(label="Delete selected bytes", command=self._delete_selected_bytes,
                                 state=tk.NORMAL if delete_enabled else tk.DISABLED)
        context_menu.add_command(label="Crop selected bytes", command=self._crop_selected_bytes,
                                 state=tk.NORMAL if delete_enabled else tk.DISABLED)
        context_menu.add_separator()

        # --- NEW: Checksum/Hash Calculator ---
        checksum_menu = tk.Menu(context_menu, tearoff=0)
        if hasattr(self.app_instance, '_apply_menu_theme'):  # Theme submenu
            self.app_instance._apply_menu_theme(checksum_menu)

        checksum_menu.add_command(label="MD5",
                                  command=lambda: self.app_instance.calculate_hash_for_selection("md5"),
                                  state=tk.NORMAL if is_selected_range else tk.DISABLED)
        checksum_menu.add_command(label="SHA1",
                                  command=lambda: self.app_instance.calculate_hash_for_selection("sha1"),
                                  state=tk.NORMAL if is_selected_range else tk.DISABLED)
        checksum_menu.add_command(label="SHA256",
                                  command=lambda: self.app_instance.calculate_hash_for_selection("sha256"),
                                  state=tk.NORMAL if is_selected_range else tk.DISABLED)

        # Example for CRC32 (uncomment and import zlib if you want it)
        # import zlib # Would need to be at the top of the file
        # checksum_menu.add_command(label="CRC32",
        #                           command=lambda: self.app_instance.calculate_hash_for_selection("crc32"),
        #                           state=tk.NORMAL if is_selected_range else tk.DISABLED)

        context_menu.add_cascade(label="Calculate Hash/Checksum", menu=checksum_menu,
                                 state=tk.NORMAL if is_selected_range else tk.DISABLED)
        # --- END Checksum/Hash ---

        export_menu = tk.Menu(context_menu, tearoff=0)
        if hasattr(self.app_instance, '_apply_menu_theme'): self.app_instance._apply_menu_theme(export_menu)
        export_menu.add_command(label="As Text (ASCII)", command=self._export_selected_ascii,
                                state=tk.NORMAL if is_selected_range else tk.DISABLED)  # is_selected_range not delete_enabled
        export_menu.add_command(label="As Binary (Hex)", command=self._export_selected_hex,
                                state=tk.NORMAL if is_selected_range else tk.DISABLED)  # is_selected_range not delete_enabled
        context_menu.add_cascade(label="Export selected bytes", menu=export_menu,
                                 state=tk.NORMAL if is_selected_range else tk.DISABLED)  # is_selected_range not delete_enabled

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
        # self.app_instance.status_bar.config(text="Context menu opened.") # Status will be set by actions

    def _select_all(self):
        if not self.file_data:
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            self.app_instance.status_bar.config(text="Cannot select all, file is empty.")
            return
        self.selection_start_offset = 0
        self.selection_end_offset = len(self.file_data) - 1
        self.selected = (0, 0, 'hex') if self.total_rows > 0 else None # Ensure selected is valid
        self._redraw()
        self.app_instance.status_bar.config(text=f"All {len(self.file_data)} bytes selected.")
        self.app_instance.root.event_generate("<<HexSelection>>")

    def _select_none(self):
        if self.selection_start_offset is None and self.selection_end_offset is None and self.selected is None:
            self.app_instance.status_bar.config(text="No selection to clear.")
            return

        self.selection_start_offset = None
        self.selection_end_offset = None
        self.selected = None # Clear single cell selection as well
        self._redraw()
        self.app_instance.status_bar.config(text="Selection cleared.")
        self.app_instance.root.event_generate("<<HexSelection>>")

    def _insert_bytes(self, insert_offset):
        if not self.file_data and insert_offset != 0:
            messagebox.showinfo("Insert Bytes", "No file loaded. To insert, open a file or start at offset 0.")
            self.app_instance.status_bar.config(text="Insert failed: No file loaded.")
            return

        if insert_offset < 0 or insert_offset > len(self.file_data):
            messagebox.showerror("Error", "Invalid insertion point.")
            self.app_instance.status_bar.config(text="Insert failed: Invalid insertion point.")
            return

        try:
            num_bytes_str = simpledialog.askstring("Insert Bytes", "Number of bytes to insert:",
                                                   parent=self.app_instance.root)
            if num_bytes_str is None:
                self.app_instance.status_bar.config(text="Insert cancelled.")
                return
            num_bytes = int(num_bytes_str.strip())
            if num_bytes <= 0:
                messagebox.showwarning("Warning", "Number of bytes must be positive.")
                self.app_instance.status_bar.config(text="Insert failed: Number of bytes must be positive.")
                return

            value_str = simpledialog.askstring("Insert Bytes", f"Value for {num_bytes} bytes (e.g., '00' or 'FF'):",
                                               parent=self.app_instance.root)
            if value_str is None:
                self.app_instance.status_bar.config(text="Insert cancelled.")
                return
            value_str = value_str.strip()

            if not (len(value_str) == 2 and all(c in "0123456789abcdefABCDEF" for c in value_str.lower())):
                messagebox.showerror("Error", "Value must be a 2-digit hex string (e.g., '00', 'FF').")
                self.app_instance.status_bar.config(text="Insert failed: Invalid fill value.")
                return
            fill_byte = int(value_str, 16)

            # self.app_instance._save_undo_state() # MOVED

            new_file_data = bytearray()
            new_file_data.extend(self.file_data[:insert_offset])
            new_file_data.extend(bytearray([fill_byte] * num_bytes))
            new_file_data.extend(self.file_data[insert_offset:])

            self.load_file(new_file_data) # This is HexTable.load_file
            self.app_instance.file_size = len(new_file_data)
            self.app_instance._update_file_info()
            self.app_instance._save_undo_state() # MOVED HERE
            self.goto_offset_and_display(insert_offset)
            self._highlight_changed_bytes(insert_offset, insert_offset + num_bytes - 1)
            self.app_instance.status_bar.config(
                text=f"Inserted {num_bytes} bytes at 0x{insert_offset:08X}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid number of bytes or value.")
            self.app_instance.status_bar.config(text="Insert failed: Invalid input.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert bytes: {e}")
            self.app_instance.status_bar.config(text=f"Insert failed: {e}")

    def _delete_selected_bytes(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Delete Bytes", "No bytes selected.")
            self.app_instance.status_bar.config(text="Delete failed: No bytes selected.")
            return

        start = self.selection_start_offset
        end = self.selection_end_offset + 1 # end is exclusive for slicing
        num_deleted = end - start

        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete {num_deleted} bytes from 0x{start:08X} to 0x{self.selection_end_offset:08X}?"):
            self.app_instance.status_bar.config(text="Delete cancelled.")
            return

        try:
            # self.app_instance._save_undo_state() # MOVED
            new_file_data = bytearray()
            new_file_data.extend(self.file_data[:start])
            new_file_data.extend(self.file_data[end:])

            self.load_file(new_file_data)
            self.app_instance.file_size = len(new_file_data)
            self.app_instance._update_file_info()
            self.app_instance._save_undo_state() # MOVED HERE
            new_offset = min(start, len(new_file_data) - 1 if new_file_data else 0)
            self.goto_offset_and_display(new_offset)
            # No highlight for deletion as bytes are gone
            self.app_instance.status_bar.config(
                text=f"Deleted {num_deleted} bytes from 0x{start:08X}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete bytes: {e}")
            self.app_instance.status_bar.config(text=f"Delete failed: {e}")

    def _crop_selected_bytes(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Crop Bytes", "No bytes selected.")
            self.app_instance.status_bar.config(text="Crop failed: No bytes selected.")
            return

        start = self.selection_start_offset
        end = self.selection_end_offset + 1 # end is exclusive for slicing
        num_cropped = end - start

        if not messagebox.askyesno("Confirm Crop",
                                   f"Crop file to selected {num_cropped} bytes from 0x{start:08X} to 0x{self.selection_end_offset:08X}?\nThis will delete all *non-selected* bytes."):
            self.app_instance.status_bar.config(text="Crop cancelled.")
            return

        try:
            # self.app_instance._save_undo_state() # MOVED
            cropped_data = self.file_data[start:end] # This creates a new bytearray slice

            self.load_file(cropped_data) # Load the new cropped data
            self.app_instance.file_size = len(cropped_data)
            self.app_instance._update_file_info()
            self.app_instance._save_undo_state() # MOVED HERE
            self.goto_offset_and_display(0)
            # Potentially highlight the entire remaining data or nothing specific for crop
            self.app_instance.status_bar.config(
                text=f"File cropped to {len(cropped_data)} bytes.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to crop bytes: {e}")
            self.app_instance.status_bar.config(text=f"Crop failed: {e}")

    def _export_selected_ascii(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Export", "No bytes selected for export.")
            self.app_instance.status_bar.config(text="Export failed: No bytes selected.")
            return

        start = self.selection_start_offset
        end = self.selection_end_offset + 1

        selected_bytes = self.file_data[start:end]
        ascii_text = "".join([chr(b) if 32 <= b < 127 else '.' for b in selected_bytes])

        path = filedialog.asksaveasfilename(
            title="Export Selected ASCII As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            parent=self.app_instance.root
        )
        if not path:
            self.app_instance.status_bar.config(text="ASCII export cancelled.")
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(ascii_text)
            messagebox.showinfo("Export Complete", f"Selected ASCII exported to {os.path.basename(path)}")
            self.app_instance.status_bar.config(
                text=f"Exported {len(selected_bytes)} bytes as ASCII to {os.path.basename(path)}.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export ASCII: {e}")
            self.app_instance.status_bar.config(text=f"ASCII export failed: {e}")

    def _export_selected_hex(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Export", "No bytes selected for export.")
            self.app_instance.status_bar.config(text="Export failed: No bytes selected.")
            return

        start = self.selection_start_offset
        end = self.selection_end_offset + 1

        selected_bytes = self.file_data[start:end]

        path = filedialog.asksaveasfilename(
            title="Export Selected Binary As",
            defaultextension=".bin",
            filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")],
            parent=self.app_instance.root
        )
        if not path:
            self.app_instance.status_bar.config(text="Binary export cancelled.")
            return

        try:
            with open(path, "wb") as f:
                f.write(selected_bytes)
            messagebox.showinfo("Export Complete", f"Selected binary data exported to {os.path.basename(path)}")
            self.app_instance.status_bar.config(
                text=f"Exported {len(selected_bytes)} bytes as binary to {os.path.basename(path)}.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export binary: {e}")
            self.app_instance.status_bar.config(text=f"Binary export failed: {e}")

    def _start_edit(self, row, col, kind):
        idx = row * BYTES_PER_ROW + col
        if idx >= len(self.file_data):
            self.app_instance.status_bar.config(text="Cannot edit past end of file.")
            return

        bbox = self._calculate_drawn_cell_bbox(row, col, kind)
        if not bbox:
            # This can happen if the cell is scrolled out of view between selection and edit attempt
            self.app_instance.status_bar.config(text="Cannot edit: Cell not visible.")
            return

        value = self.file_data[idx]
        text = f"{value:02X}" if kind == "hex" else chr(value) if 32 <= value < 127 else "."

        if self.edit_entry: # Destroy any existing edit entry
            self.edit_entry.destroy()
        self.edit_entry = None

        self.edit_entry = tk.Entry(
            self,
            font=HEX_FONT if kind == "hex" else ASCII_FONT,
            width=2 if kind == "hex" else 1,
            justify="center",
            bg=self.colors["EDIT_BG"],
            fg=self.colors["EDIT_FG"],
            insertbackground=self.colors["EDIT_CURSOR"],
            relief="ridge",
            highlightthickness=1,
            highlightbackground=self.colors["CURSOR_COLOR"],
            highlightcolor=self.colors["CURSOR_COLOR"]
        )
        self.edit_entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        self.edit_entry.insert(0, text)
        self.edit_entry.select_range(0, tk.END)
        self.edit_entry.focus_set()
        self.editing = True
        self.edit_entry.bind("<Return>", lambda e: self._close_edit(save=True))
        self.edit_entry.bind("<Escape>", lambda e: self._close_edit(save=False))
        # Using add='+' ensures our binding doesn't replace default FocusOut behavior
        self.edit_entry.bind("<FocusOut>", lambda e: self._close_edit(save=True), add="+")
        self.after(500, self._blink_cursor) # Start blinker
        self._redraw() # Redraw to show selection style changes if any during edit mode
        self.app_instance.status_bar.config(text=f"Editing byte at 0x{idx:08X}.")

    def _close_edit(self, save):
        if not self.editing or self.edit_entry is None:
            # If FocusOut calls this after already closed by Return/Escape
            if self.edit_entry: self.edit_entry.destroy()
            self.edit_entry = None
            self.editing = False # Ensure editing is false
            return

        row, col, kind = self.selected # Assuming self.selected is valid
        idx = row * BYTES_PER_ROW + col
        old_value = self.file_data[idx] if idx < len(self.file_data) else None

        if save:
            try:
                val_str = self.edit_entry.get() # Get value from entry
                if idx < len(self.file_data): # Ensure index is still valid
                    b = -1 # Default to an invalid byte to ensure it's set
                    if kind == "hex":
                        if not (len(val_str) == 2 and all(c in "0123456789abcdefABCDEF" for c in val_str.lower())):
                            raise ValueError("Invalid hex format (must be 2 hex digits)")
                        b = int(val_str, 16)
                    else: # ascii
                        if not val_str: b = ord('.') # Empty input becomes '.'
                        elif len(val_str) > 1: b = ord(val_str[0]) # Take first char if multiple entered
                        else: b = ord(val_str)
                        if not (32 <= b < 127): # If not printable, make it '.'
                            b = ord(".")

                    if old_value is not None and old_value != b: # If a change is actually happening
                        self.file_data[idx] = b # Apply the change
                        self.app_instance._save_undo_state() # Save the new state AFTER modification
                        self._highlight_changed_bytes(idx, idx)
                        self.app_instance.status_bar.config(
                            text=f"Byte at 0x{idx:08X} changed from {old_value:02X} to {b:02X}.")
                    else:
                        # self.file_data[idx] = b # No actual change, or apply anyway if needed
                        self.app_instance.status_bar.config(text=f"Edit at 0x{idx:08X} saved (no change).")
                else:
                    self.app_instance.status_bar.config(text="Edit failed: Index out of bounds after file change.")
            except Exception as e:
                self.app_instance.status_bar.config(text=f"Edit failed: {e}. Value not saved.")
        else:
            self.app_instance.status_bar.config(text="Edit cancelled.")

        if self.edit_entry:
            self.edit_entry.destroy()
        self.edit_entry = None
        self.editing = False
        self._redraw() # Redraw to remove edit cursor and reflect changes
        self.app_instance.root.event_generate("<<HexSelection>>") # Update inspector, etc.

    def _blink_cursor(self):
        if not self.editing:
            self.blink_on = True # Reset for next edit
            self._redraw() # Ensure cursor is removed if editing stopped abruptly
            return
        self.blink_on = not self.blink_on
        self._redraw()
        self.after(500, self._blink_cursor)

    def _calculate_drawn_cell_bbox(self, global_row, global_col, kind):
        display_start_row_logical = self.current_display_offset // BYTES_PER_ROW
        row_on_page = global_row - display_start_row_logical

        if not (0 <= row_on_page < self.visible_data_rows):
            return None # Cell is not currently visible

        y_on_canvas = (row_on_page * ROW_H) + self.header_height

        offset_col_x0 = LINE_NUM_COL_W
        hex_col_x0 = offset_col_x0 + 90
        ascii_col_x0 = hex_col_x0 + BYTES_PER_ROW * CELL_W + 16

        if kind == "hex":
            x = hex_col_x0 + global_col * CELL_W
            # Adjusted bbox for entry widget to fit better
            return (x + 1, y_on_canvas + 1, CELL_W - 2, ROW_H - 2)
        else: # ascii
            x = ascii_col_x0 + global_col * ASCII_W
            return (x + 1, y_on_canvas + 1, ASCII_W - 2, ROW_H - 2)


    def _on_canvas_configure(self):
        new_height = self.winfo_height()
        if new_height > self.header_height: # Ensure header height is less than canvas height
            new_visible_rows = max(0, (new_height - self.header_height) // ROW_H)
            if new_visible_rows != self.visible_data_rows:
                self.visible_data_rows = new_visible_rows
                self._redraw()
                self.app_instance.root.event_generate("<<HexScroll>>") # Notify app of potential scroll change
        elif self.visible_data_rows != 0 : # Canvas shrunk too small
            self.visible_data_rows = 0
            self._redraw()
            self.app_instance.root.event_generate("<<HexScroll>>")


    def apply_theme(self, colors):
        self.colors = colors
        self.config(bg=self.colors["BG"])
        self._redraw()

    def load_file(self, data):
        self.file_data = bytearray(data) # Ensure it's a mutable bytearray
        self.total_rows = (len(data) + BYTES_PER_ROW - 1) // BYTES_PER_ROW
        if len(data) == 0: # Handle empty file case specifically for total_rows
            self.total_rows = 0
        self.selected = None
        self.selection_start_offset = None
        self.selection_end_offset = None
        self.editing = False # Reset editing state
        if self.edit_entry: # Clean up edit widget if it exists
            self.edit_entry.destroy()
            self.edit_entry = None
        self.current_display_offset = 0 # Reset scroll to top

        # self._on_canvas_configure() will be called due to packing or existing config,
        # or explicitly call it if needed after UI is stable.
        # self._redraw() will be called by _on_canvas_configure or goto_offset_and_display
        self.after_idle(self._on_canvas_configure) # Ensure configure runs after potential UI updates
        self.after_idle(self._redraw) # And redraw after configure


    def goto_offset_and_display(self, target_offset):
        if not self.file_data and target_offset != 0 : # Allow goto 0 for empty file
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            self.app_instance.status_bar.config(text="No file loaded.")
            if self.total_rows == 0: # Ensure redraw if file is truly empty
                 self._redraw()
            return

        # Clamp target_offset to valid range
        if len(self.file_data) > 0:
            target_offset = max(0, min(len(self.file_data) - 1, target_offset))
        elif target_offset != 0: # For empty file, only offset 0 is valid
            target_offset = 0
        elif len(self.file_data) == 0 and target_offset == 0:
            pass # Allow offset 0 for empty file
        else: # Should not happen if file_data is empty and offset is not 0
            self.app_instance.status_bar.config(text="Invalid offset for current file state.")
            return


        target_row_logical = target_offset // BYTES_PER_ROW

        # Adjust current_display_offset to bring the target_row into view
        if self.total_rows <= self.visible_data_rows:
            # If all rows fit, display from the top
            self.current_display_offset = 0
        else:
            # Try to center the target_row
            top_row_for_centering = max(0, target_row_logical - (self.visible_data_rows // 2))
            # Ensure we don't scroll past the end
            max_top_row = max(0, self.total_rows - self.visible_data_rows)
            final_top_row_to_display = min(max_top_row, top_row_for_centering)
            self.current_display_offset = final_top_row_to_display * BYTES_PER_ROW

        if len(self.file_data) > 0 or (len(self.file_data) == 0 and target_offset == 0) :
            self.selected = (target_row_logical, target_offset % BYTES_PER_ROW, "hex")
        else:
            self.selected = None # No selection if truly no data and not offset 0

        # Clear range selection when jumping to a specific offset this way
        # self.selection_start_offset = None
        # self.selection_end_offset = None
        # OR set selection to the single byte:
        if self.selected:
             self.selection_start_offset = target_offset
             self.selection_end_offset = target_offset
        else:
             self.selection_start_offset = None
             self.selection_end_offset = None


        self._redraw()
        self.app_instance.root.event_generate("<<HexSelection>>") # Update inspector, status bar etc.

    def scroll_pages(self, direction): # direction is -1 for up, 1 for down
        if not self.file_data:
            self.app_instance.status_bar.config(text="No file loaded for scrolling.")
            return

        page_size_bytes = self.visible_data_rows * BYTES_PER_ROW
        if page_size_bytes == 0 and self.visible_data_rows > 0: # Avoid division by zero if BYTES_PER_ROW is 0
             page_size_bytes = self.visible_data_rows # scroll by lines if BYTES_PER_ROW is problematic

        new_offset = self.current_display_offset + (direction * page_size_bytes)

        # Calculate the maximum possible starting offset for a page
        # This is the offset of the first byte of the page that still shows the last row of data
        if self.total_rows > self.visible_data_rows:
            last_possible_page_start_offset = (self.total_rows - self.visible_data_rows) * BYTES_PER_ROW
        else:
            last_possible_page_start_offset = 0 # All data fits, so only top page is possible

        self.current_display_offset = max(0, min(new_offset, last_possible_page_start_offset))
        self._redraw()
        self.app_instance.root.event_generate("<<HexScroll>>")

    def _on_mousewheel(self, event):
        if not self.file_data:
            self.app_instance.status_bar.config(text="No file loaded for scrolling.")
            return

        lines_to_scroll = 3 # Number of lines to scroll per wheel "tick"
        delta_lines = 0

        if event.num == 4:  # Linux scroll up
            delta_lines = -lines_to_scroll
        elif event.num == 5:  # Linux scroll down
            delta_lines = lines_to_scroll
        elif event.delta:  # Windows/macOS
            delta_lines = -int(event.delta / 120) * lines_to_scroll # 120 is a common delta value

        if delta_lines == 0: return # No scroll detected

        delta_bytes = delta_lines * BYTES_PER_ROW
        new_offset = self.current_display_offset + delta_bytes

        if self.total_rows > self.visible_data_rows:
            last_possible_start_offset = (self.total_rows - self.visible_data_rows) * BYTES_PER_ROW
        else:
            last_possible_start_offset = 0

        self.current_display_offset = max(0, min(new_offset, last_possible_start_offset))
        self._redraw()
        self.app_instance.root.event_generate("<<HexScroll>>")

    def _on_key_press(self, event):
        if self.editing: # Don't handle navigation keys if an edit widget is active
            return

        handled = False
        if event.keysym == "PageUp":
            self.scroll_pages(-1)
            handled = True
        elif event.keysym == "PageDown":
            self.scroll_pages(1)
            handled = True
        elif event.keysym == "Up":
            if not self.file_data: return "break" # Or pass, if break interferes
            if self.selected:
                row, col, kind = self.selected
                new_row = row - 1
                if new_row >= 0:
                    self.selected = (new_row, col, kind)
                    self.selection_start_offset = new_row * BYTES_PER_ROW + col
                    self.selection_end_offset = self.selection_start_offset
                    self._ensure_selection_visible()
                # else: at top, do nothing or beep
            elif self.file_data: # No selection, but file has data, select first byte of current view or file
                target_offset = max(0, self.current_display_offset)
                self.selected = (target_offset // BYTES_PER_ROW, target_offset % BYTES_PER_ROW, "hex")
                self.selection_start_offset = target_offset
                self.selection_end_offset = target_offset
            handled = True
        elif event.keysym == "Down":
            if not self.file_data: return "break"
            if self.selected:
                row, col, kind = self.selected
                new_row = row + 1
                if new_row < self.total_rows: # Check against total logical rows
                    self.selected = (new_row, col, kind)
                    self.selection_start_offset = new_row * BYTES_PER_ROW + col
                    self.selection_end_offset = self.selection_start_offset
                    self._ensure_selection_visible()
                # else: at bottom
            elif self.file_data:
                target_offset = max(0, self.current_display_offset)
                self.selected = (target_offset // BYTES_PER_ROW, target_offset % BYTES_PER_ROW, "hex")
                self.selection_start_offset = target_offset
                self.selection_end_offset = target_offset
            handled = True
        elif event.keysym == "Left":
            if not self.file_data: return "break"
            if self.selected:
                row, col, kind = self.selected
                new_col = col - 1
                new_row = row
                if new_col < 0: # Wrap to previous row, last column
                    new_row -= 1
                    new_col = BYTES_PER_ROW - 1
                if new_row >= 0 : # Ensure still within file bounds (first row is 0)
                    self.selected = (new_row, new_col, kind)
                    self.selection_start_offset = new_row * BYTES_PER_ROW + new_col
                    self.selection_end_offset = self.selection_start_offset
                    self._ensure_selection_visible()
            elif self.file_data: # No selection, select first byte
                self.selected = (0,0, "hex")
                self.selection_start_offset = 0
                self.selection_end_offset = 0
            handled = True
        elif event.keysym == "Right":
            if not self.file_data: return "break"
            if self.selected:
                row, col, kind = self.selected
                new_col = col + 1
                new_row = row
                if new_col >= BYTES_PER_ROW: # Wrap to next row, first column
                    new_row += 1
                    new_col = 0

                # Ensure the new position is valid within the actual data length
                new_offset = new_row * BYTES_PER_ROW + new_col
                if new_offset < len(self.file_data):
                    self.selected = (new_row, new_col, kind)
                    self.selection_start_offset = new_offset
                    self.selection_end_offset = new_offset
                    self._ensure_selection_visible()
                # else: at end of data
            elif self.file_data:
                self.selected = (0,0, "hex")
                self.selection_start_offset = 0
                self.selection_end_offset = 0
            handled = True
        elif event.keysym == "Home":
            if not self.file_data: return "break"
            if event.state & 0x0004: # Ctrl+Home - Go to start of file
                self.goto_offset_and_display(0)
            elif self.selected: # Home - Go to start of current line
                row, _, kind = self.selected
                self.selected = (row, 0, kind)
                self.selection_start_offset = row * BYTES_PER_ROW
                self.selection_end_offset = self.selection_start_offset
                self._ensure_selection_visible() # May not be needed if already visible
            elif self.file_data:
                self.selected = (0,0,"hex")
                self.selection_start_offset = 0
                self.selection_end_offset = 0
            handled = True
        elif event.keysym == "End":
            if not self.file_data: return "break"
            if event.state & 0x0004: # Ctrl+End - Go to end of file
                 self.goto_offset_and_display(len(self.file_data) - 1 if len(self.file_data) > 0 else 0)
            elif self.selected: # End - Go to end of current line (or last byte of data on that line)
                row, _, kind = self.selected
                # Find the last valid column in this row
                last_col_in_row = BYTES_PER_ROW - 1
                # If this row is the last row of the file, it might not be full
                if row == self.total_rows - 1 and len(self.file_data) > 0:
                    last_col_in_row = (len(self.file_data) - 1) % BYTES_PER_ROW

                self.selected = (row, last_col_in_row, kind)
                self.selection_start_offset = row * BYTES_PER_ROW + last_col_in_row
                self.selection_end_offset = self.selection_start_offset
                self._ensure_selection_visible()
            elif self.file_data: # No selection, go to last byte of file
                last_offset = len(self.file_data) -1
                self.selected = (last_offset // BYTES_PER_ROW, last_offset % BYTES_PER_ROW, "hex")
                self.selection_start_offset = last_offset
                self.selection_end_offset = last_offset

            handled = True
        # Consider adding Enter key to start editing the selected byte
        elif event.keysym == "Return" and self.selected and not self.editing:
            row, col, kind = self.selected
            self._start_edit(row, col, kind if kind else "hex") # Default to hex if kind is None
            handled = True


        if handled:
            self._redraw()
            self.app_instance.root.event_generate("<<HexSelection>>") # Update inspector etc.
            return "break" # Prevents further processing of the event by Tkinter

    def _ensure_selection_visible(self):
        if not self.selected or not self.file_data: return

        selected_logical_row = self.selected[0]
        current_top_display_row_logical = self.current_display_offset // BYTES_PER_ROW
        # visible_data_rows can be 0 if canvas is too small
        current_bottom_display_row_logical = current_top_display_row_logical + max(0, self.visible_data_rows - 1)


        needs_redraw = False
        if selected_logical_row < current_top_display_row_logical:
            # Scroll up: Set the new top display row to be the selected row
            self.current_display_offset = selected_logical_row * BYTES_PER_ROW
            needs_redraw = True
        elif selected_logical_row > current_bottom_display_row_logical:
            # Scroll down: Set the new top display row so selected row is the last visible one
            # (or first if it makes more sense, this makes it last)
            self.current_display_offset = max(0, (selected_logical_row - self.visible_data_rows + 1)) * BYTES_PER_ROW
            needs_redraw = True

        if needs_redraw:
            self._redraw()
            self.app_instance.root.event_generate("<<HexScroll>>")


    def _get_offset_from_event(self, event):
        x, y = event.x, event.y
        y_relative_to_data_start_on_canvas = y - self.header_height

        if y_relative_to_data_start_on_canvas < 0: return None, None # Clicked in header

        # Calculate which logical row on the page was clicked
        # Ensure ROW_H is not zero to prevent division by zero
        if ROW_H == 0: return None, None
        logical_row_on_page = int(y_relative_to_data_start_on_canvas // ROW_H)

        # Convert to global logical row based on current scroll offset
        global_logical_row = (self.current_display_offset // BYTES_PER_ROW) + logical_row_on_page

        # Check if this global logical row is valid (within the total rows of data)
        if not (0 <= global_logical_row < self.total_rows): return None, None # Clicked below data

        # Define column start positions (consistent with _redraw)
        offset_col_x0 = LINE_NUM_COL_W
        hex_col_x0 = offset_col_x0 + 90
        ascii_col_x0 = hex_col_x0 + BYTES_PER_ROW * CELL_W + 16
        # Define end of ascii column for boundary check
        ascii_col_x1 = ascii_col_x0 + BYTES_PER_ROW * ASCII_W


        clicked_kind = None
        target_col = -1

        # Check if click is in Hex area
        if hex_col_x0 <= x < ascii_col_x0 - 16: # -16 for the gap
            # Ensure CELL_W is not zero
            if CELL_W == 0: return None, None
            col_in_hex_area = (x - hex_col_x0) // CELL_W
            if 0 <= col_in_hex_area < BYTES_PER_ROW:
                clicked_kind = "hex"
                target_col = col_in_hex_area

        # Check if click is in ASCII area (if not found in Hex)
        elif ascii_col_x0 <= x < ascii_col_x1:
            # Ensure ASCII_W is not zero
            if ASCII_W == 0: return None, None
            col_in_ascii_area = (x - ascii_col_x0) // ASCII_W
            if 0 <= col_in_ascii_area < BYTES_PER_ROW:
                clicked_kind = "ascii"
                target_col = col_in_ascii_area

        if clicked_kind and target_col != -1:
            clicked_byte_offset = (global_logical_row * BYTES_PER_ROW + target_col)
            # Final check: is this offset actually within the loaded file data?
            if clicked_byte_offset < len(self.file_data):
                return clicked_byte_offset, clicked_kind

        return None, None # Clicked outside any valid data cell



class HexEditorApp:
    def __init__(self, root):
        self.root = root
        root.title("« Hex Editor »")
        root.state('zoomed')
        self.bookmarks = {}

        self.colors = PYTHONPLUS_THEME_COLORS
        self.inspector_endianness = tk.StringVar(value="<")
        self.ascii_encoding_var = tk.StringVar(value="latin-1")
        self.supported_encodings = ["latin-1", "utf-8", "ascii", "cp437", "cp1252"]

        # --- BooleanVars for panel visibility ---
        self.show_inspector_panel = tk.BooleanVar(value=True)
        self.show_view_options_panel = tk.BooleanVar(value=True)
        self.show_file_info_panel = tk.BooleanVar(value=True)
        self.show_goto_panel = tk.BooleanVar(value=True)
        self.show_bookmarks_panel = tk.BooleanVar(value=True)

        # Add listeners to these BooleanVars
        # The lambda calls toggle_panel_visibility with the panel_name
        self.show_inspector_panel.trace_add("write", lambda name, index, mode,
                                                            sv=self.show_inspector_panel: self.toggle_panel_visibility(
            "inspector"))
        self.show_view_options_panel.trace_add("write", lambda name, index, mode,
                                                               sv=self.show_view_options_panel: self.toggle_panel_visibility(
            "view_options"))
        self.show_file_info_panel.trace_add("write", lambda name, index, mode,
                                                            sv=self.show_file_info_panel: self.toggle_panel_visibility(
            "file_info"))
        self.show_goto_panel.trace_add("write",
                                       lambda name, index, mode, sv=self.show_goto_panel: self.toggle_panel_visibility(
                                           "goto"))
        self.show_bookmarks_panel.trace_add("write", lambda name, index, mode,
                                                            sv=self.show_bookmarks_panel: self.toggle_panel_visibility(
            "bookmarks"))

        self._set_ttk_style()
        self.root.configure(bg=self.colors["PANEL_BG"])

        self.frame_main = tk.Frame(root, bg=self.colors["PANEL_BG"])
        self.frame_main.pack(fill="both", expand=1)

        # Scrollable Left Panel Setup (remains mostly the same)
        left_panel_container = tk.Frame(self.frame_main, width=270, bg=self.colors["PANEL_BG"])
        left_panel_container.pack(side="left", fill="y", padx=5, pady=5)
        left_panel_container.pack_propagate(False)

        self.left_canvas = tk.Canvas(left_panel_container, bg=self.colors["PANEL_BG"], highlightthickness=0)
        self.left_scrollbar = ttk.Scrollbar(left_panel_container, orient="vertical", command=self.left_canvas.yview)

        self.scrollable_left_frame = ttk.Frame(self.left_canvas, style="TFrame")

        self.scrollable_left_frame.bind(
            "<Configure>",
            lambda e: self.left_canvas.configure(
                scrollregion=self.left_canvas.bbox("all")
            )
        )

        self.left_canvas_window = self.left_canvas.create_window((0, 0), window=self.scrollable_left_frame, anchor="nw",
                                                                 tags="scrollable_frame_tag")

        def _configure_canvas_window(event):  # Renamed to avoid conflict if used elsewhere
            self.left_canvas.itemconfig('scrollable_frame_tag', width=event.width)
            self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

        self.left_canvas.bind("<Configure>", _configure_canvas_window)

        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

        self.left_scrollbar.pack(side="right", fill="y")
        self.left_canvas.pack(side="left", fill="both", expand=True)

        for widget_to_bind_scroll in [self.left_canvas, self.scrollable_left_frame]:
            widget_to_bind_scroll.bind("<MouseWheel>", self._on_left_panel_dedicated_mousewheel, add="+")
            widget_to_bind_scroll.bind("<Button-4>", self._on_left_panel_dedicated_mousewheel, add="+")
            widget_to_bind_scroll.bind("<Button-5>", self._on_left_panel_dedicated_mousewheel, add="+")

        # Right side container setup (remains the same)
        self.right_side_container = tk.Frame(self.frame_main, bg=self.colors["PANEL_BG"])
        self.right_side_container.pack(side="left", fill="both", expand=1, padx=0, pady=5)
        self.hex_view_container = tk.Frame(self.right_side_container, bg=self.colors["PANEL_BG"])
        self.hex_view_container.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.hex_table = HexTable(self.hex_view_container, self)
        self.hex_table.pack(side="top", fill="both", expand=1)
        self.page_nav_frame = ttk.Frame(self.hex_view_container, style="TFrame")
        self.page_nav_frame.pack(side="bottom", fill="x", pady=(2, 0))
        self.btn_top_file = ttk.Button(self.page_nav_frame, text="<< Top of File",
                                       command=lambda: self.hex_table.goto_offset_and_display(
                                           0) if self.hex_table.file_data else None)
        self.btn_top_file.pack(side="left", padx=2)
        ToolTip(self.btn_top_file, "Go to the Top of File (Ctrl+T)")
        self.btn_prev_page = ttk.Button(self.page_nav_frame, text="< Previous Page",
                                        command=lambda: self.hex_table.scroll_pages(
                                            -1) if self.hex_table.file_data else None)
        self.btn_prev_page.pack(side="left", expand=True, padx=2)
        ToolTip(self.btn_prev_page, "Go to the Previous Page (Ctrl+P)")
        self.btn_next_page = ttk.Button(self.page_nav_frame, text="Next Page >",
                                        command=lambda: self.hex_table.scroll_pages(
                                            1) if self.hex_table.file_data else None)
        self.btn_next_page.pack(side="right", expand=True, padx=2)
        ToolTip(self.btn_next_page, "Go to the Next Page (Ctrl+N)")
        self.btn_end_file = ttk.Button(self.page_nav_frame, text="End of File >>", command=self._goto_end_of_file)
        self.btn_end_file.pack(side="right", padx=2)
        ToolTip(self.btn_end_file, "Go to the End of File (Ctrl+E)")
        self.current_offset_display_label = ttk.Label(self.page_nav_frame, text="Offset: N/A", font=("Arial", 9))
        self.current_offset_display_label.pack(side="left", padx=10)
        self.search_panel = tk.Frame(self.right_side_container, width=270, bg=self.colors["PANEL_BG"])
        self.search_panel.pack(side="right", fill="y", padx=(5, 5), pady=0)
        self.search_panel.pack_propagate(False)

        # Build UI panels
        self._build_left_panel_widgets()  # This will now create the containers like self.inspector_panel_container
        self._build_search_panel_widgets()

        self.status_bar = tk.Label(root, text="Ready", anchor="w", font=("Arial", 9))
        self.status_bar.pack(side="bottom", fill="x", ipady=2)

        # Menubar setup
        menubar = tk.Menu(root)
        fmenu = tk.Menu(menubar, tearoff=0)
        fmenu.add_command(label="Open...", command=self.load_file, accelerator="Ctrl+O")
        fmenu.add_separator()
        fmenu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+S")
        fmenu.add_separator()
        self.recent_files_menu = tk.Menu(fmenu, tearoff=0)
        fmenu.add_cascade(label="Recent Files", menu=self.recent_files_menu)
        fmenu.add_separator()
        fmenu.add_command(label="Exit", command=root.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=fmenu)

        self.edit_menu = tk.Menu(menubar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Copy", command=self.copy_selection, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Cut", command=self.cut_selection, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Paste", command=self.paste_at_offset, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Fill Selection...", command=self.fill_selection)
        menubar.add_cascade(label="Edit", menu=self.edit_menu)

        # --- NEW: View Menu (or "Panels" / "Explorer") ---
        self.view_menu = tk.Menu(menubar, tearoff=0)  # Storing as self.view_menu
        self.view_menu.add_checkbutton(label="Data Inspector", variable=self.show_inspector_panel, onvalue=True,
                                       offvalue=False)
        self.view_menu.add_checkbutton(label="View Options", variable=self.show_view_options_panel, onvalue=True,
                                       offvalue=False)
        self.view_menu.add_checkbutton(label="File Info", variable=self.show_file_info_panel, onvalue=True,
                                       offvalue=False)
        self.view_menu.add_checkbutton(label="Go To", variable=self.show_goto_panel, onvalue=True, offvalue=False)
        self.view_menu.add_checkbutton(label="Bookmarks", variable=self.show_bookmarks_panel, onvalue=True,
                                       offvalue=False)
        menubar.add_cascade(label="View Panels", menu=self.view_menu)
        # --- END NEW VIEW MENU ---

        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Light Theme", command=lambda: self._apply_theme(LIGHT_THEME_COLORS))
        theme_menu.add_separator()
        theme_menu.add_command(label="Dark Blue Theme", command=lambda: self._apply_theme(PYTHONPLUS_THEME_COLORS))
        theme_menu.add_separator()
        theme_menu.add_command(label="Dark Amber Theme", command=lambda: self._apply_theme(DARKAMBER1_THEME_COLORS))
        theme_menu.add_separator()
        theme_menu.add_command(label="Colorful Theme", command=lambda: self._apply_theme(COLORFUL_THEME_COLORS))
        menubar.add_cascade(label="Theme", menu=theme_menu)

        util_menu = tk.Menu(menubar, tearoff=0)
        util_menu.add_command(label="Hex to Dec", command=self.hex_to_dec)
        util_menu.add_command(label="Dec to Hex", command=self.dec_to_hex)
        util_menu.add_separator()
        util_menu.add_command(label="Save Config", command=self.save_config)
        util_menu.add_command(label="Load Config", command=lambda: self.load_config(startup=False))
        util_menu.add_separator()
        util_menu.add_command(label="Show ASCII Table", command=self.show_ascii_table)
        menubar.add_cascade(label="Utils", menu=util_menu)

        root.config(menu=menubar)

        # App state variables
        self.file_path = None
        self.file_size = 0
        self.search_matches = []
        self.current_match_idx = -1
        self.recent_files = []
        self._undo_stack = []
        self._redo_stack = []
        self._max_undo_states = 50
        self._is_undoing_or_redoing = False

        # Bindings and initial config
        self._apply_menu_theme(menubar)
        self.root.bind("<<HexSelection>>", self._on_hex_table_selection)
        self.root.bind("<<HexScroll>>", self._on_hex_table_scroll)
        self._bind_shortcuts()

        self.load_config(startup=True)

        self._save_undo_state()
        self._update_undo_redo_status()
        self._update_recent_files_menu()

        self._apply_theme(self.colors)
        self.hex_table.focus_set()
        # Initial call to set panel visibility based on BooleanVars after UI is built
        self.root.after_idle(self._initial_panel_visibility_setup)
        self.root.after_idle(lambda: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))


    def _set_ttk_style(self):
        s = ttk.Style()
        s.theme_use('clam') # clam, alt, default, classic

        s.configure("TFrame", background=self.colors["PANEL_BG"])
        s.configure("TLabel", background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        s.configure("TLabelframe", background=self.colors["PANEL_BG"], foreground=self.colors["PANEL_FG"],
                    font=("Arial", 9, "bold"), bordercolor=self.colors["HEX_CELL_OUTLINE"],
                    relief="ridge")
        s.configure("TLabelframe.Label", background=self.colors["PANEL_BG"], foreground=self.colors["PANEL_FG"],
                    font=("Arial", 9, "bold")) # Label within Labelframe

        s.configure("TCombobox",
                    fieldbackground=self.colors["EDIT_BG"],
                    background=self.colors["BUTTON_BG"], # Arrow button background
                    foreground=self.colors["FG"], # Text color
                    selectbackground=self.colors["BUTTON_ACTIVE_BG"], # Background of selected item in dropdown
                    selectforeground=self.colors["FG"], # Foreground of selected item in dropdown
                    bordercolor=self.colors["HEX_CELL_OUTLINE"],
                    arrowcolor=self.colors["FG"], # Color of the dropdown arrow
                    relief="ridge"
                    )
        s.map("TCombobox",
              fieldbackground=[("readonly", self.colors["EDIT_BG"])],
              background=[("readonly", self.colors["BUTTON_BG"])],
              foreground=[("readonly", self.colors["FG"])],
              selectbackground=[("readonly", self.colors["BUTTON_ACTIVE_BG"])],
              selectforeground=[("readonly", self.colors["FG"])],
              bordercolor=[("readonly", self.colors["HEX_CELL_OUTLINE"])])


        s.configure("TButton",
                    background=self.colors["BUTTON_BG"],
                    foreground=self.colors["BUTTON_FG"],
                    relief="ridge",
                    font=("Arial", 9, "bold"),
                    bordercolor=self.colors["HEX_CELL_OUTLINE"], # Border color
                    focusthickness=1,
                    focuscolor=self.colors["CURSOR_COLOR"] # Color of focus highlight
                    )
        s.map("TButton",
              background=[("active", self.colors["BUTTON_ACTIVE_BG"])], # Mouse over
              foreground=[("active", self.colors["FG"])]) # Mouse over text

    def _apply_theme(self, new_colors):
        self.colors = new_colors
        self.root.config(bg=self.colors["PANEL_BG"])

        # --- (omitting other parts of _apply_theme for brevity, assume they are correct) ---
        # Ensure all these hasattr checks are in your full _apply_theme
        if hasattr(self, 'frame_main'): self.frame_main.config(bg=self.colors["PANEL_BG"])
        if hasattr(self, 'left_panel'): self.left_panel.config(bg=self.colors["PANEL_BG"])
        # ... etc for all basic frames and status_bar

        self._set_ttk_style()
        if hasattr(self, 'hex_table'): self.hex_table.apply_theme(self.colors)
        # ... etc for inspector, file info, go to panels ...

        # Search & Replace Panel
        if hasattr(self, 'match_count_label'):
            self.match_count_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        if hasattr(self, 'search_entry_widget'):
            self.search_entry_widget.config(
                bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
                highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"],
                relief="ridge")
        if hasattr(self, 'replace_entry_widget'):
            self.replace_entry_widget.config(
                bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
                highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"],
                relief="ridge")
        if hasattr(self, 'search_results_listbox'):
            self.search_results_listbox.config(
                bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"],
                selectbackground=self.colors["HEX_SEL_COLOR"], selectforeground=self.colors["HEX_VALUE_COLOR"],
                highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"],
                relief="ridge")

        # Offset Replace Panel
        if hasattr(self, 'offset_entry_widget'):  # For the offset
            self.offset_entry_widget.config(
                bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
                highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"],
                relief="ridge")
        # MODIFICATION: Theme the new dedicated entry widget
        if hasattr(self, 'offset_replace_value_entry_widget'):  # For the replacement value
            self.offset_replace_value_entry_widget.config(
                bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
                highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"],
                relief="ridge")

        # --- (omitting other parts of _apply_theme for brevity, assume they are correct) ---
        if hasattr(self, 'bookmarks_listbox'):  # Bookmarks
            self.bookmarks_listbox.config(
                bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"],
                selectbackground=self.colors["HEX_SEL_COLOR"], selectforeground=self.colors["HEX_VALUE_COLOR"],
                relief="ridge", highlightthickness=1,
                highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"]
            )
        if hasattr(self, 'current_offset_display_label'):  # Page Nav
            self.current_offset_display_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])

        if self.root.cget("menu"):  # Menubar
            try:
                menubar_widget_path = self.root.cget("menu")
                if menubar_widget_path:
                    menubar = self.root.nametowidget(menubar_widget_path)
                    self._apply_menu_theme(menubar)
            except tk.TclError:
                pass

        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=f"Theme changed to {self.colors.get('THEME_NAME', 'Custom Theme')}.")
            self._update_undo_redo_status()

    def _initial_panel_visibility_setup(self):
        """Sets the initial visibility of all toggleable panels and packs the exit button."""

        desired_panel_order = ["inspector", "view_options", "file_info", "goto", "bookmarks"]

        # Ensure all panels are initially unpacked (state managed by BooleanVars)
        panel_map_for_init = {
            "inspector": getattr(self, 'inspector_panel_container', None),
            "view_options": getattr(self, 'view_options_panel_container', None),
            "file_info": getattr(self, 'file_info_panel_container', None),
            "goto": getattr(self, 'goto_panel_container', None),
            "bookmarks": getattr(self, 'bookmarks_panel_container', None)
        }
        for p_container in panel_map_for_init.values():
            if p_container and p_container.winfo_ismapped():
                p_container.pack_forget()

        # Now, apply visibility based on BooleanVars, which will pack them in order
        for panel_name in desired_panel_order:
            # This will call the revised toggle_panel_visibility, which now handles ordering
            # by repacking all visible items in sequence.
            # The initial_setup=True flag is still useful to suppress status messages.
            # The BooleanVar's trace will trigger toggle_panel_visibility.
            # To be absolutely explicit for initial setup:
            if panel_name == "inspector":
                self.toggle_panel_visibility("inspector", initial_setup=True)
            elif panel_name == "view_options":
                self.toggle_panel_visibility("view_options", initial_setup=True)
            elif panel_name == "file_info":
                self.toggle_panel_visibility("file_info", initial_setup=True)
            elif panel_name == "goto":
                self.toggle_panel_visibility("goto", initial_setup=True)
            elif panel_name == "bookmarks":
                self.toggle_panel_visibility("bookmarks", initial_setup=True)

        # Pack the exit button container at the very bottom of the scrollable_left_frame.
        # It should be packed *after* all other panels have had their chance to pack based on visibility.
        if hasattr(self, 'exit_button_container'):
            if self.exit_button_container.winfo_ismapped():  # Should not be, but as a safeguard
                self.exit_button_container.pack_forget()
            # Pack it at the bottom of self.scrollable_left_frame
            self.exit_button_container.pack(side="bottom", fill="x", pady=(10, 5), anchor="s")

        self.root.after_idle(lambda: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))


    def _apply_menu_theme(self, menu_widget):
        menu_widget.config(
            bg=self.colors["PANEL_BG"],
            fg=self.colors["PANEL_FG"],
            activebackground=self.colors["BUTTON_ACTIVE_BG"], # When mouse hovers over menu item
            activeforeground=self.colors["FG"],
            # relief=tk.FLAT # Optional: for a flatter menu look
        )
        # Iterate through menu items to apply to submenus
        end_index = menu_widget.index('end')
        if end_index is not None: # Check if end_index is not None (menu might be empty)
            for i in range(end_index + 1):
                if menu_widget.type(i) == 'cascade':
                    submenu_name = menu_widget.entrycget(i, "menu")
                    if submenu_name: # Ensure submenu exists
                        try:
                            submenu = self.root.nametowidget(submenu_name)
                            self._apply_menu_theme(submenu)
                        except tk.TclError:
                            # Submenu might not be fully realized yet, or name is incorrect
                            # print(f"Warning: Could not find submenu {submenu_name} to apply theme.")
                            pass # Can add logging here if needed

    def get_config_path(self):
        """Helper to consistently get the config file path."""
        try:
            # Ideal: Use a dedicated app data directory
            # For simplicity here, we'll try to put it next to the script.
            # If running as a frozen app (e.g., PyInstaller), __file__ might not be suitable.
            base_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            # __file__ is not defined (e.g., running in an interactive interpreter directly)
            # Fallback to current working directory
            base_path = os.getcwd()
        return os.path.join(base_path, "config.dat")



    def add_bookmark(self):
        if not self.hex_table.selected:
            messagebox.showwarning("Add Bookmark", "No byte selected to bookmark.")
            return

        row, col, _ = self.hex_table.selected
        offset = row * BYTES_PER_ROW + col

        bookmark_name = simpledialog.askstring("Add Bookmark", "Enter a name for the bookmark:", parent=self.root)
        if bookmark_name:
            self.bookmarks[bookmark_name] = offset
            self.update_bookmarks_list()
            self.status_bar.config(text=f"Bookmark '{bookmark_name}' added at offset 0x{offset:08X}.")
            self._update_undo_redo_status()

    def delete_bookmark(self):
        selected_bookmark_indices = self.bookmarks_listbox.curselection()
        if not selected_bookmark_indices:
            messagebox.showwarning("Delete Bookmark", "No bookmark selected to delete.")
            return

        selected_item_text = self.bookmarks_listbox.get(selected_bookmark_indices[0])
        # Extract name carefully, assuming format "Name (0xOffset)"
        bookmark_name = selected_item_text.split(" (0x")[0]

        if bookmark_name in self.bookmarks:
            del self.bookmarks[bookmark_name]
            self.update_bookmarks_list()
            self.status_bar.config(text=f"Bookmark '{bookmark_name}' deleted.")
            self._update_undo_redo_status()
        else:
            # This case should ideally not happen if listbox is synced with self.bookmarks
            messagebox.showwarning("Delete Bookmark", f"Bookmark '{bookmark_name}' not found in internal list.")


    def update_bookmarks_list(self):
        self.bookmarks_listbox.delete(0, tk.END)
        # Sort bookmarks by name for consistent display
        for name, offset in sorted(self.bookmarks.items()):
            self.bookmarks_listbox.insert(tk.END, f"{name} (0x{offset:08X})")

    def goto_bookmark(self):
        selected_bookmark_indices = self.bookmarks_listbox.curselection()
        if not selected_bookmark_indices:
            # messagebox.showwarning("Go To Bookmark", "No bookmark selected.") # Can be noisy
            return

        selected_item_text = self.bookmarks_listbox.get(selected_bookmark_indices[0])
        bookmark_name = selected_item_text.split(" (0x")[0]

        if bookmark_name in self.bookmarks:
            offset = self.bookmarks[bookmark_name]
            if offset < len(self.hex_table.file_data) or (len(self.hex_table.file_data) == 0 and offset == 0):
                self.hex_table.goto_offset_and_display(offset)
                self.status_bar.config(text=f"Navigated to bookmark '{bookmark_name}' at offset 0x{offset:08X}.")
            else:
                messagebox.showwarning("Go To Bookmark", f"Bookmark '{bookmark_name}' (offset 0x{offset:08X}) is out of current file bounds.")
                self.status_bar.config(text=f"Bookmark '{bookmark_name}' out of bounds.")
            self._update_undo_redo_status()

        else:
            messagebox.showwarning("Go To Bookmark", "Selected bookmark not found in internal list.")


    def _goto_end_of_file(self):
        if self.file_size > 0:
            self.hex_table.goto_offset_and_display(self.file_size - 1)
            self.status_bar.config(text=f"Navigated to end of file (0x{self.file_size - 1:08X}).")
        else: # File is empty
            self.hex_table.goto_offset_and_display(0) # Go to offset 0 for empty file
            self.status_bar.config(text="File is empty. At offset 0x00000000.")
        self._update_undo_redo_status()


    def _on_hex_table_selection(self, event=None): # Add event=None for direct calls
        current_offset = -1
        if self.hex_table.selected:
            row, col, _ = self.hex_table.selected
            current_offset = row * BYTES_PER_ROW + col
            # Ensure offset is valid if file shrinks
            if current_offset >= len(self.hex_table.file_data) and len(self.hex_table.file_data) > 0:
                current_offset = len(self.hex_table.file_data) -1
            elif len(self.hex_table.file_data) == 0:
                 current_offset = 0 # for empty file, cursor at 0

        if current_offset != -1 :
            self.current_addr_label.config(text=f"0x{current_offset:08X}")
            self.current_offset_display_label.config(text=f"Offset: 0x{current_offset:08X} ({current_offset} dec)")
            self.update_inspector(current_offset)
        else: # No selection (e.g. file just cleared, or select_none called)
            self.current_addr_label.config(text="0x00000000")
            self.current_offset_display_label.config(text="Offset: N/A")
            self.update_inspector(0) # Inspector shows for offset 0 or N/A

        self._update_status_bar_info(current_offset if current_offset !=-1 else 0) # Update status bar

    def _on_hex_table_scroll(self, event=None): # Add event=None
        # When scrolling, the 'selected' byte might not change, but the view does.
        # Update info based on the top-left visible byte of the data area.
        offset = self.hex_table.current_display_offset
        # self.current_addr_label.config(text=f"0x{offset:08X}") # This shows top-left, might be confusing
        # self.current_offset_display_label.config(text=f"Offset: 0x{offset:08X} ({offset} dec)")
        # update_inspector based on selected, or top-left if no selection?
        # For now, let selection event handle inspector and detailed offset.
        # Scroll event primarily updates general status or scroll-related info.
        self._update_status_bar_info(offset) # Or use self.hex_table.selected if preferred

    def _update_status_bar_info(self, offset):
        if not self.hex_table.file_data:
            # Keep "Ready" or specific message from other actions, then add undo/redo
            current_text = self.status_bar.cget("text").split(" | Undo:")[0]
            if not current_text or "Undo:" in current_text or "Redo:" in current_text: # Avoid double status
                current_text = "Ready"
            self.status_bar.config(text=current_text) # Set base text first
            self.current_offset_display_label.config(text="Offset: N/A")
            self._update_undo_redo_status() # Append undo/redo info
            return

        # Ensure offset is valid for the current file_data
        if len(self.hex_table.file_data) > 0:
            valid_offset = max(0, min(offset, len(self.hex_table.file_data) - 1))
            byte_at_offset = self.hex_table.file_data[valid_offset]
            ascii_char = chr(byte_at_offset) if 32 <= byte_at_offset < 127 else '.'
            base_status = f"Offset: 0x{valid_offset:08X} | ASCII: '{ascii_char}' (0x{byte_at_offset:02X})"
            self.status_bar.config(text=base_status)
            self.current_offset_display_label.config(text=f"Offset: 0x{valid_offset:08X} ({valid_offset} dec)")
        else: # File is empty but not None
            base_status = "Offset: 0x00000000 | ASCII: '.' (Empty File)"
            self.status_bar.config(text=base_status)
            self.current_offset_display_label.config(text="Offset: 0x00000000 (0 dec)")

        self._update_undo_redo_status() # Append undo/redo info to the base_status

    def _build_left_panel_widgets(self):
        # panel is self.scrollable_left_frame
        panel = self.scrollable_left_frame

        # --- Create ALL panel containers first (these are Frames that will be shown/hidden) ---
        self.inspector_panel_container = ttk.Frame(panel, style="TFrame")
        self.view_options_panel_container = ttk.Frame(panel, style="TFrame")
        self.file_info_panel_container = ttk.Frame(panel, style="TFrame")
        self.goto_panel_container = ttk.Frame(panel, style="TFrame")
        self.bookmarks_panel_container = ttk.Frame(panel, style="TFrame")
        self.exit_button_container = ttk.Frame(panel, style="TFrame")

        # --- Populate Data Inspector Section (content packed into its container) ---
        self.inspector_frame = ttk.LabelFrame(self.inspector_panel_container, text="════█ Data Inspector █════════════",
                                              style="TLabelframe")
        self.inspector_frame.pack(fill="x", expand=True, padx=3, pady=5)
        # ... (Full content of inspector_frame as in your last correct version: endian_frame, labels etc.)
        self.inspector_frame.columnconfigure(0, weight=1)
        self.inspector_frame.columnconfigure(1, weight=2)
        endian_frame = ttk.Frame(self.inspector_frame)
        endian_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(2, 5))
        ttk.Label(endian_frame, text="Endian:").pack(side="left", padx=(5, 2))
        little_endian_rb = ttk.Radiobutton(endian_frame, text="Little", variable=self.inspector_endianness,
                                           value="<", command=self._on_endianness_change)
        little_endian_rb.pack(side="left", padx=2)
        ToolTip(little_endian_rb, "Interpret multi-byte values as Little-endian.")
        big_endian_rb = ttk.Radiobutton(endian_frame, text="Big", variable=self.inspector_endianness,
                                        value=">", command=self._on_endianness_change)
        big_endian_rb.pack(side="left", padx=2)
        ToolTip(big_endian_rb, "Interpret multi-byte values as Big-endian.")
        self.inspector_labels = {}
        self.inspector_static_labels = {}
        single_byte_interpretations = [
            ("Byte (Dec)", "dec"), ("Byte (Hex)", "hex"), ("Byte (Oct)", "oct"),
            ("Byte (Bin)", "bin"), ("Byte (ASCII)", "ascii")
        ]
        multi_byte_interpretations = [
            ("8-bit Signed", "b"), ("8-bit Unsigned", "B"),
            ("16-bit Signed", "h"), ("16-bit Unsigned", "H"),
            ("32-bit Signed", "i"), ("32-bit Unsigned", "I"),
            ("64-bit Signed", "q"), ("64-bit Unsigned", "Q"),
            ("16-bit Float (FP16)", "e"), ("32-bit Float (FP32)", "f"), ("64-bit Float (FP64)", "d")
        ]
        self.inspector_formats = {name: base_char for name, base_char in multi_byte_interpretations}
        current_grid_row = 1
        for name, _ in single_byte_interpretations:
            static_label = ttk.Label(self.inspector_frame, text=f"{name}:", anchor="w", font=("Arial", 8))
            static_label.grid(row=current_grid_row, column=0, sticky="w", padx=(5, 2), pady=1)
            self.inspector_static_labels[name] = static_label
            value_label = ttk.Label(self.inspector_frame, text="N/A", anchor="w", font=("Arial", 8))
            value_label.grid(row=current_grid_row, column=1, sticky="ew", padx=(2, 5), pady=1)
            self.inspector_labels[name] = value_label
            current_grid_row += 1
        sep = ttk.Separator(self.inspector_frame, orient='horizontal')
        sep.grid(row=current_grid_row, column=0, columnspan=2, sticky='ew', pady=5)
        current_grid_row += 1
        for name, _ in multi_byte_interpretations:
            static_label = ttk.Label(self.inspector_frame, text=f"{name}:", anchor="w", font=("Arial", 8))
            static_label.grid(row=current_grid_row, column=0, sticky="w", padx=(5, 2), pady=1)
            self.inspector_static_labels[name] = static_label
            value_label = ttk.Label(self.inspector_frame, text="N/A", anchor="w", font=("Arial", 8))
            value_label.grid(row=current_grid_row, column=1, sticky="ew", padx=(2, 5), pady=1)
            self.inspector_labels[name] = value_label
            current_grid_row += 1

        # --- Populate View Options Section ---
        self.view_options_frame = ttk.LabelFrame(self.view_options_panel_container,
                                                 text="════█ View Options █════════════", style="TLabelframe")
        self.view_options_frame.pack(fill="x", expand=True, padx=3, pady=5)
        encoding_frame = ttk.Frame(self.view_options_frame)
        encoding_frame.pack(fill="x", padx=5, pady=3)
        ttk.Label(encoding_frame, text="ASCII Encoding:").pack(side="left", padx=(0, 3))
        self.encoding_combo = ttk.Combobox(encoding_frame, textvariable=self.ascii_encoding_var,
                                           values=self.supported_encodings, state="readonly", width=15)
        self.encoding_combo.pack(side="left", expand=True, fill="x")
        self.encoding_combo.bind("<<ComboboxSelected>>", self._on_encoding_change)
        ToolTip(self.encoding_combo, "Select character encoding for the ASCII display column.")

        # --- Populate File Info Section ---
        self.finf_frame = ttk.LabelFrame(self.file_info_panel_container, text="════█ File Info █══════════════════",
                                         style="TLabelframe")
        self.finf_frame.pack(fill="x", expand=True, padx=3, pady=5)
        # ... (full content of finf_frame from your previous correct version) ...
        self.file_path_label = ttk.Label(self.finf_frame, text="Filename: N/A", wraplength=240, anchor="w")
        self.file_path_label.pack(fill="x", padx=5, pady=1)
        self.file_size_label = ttk.Label(self.finf_frame, text="File Size: N/A", anchor="w")
        self.file_size_label.pack(fill="x", padx=5, pady=1)
        self.created_label = ttk.Label(self.finf_frame, text="Created: N/A", anchor="w")
        self.created_label.pack(fill="x", padx=5, pady=1)
        self.modified_label = ttk.Label(self.finf_frame, text="Modified: N/A", anchor="w")
        self.modified_label.pack(fill="x", padx=5, pady=1)
        self.file_type_label = ttk.Label(self.finf_frame, text="File Type: N/A", anchor="w")
        self.file_type_label.pack(fill="x", padx=5, pady=1)
        self.md5_label = ttk.Label(self.finf_frame, text="MD5 Hash: N/A", anchor="w")
        self.md5_label.pack(fill="x", padx=5, pady=1)

        # --- Populate Go To Section ---
        self.goto_frame = ttk.LabelFrame(self.goto_panel_container, text="════█ Go To █════════════════════",
                                         style="TLabelframe")
        self.goto_frame.pack(fill="x", expand=True, padx=3, pady=5)
        # ... (full content of goto_frame from your previous correct version) ...
        self.current_addr_label = ttk.Label(self.goto_frame, text="0x00000000", font=("Consolas", 10, "bold"))
        self.current_addr_label.pack(fill="x", padx=5, pady=(2, 1))
        ToolTip(self.current_addr_label, "Current cursor offset. Right-click to copy, Double-click to use offset.")
        self.current_addr_label.bind("<Button-3>", self._show_current_addr_context_menu)
        self.current_addr_label.bind("<Double-Button-1>", self._use_current_addr_offset)
        self.last_replaced_offset_label = ttk.Label(self.goto_frame, text="Last Replaced: N/A", font=("Arial", 8))
        self.last_replaced_offset_label.pack(fill="x", padx=5, pady=(1, 2))
        fr_offset = ttk.Frame(self.goto_frame)
        fr_offset.pack(fill="x", padx=5, pady=2)
        self.goto_offset_label = ttk.Label(fr_offset, text="Offset:")
        self.goto_offset_label.pack(side="left")
        self.goto_var = tk.StringVar(value="0")
        self.goto_entry_widget = tk.Entry(fr_offset, textvariable=self.goto_var, width=12,
                                          relief="ridge", highlightthickness=1)
        self.goto_entry_widget.pack(side="left", padx=2, expand=True, fill="x")
        ToolTip(self.goto_entry_widget, "Enter hexadecimal offset (e.g., 0x100) or decimal (e.g., 256) to jump to.")
        self.goto_button = ttk.Button(fr_offset, text="Go", command=self.goto_offset, state="disabled", width=5)
        self.goto_button.pack(side="left", padx=(2, 0))
        fr_line = ttk.Frame(self.goto_frame)
        fr_line.pack(fill="x", padx=5, pady=2)
        self.goto_line_label = ttk.Label(fr_line, text="Line:   ")
        self.goto_line_label.pack(side="left")
        self.goto_line_var = tk.StringVar(value="0")
        self.goto_line_entry_widget = tk.Entry(fr_line, textvariable=self.goto_line_var, width=12,
                                               relief="ridge", highlightthickness=1)
        self.goto_line_entry_widget.pack(side="left", padx=2, expand=True, fill="x")
        ToolTip(self.goto_line_entry_widget, "Enter a decimal line number to jump to.")
        self.goto_line_button = ttk.Button(fr_line, text="Go", command=self.goto_line, state="disabled", width=5)
        self.goto_line_button.pack(side="left", padx=(2, 0))

        # --- Populate Bookmarks Section ---
        self.bookmarks_frame = ttk.LabelFrame(self.bookmarks_panel_container, text="════█ Bookmarks █════════════════",
                                              style="TLabelframe")
        self.bookmarks_frame.pack(fill="x", expand=True, padx=3, pady=5)
        # ... (full content of bookmarks_frame from your previous correct version) ...
        self.bookmarks_listbox = tk.Listbox(self.bookmarks_frame, height=5, exportselection=False,
                                            relief="ridge", highlightthickness=1)
        self.bookmarks_listbox.pack(fill="x", padx=2, pady=2)
        self.bookmarks_listbox.bind("<<ListboxSelect>>", lambda e: self.goto_bookmark())
        ToolTip(self.bookmarks_listbox, "Click a bookmark to jump to its offset.")
        bm_button_frame = ttk.Frame(self.bookmarks_frame)
        bm_button_frame.pack(fill="x", pady=(0, 2))
        add_bookmark_button = ttk.Button(bm_button_frame, text="Add", command=self.add_bookmark)
        add_bookmark_button.pack(side="left", expand=True, fill="x", padx=(2, 1))
        ToolTip(add_bookmark_button, "Add a bookmark at the current cursor position.")
        delete_bookmark_button = ttk.Button(bm_button_frame, text="Delete", command=self.delete_bookmark)
        delete_bookmark_button.pack(side="left", expand=True, fill="x", padx=(1, 2))
        ToolTip(delete_bookmark_button, "Delete the selected bookmark from the list.")

        # --- Populate Exit Button Container ---
        self.exit_button = ttk.Button(self.exit_button_container, text="Exit Application", command=self.root.quit,
                                      style="TButton")
        self.exit_button.pack(fill="x", padx=3, pady=5)
        ToolTip(self.exit_button, "Close the Hex Editor (Ctrl+Q)")


    def _build_search_panel_widgets(self):
        panel = self.search_panel

        srep_frame = ttk.LabelFrame(panel, text="════█ Search & Replace █════════════", style="TLabelframe")
        srep_frame.pack(fill="x", padx=3, pady=5)

        search_type_frame = ttk.Frame(srep_frame)
        search_type_frame.pack(fill="x", padx=2, pady=2)
        ttk.Label(search_type_frame, text="Type:").pack(side="left", padx=(0, 2))
        self.search_type = tk.StringVar(value="ASCII")
        search_type_combo = ttk.Combobox(search_type_frame, textvariable=self.search_type, values=["ASCII", "HEX"],
                                         width=8, state="readonly", style="TCombobox")
        search_type_combo.pack(side="left", expand=True, fill="x")

        search_entry_frame = ttk.Frame(srep_frame)
        search_entry_frame.pack(fill="x", padx=2, pady=2)
        ttk.Label(search_entry_frame, text="Find:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry_widget = tk.Entry(search_entry_frame, textvariable=self.search_var,
                                            relief="ridge", highlightthickness=1)
        self.search_entry_widget.pack(side="left", expand=True, fill="x")
        ToolTip(self.search_entry_widget, "Enter hex bytes (e.g., '0A B2') or ASCII text to search for.")

        replace_entry_frame = ttk.Frame(srep_frame)
        replace_entry_frame.pack(fill="x", padx=2, pady=2)
        ttk.Label(replace_entry_frame, text="Repl:").pack(side="left", padx=(0, 5))  # "Repl:" for Search/Replace All
        self.replace_var = tk.StringVar()  # This is for "Search & Replace All"
        self.replace_entry_widget = tk.Entry(replace_entry_frame, textvariable=self.replace_var,
                                             relief="ridge", highlightthickness=1)
        self.replace_entry_widget.pack(side="left", expand=True, fill="x")
        ToolTip(self.replace_entry_widget,
                "For 'Search & Replace All': Enter hex bytes or ASCII text to replace with (length usually matches search term).")

        search_buttons_frame = ttk.Frame(srep_frame)
        search_buttons_frame.pack(fill="x", expand=True, pady=(5, 2))
        self.search_button = ttk.Button(search_buttons_frame, text="Search All", command=self.search_bytes,
                                        state="disabled")
        self.search_button.pack(side="left", expand=True, fill="x", padx=(0, 1))
        self.search_replace_button = ttk.Button(search_buttons_frame, text="Replace All",
                                                command=self.search_and_replace_all, state="disabled")
        self.search_replace_button.pack(side="left", expand=True, fill="x", padx=(1, 0))

        self.nav_buttons_frame = ttk.Frame(srep_frame)
        self.nav_buttons_frame.pack(fill="x", pady=2, expand=True)
        prev_button = ttk.Button(self.nav_buttons_frame, text="< Prev", width=6, command=self.search_prev,
                                 state="disabled")
        prev_button.pack(side="left", padx=(0, 1))
        ToolTip(prev_button, "Go to the previous search match (Shift+F3).")
        next_button = ttk.Button(self.nav_buttons_frame, text="Next >", width=6, command=self.search_next,
                                 state="disabled")
        next_button.pack(side="left", padx=(1, 2))
        ToolTip(next_button, "Go to the next search match (F3).")

        self.match_count_label = ttk.Label(self.nav_buttons_frame, text="Matches: 0/0", anchor="e")
        self.match_count_label.pack(side="right", padx=2, fill="x")

        self.search_results_frame = ttk.LabelFrame(panel, text="════█ Search Results █═════════════",
                                                   style="TLabelframe")
        self.search_results_frame.pack(fill="both", expand=True, padx=3, pady=5)
        self.search_results_listbox_frame = ttk.Frame(self.search_results_frame, style="TFrame")
        self.search_results_listbox_frame.pack(fill="both", expand=True, pady=(0, 2))
        self.search_results_listbox = tk.Listbox(self.search_results_listbox_frame,
                                                 height=1,
                                                 selectmode=tk.SINGLE, exportselection=False,
                                                 relief="ridge", highlightthickness=1)
        self.search_results_listbox.pack(side="left", fill="both", expand=True)
        self.search_results_listbox.bind("<<ListboxSelect>>", self._on_search_result_select)
        ToolTip(self.search_results_listbox, "Click an offset to jump to the match. Results are from 'Search All'.")
        self.search_results_scrollbar = ttk.Scrollbar(self.search_results_listbox_frame, orient="vertical",
                                                      command=self.search_results_listbox.yview)
        self.search_results_scrollbar.pack(side="right", fill="y")
        self.search_results_listbox.config(yscrollcommand=self.search_results_scrollbar.set)
        self.clear_results_button = ttk.Button(self.search_results_frame, text="Clear Results",
                                               command=self.clear_search_results, state="disabled")
        self.clear_results_button.pack(fill="x", padx=2, pady=(2, 0))

        # --- MODIFICATIONS FOR "Replace Byte at Offset" ---
        offrep_frame = ttk.LabelFrame(panel, text="════█ Replace Byte at Offset █═════", style="TLabelframe")
        offrep_frame.pack(fill="x", padx=3, pady=5)

        offset_entry_frame = ttk.Frame(offrep_frame)
        offset_entry_frame.pack(fill="x", padx=2, pady=(2, 1))  # Adjusted pady
        ttk.Label(offset_entry_frame, text="Offset:").pack(side="left", padx=(0, 2))
        self.offset_var = tk.StringVar(value="0")
        self.offset_entry_widget = tk.Entry(offset_entry_frame, textvariable=self.offset_var,
                                            relief="ridge", highlightthickness=1)
        self.offset_entry_widget.pack(side="left", expand=True, fill="x")
        ToolTip(self.offset_entry_widget, "Enter dec or hex (0x) offset for single byte.")

        # NEW DEDICATED ENTRY FOR REPLACEMENT VALUE
        offset_val_frame = ttk.Frame(offrep_frame)
        offset_val_frame.pack(fill="x", padx=2, pady=(1, 2))  # Adjusted pady
        ttk.Label(offset_val_frame, text="Value: ").pack(side="left", padx=(0, 3))  # Label for the new entry
        self.offset_replace_value_var = tk.StringVar(value="00")  # New StringVar for this entry
        self.offset_replace_value_entry_widget = tk.Entry(offset_val_frame,  # New Entry widget
                                                          textvariable=self.offset_replace_value_var,
                                                          relief="ridge", highlightthickness=1)
        self.offset_replace_value_entry_widget.pack(side="left", expand=True, fill="x")
        ToolTip(self.offset_replace_value_entry_widget,
                "Enter a 1 byte value (e.g., '65' or '0A' or 'A').")
        # --- END OF MODIFICATIONS FOR NEW ENTRY ---

        self.offset_replace_button = ttk.Button(offrep_frame, text="Replace Byte", command=self.offset_replace,
                                                state="disabled")
        self.offset_replace_button.pack(fill="x", padx=2, pady=(5, 2))  # Added some top padding
        ToolTip(self.offset_replace_button,
                "Replace a single byte at the specified offset with the specified 'Value'.")

    def _on_endianness_change(self):
        """Called when the endianness radio button changes."""
        endian_prefix = self.inspector_endianness.get()
        endian_name = "Little-endian" if endian_prefix == "<" else "Big-endian"

        # Update status bar, ensuring other parts of status are not overwritten
        current_status = self.status_bar.cget("text")
        status_parts = current_status.split(" | Undo:")
        base_status = f"Inspector set to {endian_name}."
        if len(status_parts) > 1:
            self.status_bar.config(text=f"{base_status} | Undo:{status_parts[1]}")
        else:
            self.status_bar.config(text=base_status)
            self._update_undo_redo_status()  # Call this if the undo part was not present

        # Trigger inspector update
        current_offset_to_update = -1
        if self.hex_table.selected:
            row, col, _ = self.hex_table.selected
            offset = row * BYTES_PER_ROW + col
            if 0 <= offset < len(self.hex_table.file_data):
                current_offset_to_update = offset

        if current_offset_to_update != -1:
            self.update_inspector(current_offset_to_update)
        elif hasattr(self, 'current_addr_label') and self.current_addr_label.cget("text") not in ["N/A",
                                                                                                  "0x00000000"]:  # If no selection, try current address if valid
            try:
                offset_str = self.current_addr_label.cget("text")
                if offset_str.startswith("0x"):
                    offset_val = int(offset_str, 16)
                    if 0 <= offset_val < len(self.hex_table.file_data):
                        self.update_inspector(offset_val)
            except ValueError:
                pass  # current_addr_label might not be a valid offset

    def _on_left_panel_dedicated_mousewheel(self, event):
        """
        Dedicated mouse wheel handler for the left panel's canvas.
        """
        scroll_amount_y = 0
        if event.num == 4:  # Linux scroll up
            scroll_amount_y = -1
        elif event.num == 5:  # Linux scroll down
            scroll_amount_y = 1
        elif event.delta:  # Windows/macOS
            scroll_amount_y = -1 if event.delta > 0 else 1

        if scroll_amount_y != 0:
            self.left_canvas.yview_scroll(scroll_amount_y * 3, "units")
            return "break"
        return None



    def toggle_panel_visibility(self, panel_name_to_toggle, initial_setup=False):
        """Toggles the visibility of a specified panel and re-packs all visible panels in order."""

        panel_map = {
            "inspector": (getattr(self, 'inspector_panel_container', None), self.show_inspector_panel),
            "view_options": (getattr(self, 'view_options_panel_container', None), self.show_view_options_panel),
            "file_info": (getattr(self, 'file_info_panel_container', None), self.show_file_info_panel),
            "goto": (getattr(self, 'goto_panel_container', None), self.show_goto_panel),
            "bookmarks": (getattr(self, 'bookmarks_panel_container', None), self.show_bookmarks_panel)
        }

        # Get the specific panel and its boolean var being toggled
        current_panel_container, current_boolean_var = panel_map.get(panel_name_to_toggle, (None, None))

        if not current_panel_container or not current_boolean_var:
            if not initial_setup:  # Don't show error during initial setup if a panel isn't defined
                print(f"Warning: Panel '{panel_name_to_toggle}' not found for visibility toggle.")
            return

        # The BooleanVar has already been changed by the trace or menu click,
        # so boolean_var.get() reflects the NEW desired state.
        make_visible = current_boolean_var.get()

        if not make_visible:  # If we are hiding the panel
            if current_panel_container.winfo_ismapped():
                current_panel_container.pack_forget()
        else:  # If we are showing the panel (or it was already shown and the var was just set again)
            # To ensure correct order, we will forget all toggleable panels
            # and then re-pack only the ones that should be visible, in the correct order.

            # First, forget all panels in our map that are currently packed
            for p_name, (p_container, b_var) in panel_map.items():
                if p_container and p_container.winfo_ismapped():
                    p_container.pack_forget()

            # Now, re-pack all panels that *should* be visible, in the defined order
            # The exit_button_container will be packed last by _initial_panel_visibility_setup
            # or should be re-packed after this loop if it was also forgotten.

            desired_panel_order = ["inspector", "view_options", "file_info", "goto", "bookmarks"]
            pack_options = {"fill": "x", "padx": 0, "pady": (0, 1), "anchor": "n"}  # Small pady between panels

            for p_name_in_order in desired_panel_order:
                p_container_to_pack, b_var_to_check = panel_map[p_name_in_order]
                if p_container_to_pack and b_var_to_check.get():  # If it should be visible
                    p_container_to_pack.pack(**pack_options)

        if not initial_setup:
            self.status_bar.config(text=f"Panel '{panel_name_to_toggle.replace('_', ' ').title()}' "
                                        f"{'shown' if make_visible else 'hidden'}.")
            self._update_undo_redo_status()

        self.root.after_idle(lambda: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))

    def _on_encoding_change(self, event=None):  # event is passed by bind
        """Called when the ASCII encoding selection changes."""
        new_encoding = self.ascii_encoding_var.get()

        if hasattr(self, 'hex_table'):
            self.hex_table.selected_encoding = new_encoding
            self.hex_table._redraw()  # Redraw HexTable to reflect new encoding in ASCII column

            self.status_bar.config(text=f"ASCII encoding set to {new_encoding}.")
            self._update_undo_redo_status()  # Append undo/redo counts
        else:
            # This case should ideally not happen if UI is built correctly
            self.status_bar.config(text=f"Error: Hex table not available to set encoding {new_encoding}.")
            self._update_undo_redo_status()

    def update_inspector(self, sel_offset):
        fd = self.hex_table.file_data
        endian_prefix = self.inspector_endianness.get()

        # Initialize all inspector labels to "N/A"
        # These names must match the keys used when creating self.inspector_labels
        all_label_names = [
            "Byte (Dec)", "Byte (Hex)", "Byte (Oct)", "Byte (Bin)", "Byte (ASCII)",
            "8-bit Signed", "8-bit Unsigned", "16-bit Signed", "16-bit Unsigned",
            "32-bit Signed", "32-bit Unsigned", "64-bit Signed", "64-bit Unsigned",
            "16-bit Float (FP16)", "32-bit Float (FP32)", "64-bit Float (FP64)"
        ]
        for name in all_label_names:
            if hasattr(self, 'inspector_labels') and name in self.inspector_labels:
                self.inspector_labels[name].config(text="N/A")

        if not fd or sel_offset < 0 or sel_offset >= len(fd):
            return

        # --- Single Byte Interpretations ---
        byte_value = fd[sel_offset]
        if "Byte (Dec)" in self.inspector_labels: self.inspector_labels["Byte (Dec)"].config(text=str(byte_value))
        if "Byte (Hex)" in self.inspector_labels: self.inspector_labels["Byte (Hex)"].config(text=f"0x{byte_value:02X}")
        if "Byte (Oct)" in self.inspector_labels: self.inspector_labels["Byte (Oct)"].config(text=f"0o{byte_value:03o}")
        if "Byte (Bin)" in self.inspector_labels: self.inspector_labels["Byte (Bin)"].config(text=f"0b{byte_value:08b}")
        char_val = chr(byte_value) if 32 <= byte_value < 127 else '.'
        if "Byte (ASCII)" in self.inspector_labels: self.inspector_labels["Byte (ASCII)"].config(text=f"'{char_val}'")

        # --- Multi-Byte Interpretations (using self.inspector_formats) ---
        if hasattr(self, 'inspector_formats'):
            for name, base_fmt_char in self.inspector_formats.items():
                if name not in self.inspector_labels: continue  # Skip if label wasn't created

                # For 8-bit values, endianness doesn't apply for the value itself,
                # but struct still needs a prefix if it's part of a multi-byte view context.
                # However, 'b' and 'B' are single bytes.
                if base_fmt_char.lower() in ['b', 'B']:  # 'b' and 'B' are single byte formats
                    fmt_str = base_fmt_char
                else:
                    fmt_str = endian_prefix + base_fmt_char

                try:
                    num_bytes_needed = struct.calcsize(fmt_str)
                    if sel_offset + num_bytes_needed <= len(fd):
                        chunk = fd[sel_offset: sel_offset + num_bytes_needed]
                        value = struct.unpack(fmt_str, chunk)[0]
                        if isinstance(value, float):
                            self.inspector_labels[name].config(text=f"{value:.6g}")
                        else:
                            self.inspector_labels[name].config(text=str(value))
                    else:
                        self.inspector_labels[name].config(text="N/A (EOF)")
                except (struct.error, IndexError):
                    self.inspector_labels[name].config(text="Error")
                except Exception:
                    self.inspector_labels[name].config(text="Unpack Error")


        # self.status_bar.config(text=f"Inspector updated for offset 0x{sel_offset:08X}.")
        # self._update_undo_redo_status() # Already called by _on_hex_table_selection

    def load_file(self, path=None): # Allow path to be passed for recent files
        if path is None:
            filetypes = [
                ("All Files", "*.*"),
                ("Executable Files", "*.exe;*.dll;*.so;*.dylib"),
                ("Text Files", "*.txt;*.log;*.json;*.xml;*.csv"),
                ("Binary Files", "*.bin;*.dat"),
                ("Image Files", "*.jpg;*.png;*.gif;*.bmp;*.ico"),
                ("Archive Files", "*.zip;*.rar;*.tar;*.gz"),
            ]
            path = filedialog.askopenfilename(title="Open File", filetypes=filetypes)

        if not path:
            current_status = self.status_bar.cget("text").split(" | Undo:")[0]
            if "cancelled" not in current_status.lower() and "failed" not in current_status.lower(): # Avoid double status
                 self.status_bar.config(text="File open cancelled.")
            self._update_undo_redo_status()
            return
        try:
            with open(path, "rb") as f:
                data = f.read()

            self.hex_table.load_file(data) # This now correctly populates HexTable's data
            self.file_path = path
            self.file_size = len(data)
            self._update_file_info() # Update UI elements like file path, size, etc.

            if self.hex_table.total_rows > 0 or len(data) == 0 : # Go to 0 for empty file too
                self.hex_table.goto_offset_and_display(0) # Select first byte and scroll to top
            else: # Should not happen if load_file sets total_rows correctly for empty
                self.hex_table.selected = None
                self.hex_table.selection_start_offset = None
                self.hex_table.selection_end_offset = None
                self.current_addr_label.config(text="0x00000000")
                self.current_offset_display_label.config(text="Offset: N/A")
                self.update_inspector(0)

            # self.hex_table._redraw() # goto_offset_and_display and load_file should handle redraw
            self._update_widget_states(True) # Enable widgets
            self.clear_search_results()

            # Add to recent files
            if path in self.recent_files:
                self.recent_files.remove(path)
            self.recent_files.insert(0, path)
            if len(self.recent_files) > 10: # Max 10 recent files
                self.recent_files.pop()
            self._update_recent_files_menu()
            self.save_config() # Save config including recent files

            self.status_bar.config(text=f"Opened {os.path.basename(path)} ({self.file_size} bytes).")
            self._save_undo_state() # Save this loaded state as the first undo state
            # _update_undo_redo_status is called by _save_undo_state

        except MemoryError:
            messagebox.showerror("Memory Error", f"File '{os.path.basename(path)}' is too large to load into memory.")
            self.status_bar.config(text="Failed: File too large.")
            self._update_widget_states(False)
            self.clear_search_results()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file '{os.path.basename(path)}': {str(e)}")
            self.status_bar.config(text=f"Failed to load file: {os.path.basename(path)}.")
            self._update_widget_states(False)
            self.clear_search_results()
        self._update_undo_redo_status() # Ensure status bar is updated

    def _update_widget_states(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.search_button.config(state=state)
        self.search_replace_button.config(state=state)
        self.offset_replace_button.config(state=state)
        self.goto_button.config(state=state)
        self.goto_line_button.config(state=state)
        # Potentially disable/enable other widgets like save, context menu items etc.
        # For menu items: self.root.nametowidget(self.root.cget("menu")).entryconfig("File", state=state)
        # but this is for top-level. Individual commands need more specific handling if desired.

    def _update_recent_files_menu(self):
        self.recent_files_menu.delete(0, tk.END)
        for path in self.recent_files:
            # Use a default argument for path in lambda to capture current value
            self.recent_files_menu.add_command(label=os.path.basename(path),
                                               command=lambda p=path: self.load_file(p))
        if not self.recent_files:
            self.recent_files_menu.add_command(label="(No recent files)", state=tk.DISABLED)


    def save_file_as(self):
        if not self.hex_table.file_data and not self.file_path: # Stricter check: must have data
            messagebox.showinfo("Save As", "No data to save.")
            self.status_bar.config(text="Save As cancelled: No data.")
            self._update_undo_redo_status()
            return

        initial_dir = os.path.dirname(self.file_path) if self.file_path else os.getcwd()
        initial_filename = ""
        if self.file_path:
            original_filename = os.path.basename(self.file_path)
            name, ext = os.path.splitext(original_filename)
            # Suggest "filename_modified.ext" or similar if it's an existing file
            initial_filename = f"{name}_modified{ext}" if name else f"modified_file{ext}"
        else: # New, unsaved data
            initial_filename = "untitled.bin"


        filetypes = [
            ("Binary Files", "*.bin"),
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Executable Files", "*.exe"),
        ]

        path = filedialog.asksaveasfilename(
            title="Save File As",
            initialdir=initial_dir,
            initialfile=initial_filename,
            filetypes=filetypes,
            defaultextension=".bin" # Default if user doesn't type extension
        )

        if not path:
            self.status_bar.config(text="Save As cancelled by user.")
            self._update_undo_redo_status()
            return

        try:
            with open(path, "wb") as f:
                f.write(self.hex_table.file_data) # Save current data from HexTable
            # Optionally update self.file_path and title if this is considered a "Save" action
            # self.file_path = path
            # self.root.title(f"« Hex Editor » - {os.path.basename(path)}")
            # self._update_file_info() # Refresh file info panel
            messagebox.showinfo("Save As", f"File saved successfully to {os.path.basename(path)}")
            self.status_bar.config(text=f"Saved to {os.path.basename(path)}.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {e}")
            self.status_bar.config(text=f"Failed to save to {os.path.basename(path)}.")
        self._update_undo_redo_status()


    def _update_file_info(self):
        fp = self.file_path or "N/A"
        sz = self.file_size # This is len(self.hex_table.file_data)

        self.file_path_label.config(text=f"Filename: {os.path.basename(fp)}")
        ToolTip(self.file_path_label, fp) # Show full path in tooltip
        self.file_size_label.config(text=f"File Size: 0x{sz:08X} ({sz} bytes)")

        # Reset time/type/hash info first
        self.created_label.config(text="Created: N/A")
        self.modified_label.config(text="Modified: N/A")
        self.file_type_label.config(text="File Type: N/A")
        self.md5_label.config(text="MD5 Hash: N/A")


        if self.file_path and os.path.exists(self.file_path): # Only if path is set and file exists on disk
            try:
                st = os.stat(self.file_path)
                self.created_label.config(
                    text=f"Created: {datetime.datetime.fromtimestamp(st.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
                self.modified_label.config(
                    text=f"Modified: {datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception:
                pass # Silently ignore stat errors if file disappears or permissions change

        # File type detection based on current self.hex_table.file_data
        file_type_desc = "Unknown"
        current_data = self.hex_table.file_data
        if len(current_data) >= 2:
            if current_data.startswith(b'MZ'):
                file_type_desc = "MS-DOS Executable"
                if len(current_data) >= 0x40:
                    try:
                        pe_offset = struct.unpack("<I", current_data[0x3c:0x40])[0]
                        if len(current_data) >= pe_offset + 4 and current_data[pe_offset:pe_offset + 4] == b'PE\0\0':
                            file_type_desc = "Windows PE"
                            if len(current_data) >= pe_offset + 24 + 2: # OptionalHeader magic
                                optional_header_magic = struct.unpack("<H", current_data[pe_offset + 24 : pe_offset + 24 + 2])[0]
                                if optional_header_magic == 0x10B: file_type_desc += " (32-bit)"
                                elif optional_header_magic == 0x20B: file_type_desc += " (64-bit)"
                    except (struct.error, IndexError): pass # Could be a malformed PE
            elif current_data.startswith(b'\x7fELF'): file_type_desc = "ELF Executable"
            elif current_data.startswith(b'\xCA\xFE\xBA\xBE'): file_type_desc = "Java Class File"
            elif current_data.startswith(b'PK\x03\x04'): file_type_desc = "ZIP Archive"
            elif current_data.startswith(b'%PDF'): file_type_desc = "PDF Document"
            elif current_data.startswith(b'\xFF\xD8\xFF'): file_type_desc = "JPEG Image"
            elif current_data.startswith(b'\x89PNG'): file_type_desc = "PNG Image"
            elif current_data.startswith(b'GIF87a') or current_data.startswith(b'GIF89a'): file_type_desc = "GIF Image"

        self.file_type_label.config(text=f"File Type: {file_type_desc}")

        # MD5 hash of the current self.hex_table.file_data
        if current_data:
            if len(current_data) < 100 * 1024 * 1024: # Limit for quick hashing
                md5 = hashlib.md5()
                md5.update(current_data)
                self.md5_label.config(text=f"MD5 Hash: {md5.hexdigest()}")
            else:
                self.md5_label.config(text="MD5 Hash: Data too large for quick hash")
        else:
            self.md5_label.config(text="MD5 Hash: No data")

        # self.status_bar.config(text=f"File info updated for {os.path.basename(fp) if fp!='N/A' else 'current data'}.")
        # self._update_undo_redo_status() # Called by calling function usually

    def goto_offset(self):
        if not self.hex_table.file_data:
            messagebox.showwarning("Go To Offset", "No file loaded to navigate.")
            self.status_bar.config(text="Go To failed: No file loaded.")
            self._update_undo_redo_status()
            return
        try:
            offset_str = self.goto_var.get().strip()
            if not offset_str:
                messagebox.showwarning("Warning", "Please enter an offset.")
                self.status_bar.config(text="Go To failed: No offset entered.")
                self._update_undo_redo_status()
                return

            offset = -1
            if offset_str.lower().startswith("0x"):
                offset = int(offset_str, 16)
            else:
                offset = int(offset_str) # Assume decimal

            if 0 <= offset < len(self.hex_table.file_data):
                self.hex_table.goto_offset_and_display(offset)
                self.status_bar.config(text=f"Navigated to offset 0x{offset:08X}.")
            elif len(self.hex_table.file_data) == 0 and offset == 0: # Allow goto 0 for empty file
                self.hex_table.goto_offset_and_display(0)
                self.status_bar.config(text="At offset 0x00000000 (Empty file).")
            else:
                messagebox.showwarning("Invalid Offset", f"Offset 0x{offset:X} is out of file bounds (0x0 - 0x{len(self.hex_table.file_data)-1:X}).")
                self.status_bar.config(text="Go To failed: Offset out of bounds.")
        except ValueError:
            messagebox.showerror("Error", "Invalid offset format. Please use hex (e.g., 0x1A) or decimal.")
            self.status_bar.config(text="Go To failed: Invalid offset format.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.status_bar.config(text=f"Go To failed: {e}")
        self._update_undo_redo_status()


    def goto_line(self):
        if not self.hex_table.file_data:
            messagebox.showwarning("Go To Line", "No file loaded to navigate.")
            self.status_bar.config(text="Go To Line failed: No file loaded.")
            self._update_undo_redo_status()
            return
        try:
            line_str = self.goto_line_var.get().strip()
            if not line_str:
                messagebox.showwarning("Warning", "Please enter a line number.")
                self.status_bar.config(text="Go To Line failed: No line number entered.")
                self._update_undo_redo_status()
                return

            line_num = int(line_str) # Assumed to be decimal
            if line_num < 0:
                messagebox.showwarning("Invalid Line", "Line number cannot be negative.")
                self.status_bar.config(text="Go To Line failed: Line number negative.")
                self._update_undo_redo_status()
                return

            target_offset = line_num * BYTES_PER_ROW

            if 0 <= target_offset < len(self.hex_table.file_data):
                self.hex_table.goto_offset_and_display(target_offset)
                self.status_bar.config(text=f"Navigated to line {line_num} (Offset 0x{target_offset:08X}).")
            elif len(self.hex_table.file_data) == 0 and target_offset == 0: # Allow line 0 for empty
                self.hex_table.goto_offset_and_display(0)
                self.status_bar.config(text="At line 0, offset 0x00000000 (Empty file).")

            else:
                max_line = (len(self.hex_table.file_data) -1) // BYTES_PER_ROW if len(self.hex_table.file_data) > 0 else 0
                messagebox.showwarning("Invalid Line", f"Line number {line_num} is out of file bounds (0 - {max_line}).")
                self.status_bar.config(text="Go To Line failed: Line number out of bounds.")
        except ValueError:
            messagebox.showerror("Error", "Invalid line number format. Please use a decimal integer.")
            self.status_bar.config(text="Go To Line failed: Invalid format.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.status_bar.config(text=f"Go To Line failed: {e}")
        self._update_undo_redo_status()


    def search_bytes(self): # This is "Search All"
        s_term = self.search_var.get() # Don't strip yet, spaces might be intentional for ASCII
        mode = self.search_type.get()
        data = self.hex_table.file_data

        self.clear_search_results() # Clear previous results

        if not s_term: # Check after getting, not after strip for ASCII
            self.status_bar.config(text="Search term is empty.")
            self._update_undo_redo_status()
            self._update_search_nav_buttons()
            return

        try:
            search_bytes = b""
            if mode == "HEX":
                s_term_no_space = s_term.replace(" ", "").replace("\t", "")
                if not s_term_no_space: # Empty after stripping spaces
                     self.status_bar.config(text="Hex search term is effectively empty.")
                     self._update_undo_redo_status()
                     self._update_search_nav_buttons()
                     return
                if len(s_term_no_space) % 2 != 0:
                    messagebox.showerror("Hex Search Error", "Hex search string must have an even number of characters (e.g., 'AB CD' or 'ABCD').")
                    self.status_bar.config(text="Search failed: Invalid hex length.")
                    self._update_undo_redo_status()
                    self._update_search_nav_buttons()
                    return
                search_bytes = bytes.fromhex(s_term_no_space)
            else: # ASCII
                search_bytes = s_term.encode("latin-1") # Or 'utf-8' with error handling, latin-1 maps 0-255

            if not search_bytes: # If encoding results in empty bytes
                self.status_bar.config(text="Search term results in empty byte sequence.")
                self._update_undo_redo_status()
                self._update_search_nav_buttons()
                return

            self.hex_table.match_length = len(search_bytes) # Store for highlighting

            idx = 0
            while idx < len(data):
                found_at = data.find(search_bytes, idx)
                if found_at == -1:
                    break
                self.search_matches.append(found_at)
                line_number = found_at // BYTES_PER_ROW
                self.search_results_listbox.insert(tk.END, f"L:{line_number}, Off:0x{found_at:08X}")
                idx = found_at + 1 # Start next search after this match

            if self.search_matches:
                self.current_match_idx = 0
                self.search_results_listbox.selection_set(0)
                self.search_results_listbox.see(0)
                self._highlight_match() # This will also call _show_search_result via goto_offset
                self.status_bar.config(text=f"Found {len(self.search_matches)} instance(s).")
                self.clear_results_button.config(state="normal")
            else:
                self.status_bar.config(text="No matches found.")
                # _show_search_result will be called by _highlight_match or directly if no matches
                self._show_search_result() # Update "Matches: 0/0"

        except ValueError as ve: # Specifically for bytes.fromhex
            messagebox.showerror("Search Error", f"Invalid Hex format: {ve}. Use hex characters (0-9, A-F) e.g., '0A B2'.")
            self.status_bar.config(text="Search failed: Invalid hex format.")
        except Exception as e:
            messagebox.showerror("Search Error", f"An unexpected error occurred during search: {str(e)}")
            self.status_bar.config(text=f"Search failed: {e}")

        self._update_undo_redo_status()
        self._update_search_nav_buttons()


    def _update_search_nav_buttons(self):
        state = tk.NORMAL if self.search_matches else tk.DISABLED
        # Assuming nav_buttons_frame's children are prev and next buttons
        for widget in self.nav_buttons_frame.winfo_children(): # You'll need to store nav_buttons_frame as self.nav_buttons_frame
            if isinstance(widget, ttk.Button):
                widget.config(state=state)


    def _highlight_match(self):
        if not self.search_matches or self.current_match_idx < 0 or self.current_match_idx >= len(self.search_matches):
            # Clear previous selection if any from search highlighting
            # self.hex_table.selection_start_offset = None
            # self.hex_table.selection_end_offset = None
            # self.hex_table._redraw() # Don't clear user's manual selection
            if self.search_results_listbox.size() > 0: # Check if listbox has items
                try:
                    self.search_results_listbox.selection_clear(0, tk.END)
                except tk.TclError: pass # If listbox is empty or item doesn't exist
            self._show_search_result() # Update "Matches: 0/0"
            return

        match_offset = self.search_matches[self.current_match_idx]
        match_length = getattr(self.hex_table, 'match_length', 1)

        # Set selection range for highlighting
        self.hex_table.selection_start_offset = match_offset
        self.hex_table.selection_end_offset = match_offset + match_length - 1
        # Set single cursor selection to the start of the match
        self.hex_table.selected = (match_offset // BYTES_PER_ROW, match_offset % BYTES_PER_ROW, "hex")

        self.hex_table.goto_offset_and_display(match_offset) # This will redraw and trigger selection event

        # Update listbox selection
        if self.search_results_listbox.size() > 0:
            try:
                self.search_results_listbox.selection_clear(0, tk.END)
                self.search_results_listbox.selection_set(self.current_match_idx)
                self.search_results_listbox.see(self.current_match_idx) # Ensure it's visible
            except tk.TclError: pass # Handle cases where index might be out of bounds if list is modified

        self._show_search_result() # Update "Matches: X/Y" label
        # Status bar updated by goto_offset_and_display's selection event chain


    def _on_search_result_select(self, event):
        selected_indices = self.search_results_listbox.curselection()
        if not selected_indices:
            return

        selected_idx = int(selected_indices[0])
        if 0 <= selected_idx < len(self.search_matches):
            self.current_match_idx = selected_idx
            self._highlight_match() # This will navigate and update UI
            # Status bar will be updated by the chain of events from _highlight_match -> goto_offset -> _on_hex_table_selection
            # self.status_bar.config(text=f"Jumped to match {self.current_match_idx + 1} from list.")
            # self._update_undo_redo_status() # Called by status bar update chain

    def _show_search_result(self):
        total = len(self.search_matches)
        current_display_num = self.current_match_idx + 1 if self.current_match_idx >= 0 and total > 0 else 0
        self.match_count_label.config(text=f"Matches: {current_display_num}/{total}")
        # Status bar update is handled by other functions that call this or by selection events
        # Example: self.status_bar.config(text=f"Showing match {current_display_num} of {total}.")
        # self._update_undo_redo_status()


    def search_next(self):
        if not self.search_matches:
            self.status_bar.config(text="No search matches to navigate.")
            self._update_undo_redo_status()
            return

        self.current_match_idx = (self.current_match_idx + 1) % len(self.search_matches)
        self._highlight_match()
        # Status bar is updated by event chain of _highlight_match
        # self.status_bar.config(text=f"Moved to next match {self.current_match_idx + 1} of {len(self.search_matches)}.")
        # self._update_undo_redo_status()


    def search_prev(self):
        if not self.search_matches:
            self.status_bar.config(text="No search matches to navigate.")
            self._update_undo_redo_status()
            return

        self.current_match_idx = (self.current_match_idx - 1 + len(self.search_matches)) % len(self.search_matches)
        self._highlight_match()
        # self.status_bar.config(text=f"Moved to previous match {self.current_match_idx + 1} of {len(self.search_matches)}.")
        # self._update_undo_redo_status()

    def clear_search_results(self):
        self.search_matches.clear()
        self.current_match_idx = -1
        self.search_results_listbox.delete(0, tk.END)
        # self._highlight_match() # Don't highlight, just clear
        self.hex_table.match_length = 1 # Reset match length
        # Optionally clear selection related to search
        # self.hex_table.selection_start_offset = None
        # self.hex_table.selection_end_offset = None
        # self.hex_table._redraw()
        self._show_search_result() # Update "Matches: 0/0"
        self.clear_results_button.config(state="disabled")
        self._update_search_nav_buttons() # Disable prev/next if no matches
        self.status_bar.config(text="Search results cleared.")
        self._update_undo_redo_status()

    def search_and_replace_all(self): # Renamed for clarity
        s_term = self.search_var.get() # No strip for ASCII
        r_term = self.replace_var.get() # No strip for ASCII
        mode = self.search_type.get()
        data = self.hex_table.file_data

        if not s_term: # Check original terms
            messagebox.showwarning("Warning", "Search term cannot be empty for replace all.")
            self.status_bar.config(text="Replace All failed: Search term empty.")
            self._update_undo_redo_status()
            return
        # r_term can be empty if user wants to delete occurrences (by replacing with nothing)

        try:
            search_bytes, replace_bytes = b"", b""
            if mode == "HEX":
                s_term_no_space = s_term.replace(" ", "").replace("\t", "")
                r_term_no_space = r_term.replace(" ", "").replace("\t", "")

                if not s_term_no_space:
                    messagebox.showwarning("Warning", "Hex search term is effectively empty.")
                    self.status_bar.config(text="Replace All failed: Hex search term empty.")
                    self._update_undo_redo_status()
                    return

                if len(s_term_no_space) % 2 != 0:
                    messagebox.showerror("Error", "Search Hex string must have an even number of characters.")
                    self.status_bar.config(text="Replace All failed: Invalid search hex length.")
                    self._update_undo_redo_status()
                    return
                search_bytes = bytes.fromhex(s_term_no_space)

                if r_term_no_space: # Only parse if replace term is not empty
                    if len(r_term_no_space) % 2 != 0:
                        messagebox.showerror("Error", "Replace Hex string must have an even number of characters.")
                        self.status_bar.config(text="Replace All failed: Invalid replace hex length.")
                        self._update_undo_redo_status()
                        return
                    replace_bytes = bytes.fromhex(r_term_no_space)
                # If r_term_no_space is empty, replace_bytes remains b"" (deletion)

            else: # ASCII
                search_bytes = s_term.encode("latin-1") # Or 'utf-8'
                replace_bytes = r_term.encode("latin-1") # Or 'utf-8'

            if not search_bytes: # Should be caught earlier but as a safeguard
                self.status_bar.config(text="Replace All failed: Search bytes are empty.")
                self._update_undo_redo_status()
                return

            # For "Replace All", the lengths usually need to match unless you are doing complex replacements
            # For simple byte-for-byte or pattern replacement, they often do.
            # If you want to allow different lengths for replace_all, this check needs to be removed/modified.
            # Current Tkinter simpledialog-like replace usually implies same length or byte-wise.
            # For this function, let's assume it's a direct replacement, so if search_bytes is found,
            # it's replaced by replace_bytes, which could change the file size.

            num_found = data.count(search_bytes)
            if num_found == 0:
                self.status_bar.config(text="No matches found to replace.")
                self._update_undo_redo_status()
                return

            confirm_msg = f"Replace {num_found} instance(s) of '{s_term}' with '{r_term}'?"
            if len(search_bytes) != len(replace_bytes):
                confirm_msg += "\nWarning: Search and replace patterns have different lengths. File size will change."

            if not messagebox.askyesno("Confirm Replace All", confirm_msg, parent=self.root):
                self.status_bar.config(text="Replace All cancelled.")
                self._update_undo_redo_status()
                return

            # self._save_undo_state() # MOVED
            new_data = data.replace(search_bytes, replace_bytes) # bytearray.replace works

            self.hex_table.load_file(new_data)
            self.file_size = len(new_data)
            self._update_file_info()
            self.app_instance._save_undo_state() # MOVED HERE

            # After replacement, re-search to update listbox and highlight first new match if any
            # Or just clear search results as offsets would have changed.
            self.clear_search_results() # Clear old matches
            # Optionally, run search_bytes() again if desired, or prompt user.
            # For now, just state replacements done.
            self.hex_table.goto_offset_and_display(0) # Go to start of file
            self._highlight_changed_bytes(0, len(new_data) -1) # Highlight everything as it might have changed

            self.status_bar.config(text=f"Replaced {num_found} instance(s).")

        except ValueError as ve: # From hex parsing
            messagebox.showerror("Error", f"Invalid Hex format: {ve}.")
            self.status_bar.config(text="Replace All failed: Invalid hex format.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during replace all: {str(e)}")
            self.status_bar.config(text=f"Replace All failed: {e}")
        self._update_undo_redo_status()


    def copy_selection(self):
        start = self.hex_table.selection_start_offset
        end = self.hex_table.selection_end_offset # This is inclusive

        if start is None or end is None or not self.hex_table.file_data:
            self.status_bar.config(text="No selection to copy.")
            self._update_undo_redo_status()
            return

        # Ensure start <= end and they are within bounds
        start = max(0, start)
        end = min(len(self.hex_table.file_data) - 1, end)
        if start > end: # Should not happen if selection logic is correct
            self.status_bar.config(text="Invalid selection range for copy.")
            self._update_undo_redo_status()
            return

        selected_bytes = self.hex_table.file_data[start : end + 1]
        if not selected_bytes:
            self.status_bar.config(text="Selection is empty, nothing to copy.")
            self._update_undo_redo_status()
            return

        hex_string = "".join(f"{b:02X}" for b in selected_bytes)

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(hex_string) # Copy as hex string
            # self.root.update_idletasks() # Might not be necessary
            self.status_bar.config(text=f"Copied {len(selected_bytes)} bytes (0x{start:08X}-0x{end:08X}) as hex.")
        except tk.TclError:
            messagebox.showerror("Clipboard Error", "Could not access the clipboard.")
            self.status_bar.config(text="Copy failed: Clipboard error.")
        self._update_undo_redo_status()


    def cut_selection(self):
        start = self.hex_table.selection_start_offset
        end = self.hex_table.selection_end_offset # Inclusive

        if start is None or end is None or not self.hex_table.file_data:
            self.status_bar.config(text="No selection to cut.")
            self._update_undo_redo_status()
            return

        # Validate range
        start = max(0, start)
        end = min(len(self.hex_table.file_data) - 1, end)
        if start > end:
            self.status_bar.config(text="Invalid selection range for cut.")
            self._update_undo_redo_status()
            return

        num_bytes_to_cut = end - start + 1

        if not messagebox.askyesno("Confirm Cut", f"Cut {num_bytes_to_cut} bytes from 0x{start:08X} to 0x{end:08X}?", parent=self.root):
            self.status_bar.config(text="Cut cancelled.")
            self._update_undo_redo_status()
            return

        self.copy_selection() # First, copy the selection to clipboard
        # self._save_undo_state() # MOVED

        # Create new data by removing the cut portion
        new_file_data = bytearray()
        new_file_data.extend(self.hex_table.file_data[:start])
        new_file_data.extend(self.hex_table.file_data[end + 1:])

        self.hex_table.load_file(new_file_data)
        self.file_size = len(new_file_data)
        self._update_file_info()
        self.app_instance._save_undo_state() # MOVED HERE

        # Determine new cursor position (usually at the start of the cut)
        new_offset = min(start, len(new_file_data) -1 if new_file_data else 0)
        self.hex_table.goto_offset_and_display(new_offset)
        # No highlight for cut as bytes are gone
        self.status_bar.config(text=f"Cut {num_bytes_to_cut} bytes from 0x{start:08X}.")
        self._update_undo_redo_status()

    def paste_at_offset(self, target_offset=None):  # Added target_offset=None
        # If target_offset is not provided by the caller (e.g. context menu), determine it.
        if target_offset is None:
            if self.hex_table.selected:  # Paste at cursor
                row, col, _ = self.hex_table.selected
                target_offset = row * BYTES_PER_ROW + col
            elif self.hex_table.selection_start_offset is not None:  # Paste at start of selection
                target_offset = self.hex_table.selection_start_offset
            elif len(self.hex_table.file_data) == 0:  # File is empty, paste at start
                target_offset = 0
            else:
                self.status_bar.config(text="No active cursor/selection to paste at. Click to set cursor.")
                self._update_undo_redo_status()
                return

        # Ensure target_offset is within current data bounds (or at the very end for insertion)
        target_offset = max(0, min(target_offset, len(self.hex_table.file_data)))

        try:
            clipboard_content = self.root.clipboard_get()
        except tk.TclError:
            self.status_bar.config(text="Clipboard is empty or contains non-text data.")
            self._update_undo_redo_status()
            return

        paste_bytes = None
        clean_hex_string = "".join(c for c in clipboard_content if c in "0123456789abcdefABCDEF").strip()
        if clean_hex_string and len(clean_hex_string) % 2 == 0:
            try:
                paste_bytes = bytes.fromhex(clean_hex_string)
            except ValueError:
                paste_bytes = None

        if paste_bytes is None:
            try:
                paste_bytes = clipboard_content.encode('latin-1')
            except UnicodeEncodeError:
                messagebox.showwarning("Paste Error",
                                       "Clipboard content cannot be interpreted as Hex or simple ASCII/Latin-1 bytes.")
                self.status_bar.config(text="Paste failed: Invalid clipboard content type.")
                self._update_undo_redo_status()
                return

        if not paste_bytes:
            self.status_bar.config(text="No data to paste from clipboard after processing.")
            self._update_undo_redo_status()
            return

        # Current behavior: Insert paste_bytes at target_offset, shifting existing data
        new_file_data = bytearray(self.hex_table.file_data)  # Make a mutable copy
        new_file_data[target_offset:target_offset] = paste_bytes  # Slice assignment for insertion

        original_length = len(self.hex_table.file_data)
        self.hex_table.load_file(new_file_data)  # This updates HexTable's internal data
        self.file_size = len(new_file_data)  # Update app's file_size
        self._update_file_info()
        self._save_undo_state()

        new_cursor_pos = target_offset + len(paste_bytes)
        self.hex_table.goto_offset_and_display(new_cursor_pos)

        # Highlight the pasted region
        self._highlight_changed_bytes(target_offset, new_cursor_pos - 1)

        self.status_bar.config(text=f"Pasted {len(paste_bytes)} bytes at 0x{target_offset:08X}.")
        self._update_undo_redo_status()

    def fill_selection(self):
        start = self.hex_table.selection_start_offset
        end = self.hex_table.selection_end_offset  # Inclusive

        if start is None or end is None or not self.hex_table.file_data:
            messagebox.showinfo("Fill Selection", "No bytes selected to fill.", parent=self.root)
            self.status_bar.config(text="Fill Selection cancelled: No selection.")
            self._update_undo_redo_status()
            return

        start = max(0, start)
        end = min(len(self.hex_table.file_data) - 1, end)
        if start > end:
            self.status_bar.config(text="Fill Selection: Invalid selection range.")
            self._update_undo_redo_status()
            return

        num_bytes_to_fill = end - start + 1
        value_str = simpledialog.askstring("Fill Selection",
                                           f"Enter byte value to fill {num_bytes_to_fill} byte(s) (e.g., '00' or 'FF'):",
                                           parent=self.root)
        if value_str is None:
            self.status_bar.config(text="Fill Selection cancelled.")
            self._update_undo_redo_status()
            return

        value_str = value_str.strip()
        if not (len(value_str) == 2 and all(c in "0123456789abcdefABCDEF" for c in value_str.lower())):
            messagebox.showerror("Error", "Value must be a 2-digit hex string (e.g., '00', 'FF').", parent=self.root)
            self.status_bar.config(text="Fill Selection failed: Invalid fill value format.")
            self._update_undo_redo_status()
            return

        try:
            fill_byte = int(value_str, 16)

            # Directly modify the existing file_data bytearray in HexTable
            # No need to create a new modified_data if HexTable.file_data is already a bytearray
            changed_anything = False
            for i in range(start, end + 1):
                if self.hex_table.file_data[i] != fill_byte:
                    self.hex_table.file_data[i] = fill_byte
                    changed_anything = True

            if not changed_anything:
                self.status_bar.config(text=f"Selected bytes already filled with 0x{fill_byte:02X}. No change made.")
                self._update_undo_redo_status()
                # Still redraw and go to offset to ensure view is consistent if user expected something
                self.hex_table.goto_offset_and_display(start)
                self.hex_table._redraw()
                return

            # Since we modified HexTable.file_data directly, save its state
            self._save_undo_state()  # CORRECTED: Was self.app_instance._save_undo_state()

            # self.file_size remains the same, but MD5/checksums change
            self._update_file_info()  # Update hash, etc.

            self.hex_table.goto_offset_and_display(start)
            self.hex_table._redraw()  # Explicit redraw to show changes immediately
            self._highlight_changed_bytes(start, end)  # Call the helper method

            self.status_bar.config(
                text=f"Filled {num_bytes_to_fill} bytes with 0x{fill_byte:02X} from 0x{start:08X} to 0x{end:08X}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid byte value entered (not a valid hex byte).", parent=self.root)
            self.status_bar.config(text="Fill Selection failed: Invalid byte value.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during fill: {e}", parent=self.root)
            self.status_bar.config(text=f"Fill Selection failed: {e}")
        self._update_undo_redo_status()


    def hex_to_dec(self):
        hex_str = simpledialog.askstring("Hex to Decimal", "Enter hex value (e.g., 1A or 0x1A):", parent=self.root)
        if hex_str:
            try:
                # Remove "0x" prefix if present, and strip whitespace
                clean_hex_str = hex_str.lower().removeprefix("0x").strip()
                if not clean_hex_str: raise ValueError("Empty hex string")
                dec_value = int(clean_hex_str, 16)
                messagebox.showinfo("Result", f"Hex {clean_hex_str.upper()} = Decimal {dec_value}", parent=self.root)
                self.status_bar.config(text=f"Converted Hex {clean_hex_str.upper()} to Decimal {dec_value}.")
            except ValueError:
                messagebox.showerror("Error", "Invalid hex value.", parent=self.root)
                self.status_bar.config(text="Hex to Dec failed: Invalid hex value.")
        else: # User cancelled
            self.status_bar.config(text="Hex to Dec cancelled.")
        self._update_undo_redo_status()


    def dec_to_hex(self):
        dec_str = simpledialog.askstring("Decimal to Hex", "Enter decimal value:", parent=self.root) # Removed 0-255 constraint
        if dec_str:
            try:
                clean_dec_str = dec_str.strip()
                if not clean_dec_str: raise ValueError("Empty decimal string")
                dec_value = int(clean_dec_str)
                # No specific range check, convert any integer
                hex_value = f"{dec_value:X}" # Use uppercase X, no fixed padding
                messagebox.showinfo("Result", f"Decimal {dec_value} = Hex 0x{hex_value}", parent=self.root)
                self.status_bar.config(text=f"Converted Decimal {dec_value} to Hex 0x{hex_value}.")
            except ValueError:
                messagebox.showerror("Error", "Invalid decimal value.", parent=self.root)
                self.status_bar.config(text="Dec to Hex failed: Invalid decimal value.")
        else: # User cancelled
            self.status_bar.config(text="Dec to Hex cancelled.")
        self._update_undo_redo_status()

    def calculate_hash_for_selection(self, hash_type="md5"):
        start = self.hex_table.selection_start_offset
        end = self.hex_table.selection_end_offset  # Inclusive

        if start is None or end is None or not self.hex_table.file_data:
            self.status_bar.config(text="No selection to calculate hash.")
            self._update_undo_redo_status()
            return

        # Ensure valid range, although selection logic should maintain this
        start = max(0, start)
        end = min(len(self.hex_table.file_data) - 1, end)
        if start > end:
            self.status_bar.config(text="Invalid selection range for hash calculation.")
            self._update_undo_redo_status()
            return

        selected_data = self.hex_table.file_data[start: end + 1]
        if not selected_data:
            self.status_bar.config(text="Empty selection, no hash calculated.")
            self._update_undo_redo_status()
            return

        hash_result_str = ""
        display_hash_type = hash_type.upper()

        try:
            if hash_type == "md5":
                hasher = hashlib.md5()
                hasher.update(selected_data)
                hash_result_str = hasher.hexdigest()
            elif hash_type == "sha1":
                hasher = hashlib.sha1()
                hasher.update(selected_data)
                hash_result_str = hasher.hexdigest()
            elif hash_type == "sha256":
                hasher = hashlib.sha256()
                hasher.update(selected_data)
                hash_result_str = hasher.hexdigest()
            # elif hash_type == "crc32":
            #     import zlib # Make sure zlib is imported at the top of your script
            #     crc_val = zlib.crc32(selected_data)
            #     hash_result_str = f"{crc_val & 0xFFFFFFFF:08x}" # Keep as hex string
            #     display_hash_type = "CRC32"
            else:
                self.status_bar.config(text=f"Unsupported hash type: {hash_type}")
                self._update_undo_redo_status()
                return

            result_title = f"{display_hash_type} for Selection"
            result_message = (f"{display_hash_type} (0x{start:08X} - 0x{end:08X}, {len(selected_data)} bytes):\n\n"
                              f"{hash_result_str}")

            # Display in a Toplevel window with a Text widget for easy copying
            result_win = tk.Toplevel(self.root)
            result_win.title(result_title)
            result_win.transient(self.root)  # Keep on top of main window
            result_win.geometry("550x120")  # Adjust size as needed
            result_win.minsize(400, 100)

            # Apply theme to the result window if possible
            result_win.config(bg=self.colors.get("PANEL_BG", "#e0e0e0"))

            text_area = tk.Text(result_win, wrap=tk.WORD, height=3, font=("Consolas", 10),
                                bg=self.colors.get("EDIT_BG", "#ffffff"),
                                fg=self.colors.get("EDIT_FG", "#000000"),
                                relief=tk.SOLID, borderwidth=1)
            text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_area.insert(tk.END, result_message)
            text_area.config(state=tk.DISABLED)  # Make it read-only

            button_frame = ttk.Frame(result_win, style="TFrame")  # Use themed frame
            button_frame.pack(pady=(0, 10))

            copy_button = ttk.Button(button_frame, text="Copy Hash",
                                     command=lambda h=hash_result_str: self._copy_text_to_clipboard(h))
            copy_button.pack(side=tk.LEFT, padx=5)

            close_button = ttk.Button(button_frame, text="Close", command=result_win.destroy)
            close_button.pack(side=tk.LEFT, padx=5)

            result_win.grab_set()  # Make it modal to the application
            self.root.wait_window(result_win)  # Wait for this window to close

            self.status_bar.config(text=f"Calculated {display_hash_type} for selection (0x{start:08X}-0x{end:08X}).")

        except ImportError:  # Specifically for zlib if CRC32 is enabled
            messagebox.showerror("Import Error",
                                 f"The 'zlib' module is required for {display_hash_type} but not found.",
                                 parent=self.root)
            self.status_bar.config(text=f"Error: zlib module not found for {display_hash_type}.")
        except Exception as e:
            messagebox.showerror("Hash Error", f"Error calculating {display_hash_type}: {e}", parent=self.root)
            self.status_bar.config(text=f"Error calculating {display_hash_type}.")
        self._update_undo_redo_status()

    def save_config(self):
        config_file_path = self.get_config_path()  # Uses the helper method

        theme_name_map = {
            id(LIGHT_THEME_COLORS): "LIGHT_THEME_COLORS",
            id(PYTHONPLUS_THEME_COLORS): "PYTHONPLUS_THEME_COLORS",
            id(DARKAMBER1_THEME_COLORS): "DARKAMBER1_THEME_COLORS",
            id(COLORFUL_THEME_COLORS): "COLORFUL_THEME_COLORS"
        }
        # Use self.colors which is updated by _apply_theme
        current_theme_name = theme_name_map.get(id(self.colors), "PYTHONPLUS_THEME_COLORS")  # Default if custom

        config = {
            "version": "2.3",  # Good practice to version your config
            "theme": current_theme_name,
            "recent_files": self.recent_files[:10],  # Save up to 10 recent files
            "bookmarks": self.bookmarks,
            "last_file_path": self.file_path if self.file_path else "",
            "last_file_pos": self.hex_table.current_display_offset if self.hex_table.file_data else 0,
            "ascii_encoding": self.ascii_encoding_var.get() if hasattr(self, 'ascii_encoding_var') else "latin-1",
            "inspector_endianness": self.inspector_endianness.get() if hasattr(self, 'inspector_endianness') else "<"
            # Add other persistent settings here if needed
            # "window_geometry": self.root.geometry() # Example for window size/pos
        }
        try:
            with open(config_file_path, "w") as f:
                json.dump(config, f, indent=4)
            # Avoid messagebox for routine saves, status bar is enough
            self.status_bar.config(text=f"Configuration saved.")
        except Exception as e:
            messagebox.showerror("Save Config Error", f"Failed to save configuration to {config_file_path}:\n{e}",
                                 parent=self.root)
            self.status_bar.config(text="Failed to save configuration.")
        self._update_undo_redo_status()  # Ensure undo/redo counts are appended correctly


    def load_config(self, startup=False):
        config_file_path = self.get_config_path()
        # print(f"Attempting to load config from: {config_file_path}") # For debugging

        if os.path.exists(config_file_path):
            try:
                with open(config_file_path, "r") as f:
                    config = json.load(f)

                theme_map = {
                    "LIGHT_THEME_COLORS": LIGHT_THEME_COLORS,
                    "PYTHONPLUS_THEME_COLORS": PYTHONPLUS_THEME_COLORS,
                    "DARKAMBER1_THEME_COLORS": DARKAMBER1_THEME_COLORS,
                    "COLORFUL_THEME_COLORS": COLORFUL_THEME_COLORS
                }
                chosen_theme_name = config.get("theme", "PYTHONPLUS_THEME_COLORS")
                chosen_theme = theme_map.get(chosen_theme_name, PYTHONPLUS_THEME_COLORS)
                self._apply_theme(chosen_theme)  # Apply theme first

                self.recent_files = config.get("recent_files", [])
                self._update_recent_files_menu()

                self.bookmarks = config.get("bookmarks", {})
                self.update_bookmarks_list()

                file_to_load_on_startup = config.get("last_file_path", "") if startup else None

                if file_to_load_on_startup and os.path.exists(file_to_load_on_startup):
                    self.load_file(path=file_to_load_on_startup)

                    if self.file_path == file_to_load_on_startup:
                        last_pos = config.get("last_file_pos", 0)
                        if self.hex_table.file_data:
                            self.hex_table.goto_offset_and_display(last_pos)
                        self.status_bar.config(
                            text=f"Loaded last session: {os.path.basename(file_to_load_on_startup)}.")
                    else:
                        self._update_widget_states(False)
                elif startup:
                    self._update_widget_states(False)
                    if file_to_load_on_startup:
                        self.status_bar.config(
                            text=f"Last session file not found: {os.path.basename(file_to_load_on_startup)}.")
                    else:
                        self.status_bar.config(text="Configuration loaded. No previous file.")
                elif not startup:
                    self.status_bar.config(text="Configuration loaded.")


            except json.JSONDecodeError:
                msg = f"{os.path.basename(config_file_path)} is corrupted or not valid JSON."
                if not startup: messagebox.showerror("Config Error", msg, parent=self.root)
                self.status_bar.config(text=f"Error: Config file corrupted. Defaults applied.")
                self._apply_theme(PYTHONPLUS_THEME_COLORS)
                self._update_widget_states(False)
            except Exception as e:
                msg = f"Error loading config: {str(e)}"
                if not startup: messagebox.showerror("Config Error", msg, parent=self.root)
                self.status_bar.config(text=f"Error loading config. Defaults applied.")
                self._apply_theme(PYTHONPLUS_THEME_COLORS)
                self._update_widget_states(False)
        else:
            if not startup:
                messagebox.showwarning("Load Config", f"No configuration file found at:\n{config_file_path}",
                                       parent=self.root)
            self.status_bar.config(text="No configuration file found. Using defaults.")
            self._apply_theme(PYTHONPLUS_THEME_COLORS)
            self._update_widget_states(False)

        self._update_undo_redo_status()


    def _save_undo_state(self):
        if self._is_undoing_or_redoing:
            return

        current_data_snapshot = bytearray(self.hex_table.file_data)

        # Only add to stack if it's different from the last saved state,
        # or if the stack is empty (initial state).
        if not self._undo_stack or self._undo_stack[-1] != current_data_snapshot:
            if len(self._undo_stack) >= self._max_undo_states:
                self._undo_stack.pop(0) # Remove oldest state if max is reached
            self._undo_stack.append(current_data_snapshot)
            self._redo_stack.clear() # Any new action clears the redo stack
        self._update_undo_redo_status()

    def undo(self):
        if len(self._undo_stack) > 1: # Need at least two states: [previous_state, current_state_being_undone]
            self._is_undoing_or_redoing = True

            current_state_being_undone = self._undo_stack.pop() # Remove current from undo
            self._redo_stack.append(current_state_being_undone) # Add it to redo

            state_to_restore = self._undo_stack[-1] # This is the state we want to go back to

            # Preserve selection/view if possible
            original_selected_offset = -1
            if self.hex_table.selected:
                row, col, _ = self.hex_table.selected
                original_selected_offset = row * BYTES_PER_ROW + col

            self.hex_table.load_file(bytearray(state_to_restore)) # Load a copy
            self.file_size = len(state_to_restore)
            self._update_file_info() # Update MD5, file type, etc.

            if original_selected_offset != -1:
                # Try to restore selection, clamping to new file size
                new_offset = min(max(0, original_selected_offset), self.file_size -1 if self.file_size > 0 else 0)
                self.hex_table.goto_offset_and_display(new_offset)
            elif self.file_size > 0 : # No prior selection, or file was empty
                self.hex_table.goto_offset_and_display(0) # Go to start
            else: # File became empty
                 self.hex_table.goto_offset_and_display(0) # Go to 0 for empty file
                 self._on_hex_table_selection() # Manually trigger update for empty file state

            self.status_bar.config(text="Undo successful.")
            self._is_undoing_or_redoing = False
        else:
            self.status_bar.config(text="Nothing to undo.")
        self._update_undo_redo_status()


    def redo(self):
        if self._redo_stack:
            self._is_undoing_or_redoing = True

            state_to_restore = self._redo_stack.pop() # Get state from redo
            self._undo_stack.append(state_to_restore) # Add it back to undo_stack as current state

            original_selected_offset = -1
            if self.hex_table.selected:
                row, col, _ = self.hex_table.selected
                original_selected_offset = row * BYTES_PER_ROW + col

            self.hex_table.load_file(bytearray(state_to_restore)) # Load a copy
            self.file_size = len(state_to_restore)
            self._update_file_info()

            if original_selected_offset != -1:
                new_offset = min(max(0, original_selected_offset), self.file_size -1 if self.file_size > 0 else 0)
                self.hex_table.goto_offset_and_display(new_offset)
            elif self.file_size > 0:
                self.hex_table.goto_offset_and_display(0)
            else:
                 self.hex_table.goto_offset_and_display(0)
                 self._on_hex_table_selection()

            self.status_bar.config(text="Redo successful.")
            self._is_undoing_or_redoing = False
        else:
            self.status_bar.config(text="Nothing to redo.")
        self._update_undo_redo_status()

    def _update_undo_redo_status(self):
        current_status_text = self.status_bar.cget("text")
        # Remove old undo/redo part if it exists
        main_status = current_status_text.split(" | Undo:")[0].split(" | Redo:")[0].strip()

        # _undo_stack[0] is the initial state. Countable undo actions are len-1.
        undo_count = max(0, len(self._undo_stack) - 1)
        redo_count = len(self._redo_stack)

        new_status_suffix = ""
        if undo_count > 0 or redo_count > 0:  # Only show if there's something to report
            new_status_suffix = f" | Undo: {undo_count} | Redo: {redo_count}"

        self.status_bar.config(text=f"{main_status}{new_status_suffix}")

        # MODIFIED PART STARTS
        # Update menu item states using the stored self.edit_menu reference
        if hasattr(self, 'edit_menu') and self.edit_menu:  # Check if edit_menu exists
            try:
                self.edit_menu.entryconfig("Undo", state=tk.NORMAL if undo_count > 0 else tk.DISABLED)
                self.edit_menu.entryconfig("Redo", state=tk.NORMAL if redo_count > 0 else tk.DISABLED)
            except tk.TclError:  # In case "Undo" or "Redo" labels are not found (should not happen with correct setup)
                # This might happen if the menu structure changes unexpectedly or during very early init
                # print("Warning: Could not configure Undo/Redo menu items in _update_undo_redo_status.")
                pass
        # MODIFIED PART ENDS


    def show_ascii_table(self, event=None):
        ascii_window = tk.Toplevel(self.root)
        ascii_window.title("ASCII Table (CP437 Chars)")
        ascii_window.geometry("750x550") # Adjusted size
        ascii_window.minsize(400, 300)
        ascii_window.transient(self.root) # Keep on top of main window
        ascii_window.grab_set() # Modal behavior

        # Use a themed frame consistent with the app
        main_frame = ttk.Frame(ascii_window, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Canvas for scrollable content
        canvas = tk.Canvas(main_frame, bg=self.colors["PANEL_BG"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        scrollable_frame = ttk.Frame(canvas, style="TFrame") # Frame inside canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Header
        header_font = tkfont.Font(family="Consolas", size=10, weight="bold")
        header_label_text = "Dec (Char) Hex | Dec (Char) Hex | ..."
        header_label = ttk.Label(scrollable_frame, text=header_label_text, font=header_font,
                                 foreground=self.colors["OFFSET_COLOR"], background=self.colors["OFFSET_BG"],
                                 padding=(5,2), relief="raised", borderwidth=1)
        header_label.grid(row=0, column=0, columnspan=16, sticky="ew", pady=(0,5))


        cell_font = tkfont.Font(family="Consolas", size=12)
        selected_value = tk.IntVar(value=0) # Store selected decimal value

        # Context Menu
        context_menu = tk.Menu(ascii_window, tearoff=0)
        self._apply_menu_theme(context_menu) # Apply app theme to context menu
        context_menu.add_command(label="Copy Value (Dec)", command=lambda: self._copy_ascii_value(selected_value.get(), "dec"))
        context_menu.add_command(label="Copy Value (Hex)", command=lambda: self._copy_ascii_value(selected_value.get(), "hex"))
        context_menu.add_command(label="Copy Character", command=lambda: self._copy_ascii_value(selected_value.get(), "char"))
        context_menu.add_command(label="Copy All Info", command=lambda: self._copy_ascii_value(selected_value.get(), "all"))


        cells = {} # To store cell labels for highlighting

        def on_cell_click(value):
            selected_value.set(value)
            update_highlight()
            ascii_window.title(f"ASCII Table - Selected: Dec {value} (0x{value:02X})")
            self.status_bar.config(text=f"ASCII Table: Selected Dec {value} (0x{value:02X}).")
            self._update_undo_redo_status()


        def on_cell_right_click(event, value):
            on_cell_click(value) # Select the cell first
            context_menu.tk_popup(event.x_root, event.y_root)

        def update_highlight():
            for val, (label_widget, _) in cells.items():
                bg_color = self.colors["HEX_SEL_COLOR"] if val == selected_value.get() else self.colors["HEX_CELL_EVEN_BG"] if (val // 16 + val % 16) % 2 == 0 else self.colors["HEX_CELL_ODD_BG"]
                label_widget.config(background=bg_color)
                if val == selected_value.get():
                     label_widget.config(foreground=self.colors["HEX_VALUE_COLOR"]) # Ensure contrast on selection
                else:
                     label_widget.config(foreground=self.colors["FG"])


        cols_per_row_display = 8 # How many full entries (Dec (Char) Hex) per visual row
        max_val = 255

        current_row = 1 # Start after header
        current_col = 0
        for i in range(max_val + 1):
            char_display = '.'
            try:
                # Try to decode using CP437 (common for old DOS-like tables)
                # For other encodings, this might need to change.
                char_display = bytes([i]).decode('cp437', errors='replace')
                if not char_display.isprintable() and i not in [0,7,8,9,10,11,12,13,27]: # Allow some control chars to show if printable by font
                     if 0 <= i <= 31 or i == 127: char_display = '.' # Common unprintables
            except UnicodeDecodeError:
                char_display = '?' # Should not happen with 'replace'

            cell_text = f"{i:3d} ({char_display}) {i:02X}"
            bg_color = self.colors["HEX_CELL_EVEN_BG"] if (i // 16 + i % 16) % 2 == 0 else self.colors["HEX_CELL_ODD_BG"]

            cell_label = ttk.Label(scrollable_frame, text=cell_text, font=cell_font, padding=(3,1),
                                   relief="groove", borderwidth=1, anchor="center",
                                   background=bg_color, foreground=self.colors["FG"])
            cell_label.grid(row=current_row, column=current_col, sticky="nsew", padx=1, pady=1)
            scrollable_frame.grid_columnconfigure(current_col, weight=1) # Allow columns to expand

            cell_label.bind("<Button-1>", lambda e, v=i: on_cell_click(v))
            cell_label.bind("<Button-3>", lambda e, v=i: on_cell_right_click(e, v))
            cells[i] = (cell_label, char_display) # Store label and actual char

            current_col += 1
            if current_col >= cols_per_row_display:
                current_col = 0
                current_row += 1

        scrollable_frame.grid_rowconfigure(current_row, weight=1) # Allow last row to expand if needed

        update_highlight() # Initial highlight for value 0
        self.status_bar.config(text="ASCII Table opened.")
        self._update_undo_redo_status()


    def _copy_ascii_value(self, dec_value, copy_type):
        char_val = '.'
        try: char_val = bytes([dec_value]).decode('cp437', errors='replace')
        except: pass
        if not char_val.isprintable() and dec_value not in [0,7,8,9,10,11,12,13,27]:
            if 0 <= dec_value <= 31 or dec_value == 127: char_val = '.'


        hex_val = f"0x{dec_value:02X}"
        str_dec_val = str(dec_value)

        copy_text = ""
        if copy_type == "dec": copy_text = str_dec_val
        elif copy_type == "hex": copy_text = hex_val
        elif copy_type == "char": copy_text = char_val
        elif copy_type == "all": copy_text = f"Dec: {str_dec_val}, Hex: {hex_val}, Char: '{char_val}'"

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(copy_text)
            self.status_bar.config(text=f"ASCII Table: Copied '{copy_text}' to clipboard.")
        except tk.TclError:
            messagebox.showerror("Clipboard Error", "Could not access clipboard.", parent=self.root.focus_get()) # Parent might be ASCII window
            self.status_bar.config(text="ASCII Table: Clipboard error.")
        self._update_undo_redo_status()

    def offset_replace(self):
        try:
            offset_str = self.offset_var.get().strip()
            # Get replacement value from the new dedicated entry
            repl_str = self.offset_replace_value_var.get().strip()

            if not offset_str or not repl_str:
                messagebox.showwarning("Warning", "Offset and Replacement Value fields cannot be empty.",
                                       parent=self.root)
                self.status_bar.config(text="Offset Replace failed: Fields empty.")
                self._update_undo_redo_status()
                return

            offset = -1
            if offset_str.lower().startswith("0x"):
                offset = int(offset_str, 16)
            else:
                offset = int(offset_str)

            if not (0 <= offset < len(self.hex_table.file_data)):
                messagebox.showwarning("Invalid Offset", f"Offset 0x{offset:X} is out of file bounds.",
                                       parent=self.root)
                self.status_bar.config(text="Offset Replace failed: Offset out of bounds.")
                self._update_undo_redo_status()
                return

            repl_value = -1
            # Interpret repl_str as a single byte (hex, decimal 0-255, or single ASCII char)
            if len(repl_str) == 2 and all(c in "0123456789abcdefABCDEF" for c in repl_str.lower()):
                repl_value = int(repl_str, 16)
            elif repl_str.isdigit():
                temp_val = int(repl_str)
                if 0 <= temp_val <= 255:
                    repl_value = temp_val
                else:
                    try:
                        repl_value = int(repl_str, 16)
                        if not (0 <= repl_value <= 255):
                            raise ValueError("Hex value out of byte range.")
                    except ValueError:
                        raise ValueError(
                            "Replacement value must be a 2-digit hex, a decimal 0-255, or a single ASCII char.")
            elif len(repl_str) == 1:
                repl_value = ord(repl_str[0])
            else:
                try:
                    repl_value = int(repl_str, 16)
                    if not (0 <= repl_value <= 255):
                        raise ValueError("Hex value out of byte range.")
                except ValueError:
                    raise ValueError(
                        "Replacement value must be a 2-digit hex, a decimal 0-255, or a single ASCII char.")

            if not (0 <= repl_value <= 255):
                messagebox.showerror("Error", "Replacement value could not be parsed to a valid byte (0-255).",
                                     parent=self.root)
                self.status_bar.config(text="Offset Replace failed: Invalid replacement format.")
                self._update_undo_redo_status()
                return

            old_value = self.hex_table.file_data[offset]
            if old_value == repl_value:
                self.status_bar.config(text=f"Byte at 0x{offset:08X} already {repl_value:02X}. No change.")
                self.hex_table.goto_offset_and_display(offset)
                self._update_undo_redo_status()
                return

            self.hex_table.file_data[offset] = repl_value
            # CORRECTED LINE:
            self._save_undo_state()  # Changed from self.app_instance._save_undo_state()

            self.hex_table._redraw()
            if hasattr(self, 'last_replaced_offset_label'):  # Check if label exists
                self.last_replaced_offset_label.config(text=f"Last Replaced: 0x{offset:08X} with 0x{repl_value:02X}")
            self.hex_table.goto_offset_and_display(offset)
            self._highlight_changed_bytes(offset, offset)
            self._update_file_info()
            self.status_bar.config(text=f"Replaced byte at 0x{offset:08X}: {old_value:02X} -> {repl_value:02X}.")

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve), parent=self.root)
            self.status_bar.config(text=f"Offset Replace failed: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)
            self.status_bar.config(text=f"Offset Replace failed: {e}")
        self._update_undo_redo_status()


    def _highlight_changed_bytes(self, start_offset, end_offset):
        """Delegates highlighting to the HexTable instance."""
        if hasattr(self, 'hex_table'):
            self.hex_table._highlight_changed_bytes(start_offset, end_offset)


    def _show_current_addr_context_menu(self, event):
        """Shows a context menu for the current_addr_label."""
        offset_text = self.current_addr_label.cget("text")

        context_menu = tk.Menu(self.root, tearoff=0)
        self._apply_menu_theme(context_menu)  # Apply current theme

        if offset_text and offset_text != "0x00000000" and offset_text != "N/A":  # Only if there's a valid offset
            context_menu.add_command(label=f"Copy Offset ({offset_text})",
                                     command=lambda: self._copy_text_to_clipboard(offset_text))
        else:
            context_menu.add_command(label="Copy Offset", state=tk.DISABLED)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def _copy_text_to_clipboard(self, text_to_copy):
        """Helper to copy given text to the clipboard."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)
            self.status_bar.config(text=f"Copied '{text_to_copy}' to clipboard.")
            self._update_undo_redo_status()
        except tk.TclError:
            messagebox.showerror("Clipboard Error", "Could not access the clipboard.", parent=self.root)
            self.status_bar.config(text="Copy failed: Clipboard error.")
            self._update_undo_redo_status()

    def _use_current_addr_offset(self, event):
        """Populates offset fields with the current_addr_label's value on double-click."""
        offset_text = self.current_addr_label.cget("text")

        if not offset_text or offset_text == "N/A":
            self.status_bar.config(text="No valid offset to use.")
            self._update_undo_redo_status()
            return

        # Try to convert to ensure it's a valid number string before using
        try:
            # We just need the string representation (e.g., "0x1A2B")
            # The StringVar for the entry widgets will handle it.
            # If it's "0x00000000", it's fine.
            if offset_text.startswith("0x"):
                _ = int(offset_text, 16)  # Validate it's a hex number
            else:  # Should ideally always be hex from current_addr_label
                _ = int(offset_text)  # Validate it's a decimal number
        except ValueError:
            self.status_bar.config(text=f"Current address '{offset_text}' is not a valid number format to use.")
            self._update_undo_redo_status()
            return

        action_taken = False
        # Populate the "Go To -> Offset" field
        if hasattr(self, 'goto_var'):
            self.goto_var.set(offset_text)
            action_taken = True

        # Populate the "Replace Byte at Offset -> Offset" field
        if hasattr(self, 'offset_var'):  # This is the StringVar for the offset_entry_widget
            self.offset_var.set(offset_text)  # Set its value
            action_taken = True

        # Potentially populate search field if it makes sense (e.g., if search type is HEX and offset is a valid search term)
        # For now, focusing on the direct offset entry fields.
        # if hasattr(self, 'search_var') and self.search_type.get() == "HEX":
        #     self.search_var.set(offset_text.lstrip("0x")) # Search usually doesn't want "0x"

        if action_taken:
            self.status_bar.config(text=f"Offset '{offset_text}' set in relevant fields.")
        else:
            self.status_bar.config(text="No relevant offset fields found to populate.")
        self._update_undo_redo_status()

    def _bind_shortcuts(self):
        self.root.bind_all("<Control-o>", lambda e: self.load_file())
        self.root.bind_all("<Control-s>", lambda e: self.save_file_as())
        self.root.bind_all("<Control-q>", lambda e: self.root.quit())
        self.root.bind_all("<Control-z>", lambda e: self.undo())
        self.root.bind_all("<Control-y>", lambda e: self.redo())
        self.root.bind_all("<Control-c>", lambda e: self.copy_selection())
        self.root.bind_all("<Control-x>", lambda e: self.cut_selection())
        self.root.bind_all("<Control-v>", lambda e: self.paste_at_offset())

        self.root.bind_all("<Control-t>", lambda e: self.hex_table.goto_offset_and_display(0) if self.hex_table.file_data else None)
        self.root.bind_all("<Control-p>", lambda e: self.hex_table.scroll_pages(-1) if self.hex_table.file_data else None)
        self.root.bind_all("<Control-n>", lambda e: self.hex_table.scroll_pages(1) if self.hex_table.file_data else None)
        self.root.bind_all("<Control-e>", lambda e: self._goto_end_of_file() if self.hex_table.file_data else None)
        self.root.bind_all("<Control-l>", lambda e: self.goto_line_entry_widget.focus_set() if hasattr(self, 'goto_line_entry_widget') else None)

        self.root.bind_all("<Control-a>", lambda e: self.hex_table._select_all() if self.hex_table.file_data else None)

        self.root.bind_all("<Control-f>", lambda e: self.search_entry_widget.focus_set() if hasattr(self, 'search_entry_widget') else None)
        self.root.bind_all("<Control-g>", lambda e: self.goto_entry_widget.focus_set() if hasattr(self, 'goto_entry_widget') else None)

        # Search navigation shortcuts
        self.root.bind_all("<F3>", lambda e: self.search_next() if self.search_matches else None)
        self.root.bind_all("<Shift-F3>", lambda e: self.search_prev() if self.search_matches else None) # F2 might be used by OS/WM

        # Allow focusing the hex table itself for keyboard navigation
        self.hex_table.focus_set() # Initial focus
        self.root.bind_all("<Escape>", lambda e: self.hex_table.focus_set() if self.hex_table else None) # Focus table on Escape

        # self.status_bar.config(text="Keyboard shortcuts enabled.") # Initial status is "Ready"
        # self._update_undo_redo_status() # Called by init


if __name__ == "__main__":
    root = tk.Tk()
    # Ensure constants are defined before HexTable is instantiated if they are used in its __init__
    # Example: ROW_H, CELL_W, etc. are used for geometry.
    app = HexEditorApp(root)
    root.mainloop()

