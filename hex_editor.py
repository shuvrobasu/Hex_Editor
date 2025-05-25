import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import os
import struct
import hashlib
import datetime
import json

# --- THEME COLOR DEFINITIONS ---

# Light Theme Colors
LIGHT_THEME_COLORS = {
    "BG": "#f0f0f0",  # Main canvas background
    "FG": "#333333",  # General text foreground
    "PANEL_BG": "#e9e9e9",  # Side panel background
    "PANEL_FG": "#1a1a1a",  # Panel titles
    "STATUS_BG": "#d0d0d0",  # Status bar background
    "STATUS_FG": "#000000",  # Status bar foreground
    "OFFSET_BG": "#e0e0e0",  # Offset column background
    "OFFSET_COLOR": "#007bff",  # Offset text (blue)
    "HEX_CELL_EVEN_BG": "#fcfcfc",  # Hex cell background (even)
    "HEX_CELL_ODD_BG": "#f5f5f5",  # Hex cell background (odd)
    "HEX_CELL_OUTLINE": "#cccccc",  # Cell borders
    "HEX_VALUE_COLOR": "#222222",  # Hex value text
    "ASCII_BG": "#f0f0f0",  # ASCII column background
    "ACCENT": "#28a745",  # ASCII character text (green)
    "HEX_SEL_COLOR": "#cceeff",  # Selected cell highlight (light blue)
    "CURSOR_COLOR": "#ffc107",  # Editing cursor/border (orange/gold)
    "EDIT_BG": "#ffffff",  # Entry widget background
    "EDIT_FG": "#000000",  # Entry widget foreground
    "EDIT_CURSOR": "#dc3545",  # Entry widget cursor (red)
    "BUTTON_BG": "#e0e0e0",  # Button background
    "BUTTON_FG": "#333333",  # Button foreground
    "BUTTON_ACTIVE_BG": "#d5d5d5",  # Button active background
    "RANGE_SEL_COLOR": "#99ccff"  # Background for selected range
}

# PythonPlus Theme Colors (Renamed from Blue Theme)
PYTHONPLUS_THEME_COLORS = {
    "BG": "#0d1b2a",
    "FG": "#e0e0e0",
    "PANEL_BG": "#1b263b",
    "PANEL_FG": "#e0e0e0",
    "STATUS_BG": "#0d1b2a",
    "STATUS_FG": "#ffffff",
    "OFFSET_BG": "#2e4a6a",
    "OFFSET_COLOR": "#7aa0ff",
    "HEX_CELL_EVEN_BG": "#233857",
    "HEX_CELL_ODD_BG": "#2a4266",
    "HEX_CELL_OUTLINE": "#4a6c9c",
    "HEX_VALUE_COLOR": "#ffffff",
    "ASCII_BG": "#0d1b2a",
    "ACCENT": "#4dd2ff",
    "HEX_SEL_COLOR": "#6aa2ff",
    "CURSOR_COLOR": "#ffdb58",
    "EDIT_BG": "#3e527d",
    "EDIT_FG": "#ffffff",
    "EDIT_CURSOR": "#00ff00",
    "BUTTON_BG": "#2e4a6a",
    "BUTTON_FG": "#e0e0e0",
    "BUTTON_ACTIVE_BG": "#3f5d88",
    "RANGE_SEL_COLOR": "#5588ff"
}

# DarkAmber1 Theme Colors (New)
DARKAMBER1_THEME_COLORS = {
    "BG": "#2b2b2b",  # Dark grey background
    "FG": "#f0f0f0",  # Light text
    "PANEL_BG": "#3c3c3c",  # Slightly lighter panel
    "PANEL_FG": "#f0f0f0",
    "STATUS_BG": "#2b2b2b",
    "STATUS_FG": "#f0f0f0",
    "OFFSET_BG": "#4a4a4a",  # Offset column
    "OFFSET_COLOR": "#ffcc00",  # Amber/gold offset
    "HEX_CELL_EVEN_BG": "#333333",  # Darker hex cells
    "HEX_CELL_ODD_BG": "#3a3a3a",  # Lighter hex cells
    "HEX_CELL_OUTLINE": "#555555",  # Grey outline
    "HEX_VALUE_COLOR": "#e0e0e0",  # White hex values
    "ASCII_BG": "#2b2b2b",
    "ACCENT": "#ffa500",  # Orange ASCII
    "HEX_SEL_COLOR": "#888800",  # Darker yellow selection
    "CURSOR_COLOR": "#ffff00",  # Bright yellow cursor
    "EDIT_BG": "#4a4a4a",
    "EDIT_FG": "#f0f0f0",
    "EDIT_CURSOR": "#00ff00",
    "BUTTON_BG": "#4a4a4a",
    "BUTTON_FG": "#f0f0f0",
    "BUTTON_ACTIVE_BG": "#5c5c5c",
    "RANGE_SEL_COLOR": "#ccaa00"  # Amber range highlight
}

# Colorful Theme (BrightColors - Similar to PySimpleGUI's theme ideas)
COLORFUL_THEME_COLORS = {
    "BG": "#1f2a36",  # Dark blue-grey for main canvas
    "FG": "#e0e0e0",  # Light text
    "PANEL_BG": "#2a394a",  # Slightly lighter panel
    "PANEL_FG": "#ffffff",  # Bright white
    "STATUS_BG": "#1f2a36",
    "STATUS_FG": "#ffffff",
    "OFFSET_BG": "#3c506e",  # Medium blue
    "OFFSET_COLOR": "#ff5733",  # Bright red-orange offset
    "HEX_CELL_EVEN_BG": "#314258",  # Darker hex cells
    "HEX_CELL_ODD_BG": "#3a4c62",  # Lighter hex cells
    "HEX_CELL_OUTLINE": "#556f8f",  # Blue outline
    "HEX_VALUE_COLOR": "#e0e0e0",
    "ASCII_BG": "#1f2a36",
    "ACCENT": "#33ff57",  # Neon green ASCII
    "HEX_SEL_COLOR": "#66b3ff",  # Sky blue selection
    "CURSOR_COLOR": "#00ffff",  # Cyan cursor
    "EDIT_BG": "#4a6385",
    "EDIT_FG": "#ffffff",
    "EDIT_CURSOR": "#ff00ff",  # Magenta cursor
    "BUTTON_BG": "#3c506e",
    "BUTTON_FG": "#e0e0e0",
    "BUTTON_ACTIVE_BG": "#4a6385",
    "RANGE_SEL_COLOR": "#a279f5"  # Purple range highlight
}

