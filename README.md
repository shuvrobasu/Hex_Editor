# « Hex Editor » - A Hexadecimal File Editor & Viewer 

« Hex Editor » is a graphical application built with Python's that allows users to open, view, and edit files in hexadecimal and ASCII formats. It provides a range of features for inspecting and manipulating binary data.

![image](https://github.com/user-attachments/assets/6af1538e-35b1-4030-a19b-b95a8a6ff8fe)


## Features

*   **Hexadecimal and ASCII Display:** View file content side-by-side in both hex and ASCII representations.
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
    *   Quick navigation to the "Top of File" and "End of File".
    *   Clear display of the current cursor offset and visible data range.
      
*   **Editing:**
    *   Directly edit bytes in either the hex or ASCII view by double-clicking or pressing Enter on a selected byte.
    *   Changes are reflected immediately in both views.
      
*   **Selection:**
    *   Select single bytes by clicking.
    *   Select ranges of bytes by clicking and dragging.
    *   "Select All" and "Select None" options via context menu.
      
*   **Search & Replace:**
    *   Search for sequences of bytes (as hex strings or ASCII text).
    *   Navigate through search matches (Next/Previous).
    *   Replace found sequences with new byte patterns (must be of the same length).
    *   Displays the count of matches.
      
*   **Offset-Specific Replace:**
    *   Replace a single byte at a user-specified offset with a new hex or decimal value.
      
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
    *   Tooltips for various input fields and buttons.
    *   Context-sensitive right-click menu in the hex view for common operations.
    *   Status bar displaying current offset information or operation results.
    *   Customizable fonts for hex and ASCII display.

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
*   **Global Constants (`BYTES_PER_ROW`, `ASCII_FONT`, etc.):** Configuration for the hex display.
*   **`ToolTip` Class:** A simple class to create hover tooltips for Tkinter widgets.
*   **`HexTable` Class (inherits `tk.Canvas`):**
    *   The core component responsible for rendering the hexadecimal and ASCII views of the file data.
    *   Handles user interactions like clicking, dragging (selection), double-clicking (editing), mouse wheel scrolling, and keyboard navigation within the hex/ASCII grid.
    *   Manages data loading, redrawing, selection highlighting, and in-place editing.
    *   Provides methods for inserting, deleting, and cropping bytes.
*   **`HexEditorApp` Class:**
    *   The main application window and controller.
    *   Sets up the overall UI layout, including the menu bar, side panel (with Data Inspector, File Info, Go To, Search/Replace, Offset Replace), hex view area, and status bar.
    *   Handles file operations (open, save as), theme switching, utility functions (converters, ASCII table), search/replace logic, and configuration management.
    *   Connects UI actions to `HexTable` methods and updates UI elements based on application state.

## Configuration

The application can save and load some basic configuration settings (last opened file, theme, last view position) to a `config.dat` file in the same directory as the script. This is handled via the "Util" menu.
