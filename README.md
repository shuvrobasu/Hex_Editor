# « Hex Editor » - A Hexadecimal File Editor & Viewer

« Hex Editor » is a graphical application built with Python's Tkinter that allows users to open, view, and edit files in hexadecimal and ASCII formats. It provides a range of features for inspecting and manipulating binary data.


![image](https://github.com/user-attachments/assets/b1dfa8f6-a862-421e-aecf-28e08e967b2e)  (Light Theme) 


## Features

*   **Hexadecimal and ASCII Display:** View file content side-by-side in both hex and ASCII representations.
*   **Line Numbers & Offsets:**
    *   **Line Numbers:** A dedicated column on the far left displays 0-indexed line numbers for easy row identification, even for very large files.
    *   **Offsets:** The traditional hexadecimal offset column is positioned next to the line numbers.
      
*   **File Operations:**
    *   Open binary files (e.g., `.exe`, `.bin`, or any file).
    *   Save modified data to a new file ("Save As...").
    *   Insert new bytes at a specified offset with a chosen fill value.
    *   Delete selected ranges of bytes.
    *   Crop the file to only the selected range of bytes.
    *   Export selected bytes as ASCII text or raw binary data.

*   **Navigation:**
    *   Scroll through files using the mouse wheel, scrollbar (implicitly via canvas), or keyboard (Up/Down arrows, PageUp/PageDown).
    *   Jump to specific offsets (hexadecimal or decimal input).
    *   Jump to specific line numbers (decimal input).
    *   Quick navigation to the "Top of File" and "End of File".
    *   Displays the current cursor offset and visible data range.
    *   Use of **Ctrl+T** (Top of file), **Ctrl+E** (End of file), **Ctrl+P** (Previous Page) & **Ctrl+N** (Next Page)
    *   Use **Ctrl+S** (Save) and **Ctrl+Q** (Quit)

*   **Editing:**
    *   Directly edit bytes in either the hex or ASCII view by double-clicking or pressing Enter on a selected byte.
    *   Changes are reflected immediately in both views.

*   **Selection:**
    *   Select single bytes by clicking.
    *   Select ranges of bytes by clicking and dragging.
    *   "Select All" and "Select None" options via context menu.

*   **Search & Replace (Moved to Right Panel):**
    *   Search for sequences of bytes (as hex strings or ASCII text).
    *   Search results now include both the **line number and offset** for better context.
    *   Navigate through search matches (Next/Previous).
    *   Replace found sequences with new byte patterns (must be of the same length).
    *   Displays the count of matches.
    *   Dedicated "Search Results" listbox for quick jumps to matches.
      
![image](https://github.com/user-attachments/assets/7c1ba60a-d663-4b32-905a-137ead7d78fc)



*   **Offset-Specific Replace (Moved to Right Panel):**
    *   Replace a single byte at a user-specified offset with a new hex or decimal value.

*   **Bookmarks**
     *   Add/Delete Bookmarks (save a specific offset with a tag name for future reference and quickly jump between sections of a file)
     *   Bookmarks are also saved in `config.dat` file for future use.
             
*   **Data Inspector:**
    *   View the data at the current cursor position interpreted as various data types (little-endian):
        *   8-bit, 16-bit, 32-bit, 64-bit Integers
        *   16-bit (half-precision), 32-bit (single-precision), 64-bit (double-precision) Floating-point numbers

*   **Theming:**
    *   Multiple built-in color themes:
        *   Light Theme
        *   Dark Blue Theme (PythonPlus)
        *   Dark Amber Theme
        *   Colorful Theme
    *   Themes affect all UI elements for a consistent look and feel.

*   **File Information Panel:**
    *   Displays filename, file size (hex and decimal).
    *   File creation and modification timestamps.
    *   Attempted file type detection (e.g., MS-DOS/PE Executable, ELF, Mach-O).
    *   MD5 hash of the file (calculated on load for smaller files).

*   **Utilities:**
    *   Hex to Decimal converter.
    *   Decimal to Hex converter (for values 0-255).
    *   Show ASCII Table: Displays a clickable and copyable table of ASCII characters (0-255) with their decimal and hex values.
    *   Save/Load Configuration: Persists the last opened file, theme, and view position to `config.dat`.

*   **User Interface Enhancements:**
    *   **Three-Panel Layout:** The application now features a distinct three-panel layout: Left Panel (Data Inspector, File Info, Go To), Center Panel (Hex/ASCII display with Line Numbers and Offsets), and Right Panel (Search & Replace, Search Results, Offset Replace).
    *   Tooltips for various input fields and buttons.
    *   Context-sensitive right-click menu in the hex view for common operations.
    *   Status bar displaying current offset information or operation results, including Undo/Redo history.
    *   Customizable fonts for hex and ASCII display.
    *   **Undo/Redo Functionality:** Supports undoing and redoing file modifications.

## Requirements

*   Python 3.x
*   Tkinter (usually included with standard Python installations)

No external libraries are required beyond the Python standard library.

## How to Run

1.  Save the code as a Python file (e.g., `hex_editor.py`).
2.  Open a terminal or command prompt.
3.  Navigate to the directory where you saved the file.
4.  Run the script using the Python interpreter:
    ```bash
    python hex_editor.py
    ```

## Code Structure Overview

*   **Theme Definitions (`LIGHT_THEME_COLORS`, etc.):** Dictionaries defining color palettes for different UI themes.
*   **Global Constants (`BYTES_PER_ROW`, `ASCII_FONT`, etc.):** Configuration for the hex display, including `LINE_NUM_COL_W` for the new line number column.
*   **`ToolTip` Class:** A simple class to create hover tooltips for Tkinter widgets.
*   **`HexTable` Class (inherits `tk.Canvas`):**
    *   The core component responsible for rendering the hexadecimal, line number, and ASCII views of the file data.
    *   Handles user interactions like clicking, dragging (selection), double-clicking (editing), mouse wheel scrolling, and keyboard navigation within the grid.
    *   Manages data loading, redrawing, selection highlighting, and in-place editing, with updated coordinate calculations to accommodate the new line number column.
    *   Provides methods for inserting, deleting, and cropping bytes.
*   **`HexEditorApp` Class:**
    *   The main application window and controller.
    *   Sets up the overall UI layout with a `left_panel`, `right_side_container` (which holds the `hex_view_container` and `search_panel`), and status bar.
    *   Includes new methods (`_build_left_panel_widgets`, `_build_search_panel_widgets`) to logically separate the UI component creation.
    *   Handles file operations (open, save as), theme switching, utility functions (converters, ASCII table), search/replace logic (now including line numbers in results), and configuration management.
    *   Connects UI actions to `HexTable` methods and updates UI elements based on application state.

## Configuration

The application can save and load some basic configuration settings (last opened file, theme, last view position) to a `config.dat` file in the same directory as the script. This is handled via the **"Utils"** menu.

## License ##

The program is distributed as per the MIT License

## Author ##

This program was designed by `Shuvro Basu` (c) 2025.
