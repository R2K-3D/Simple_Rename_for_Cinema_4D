# Simple Rename by R2K-3D

![Version](https://img.shields.io/badge/version-1.07--beta-blue)
![Cinema 4D](https://img.shields.io/badge/Cinema%204D-R20%2B-orange)
![Python](https://img.shields.io/badge/python-2.7%2B%20%7C%203.x-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Advanced batch renaming tool for Cinema 4D objects with live preview, preset management, and flexible naming options.

<img width="356" height="708" alt="Simple Rename_v1 07" src="https://github.com/user-attachments/assets/36dfd659-e084-4f9d-ab0f-086620f1ab9c" />

## ✨ Features

- **Batch Renaming** - Rename multiple objects at once with consistent naming patterns
- **Live Preview** - See changes before applying (displays up to 3 objects)
- **Smart Numbering** - Sequential numbering with custom separators and padding
- **Preset System** - Quick access to common suffixes (_Low, _High, _LP, _HP)
- **Replace Mode** - Find and replace text in existing names
- **Prefix/Postfix** - Add custom text before or after names
- **Cleanup Mode** - Remove unwanted characters from start or end
- **Symbol Removal** - Remove specific number of characters from names
- **Settings Persistence** - Automatically saves and loads your last settings
- **Undo Support** - All operations support Cinema 4D's undo system

## 🎯 Use Cases

- Clean up imported model names
- Standardize naming conventions across projects
- Prepare assets for export (Low/High poly variants)
- Organize scene hierarchy efficiently
- Batch rename materials, tags, or any Cinema 4D objects

## 📋 Requirements

- Cinema 4D R20 or later
- Python 2.7+ or 3.x (included with Cinema 4D)

## 🚀 Installation

1. Download the `simple_rename.py` script
2. Copy to one of these locations:
   - `C4D/library/scripts/` - Appears in Scripts menu
   - `C4D/library/scripts/[your_folder]/` - Custom organization
3. Restart Cinema 4D (if running)
4. Access via **Scripts → simple_rename.py**

## 📖 Usage

### Basic Renaming

1. Select objects in Object Manager
2. Run the script
3. Enter desired **Base Name**
4. Enable/disable **Numbering** as needed
5. Click **Rename Selected**

### Using Presets

Quick naming for common workflows:

- **Default** - Standard numbering mode
- **_Low** - Adds "_Low" suffix (no numbering)
- **_High** - Adds "_High" suffix (no numbering)
- **_LP** - Adds "_LP" suffix (low poly marker)
- **_HP** - Adds "_HP" suffix (high poly marker)

### Advanced Options

#### Numbering Options
- **Start Number** - Begin counting from any number (supports leading zeros: 001, 002...)
- **Separator** - Choose: `_`, `-`, space, none, or custom
- **Number Direction** - Top to bottom or bottom to top
- **Number Position** - After name (default) or before name

#### Rename Modes
- **Replace name (All)** - Complete name replacement
- **Replace & Prefix/Postfix** - Find/replace with prefix/postfix support

#### Cleanup Features
- **Cleanup Mode** - Remove characters from end or start until last/first letter
- **Remove Symbols** - Delete exact number of characters from start or end

## 🎨 Examples

### Example 1: Sequential Naming
```
Input:  Cube, Sphere, Cylinder
Settings: Base Name = "Mesh", Numbering = Yes, Separator = "_"
Output: Mesh_1, Mesh_2, Mesh_3
```

### Example 2: Low Poly Preset
```
Input:  Character, Prop, Environment
Settings: Preset = "_Low"
Output: Character_Low, Prop_Low, Environment_Low
```

### Example 3: Find & Replace
```
Input:  old_mesh_1, old_mesh_2, old_mesh_3
Settings: Mode = Replace & Prefix/Postfix, Replace "old" with "new"
Output: new_mesh_1, new_mesh_2, new_mesh_3
```

### Example 4: Leading Zeros
```
Input:  Object A, Object B, Object C
Settings: Base Name = "Asset", Start Number = "001"
Output: Asset_001, Asset_002, Asset_003
```

## ⚙️ Settings

Settings are automatically saved to:
```
C4D/prefs/rename_dialog_settings.json
```

To reset all settings, click **Reset to Default** button.

## 🔧 Technical Details

- Written in Python for Cinema 4D API
- Uses `c4d.gui.GeDialog` for interface
- JSON-based settings persistence
- Supports Unicode characters (including Cyrillic)
- Full undo/redo integration

## 🐛 Known Issues

- None reported yet

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📝 Changelog

### Version 1.07 (Beta) - Current
- Added preset system (Default, _Low, _High, _LP, _HP)
- Added symbol removal feature
- Centered Reset to Default button
- Improved layout organization
- All comments in English

### Previous Versions
- Core functionality established

## 👤 Author

**R2K-3D**

## 🙏 Acknowledgments

Thanks to [SPluzh](https://github.com/SPluzh) for contributions and inspiration

## 📄 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2025 R2K-3D

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

⭐ If you find this tool useful, please star this repository!