# --- GLOBAL CONSTANTS (Independent of Theme) ---
BYTES_PER_ROW = 16
ASCII_FONT = ("Consolas", 11)  # Kept Consolas for ASCII
HEX_FONT = ("Terminal", 11)  # Changed Hex Font to Terminal
ROW_H = 22
CELL_W = 34
ASCII_W = 15

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
        self.match_length = 1  #


        self.header_height = ROW_H
        self.visible_data_rows = 0
        self.current_display_offset = 0

        self.colors = LIGHT_THEME_COLORS

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

        self._redraw()

    def _on_canvas_configure(self):
        """Handle canvas resize event to update visible rows."""
        new_height = self.winfo_height()
        if new_height > self.header_height:
            new_visible_rows = (new_height - self.header_height) // ROW_H
            if new_visible_rows != self.visible_data_rows:
                self.visible_data_rows = new_visible_rows
                self._redraw()
                self.app_instance.current_offset_display_label.config(
                    text=f"Offset: 0x{self.current_display_offset:08X} ({self.current_display_offset} dec)")
                self.app_instance.root.event_generate("<<HexScroll>>")

    def apply_theme(self, colors):
        self.colors = colors
        self.config(bg=self.colors["BG"])
        self._redraw()

    def load_file(self, data):
        self.file_data = bytearray(data)
        self.total_rows = (len(data) + BYTES_PER_ROW - 1) // BYTES_PER_ROW
        if len(data) == 0:
            self.total_rows = 0
        self.selected = None
        self.selection_start_offset = None
        self.selection_end_offset = None
        self.editing = False
        self.current_display_offset = 0

        self.after_idle(self._on_canvas_configure)

    def goto_offset_and_display(self, target_offset):
        if not self.file_data:
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            return

        target_offset = max(0, min(len(self.file_data) - 1, target_offset))
        target_row_logical = target_offset // BYTES_PER_ROW

        if self.total_rows <= self.visible_data_rows:
            self.current_display_offset = 0
        else:
            top_row_for_centering = max(0, target_row_logical - (self.visible_data_rows // 2))
            max_top_row = max(0, self.total_rows - self.visible_data_rows)
            final_top_row_to_display = min(max_top_row, top_row_for_centering)
            self.current_display_offset = final_top_row_to_display * BYTES_PER_ROW

        self.selected = (target_row_logical, target_offset % BYTES_PER_ROW, "hex")
        self.selection_start_offset = None
        self.selection_end_offset = None
        self._redraw()
        self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{target_offset:08X} ({target_offset} dec)")
        self.app_instance.root.event_generate("<<HexSelection>>")

    def scroll_pages(self, direction):
        if not self.file_data: return

        page_size_bytes = self.visible_data_rows * BYTES_PER_ROW
        new_offset = self.current_display_offset + (direction * page_size_bytes)
        last_possible_page_start_offset = max(0, (self.total_rows - self.visible_data_rows) * BYTES_PER_ROW)
        self.current_display_offset = max(0, min(new_offset, last_possible_page_start_offset))
        self._redraw()
        self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{self.current_display_offset:08X} ({self.current_display_offset} dec)")
        self.app_instance.root.event_generate("<<HexScroll>>")

    def _on_mousewheel(self, event):
        if not self.file_data: return

        lines_to_scroll = 3
        if event.delta:
            delta_lines = -int(event.delta / 120) * lines_to_scroll
        else:
            delta_lines = -lines_to_scroll if event.num == 4 else lines_to_scroll

        delta_bytes = delta_lines * BYTES_PER_ROW
        new_offset = self.current_display_offset + delta_bytes
        last_possible_start_offset = max(0, (self.total_rows - self.visible_data_rows) * BYTES_PER_ROW)
        self.current_display_offset = max(0, min(new_offset, last_possible_start_offset))
        self._redraw()
        self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{self.current_display_offset:08X} ({self.current_display_offset} dec)")
        self.app_instance.root.event_generate("<<HexScroll>>")

    def _on_key_press(self, event):
        if self.editing:
            return

        handled = False
        if event.keysym == "PageUp":
            self.scroll_pages(-1)
            handled = True
        elif event.keysym == "PageDown":
            self.scroll_pages(1)
            handled = True
        elif event.keysym == "Up":
            new_offset = self.current_display_offset - BYTES_PER_ROW
            self.current_display_offset = max(0, new_offset)
            self._redraw()
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{self.current_display_offset:08X} ({self.current_display_offset} dec)")
            handled = True
        elif event.keysym == "Down":
            new_offset = self.current_display_offset + BYTES_PER_ROW
            max_offset_to_display = max(0, (self.total_rows - self.visible_data_rows) * BYTES_PER_ROW)
            self.current_display_offset = min(max_offset_to_display, new_offset)
            self._redraw()
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{self.current_display_offset:08X} ({self.current_display_offset} dec)")
            handled = True
        elif event.keysym == "Left":
            if self.selected:
                row, col, kind = self.selected
                new_col = col - 1
                new_row = row
                if new_col < 0:
                    new_row -= 1
                    new_col = BYTES_PER_ROW - 1
                if new_row >= 0:
                    self.selected = (new_row, new_col, kind)
                    self._ensure_selection_visible()
                else:
                    if self.file_data: self.selected = (0, 0, kind)
            elif self.file_data:
                self.selected = (0, 0, "hex")
            handled = True
        elif event.keysym == "Right":
            if self.selected:
                row, col, kind = self.selected
                new_col = col + 1
                new_row = row
                if new_col >= BYTES_PER_ROW:
                    new_row += 1
                    new_col = 0
                if new_row < self.total_rows:
                    self.selected = (new_row, new_col, kind)
                    self._ensure_selection_visible()
                else:
                    if self.file_data: self.selected = (
                    self.total_rows - 1, (len(self.file_data) - 1) % BYTES_PER_ROW, kind)
            elif self.file_data:
                self.selected = (0, 0, "hex")
            handled = True
        elif event.keysym == "Home":
            if self.selected:
                self.selected = (self.selected[0], 0, self.selected[2])
                self._ensure_selection_visible()
            elif self.file_data:
                self.selected = (0, 0, "hex")
            handled = True
        elif event.keysym == "End":
            if self.selected:
                target_col = BYTES_PER_ROW - 1
                if (self.selected[0] * BYTES_PER_ROW + target_col) >= len(self.file_data) and len(self.file_data) > 0:
                    target_col = (len(self.file_data) - 1) % BYTES_PER_ROW
                self.selected = (self.selected[0], target_col, self.selected[2])
                self._ensure_selection_visible()
            elif self.file_data:
                self.selected = (self.total_rows - 1, (len(self.file_data) - 1) % BYTES_PER_ROW, "hex")
            handled = True

        if handled:
            self._redraw()
            self.app_instance.root.event_generate("<<HexSelection>>")
            return "break"

    def _ensure_selection_visible(self):
        if not self.selected or not self.file_data: return

        selected_logical_row = self.selected[0]
        current_top_display_row_logical = self.current_display_offset // BYTES_PER_ROW
        current_bottom_display_row_logical = current_top_display_row_logical + self.visible_data_rows - 1

        if selected_logical_row < current_top_display_row_logical:
            self.current_display_offset = selected_logical_row * BYTES_PER_ROW
            self._redraw()
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{self.current_display_offset:08X} ({self.current_display_offset} dec)")
            self.app_instance.root.event_generate("<<HexScroll>>")
        elif selected_logical_row > current_bottom_display_row_logical:
            self.current_display_offset = max(0, (selected_logical_row - self.visible_data_rows + 1)) * BYTES_PER_ROW
            self._redraw()
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{self.current_display_offset:08X} ({self.current_display_offset} dec)")
            self.app_instance.root.event_generate("<<HexScroll>>")

    def _get_offset_from_event(self, event):
        x, y = event.x, event.y
        y_relative_to_data_start_on_canvas = y - self.header_height

        if y_relative_to_data_start_on_canvas < 0: return None, None

        logical_row_on_page = int(y_relative_to_data_start_on_canvas // ROW_H)
        global_logical_row = (self.current_display_offset // BYTES_PER_ROW) + logical_row_on_page

        if not (0 <= global_logical_row < self.total_rows): return None, None

        x0 = 90
        clicked_kind = None
        target_col = -1

        for col in range(BYTES_PER_ROW):
            if x0 + col * CELL_W <= x < x0 + (col + 1) * CELL_W:
                clicked_kind = "hex"
                target_col = col
                break
        ascii_x0 = x0 + BYTES_PER_ROW * CELL_W + 16
        if clicked_kind is None:
            for col in range(BYTES_PER_ROW):
                if ascii_x0 + col * ASCII_W <= x < ascii_x0 + (col + 1) * ASCII_W:
                    clicked_kind = "ascii"
                    target_col = col
                    break

        if clicked_kind and target_col != -1:
            clicked_byte_offset = (global_logical_row * BYTES_PER_ROW + target_col)
            if clicked_byte_offset < len(self.file_data):
                return clicked_byte_offset, clicked_kind

        return None, None

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
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{clicked_offset:08X} ({clicked_offset} dec)")
            self.app_instance.root.event_generate("<<HexSelection>>")
        else:
            self._select_none()

    def _on_mouse_drag(self, event):
        if self._drag_start_offset is None or not self.file_data:
            return

        current_offset_under_mouse, _ = self._get_offset_from_event(event)

        if current_offset_under_mouse is not None:
            self.selection_start_offset = min(self._drag_start_offset, current_offset_under_mouse)
            self.selection_end_offset = max(self._drag_start_offset, current_offset_under_mouse)
            self.selected = (
                current_offset_under_mouse // BYTES_PER_ROW, current_offset_under_mouse % BYTES_PER_ROW, 'hex')
            self._redraw()
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{current_offset_under_mouse:08X} ({current_offset_under_mouse} dec)")
        else:
            pass

    def _on_mouse_up(self, event):
        self._drag_start_offset = None
        self.app_instance.root.event_generate("<<HexSelection>>")

    def _on_double_click(self, event):
        if self.editing:
            self._close_edit(save=True)

        clicked_offset, clicked_kind = self._get_offset_from_event(event)

        if clicked_offset is not None:
            self.selected = (clicked_offset // BYTES_PER_ROW, clicked_offset % BYTES_PER_ROW, clicked_kind)
            self.selection_start_offset = clicked_offset
            self.selection_end_offset = clicked_offset
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{clicked_offset:08X} ({clicked_offset} dec)")
            self._start_edit(self.selected[0], self.selected[1], self.selected[2])
            return

    def _on_right_click(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        clicked_offset, clicked_kind = self._get_offset_from_event(event)
        is_click_within_current_range = False
        if self.selection_start_offset is not None and self.selection_end_offset is not None and clicked_offset is not None:
            if self.selection_start_offset <= clicked_offset <= self.selection_end_offset:
                is_click_within_current_range = True

        if clicked_offset is not None:
            self.selected = (clicked_offset // BYTES_PER_ROW, clicked_offset % BYTES_PER_ROW, "hex")
            if not is_click_within_current_range:
                self.selection_start_offset = clicked_offset
                self.selection_end_offset = clicked_offset
            self._redraw()
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{clicked_offset:08X} ({clicked_offset} dec)")
        else:
            self._select_none()

        is_data_loaded = bool(self.file_data)
        is_selected_range = (self.selection_start_offset is not None and self.selection_end_offset is not None)

        context_menu.add_command(label="Select All", command=self._select_all,
                                 state=tk.NORMAL if is_data_loaded else tk.DISABLED)
        context_menu.add_command(label="Select None", command=self._select_none,
                                 state=tk.NORMAL if is_selected_range else tk.DISABLED)
        context_menu.add_separator()

        insert_enabled = is_data_loaded and (
                    clicked_offset is not None or (len(self.file_data) == 0 and clicked_offset is None))
        insert_target_offset = clicked_offset
        if insert_target_offset is None and len(self.file_data) == 0:
            insert_target_offset = 0
        elif insert_target_offset is None:
            insert_target_offset = len(self.file_data)

        context_menu.add_command(label="Insert bytes here...", command=lambda: self._insert_bytes(insert_target_offset),
                                 state=tk.NORMAL if is_data_loaded else tk.DISABLED)

        delete_enabled = is_selected_range
        context_menu.add_command(label="Delete selected bytes", command=self._delete_selected_bytes,
                                 state=tk.NORMAL if delete_enabled else tk.DISABLED)
        context_menu.add_command(label="Crop selected bytes", command=self._crop_selected_bytes,
                                 state=tk.NORMAL if delete_enabled else tk.DISABLED)
        context_menu.add_separator()

        export_menu = tk.Menu(context_menu, tearoff=0)
        export_menu.add_command(label="As Text (ASCII)", command=self._export_selected_ascii,
                                state=tk.NORMAL if delete_enabled else tk.DISABLED)
        export_menu.add_command(label="As Binary (Hex)", command=self._export_selected_hex,
                                state=tk.NORMAL if delete_enabled else tk.DISABLED)
        context_menu.add_cascade(label="Export selected bytes", menu=export_menu,
                                 state=tk.NORMAL if delete_enabled else tk.DISABLED)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def _select_all(self):
        if not self.file_data:
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            return
        self.selection_start_offset = 0
        self.selection_end_offset = len(self.file_data) - 1
        self.selected = (0, 0, 'hex') if self.total_rows > 0 else None
        self._redraw()
        self.app_instance.current_offset_display_label.config(text=f"[Offset]: 0x00000000 (0 dec)")
        self.app_instance.root.event_generate("<<HexSelection>>")

    def _select_none(self):
        self.selection_start_offset = None
        self.selection_end_offset = None
        self.selected = None
        self._redraw()
        self.app_instance.current_offset_display_label.config(text="Offset: N/A")
        self.app_instance.root.event_generate("<<HexSelection>>")

    def _insert_bytes(self, insert_offset):
        if not self.file_data and insert_offset != 0:
            messagebox.showinfo("Insert Bytes", "No file loaded. To insert, open a file or start at offset 0.")
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            return

        if insert_offset < 0 or insert_offset > len(self.file_data):
            messagebox.showerror("Error", "Invalid insertion point.")
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            return

        try:
            num_bytes_str = simpledialog.askstring("Insert Bytes", "Number of bytes to insert:",
                                                   parent=self.app_instance.root)
            if num_bytes_str is None: return
            num_bytes = int(num_bytes_str.strip())
            if num_bytes <= 0:
                messagebox.showwarning("Warning", "Number of bytes must be positive.")
                return

            value_str = simpledialog.askstring("Insert Bytes", f"Value for {num_bytes} bytes (e.g., '00' or 'FF'):",
                                               parent=self.app_instance.root)
            if value_str is None: return
            value_str = value_str.strip()

            if not (len(value_str) == 2 and all(c in "0123456789abcdefABCDEF" for c in value_str.lower())):
                messagebox.showerror("Error", "Value must be a 2-digit hex string (e.g., '00', 'FF').")
                return
            fill_byte = int(value_str, 16)

            new_file_data = bytearray()
            new_file_data.extend(self.file_data[:insert_offset])
            new_file_data.extend(bytearray([fill_byte] * num_bytes))
            new_file_data.extend(self.file_data[insert_offset:])

            self.load_file(new_file_data)
            self.goto_offset_and_display(insert_offset)
            self.app_instance.status_bar.config(
                text=f"Inserted {num_bytes} bytes at 0x{insert_offset:08X}.")
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{insert_offset:08X} ({insert_offset} dec)")
        except ValueError:
            messagebox.showerror("Error", "Invalid number of bytes or value.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert bytes: {e}")

    def _delete_selected_bytes(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Delete Bytes", "No bytes selected.")
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            return

        start = self.selection_start_offset
        end = self.selection_end_offset + 1

        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete {end - start} bytes from 0x{start:08X} to 0x{self.selection_end_offset:08X}?"):
            return

        try:
            new_file_data = bytearray()
            new_file_data.extend(self.file_data[:start])
            new_file_data.extend(self.file_data[end:])

            self.load_file(new_file_data)
            new_offset = min(start, len(new_file_data) - 1 if new_file_data else 0)
            self.goto_offset_and_display(new_offset)
            self.app_instance.status_bar.config(
                text=f"Deleted {end - start} bytes from 0x{start:08X}.")
            self.app_instance.current_offset_display_label.config(text=f"Offset: 0x{new_offset:08X} ({new_offset} dec)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete bytes: {e}")
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")

    def _crop_selected_bytes(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Crop Bytes", "No bytes selected.")
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")
            return

        start = self.selection_start_offset
        end = self.selection_end_offset + 1

        if not messagebox.askyesno("Confirm Crop",
                                   f"Crop file to selected {end - start} bytes from 0x{start:08X} to 0x{self.selection_end_offset:08X}?\nThis will delete all *non-selected* bytes."):
            return

        try:
            self.file_data = self.file_data[start:end]
            self.load_file(self.file_data)
            self.goto_offset_and_display(0)
            self.app_instance.status_bar.config(
                text=f"File cropped to {end - start} bytes.")
            self.app_instance.current_offset_display_label.config(text=f"[Offset]: 0x00000000 (0 dec)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to crop bytes: {e}")
            self.app_instance.current_offset_display_label.config(text="Offset: N/A")

    def _export_selected_ascii(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Export", "No bytes selected for export.")
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
        if not path: return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(ascii_text)
            messagebox.showinfo("Export Complete", f"Selected ASCII exported to {os.path.basename(path)}")
            self.app_instance.status_bar.config(
                text=f"Exported {len(selected_bytes)} bytes as ASCII to {os.path.basename(path)}.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export ASCII: {e}")

    def _export_selected_hex(self):
        if self.selection_start_offset is None or self.selection_end_offset is None:
            messagebox.showinfo("Export", "No bytes selected for export.")
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
        if not path: return

        try:
            with open(path, "wb") as f:
                f.write(selected_bytes)
            messagebox.showinfo("Export Complete", f"Selected binary data exported to {os.path.basename(path)}")
            self.app_instance.status_bar.config(
                text=f"Exported {len(selected_bytes)} bytes as binary to {os.path.basename(path)}.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export binary: {e}")

    def _start_edit(self, row, col, kind):
        idx = row * BYTES_PER_ROW + col
        if idx >= len(self.file_data): return

        bbox = self._calculate_drawn_cell_bbox(row, col, kind)
        if not bbox: return

        value = self.file_data[idx]
        text = f"{value:02X}" if kind == "hex" else chr(value) if 32 <= value < 127 else "."

        if self.edit_entry:
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
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["CURSOR_COLOR"],
            highlightcolor=self.colors["CURSOR_COLOR"]
        )
        self.edit_entry.place(x=bbox[0], y=bbox[1], w=bbox[2], h=bbox[3])
        self.edit_entry.insert(0, text)
        self.edit_entry.select_range(0, tk.END)
        self.edit_entry.focus_set()
        self.editing = True
        self.edit_entry.bind("<Return>", lambda e: self._close_edit(save=True))
        self.edit_entry.bind("<Escape>", lambda e: self._close_edit(save=False))
        self.edit_entry.bind("<FocusOut>", lambda e: self._close_edit(save=True), add="+")
        self.after(500, self._blink_cursor)
        self._redraw()

    def _close_edit(self, save):
        if not self.editing: return
        if self.edit_entry is None: return

        if save:
            try:
                val = self.edit_entry.get()
                row, col, kind = self.selected
                idx = row * BYTES_PER_ROW + col
                if idx < len(self.file_data):
                    if kind == "hex":
                        if not (len(val) == 2 and all(c in "0123456789abcdefABCDEF" for c in val.lower())):
                            raise ValueError("Invalid hex format (must be 2 hex digits)")
                        b = int(val, 16)
                    else:
                        if not val:
                            b = ord('.')
                        elif len(val) > 1:
                            b = ord(val[0])
                        else:
                            b = ord(val)
                        if not (32 <= b < 127):
                            b = ord(".")
                    self.file_data[idx] = b
            except Exception:
                pass

        if self.edit_entry:
            self.edit_entry.destroy()
        self.edit_entry = None
        self.editing = False
        self._redraw()
        self.app_instance.root.event_generate("<<HexSelection>>")

    def _blink_cursor(self):
        if not self.editing: return
        self.blink_on = not self.blink_on
        self._redraw()
        self.after(500, self._blink_cursor)

    def _calculate_drawn_cell_bbox(self, global_row, global_col, kind):
        display_start_row_logical = self.current_display_offset // BYTES_PER_ROW
        row_on_page = global_row - display_start_row_logical

        if not (0 <= row_on_page < self.visible_data_rows):
            return None

        y_on_canvas = (row_on_page * ROW_H) + self.header_height

        if kind == "hex":
            x = 90 + global_col * CELL_W
            return (x, y_on_canvas, CELL_W - 2, ROW_H - 4)
        else:
            x = 90 + BYTES_PER_ROW * CELL_W + 16 + global_col * ASCII_W
            return (x, y_on_canvas, ASCII_W, ROW_H - 4)

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        self.create_rectangle(0, 0, w, self.header_height, fill=self.colors["OFFSET_BG"],
                              outline=self.colors["HEX_CELL_OUTLINE"], width=1)
        self.create_text(8, self.header_height // 2, text="Offset", anchor="w", fill=self.colors["OFFSET_COLOR"],
                         font=("Consolas", 10, "bold"))
        for col in range(BYTES_PER_ROW):
            cell_x = 90 + col * CELL_W
            self.create_text(cell_x + CELL_W // 2, self.header_height // 2, text=f"{col:X}",
                             font=("Consolas", 10, "bold"), fill=self.colors["HEX_VALUE_COLOR"])
        ascii_x0 = 90 + BYTES_PER_ROW * CELL_W + 16
        self.create_text(ascii_x0 + BYTES_PER_ROW * ASCII_W // 2, self.header_height // 2, text="ASCII",
                         font=("Consolas", 10, "bold"), fill=self.colors["ACCENT"])

        self.create_line(0, self.header_height - 1, w, self.header_height - 1, fill=self.colors["HEX_CELL_OUTLINE"],
                         width=1)

        start_logical_row_to_display = self.current_display_offset // BYTES_PER_ROW

        for row_on_page_idx in range(self.visible_data_rows):
            global_logical_row = start_logical_row_to_display + row_on_page_idx

            if global_logical_row >= self.total_rows:
                break

            y_on_canvas = (row_on_page_idx * ROW_H) + self.header_height
            data_byte_offset = global_logical_row * BYTES_PER_ROW

            self.create_rectangle(0, y_on_canvas, 90, y_on_canvas + ROW_H, fill=self.colors["OFFSET_BG"],
                                  outline=self.colors["HEX_CELL_OUTLINE"], width=1)
            self.create_text(82, y_on_canvas + ROW_H // 2, text=f"{data_byte_offset:08X}", anchor="e",
                             fill=self.colors["OFFSET_COLOR"], font=HEX_FONT)

            for col_idx in range(BYTES_PER_ROW):
                cell_x = 90 + col_idx * CELL_W
                current_byte_global_idx = data_byte_offset + col_idx
                val = self.file_data[current_byte_global_idx] if current_byte_global_idx < len(self.file_data) else None
                txt = f"{val:02X}" if val is not None else ""

                bg_color_hex = self.colors["HEX_CELL_EVEN_BG"] if (global_logical_row + col_idx) % 2 == 0 else \
                    self.colors["HEX_CELL_ODD_BG"]

                is_in_range = False
                if self.selection_start_offset is not None and self.selection_end_offset is not None:
                    if self.selection_start_offset <= current_byte_global_idx <= self.selection_end_offset:
                        is_in_range = True

                is_selected_hex_single = (self.selected == (global_logical_row, col_idx, "hex"))

                if is_in_range:
                    current_bg_color = self.colors["RANGE_SEL_COLOR"]
                elif is_selected_hex_single and not self.editing:
                    current_bg_color = self.colors["HEX_SEL_COLOR"]
                else:
                    current_bg_color = bg_color_hex

                self.create_rectangle(cell_x, y_on_canvas, cell_x + CELL_W, y_on_canvas + ROW_H, fill=current_bg_color,
                                      outline=self.colors["HEX_CELL_OUTLINE"], width=1)
                self.create_text(cell_x + CELL_W // 2, y_on_canvas + ROW_H // 2, text=txt, font=HEX_FONT,
                                 fill=self.colors["HEX_VALUE_COLOR"])

            ascii_x0 = 90 + BYTES_PER_ROW * CELL_W + 16
            for col_idx in range(BYTES_PER_ROW):
                current_byte_global_idx = data_byte_offset + col_idx
                val = self.file_data[current_byte_global_idx] if current_byte_global_idx < len(self.file_data) else None
                ch = chr(val) if val is not None and 32 <= val < 127 else "."

                bg_color_ascii = self.colors["ASCII_BG"]
                is_in_range = False
                if self.selection_start_offset is not None and self.selection_end_offset is not None:
                    if self.selection_start_offset <= current_byte_global_idx <= self.selection_end_offset:
                        is_in_range = True

                is_selected_ascii_single = (self.selected == (global_logical_row, col_idx, "ascii"))
                is_corresponding_hex_selected_single = (self.selected == (global_logical_row, col_idx, "hex"))

                if is_in_range:
                    current_bg_color = self.colors["RANGE_SEL_COLOR"]
                elif (is_selected_ascii_single or is_corresponding_hex_selected_single) and not self.editing:
                    current_bg_color = self.colors["HEX_SEL_COLOR"]
                else:
                    current_bg_color = bg_color_ascii

                self.create_rectangle(ascii_x0 + col_idx * ASCII_W, y_on_canvas, ascii_x0 + (col_idx + 1) * ASCII_W,
                                      y_on_canvas + ROW_H, fill=current_bg_color,
                                      outline=self.colors["HEX_CELL_OUTLINE"], width=1)
                self.create_text(ascii_x0 + col_idx * ASCII_W + ASCII_W // 2, y_on_canvas + ROW_H // 2, text=ch,
                                 font=ASCII_FONT, fill=self.colors["ACCENT"])

        if self.editing and self.selected and self.blink_on:
            row, col, kind = self.selected
            bbox = self._calculate_drawn_cell_bbox(row, col, kind)
            if bbox:
                self.create_rectangle(bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3],
                                      outline=self.colors["CURSOR_COLOR"], width=2)

        self.create_line(ascii_x0 - 8, self.header_height, ascii_x0 - 8, h, fill=self.colors["HEX_CELL_OUTLINE"],
                         width=2)

class HexEditorApp:
    def __init__(self, root):
        self.root = root
        root.title("« Hex Editor »")
        root.geometry("1400x800")

        self.colors = PYTHONPLUS_THEME_COLORS
        self._set_ttk_style()
        self.root.configure(bg=self.colors["PANEL_BG"])

        self.frame_main = tk.Frame(root, bg=self.colors["PANEL_BG"])
        self.frame_main.pack(fill="both", expand=1)

        self.left_panel = tk.Frame(self.frame_main, width=270, bg=self.colors["PANEL_BG"])
        self.left_panel.pack(side="left", fill="y", padx=5, pady=5)
        self._build_side_panel()

        self.hex_view_container = tk.Frame(self.frame_main, bg=self.colors["PANEL_BG"])
        self.hex_view_container.pack(side="left", fill="both", expand=1, padx=5, pady=5)

        self.hex_table = HexTable(self.hex_view_container, self)
        self.hex_table.pack(side="top", fill="both", expand=1)
        self.hex_table.apply_theme(self.colors)

        self.page_nav_frame = ttk.Frame(self.hex_view_container, style="TFrame")
        self.page_nav_frame.pack(side="bottom", fill="x", pady=(2, 0))

        ttk.Button(self.page_nav_frame, text="<< Top of File",
                   command=lambda: self.hex_table.goto_offset_and_display(0)).pack(side="left", padx=2)
        ttk.Button(self.page_nav_frame, text="< Previous Page", command=lambda: self.hex_table.scroll_pages(-1)).pack(
            side="left", expand=True, padx=2)
        ttk.Button(self.page_nav_frame, text="Next Page >", command=lambda: self.hex_table.scroll_pages(1)).pack(
            side="right", expand=True, padx=2)
        ttk.Button(self.page_nav_frame, text="End of File >>", command=self._goto_end_of_file).pack(side="right",
                                                                                                    padx=2)
        self.current_offset_display_label = ttk.Label(self.page_nav_frame, text="Offset: N/A",
                                                      background=self.colors["PANEL_BG"],
                                                      foreground=self.colors["FG"], font=("Arial", 9))
        self.current_offset_display_label.pack(side="left", padx=10)

        self.status_bar = tk.Label(root, text="Ready", anchor="w", font=("Arial", 9))
        self.status_bar.pack(side="bottom", fill="x", ipady=2)
        self.status_bar.config(bg=self.colors["STATUS_BG"], fg=self.colors["STATUS_FG"])

        menubar = tk.Menu(root)
        fmenu = tk.Menu(menubar, tearoff=0)
        fmenu.add_command(label="Open...", command=self.load_file)
        fmenu.add_separator()
        fmenu.add_command(label="Save As...", command=self.save_file_as)
        fmenu.add_separator()
        fmenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=fmenu)

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
        util_menu.add_command(label="Load Config", command=self.load_config)
        util_menu.add_separator()  # Add separator before ASCII table
        util_menu.add_command(label="Show ASCII Table", command=self.show_ascii_table)  # Add ASCII table option
        menubar.add_cascade(label="Util", menu=util_menu)

        root.config(menu=menubar)

        self.file_path = None
        self.file_size = 0
        self.search_matches = []
        self.current_match_idx = -1

        self._apply_menu_theme(menubar)

        self.hex_table.bind("<<HexSelection>>", self._on_hex_table_selection)
        self.hex_table.bind("<<HexScroll>>", self._on_hex_table_scroll)
        # Removed automatic binding to <<HexSelection>> for show_ascii_table to avoid redundancy with menu option

    def _set_ttk_style(self):
        s = ttk.Style()
        s.theme_use('clam')

        s.configure("TFrame", background=self.colors["PANEL_BG"])
        s.configure("TLabel", background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        s.configure("TLabelframe", background=self.colors["PANEL_BG"], foreground=self.colors["PANEL_FG"],
                    font=("Arial", 9, "bold"), bordercolor=self.colors["HEX_CELL_OUTLINE"], relief="flat")
        s.configure("TLabelframe.Label", background=self.colors["PANEL_BG"], foreground=self.colors["PANEL_FG"],
                    font=("Arial", 9, "bold"))

        s.configure("TCombobox",
                    fieldbackground=self.colors["EDIT_BG"],
                    background=self.colors["BUTTON_BG"],
                    foreground=self.colors["FG"],
                    selectbackground=self.colors["BUTTON_ACTIVE_BG"],
                    selectforeground=self.colors["FG"],
                    bordercolor=self.colors["HEX_CELL_OUTLINE"],
                    arrowcolor=self.colors["FG"],
                    relief="flat"
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
                    relief="flat",
                    font=("Arial", 9, "bold"),
                    bordercolor=self.colors["HEX_CELL_OUTLINE"],
                    focusthickness=1,
                    focuscolor=self.colors["CURSOR_COLOR"]
                    )
        s.map("TButton",
              background=[("active", self.colors["BUTTON_ACTIVE_BG"])],
              foreground=[("active", self.colors["FG"])])

    def _apply_theme(self, new_colors):
        self.colors = new_colors
        self.root.config(bg=self.colors["PANEL_BG"])

        self.frame_main.config(bg=self.colors["PANEL_BG"])
        self.left_panel.config(bg=self.colors["PANEL_BG"])
        self.hex_view_container.config(bg=self.colors["PANEL_BG"])
        self.status_bar.config(bg=self.colors["STATUS_BG"], fg=self.colors["STATUS_FG"])
        self._set_ttk_style()
        self.hex_table.apply_theme(self.colors)

        # Update inspector labels (values)
        for label_dict in [self.inspector_labels]:
            for label in label_dict.values():
                label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])

        # Update the static labels in the Data Inspector (e.g., "8-bit Integer:", etc.)
        for child in self.inspector_frame.winfo_children():
            if isinstance(child, ttk.Label) and child in self.inspector_static_labels.values():
                child.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])

        self.file_path_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.file_size_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.created_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.modified_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.file_type_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.md5_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.current_addr_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["OFFSET_COLOR"])
        self.match_count_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.current_offset_display_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])
        self.last_replaced_offset_label.config(background=self.colors["PANEL_BG"], foreground=self.colors["FG"])

        self.goto_entry_widget.config(
            bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
            highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"]
        )
        self.search_entry_widget.config(
            bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
            highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"]
        )
        self.replace_entry_widget.config(
            bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
            highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"]
        )
        self.offset_entry_widget.config(
            bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
            highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"]
        )
        self.offset_repl_entry_widget.config(
            bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"], insertbackground=self.colors["EDIT_CURSOR"],
            highlightbackground=self.colors["HEX_CELL_OUTLINE"], highlightcolor=self.colors["CURSOR_COLOR"]
        )

        self._apply_menu_theme(self.root.nametowidget(self.root.cget("menu")))

    def _apply_menu_theme(self, menu_widget):
        menu_widget.config(
            bg=self.colors["PANEL_BG"],
            fg=self.colors["PANEL_FG"],
            activebackground=self.colors["BUTTON_ACTIVE_BG"],
            activeforeground=self.colors["FG"]
        )
        for i in range(menu_widget.index('end') + 1):
            if menu_widget.type(i) == 'cascade':
                submenu_name = menu_widget.entrycget(i, "menu")
                if submenu_name:
                    submenu = self.root.nametowidget(submenu_name)
                    self._apply_menu_theme(submenu)

    def _goto_end_of_file(self):
        if self.file_size > 0:
            self.hex_table.goto_offset_and_display(self.file_size - 1)
        else:
            self.hex_table.goto_offset_and_display(0)

    def _on_hex_table_selection(self, event):
        if self.hex_table.selected:
            row, col, _ = self.hex_table.selected
            offset = row * BYTES_PER_ROW + col
            self.current_addr_label.config(text=f"0x{offset:08X}")
            self.current_offset_display_label.config(text=f"Offset: 0x{offset:08X} ({offset} dec)")
            self.update_inspector(offset)
            self._update_status_bar_info(offset)
        else:
            self.current_addr_label.config(text="0x00000000")
            self.current_offset_display_label.config(text="Offset: N/A")
            self.update_inspector(0)
            self._update_status_bar_info(0)

    def _on_hex_table_scroll(self, event):
        offset = self.hex_table.current_display_offset
        self.current_addr_label.config(text=f"0x{offset:08X}")
        self.current_offset_display_label.config(text=f"Offset: 0x{offset:08X} ({offset} dec)")
        self.update_inspector(offset)
        self._update_status_bar_info(offset)

    def _update_status_bar_info(self, offset):
        if not self.hex_table.file_data:
            self.status_bar.config(text="Ready")
            self.current_offset_display_label.config(text="Offset: N/A")
            return

        offset = max(0, min(offset, len(self.hex_table.file_data) - 1))

        if len(self.hex_table.file_data) > 0:
            byte_at_offset = self.hex_table.file_data[offset]
            ascii_char = chr(byte_at_offset) if 32 <= byte_at_offset < 127 else '.'
            self.status_bar.config(text=f"Offset: 0x{offset:08X} | ASCII: '{ascii_char}'")
            self.current_offset_display_label.config(text=f"Offset: 0x{offset:08X} ({offset} dec)")
        else:
            self.status_bar.config(text="Offset: 0x00000000 | ASCII: '.' (Empty File)")
            self.current_offset_display_label.config(text="Offset: N/A")

    def _build_side_panel(self):
        panel = self.left_panel

        self.inspector_frame = ttk.LabelFrame(panel, text="════█ Data Inspector (Little-endian) █════",
                                              style="TLabelframe")
        self.inspector_frame.pack(fill="x", padx=3, pady=5)

        self.inspector_frame.columnconfigure(0, weight=1)
        self.inspector_frame.columnconfigure(1, weight=1)

        self.inspector_labels = {}
        self.inspector_static_labels = {}
        for t, y in zip(
                ["8-bit Integer", "16-bit Integer", "32-bit Integer", "64-bit Integer", "16-bit Float", "32-bit Float",
                 "64-bit Float"],
                range(7)
        ):
            static_label = ttk.Label(self.inspector_frame, text=f"{t}:", background=self.colors["PANEL_BG"],
                                     foreground=self.colors["FG"], anchor="w", font=("Arial", 8))
            static_label.grid(row=y, column=0, sticky="w", padx=2, pady=1)
            self.inspector_static_labels[t] = static_label

            value_label = ttk.Label(self.inspector_frame, text="N/A", background=self.colors["PANEL_BG"],
                                    foreground=self.colors["FG"], anchor="w", font=("Arial", 8))
            value_label.grid(row=y, column=1, sticky="w", padx=2, pady=1)
            self.inspector_labels[t] = value_label

        finf = ttk.LabelFrame(panel, text="════█ File Info █══════════════════", style="TLabelframe")
        finf.pack(fill="x", padx=3, pady=5)

        self.file_path_label = ttk.Label(finf, text="Filename?", background=self.colors["PANEL_BG"],
                                         foreground=self.colors["FG"], wraplength=220, anchor="w")
        self.file_path_label.pack(fill="x", padx=2, pady=1)
        self.file_size_label = ttk.Label(finf, text="File Size?", background=self.colors["PANEL_BG"],
                                         foreground=self.colors["FG"], anchor="w")
        self.file_size_label.pack(fill="x", padx=2, pady=1)
        self.created_label = ttk.Label(finf, text="Created?", background=self.colors["PANEL_BG"],
                                       foreground=self.colors["FG"], anchor="w")
        self.created_label.pack(fill="x", padx=2, pady=1)
        self.modified_label = ttk.Label(finf, text="Modified?", background=self.colors["PANEL_BG"],
                                        foreground=self.colors["FG"], anchor="w")
        self.modified_label.pack(fill="x", padx=2, pady=1)
        self.file_type_label = ttk.Label(finf, text="File Type?", background=self.colors["PANEL_BG"],
                                         foreground=self.colors["FG"], anchor="w")
        self.file_type_label.pack(fill="x", padx=2, pady=1)
        self.md5_label = ttk.Label(finf, text="MD5 Hash?", background=self.colors["PANEL_BG"],
                                   foreground=self.colors["FG"],
                                   anchor="w")
        self.md5_label.pack(fill="x", padx=2, pady=1)

        goto = ttk.LabelFrame(panel, text="════█ Go To █════════════════════", style="TLabelframe")
        goto.pack(fill="x", padx=3, pady=5)
        self.current_addr_label = ttk.Label(goto, background=self.colors["PANEL_BG"],
                                            foreground=self.colors["OFFSET_COLOR"], font=("Consolas", 10, "bold"))
        # self.current_addr_label.pack(fill="x", padx=2, pady=1)

        self.last_replaced_offset_label = ttk.Label(goto, text="Last Replaced: N/A", background=self.colors["PANEL_BG"],
                                                    foreground=self.colors["FG"], font=("Arial", 8))
        self.last_replaced_offset_label.pack(fill="x", padx=2, pady=1)

        fr = ttk.Frame(goto, style="TFrame")
        fr.pack(fill="x", padx=2, pady=2)

        self.goto_var = tk.StringVar(value="0")
        self.goto_entry_widget = tk.Entry(fr, textvariable=self.goto_var, width=12,
                                          bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"],
                                          insertbackground=self.colors["EDIT_CURSOR"],
                                          relief="flat", highlightthickness=1,
                                          highlightbackground=self.colors["HEX_CELL_OUTLINE"],
                                          highlightcolor=self.colors["CURSOR_COLOR"])
        self.goto_entry_widget.pack(side="left", padx=2)
        ToolTip(self.goto_entry_widget, "Enter hexadecimal offset (e.g., 0x100) or decimal (e.g., 256) to jump to.")

        self.goto_button = ttk.Button(fr, text="Go", command=self.goto_offset, state="disabled")
        self.goto_button.pack(side="left", padx=2)

        srep = ttk.LabelFrame(panel, text="════█ Search & Replace █════════════", style="TLabelframe")
        srep.pack(fill="x", padx=3, pady=5)

        self.search_type = tk.StringVar(value="Hex")
        ttk.Combobox(srep, textvariable=self.search_type, values=["Hex", "ASCII"], width=8, state="readonly",
                     style="TCombobox").pack(fill="x", padx=2, pady=2)

        self.search_var = tk.StringVar()
        self.search_entry_widget = tk.Entry(srep, textvariable=self.search_var,
                                            bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"],
                                            insertbackground=self.colors["EDIT_CURSOR"],
                                            relief="flat", highlightthickness=1,
                                            highlightbackground=self.colors["HEX_CELL_OUTLINE"],
                                            highlightcolor=self.colors["CURSOR_COLOR"])
        self.search_entry_widget.pack(fill="x", padx=2, pady=2)
        ToolTip(self.search_entry_widget, "Enter hex bytes (e.g., '0A B2') or ASCII text to search for.")

        self.replace_var = tk.StringVar()
        self.replace_entry_widget = tk.Entry(srep, textvariable=self.replace_var,
                                             bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"],
                                             insertbackground=self.colors["EDIT_CURSOR"],
                                             relief="flat", highlightthickness=1,
                                             highlightbackground=self.colors["HEX_CELL_OUTLINE"],
                                             highlightcolor=self.colors["CURSOR_COLOR"])
        self.replace_entry_widget.pack(fill="x", padx=2, pady=2)
        ToolTip(self.replace_entry_widget,
                "Enter hex bytes or ASCII text to replace with (must be same length as search).")

        fr2 = ttk.Frame(srep, style="TFrame")
        fr2.pack(fill="x", expand=True)
        self.search_button = ttk.Button(fr2, text="Search", command=self.search_bytes, state="disabled")
        self.search_button.pack(side="left", expand=True, fill="x", padx=2)
        self.search_replace_button = ttk.Button(fr2, text="Search & Replace", command=self.search_and_replace,
                                                state="disabled")
        self.search_replace_button.pack(side="left", expand=True, fill="x", padx=2)

        fr3 = ttk.Frame(srep, style="TFrame")
        fr3.pack(fill="x", pady=2, expand=True)
        ttk.Button(fr3, text="<", width=3, command=self.search_prev).pack(side="left", padx=2)
        ttk.Button(fr3, text=">", width=3, command=self.search_next).pack(side="left", padx=2)
        self.match_count_label = ttk.Label(fr3, text="Matches: 0/0", background=self.colors["PANEL_BG"],
                                           foreground=self.colors["FG"])
        self.match_count_label.pack(side="left", padx=2, expand=True, fill="x")

        offrep = ttk.LabelFrame(panel, text="════█ Offset Replace █═════════════", style="TLabelframe")
        offrep.pack(fill="x", padx=3, pady=5)

        self.offset_var = tk.StringVar(value="0")
        self.offset_entry_widget = tk.Entry(offrep, textvariable=self.offset_var,
                                            bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"],
                                            insertbackground=self.colors["EDIT_CURSOR"],
                                            relief="flat", highlightthickness=1,
                                            highlightbackground=self.colors["HEX_CELL_OUTLINE"],
                                            highlightcolor=self.colors["CURSOR_COLOR"])
        self.offset_entry_widget.pack(fill="x", padx=2, pady=2)
        ToolTip(self.offset_entry_widget, "Enter decimal offset (e.g., 1024) for single byte replacement.")

        self.offset_repl_var = tk.StringVar(value="00")
        self.offset_repl_entry_widget = tk.Entry(offrep, textvariable=self.offset_repl_var,
                                                 bg=self.colors["EDIT_BG"], fg=self.colors["EDIT_FG"],
                                                 insertbackground=self.colors["EDIT_CURSOR"],
                                                 relief="flat", highlightthickness=1,
                                                 highlightbackground=self.colors["HEX_CELL_OUTLINE"],
                                                 highlightcolor=self.colors["CURSOR_COLOR"])
        self.offset_repl_entry_widget.pack(fill="x", padx=2, pady=2)
        self.offset_replace_button = ttk.Button(offrep, text="Replace at Offset", command=self.offset_replace,
                                                state="disabled")
        self.offset_replace_button.pack(fill="x", padx=2, pady=2)
        ToolTip(self.offset_repl_entry_widget, "Enter a single byte value (e.g., '65' or '0A').")

    def update_inspector(self, sel_offset):
        fd = self.hex_table.file_data

        for k in self.inspector_labels:
            self.inspector_labels[k].config(text="N/A")

        if not fd or sel_offset >= len(fd):
            return

        offset = sel_offset
        chunk = fd[offset:offset + 8]

        if len(chunk) >= 1:
            try:
                self.inspector_labels["8-bit Integer"].config(text=str(chunk[0]))
            except (struct.error, IndexError):
                pass

        if len(chunk) >= 2:
            try:
                self.inspector_labels["16-bit Integer"].config(text=str(struct.unpack("<H", chunk[:2])[0]))
            except (struct.error, IndexError):
                pass
            try:
                self.inspector_labels["16-bit Float"].config(
                    text=str(struct.unpack('<e', chunk[:2])[0]))
            except (struct.error, IndexError):
                pass

        if len(chunk) >= 4:
            try:
                self.inspector_labels["32-bit Integer"].config(text=str(struct.unpack("<I", chunk[:4])[0]))
            except (struct.error, IndexError):
                pass
            try:
                self.inspector_labels["32-bit Float"].config(
                    text=str(struct.unpack('<f', chunk[:4])[0]))
            except (struct.error, IndexError):
                pass

        if len(chunk) >= 8:
            try:
                self.inspector_labels["64-bit Integer"].config(text=str(struct.unpack("<Q", chunk[:8])[0]))
            except (struct.error, IndexError):
                pass
            try:
                self.inspector_labels["64-bit Float"].config(
                    text=str(struct.unpack('<d', chunk[:8])[0]))
            except (struct.error, IndexError):
                pass

    def load_file(self):
        filetypes = [
            ("EXE Files", "*.exe"),
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Binary Files", "*.bin"),
        ]
        path = filedialog.askopenfilename(title="Open File", filetypes=filetypes, defaultextension=".exe")
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = f.read()

            if not data:
                messagebox.showwarning("Warning", "File is empty.")
                self.hex_table.load_file(b'')
                self.status_bar.config(text=f"Opened empty file: {os.path.basename(path)}")
                self.current_offset_display_label.config(text="Offset: N/A")
                # Disable buttons for empty file
                self.search_button.config(state="disabled")
                self.search_replace_button.config(state="disabled")
                self.offset_replace_button.config(state="disabled")
                self.goto_button.config(state="disabled")  # Disable Go button
                return

            self.hex_table.load_file(data)
            self.file_path = path
            self.file_size = len(data)
            self._update_file_info()
            self.status_bar.config(text=f"Opened {os.path.basename(path)} (Size: {self.file_size} bytes).")
            self.current_offset_display_label.config(text="[Offset]: 0x00000000 (0 dec)")
            if self.hex_table.total_rows > 0:
                self.hex_table.selected = (0, 0, "hex")
                self.hex_table.selection_start_offset = 0
                self.hex_table.selection_end_offset = 0
            else:
                self.hex_table.selected = None
                self.hex_table.selection_start_offset = None
                self.hex_table.selection_end_offset = None
            self.hex_table._redraw()
            self.current_addr_label.config(text="0x00000000")
            self.update_inspector(0)
            # Enable buttons when a file is loaded
            self.search_button.config(state="normal")
            self.search_replace_button.config(state="normal")
            self.offset_replace_button.config(state="normal")
            self.goto_button.config(state="normal")  # Enable Go button
        except MemoryError:
            messagebox.showerror("Error", f"File '{os.path.basename(path)}' is too large to load into memory.")
            self.status_bar.config(text="Failed: File too large.")
            self.current_offset_display_label.config(text="Offset: N/A")
            self.search_button.config(state="disabled")
            self.search_replace_button.config(state="disabled")
            self.offset_replace_button.config(state="disabled")
            self.goto_button.config(state="disabled")  # Disable Go button
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file '{os.path.basename(path)}': {str(e)}")
            self.status_bar.config(text="Failed to load file.")
            self.current_offset_display_label.config(text="Offset: N/A")
            self.search_button.config(state="disabled")
            self.search_replace_button.config(state="disabled")
            self.offset_replace_button.config(state="disabled")
            self.goto_button.config(state="disabled")  # Disable Go button


    def save_file_as(self):
        if not self.file_path and not self.hex_table.file_data:
            messagebox.showinfo("Save As", "No file loaded or data to save.")
            return

        initial_dir = os.path.dirname(self.file_path) if self.file_path else os.getcwd()
        initial_filename = ""
        if self.file_path:
            original_filename = os.path.basename(self.file_path)
            name, ext = os.path.splitext(original_filename)
            initial_filename = f"modified_{name}{ext}"

        filetypes = [
            ("Text Files", "*.txt"),
            ("EXE Files", "*.exe"),
            ("All Files", "*.*"),
            ("Binary Files", "*.bin"),
        ]

        path = filedialog.asksaveasfilename(
            title="Save File As",
            initialdir=initial_dir,
            initialfile=initial_filename,
            filetypes=filetypes,
            defaultextension=".bin"
        )

        if not path:
            return

        try:
            with open(path, "wb") as f:
                f.write(self.hex_table.file_data)
            messagebox.showinfo("Save As", f"File saved successfully to {os.path.basename(path)}")
            self.status_bar.config(text=f"Saved to {os.path.basename(path)}.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {e}")
            self.status_bar.config(text="Failed to save file.")

    def _update_file_info(self):
        fp = self.file_path or "N/A"
        sz = self.file_size
        self.file_path_label.config(text=os.path.basename(fp))
        self.file_size_label.config(text=f"Size: 0x{sz:08X} ({sz} bytes)")

        self.created_label.config(text="N/A")
        self.modified_label.config(text="N/A")

        if os.path.exists(fp):
            try:
                st = os.stat(fp)
                self.created_label.config(
                    text=f"Created: {datetime.datetime.fromtimestamp(st.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
                self.modified_label.config(
                    text=f"Modified: {datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            except Exception:
                pass

        file_type_desc = "Unknown File Type"
        if len(self.hex_table.file_data) >= 2:
            magic_number = self.hex_table.file_data[:2]
            if magic_number == b'MZ':
                file_type_desc = "MS-DOS Executable"
                if len(self.hex_table.file_data) >= 0x40:
                    try:
                        pe_offset = struct.unpack("<I", self.hex_table.file_data[0x3c:0x40])[0]
                        if len(self.hex_table.file_data) >= pe_offset + 4:
                            if self.hex_table.file_data[pe_offset:pe_offset + 4] == b'PE\0\0':
                                file_type_desc = "Windows PE Executable"
                                if len(self.hex_table.file_data) >= pe_offset + 24 + 2:
                                    optional_header_magic = \
                                        struct.unpack("<H",
                                                      self.hex_table.file_data[pe_offset + 24: pe_offset + 24 + 2])[0]
                                    if optional_header_magic == 0x10B:
                                        file_type_desc += " (32-bit)"
                                    elif optional_header_magic == 0x20B:
                                        file_type_desc += " (64-bit)"
                    except (struct.error, IndexError):
                        file_type_desc = "MS-DOS Executable (PE parse error)"
            elif self.hex_table.file_data.startswith(b'\x7fELF'):
                file_type_desc = "ELF Executable (Linux/Unix)"
            elif self.hex_table.file_data.startswith(b'\xfe\xed\xfa\xce') or \
                    self.hex_table.file_data.startswith(b'\xce\xfa\xed\xfe') or \
                    self.hex_table.file_data.startswith(b'\xfe\xed\xfa\xcf') or \
                    self.hex_table.file_data.startswith(b'\xcf\xfa\xed\xfe'):
                file_type_desc = "Mach-O Executable (macOS)"
            elif fp.lower().endswith(".txt"):
                file_type_desc = "Text File"
            elif fp.lower().endswith(".bin"):
                file_type_desc = "Binary File"

        self.file_type_label.config(text=f"Type: {file_type_desc}")

        self.md5_label.config(text="MD5 Hash: Calculating...")
        self.root.update_idletasks()
        try:
            if os.path.exists(fp) and self.file_size < 100 * 1024 * 1024:
                md5 = hashlib.md5()
                with open(fp, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        md5.update(chunk)
                self.md5_label.config(text=f"MD5 Hash: {md5.hexdigest()}")
            elif os.path.exists(fp):
                self.md5_label.config(text="MD5 Hash: Too large for quick calculation")
            else:
                self.md5_label.config(text="MD5 Hash: N/A")
        except Exception:
            self.md5_label.config(text="MD5 Hash: N/A")

    def goto_offset(self):
        try:
            offset_str = self.goto_var.get().strip()
            if not offset_str:
                messagebox.showwarning("Warning", "Please enter an offset.")
                return

            if offset_str.lower().startswith("0x"):
                offset = int(offset_str, 16)
            else:
                offset = int(offset_str)

            if 0 <= offset < len(self.hex_table.file_data):
                self.hex_table.goto_offset_and_display(offset)
                self.current_offset_display_label.config(text=f"Offset: 0x{offset:08X} ({offset} dec)")
            else:
                messagebox.showwarning("Invalid Offset", "Offset is out of file bounds.")
        except ValueError:
            messagebox.showerror("Error", "Invalid offset format. Please use hex (e.g., 0x1A) or decimal.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def search_bytes(self):
        s = self.search_var.get().strip()
        mode = self.search_type.get()
        data = self.hex_table.file_data

        if not s:
            self.search_matches.clear()
            self.current_match_idx = -1
            self._show_search_result()
            self.status_bar.config(text="Search term is empty.")
            return

        try:
            if mode == "Hex":
                s = s.replace(" ", "")
                if len(s) % 2 != 0:
                    messagebox.showerror("Error", "Hex search string must have an even number of characters.")
                    return
                search_bytes = bytes.fromhex(s)
            else:  # ASCII
                search_bytes = s.encode("ascii")

            self.search_matches.clear()
            self.current_match_idx = -1

            for i in range(len(data) - len(search_bytes) + 1):
                if data[i:i + len(search_bytes)] == search_bytes:
                    self.search_matches.append(i)

            if self.search_matches:
                self.current_match_idx = 0
                self._highlight_match()
                self.status_bar.config(text=f"Found {len(self.search_matches)} matches.")
                self.current_offset_display_label.config(
                    text=f"Offset: 0x{self.search_matches[self.current_match_idx]:08X} ({self.search_matches[self.current_match_idx]} dec)")
            else:
                self.status_bar.config(text="No matches found.")
                self.current_offset_display_label.config(text="Offset: N/A")
            self._show_search_result()

        except ValueError:
            messagebox.showerror("Error", "Invalid search format. Use hex (e.g., '0A B2') or ASCII text.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def _highlight_match(self):
        if not self.search_matches or self.current_match_idx < 0:
            self.hex_table.selection_start_offset = None
            self.hex_table.selection_end_offset = None
            self.hex_table._redraw()
            self.current_offset_display_label.config(text="Offset: N/A")
            return

        match_offset = self.search_matches[self.current_match_idx]
        # Use the stored match_length instead of recalculating
        match_length = getattr(self.hex_table, 'match_length', 1)  # Default to 1 if not set

        self.hex_table.selection_start_offset = match_offset
        self.hex_table.selection_end_offset = match_offset + match_length - 1
        self.hex_table.selected = (match_offset // BYTES_PER_ROW, match_offset % BYTES_PER_ROW, "hex")
        self.hex_table.goto_offset_and_display(match_offset)
        self.current_offset_display_label.config(text=f"Offset: 0x{match_offset:08X} ({match_offset} dec)")

    def _show_search_result(self):
        total = len(self.search_matches)
        current = self.current_match_idx + 1 if self.current_match_idx >= 0 else 0
        self.match_count_label.config(text=f"Matches: {current}/{total}")
        if total > 0:
            self.current_offset_display_label.config(
                text=f"Offset: 0x{self.search_matches[self.current_match_idx]:08X} ({self.search_matches[self.current_match_idx]} dec)")
        else:
            self.current_offset_display_label.config(text="Offset: N/A")

    def search_next(self):
        if not self.search_matches:
            self.status_bar.config(text="No matches to navigate.")
            self.current_offset_display_label.config(text="Offset: N/A")
            return

        self.current_match_idx = (self.current_match_idx + 1) % len(self.search_matches)
        self._highlight_match()
        self._show_search_result()
        self.status_bar.config(text=f"Match {self.current_match_idx + 1} of {len(self.search_matches)}.")

    def search_prev(self):
        if not self.search_matches:
            self.status_bar.config(text="No matches to navigate.")
            self.current_offset_display_label.config(text="Offset: N/A")
            return

        self.current_match_idx = (self.current_match_idx - 1) % len(self.search_matches)
        self._highlight_match()
        self._show_search_result()
        self.status_bar.config(text=f"Match {self.current_match_idx + 1} of {len(self.search_matches)}.")

    def search_and_replace(self):
        s = self.search_var.get().strip()
        r = self.replace_var.get().strip()
        mode = self.search_type.get()
        data = self.hex_table.file_data

        if not s or not r:
            messagebox.showwarning("Warning", "Search and replace fields cannot be empty.")
            return

        try:
            if mode == "Hex":
                s = s.replace(" ", "")
                r = r.replace(" ", "")
                if len(s) % 2 != 0 or len(r) % 2 != 0:
                    messagebox.showerror("Error", "Hex strings must have an even number of characters.")
                    return
                search_bytes = bytes.fromhex(s)
                replace_bytes = bytes.fromhex(r)
            else:  # ASCII
                search_bytes = s.encode("ascii")
                replace_bytes = r.encode("ascii")

            if len(search_bytes) != len(replace_bytes):
                messagebox.showerror("Error", "Search and replace patterns must be the same length.")
                return

            self.search_matches.clear()
            self.current_match_idx = -1

            for i in range(len(data) - len(search_bytes) + 1):
                if data[i:i + len(search_bytes)] == search_bytes:
                    self.search_matches.append(i)

            if not self.search_matches:
                self.status_bar.config(text="No matches found for replacement.")
                self._show_search_result()
                self.current_offset_display_label.config(text="Offset: N/A")
                return

            if not messagebox.askyesno("Confirm Replace",
                                       f"Replace {len(self.search_matches)} matches of '{s}' with '{r}'?"):
                return

            new_data = bytearray(data)
            for match_offset in self.search_matches:
                new_data[match_offset:match_offset + len(replace_bytes)] = replace_bytes

            self.hex_table.load_file(new_data)
            self.status_bar.config(text=f"Replaced {len(self.search_matches)} matches.")
            self.current_match_idx = 0
            # Pass the actual byte length to _highlight_match
            self.hex_table.match_length = len(search_bytes)  # Store the byte length
            self._highlight_match()
            self._show_search_result()
            self.current_offset_display_label.config(
                text=f"Offset: 0x{self.search_matches[self.current_match_idx]:08X} ({self.search_matches[self.current_match_idx]} dec)")

        except ValueError:
            messagebox.showerror("Error", "Invalid format in search or replace field.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    import json

    def hex_to_dec(self):
        hex_str = simpledialog.askstring("Hex to Decimal", "Enter hex value (e.g., 1A or 0x1A):", parent=self.root)
        if hex_str:
            try:
                if hex_str.lower().startswith("0x"):
                    hex_str = hex_str[2:]
                dec_value = int(hex_str, 16)
                messagebox.showinfo("Result", f"Hex {hex_str} = Decimal {dec_value}")
            except ValueError:
                messagebox.showerror("Error", "Invalid hex value.")

    def dec_to_hex(self):
        dec_str = simpledialog.askstring("Decimal to Hex", "Enter decimal value (0-255):", parent=self.root)
        if dec_str:
            try:
                dec_value = int(dec_str)
                if 0 <= dec_value <= 255:
                    hex_value = f"{dec_value:02X}"
                    messagebox.showinfo("Result", f"Decimal {dec_value} = Hex 0x{hex_value}")
                else:
                    messagebox.showerror("Error", "Value must be between 0 and 255.")
            except ValueError:
                messagebox.showerror("Error", "Invalid decimal value.")

    def save_config(self):
        config = {
            "file_path": self.file_path if self.file_path else "",
            "theme": self.colors.__name__ if hasattr(self.colors, '__name__') else "PYTHONPLUS_THEME_COLORS",
            "current_file_pos": self.hex_table.current_display_offset if self.hex_table.file_data else 0,
            "current_file_size": self.file_size,
            "created_date": self.created_label.cget("text") if self.created_label.cget("text") != "N/A" else "",
            "modified_date": self.modified_label.cget("text") if self.modified_label.cget("text") != "N/A" else ""
        }
        with open("config.dat", "w") as f:
            json.dump(config, f)
        messagebox.showinfo("Save Config", "Configuration saved to config.dat")

    def load_config(self):
        if os.path.exists("config.dat"):
            with open("config.dat", "r") as f:
                config = json.load(f)

            self.file_path = config.get("file_path", "")
            if self.file_path and os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "rb") as f:
                        data = f.read()
                    self.hex_table.load_file(data)
                    self.file_size = len(data)
                    self._update_file_info()
                    self.hex_table.goto_offset_and_display(config.get("current_file_pos", 0))
                    self.status_bar.config(
                        text=f"Loaded {os.path.basename(self.file_path)} (Size: {self.file_size} bytes).")
                    # Enable buttons when a file is loaded
                    self.search_button.config(state="normal")
                    self.search_replace_button.config(state="normal")
                    self.offset_replace_button.config(state="normal")
                    self.goto_button.config(state="normal")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                    self.status_bar.config(text="Failed to load file.")

            theme_map = {
                "LIGHT_THEME_COLORS": LIGHT_THEME_COLORS,
                "PYTHONPLUS_THEME_COLORS": PYTHONPLUS_THEME_COLORS,
                "DARKAMBER1_THEME_COLORS": DARKAMBER1_THEME_COLORS,
                "COLORFUL_THEME_COLORS": COLORFUL_THEME_COLORS
            }
            self._apply_theme(theme_map.get(config.get("theme", "PYTHONPLUS_THEME_COLORS"), PYTHONPLUS_THEME_COLORS))

            self.created_label.config(text=config.get("created_date", "N/A"))
            self.modified_label.config(text=config.get("modified_date", "N/A"))
            self.file_size_label.config(
                text=f"Size: 0x{config.get('current_file_size', 0):08X} ({config.get('current_file_size', 0)} bytes)")
        else:
            messagebox.showwarning("Load Config", "No config.dat file found.")

    def show_ascii_table(self, event=None):
        import tkinter.font as tkfont
        ascii_window = tk.Toplevel(self.root)
        ascii_window.title("ASCII Table")
        ascii_window.geometry("1024x768")

        default_font = tkfont.Font(family="Courier New", size=18, weight="bold")
        ascii_window.option_add("*Font", default_font)

        frame = tk.Frame(ascii_window)
        frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame, bg=self.colors["PANEL_BG"])
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        selected_value = [0]
        rect_ids = {}

        context_menu = tk.Menu(ascii_window, tearoff=0)
        context_menu.add_command(
            label="Copy",
            command=lambda: copy_values(selected_value[0])
        )

        def on_cell_click(event, value):
            selected_value[0] = value
            update_highlight()
            ascii_window.title(f"ASCII Table - Selected {value}")

        def on_cell_right_click(event, value):
            selected_value[0] = value
            update_highlight()
            context_menu.post(event.x_root, event.y_root)

        def update_highlight():
            for rid in rect_ids.values():
                canvas.itemconfig(rid, fill=self.colors["PANEL_BG"])
            rid = rect_ids.get(selected_value[0])
            if rid:
                canvas.itemconfig(rid, fill=self.colors["HEX_SEL_COLOR"])

        def copy_values(value):
            hex_value = hex(value)
            dec_value = str(value)
            combined_value = f"{hex_value}, {dec_value}"
            ascii_window.clipboard_clear()
            ascii_window.clipboard_append(combined_value)

        box_w, box_h = 45, 60
        pad_x, pad_y = 12, 12

        for i in range(256):
            row, col = divmod(i, 16)
            x = col * box_w + pad_x
            y = row * box_h + pad_y

            char = '.'
            if 32 <= i < 127 or 160 <= i < 256:
                try:
                    char = bytes([i]).decode('cp437')
                except:
                    pass

            bg = self.colors["HEX_SEL_COLOR"] if i == selected_value[0] else self.colors["PANEL_BG"]
            tag = f"cell_{i}"

            rid = canvas.create_rectangle(x, y, x + box_w, y + box_h,
                                          fill=bg, outline=self.colors["HEX_CELL_OUTLINE"], tags=(tag,))
            canvas.create_text(x + box_w / 2, y + box_h / 2, text=f"{i} ({char})",
                               fill=self.colors["FG"], tags=(tag,))

            rect_ids[i] = rid
            canvas.tag_bind(tag, "<Button-1>", lambda e, v=i: on_cell_click(e, v))
            canvas.tag_bind(tag, "<Button-3>", lambda e, v=i: on_cell_right_click(e, v))

        canvas.configure(scrollregion=canvas.bbox("all"))
        ascii_window.transient(self.root)
        ascii_window.grab_set()

    def offset_replace(self):
        try:
            offset_str = self.offset_var.get().strip()
            repl_str = self.offset_repl_var.get().strip()

            if not offset_str or not repl_str:
                messagebox.showwarning("Warning", "Offset and replacement value cannot be empty.")
                return

            if offset_str.lower().startswith("0x"):
                offset = int(offset_str, 16)
            else:
                offset = int(offset_str)

            if not (0 <= offset < len(self.hex_table.file_data)):
                messagebox.showwarning("Invalid Offset", "Offset is out of file bounds.")
                return

            if len(repl_str) == 2 and all(c in "0123456789abcdefABCDEF" for c in repl_str.lower()):
                repl_value = int(repl_str, 16)
            elif repl_str.isdigit() and 0 <= int(repl_str) <= 255:
                repl_value = int(repl_str)
            else:
                messagebox.showerror("Error", "Replacement must be a hex byte (e.g., '0A') or decimal (0-255).")
                return

            self.hex_table.file_data[offset] = repl_value
            self.hex_table._redraw()
            self.last_replaced_offset_label.config(text=f"Last Replaced: 0x{offset:08X}")
            self.current_offset_display_label.config(text=f"Offset: 0x{offset:08X} ({offset} dec)")
            self.hex_table.goto_offset_and_display(offset)
            self.status_bar.config(text=f"Replaced byte at 0x{offset:08X} with {repl_value:02X}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid offset or replacement format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    app = HexEditorApp(root)
    root.mainloop()
