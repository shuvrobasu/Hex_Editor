# « Hex Editor » - A Hexadecimal File Editor & Viewer

« Hex Editor » is a graphical application built with Python's Tkinter that allows users to open, view, and edit files in hexadecimal and ASCII formats. It provides a range of features for inspecting and manipulating binary data.

![image](https://github.com/user-attachments/assets/0efa5a4f-bce9-44dd-be31-f3a07968d3ba)
 (Light Theme) 

## Features

*   **Hexadecimal and ASCII Display:** 
    *   View file content side-by-side in both hex and ASCII representations.
    *   **Character Encoding Selection:** Choose from various encodings (e.g., Latin-1, UTF-8, ASCII, CP1252) for the ASCII column display via a dropdown in the "View Options" panel.
*   **Line Numbers & Offsets:**
    *   **Line Numbers:** A dedicated column on the far left displays 0-indexed line numbers for easy row identification.
    *   **Offsets:** The traditional hexadecimal offset column is positioned next to the line numbers.
      
*   **File Operations:**
    *   Open binary files (e.g., `.exe`, `.bin`, or any file).
    *   Save modified data to a new file ("Save As...").
    *   Insert new bytes at a specified offset with a chosen fill value.
    *   Delete selected ranges of bytes.
    *   Crop the file to only the selected range of bytes.
    *   Export selected bytes as ASCII text or raw binary data.

*   **Navigation:**
    *   Scroll through files using the mouse wheel, scrollbar, or keyboard (Up/Down arrows, PageUp/PageDown).
    *   Jump to specific offsets (hexadecimal or decimal input).
    *   Jump to specific line numbers (decimal input).
    *   Quick navigation to the "Top of File" and "End of File".
    *   Displays the current cursor offset and visible data range.
    *   Use of **Ctrl+T** (Top of file), **Ctrl+E** (End of file), **Ctrl+P** (Previous Page) & **Ctrl+N** (Next Page)
    *   Use **Ctrl+S** (Save) and **Ctrl+Q** (Quit)

*   **Editing:**
    *   Directly edit bytes in either the hex or ASCII view by double-clicking or pressing Enter on a selected byte.
    *   Changes are reflected immediately in both views.
    *   **Fill Selection:** Fill a selected range of bytes with a specified hex value.

*   **Selection:**
    *   Select single bytes by clicking.
    *   Select ranges of bytes by clicking and dragging.
    *   "Select All" and "Select None" options via context menu.

*   **Search & Replace (Right Panel):**
    *   Search for sequences of bytes (as hex strings or ASCII text).
    *   Search results include both line number and offset.
    *   Navigate through search matches (Next/Previous, F3/Shift+F3).
    *   Replace all found sequences with new byte patterns.
    *   Displays the count of matches.
    *   Dedicated "Search Results" listbox for quick jumps to matches.
      
    ![image](https://github.com/user-attachments/assets/9eefe8a6-265d-46ec-a4bb-a528f6dacd73)

*   **Offset-Specific Replace (Right Panel):**
    *   Replace a single byte at a user-specified offset with a new hex, decimal, or ASCII character value using a dedicated input field.

*   **Bookmarks (Left Panel):**
     *   Add/Delete Bookmarks: Save a specific offset with a tag name for quick navigation.
     *   Bookmarks are saved in the configuration file.
             
*   **Data Inspector (Left Panel):**
    *   View the data at the current cursor position interpreted as various data types:
        *   **Single Byte Views:** Decimal, Hexadecimal, Octal, Binary, and ASCII character.
        *   **Multi-Byte Views:** 8-bit, 16-bit, 32-bit, 64-bit Integers (Signed and Unsigned).
        *   **Floating-Point Views:** 16-bit (half-precision), 32-bit (single-precision), 64-bit (double-precision).
    *   **Endianness Toggle:** Switch between Little-endian and Big-endian interpretation for multi-byte values via radio buttons.

*   **Theming:**
    *   Multiple built-in color themes: Light, PythonPlus Dark Blue, Dark Amber, Colorful Dark.
    *   Themes affect all UI elements for a consistent look and feel.

*   **File Information Panel (Left Panel):**
    *   Displays filename, file size (hex and decimal).
    *   File creation and modification timestamps (if available from the OS).
    *   Attempted file type detection based on magic numbers.
    *   MD5 hash of the currently loaded data (calculated on load/modification for smaller files).

*   **Data Analysis Utilities:**
    *   **Checksum/Hash Calculator for Selection:** Calculate MD5, SHA1, or SHA256 hashes for the selected range of bytes via the context menu. Results are shown in a copyable dialog.
    *   Hex to Decimal converter.
    *   Decimal to Hex converter.
    *   Show ASCII Table: Displays a clickable and copyable table of characters (0-255, using CP437 for extended) with their decimal and hex values.

*   **User Interface Enhancements:**
    *   **Three-Panel Layout:** Left Panel (Inspector, View Options, File Info, Go To, Bookmarks), Center Panel (Hex/ASCII display), and Right Panel (Search/Replace tools).
    *   **Scrollable Left Panel:** The left panel containing various tools is scrollable if its content exceeds the window height.
    *   **Panel Visibility Toggling:** Show or hide individual sections within the left panel (Inspector, View Options, File Info, Go To, Bookmarks) via a "View Panels" menu for a customizable workspace.
    *   Tooltips for various UI elements.
    *   Context-sensitive right-click menu in the hex view.
    *   Status bar displaying current offset, byte value, ASCII character, operation results, and Undo/Redo history.
    *   Customizable fonts for hex and ASCII display (defined as constants).
    *   **Undo/Redo Functionality:** Supports undoing and redoing most file modifications.

*   **Configuration:**
    *   Save/Load: Persists settings like the last opened file, theme, last view position, ASCII encoding, inspector endianness, and bookmarks to a JSON configuration file (`hex_editor_config.json`) in the script's directory.

## Requirements

*   Python 3.x
*   Tkinter (usually included with standard Python installations)

No external libraries are required beyond the Python standard library (uses `hashlib`, `struct`, `json`, `datetime`, `os`).

## How to Run

1.  Save the code as a Python file (e.g., `hex_editor_v2.3.py`).
2.  Open a terminal or command prompt.
3.  Navigate to the directory where you saved the file.
4.  Run the script using the Python interpreter:
    ```bash
    python hex_editor_v2.3.py
    ```

## Code Structure Overview

*   **Theme Definitions & Global Constants:** Dictionaries for color palettes and constants for display configuration.
*   **`ToolTip` Class:** For hover tooltips.
*   **`HexTable` Class (inherits `tk.Canvas`):**
    *   Renders hex, line number, and ASCII views.
    *   Handles grid interactions (selection, editing, navigation).
    *   Manages data display and uses the selected character encoding for its ASCII column.
*   **`HexEditorApp` Class:**
    *   Main application window, UI layout (scrollable left panel, center, right panel), status bar, and menubar.
    *   **Left Panel Management:** Includes `_build_left_panel_widgets` which now sets up containers for toggleable panels (Inspector, View Options, File Info, etc.) within a scrollable canvas. The `toggle_panel_visibility` method manages showing/hiding these panels based on user selection from the "View Panels" menu.
    *   **Data Inspector:** `update_inspector` method now handles endianness selection and displays single-byte views (Dec, Hex, Oct, Bin, ASCII).
    *   **File Operations & Editing:** Handles file I/O, byte manipulation (insert, delete, crop, fill).
    *   **Search/Replace & Offset Replace:** Implements logic for finding and replacing byte sequences.
    *   **Utilities:** Contains methods for hash calculation for selected data, data type conversion, ASCII table display.
    *   **Theming & Configuration:** Manages theme application and saving/loading of user preferences and application state to `config.dat`.
    *   **Undo/Redo:** Implements an undo/redo stack for data modifications.

## Configuration

The application saves settings (last file, theme, view position, encoding, endianness, bookmarks) to `config.dat` in the script's directory, managed via the **"Utils" -> "Save/Load Config"** menu options and automatically on certain actions like theme changes or opening files.

## License ##

The program is distributed as per the MIT License

## Author ##

This program was designed by `Shuvro Basu` (c) 2025.
