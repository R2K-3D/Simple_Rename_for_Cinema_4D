import c4d
from c4d import gui
import re
import os
import json

class RenameDialog(gui.GeDialog):
    ID_CLEANUP_MODE = 3005
    ID_NUMERATE = 1500
    ID_SEPARATOR = 1100
    ID_START_NUMBER = 1000
    ID_MODE = 1300
    ID_PREFIX = 1003
    ID_BASENAME = 1001
    ID_POSTFIX = 1002
    ID_PRESET = 1004
    ID_REPLACE_FROM = 1400
    ID_REPLACE_TO = 1401
    ID_BUTTON_RENAME = 1200
    ID_BUTTON_CLEANUP = 1201
    ID_BUTTON_RESET = 1202
    ID_PREVIEW = 1601
    ID_CUSTOM_SEPARATOR = 2011
    ID_CUSTOM_SEPARATOR_LABEL = 2010
    ID_NUMBER_DIRECTION = 2020
    ID_NUMBER_POSITION = 2021
    ID_REMOVE_MODE = 3010
    ID_REMOVE_COUNT = 3011
    ID_BUTTON_REMOVE = 3012

    def __init__(self):
        super(RenameDialog, self).__init__()
        self.settings_file = os.path.join(c4d.storage.GeGetC4DPath(c4d.C4D_PATH_PREFS), "rename_dialog_settings.json")
        self.last_selection = []

    def LoadSettings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None

    def SaveSettings(self):
        settings = {
            'numerate': self.GetInt32(self.ID_NUMERATE),
            'separator': self.GetInt32(self.ID_SEPARATOR),
            'custom_separator': self.GetString(self.ID_CUSTOM_SEPARATOR),
            'start_number': self.GetString(self.ID_START_NUMBER),
            'mode': self.GetInt32(self.ID_MODE),
            'prefix': self.GetString(self.ID_PREFIX),
            'basename': self.GetString(self.ID_BASENAME),
            'postfix': self.GetString(self.ID_POSTFIX),
            'replace_from': self.GetString(self.ID_REPLACE_FROM),
            'replace_to': self.GetString(self.ID_REPLACE_TO),
            'number_direction': self.GetInt32(self.ID_NUMBER_DIRECTION),
            'number_position': self.GetInt32(self.ID_NUMBER_POSITION),
            'cleanup_mode': self.GetInt32(self.ID_CLEANUP_MODE),
            'preset': self.GetInt32(self.ID_PRESET),
            'remove_mode': self.GetInt32(self.ID_REMOVE_MODE),
            'remove_count': self.GetString(self.ID_REMOVE_COUNT)
        }
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except:
            pass

    def ResetToDefaults(self):
        self.SetInt32(self.ID_NUMERATE, 1)
        self.SetInt32(self.ID_SEPARATOR, 1)
        self.SetString(self.ID_CUSTOM_SEPARATOR, "-")
        self.SetString(self.ID_START_NUMBER, "1")
        self.SetInt32(self.ID_MODE, 0)
        self.SetString(self.ID_PREFIX, "")
        self.SetString(self.ID_BASENAME, "NewName")
        self.SetString(self.ID_POSTFIX, "")
        self.SetString(self.ID_REPLACE_FROM, "")
        self.SetString(self.ID_REPLACE_TO, "")
        self.SetInt32(self.ID_NUMBER_DIRECTION, 0)
        self.SetInt32(self.ID_NUMBER_POSITION, 0)
        self.SetInt32(self.ID_CLEANUP_MODE, 0)
        self.SetInt32(self.ID_PRESET, 0)
        self.SetInt32(self.ID_REMOVE_MODE, 0)
        self.SetString(self.ID_REMOVE_COUNT, "1")
        self.UpdateControls()
        self.UpdatePreview()
        self.SaveSettings()

    def CreateLayout(self):
        try:
            self.SetTitle("Simple Rename by R2K-3D v1.07 (Beta)")

            # Top section
            self.GroupBegin(5000, c4d.BFH_SCALEFIT, cols=2)
            self.GroupBorderSpace(10, 10, 10, 0)

            self.GroupBegin(5001, c4d.BFH_SCALEFIT, cols=1)
            self.AddStaticText(2001, c4d.BFH_CENTER, name="Base Name:")
            self.AddEditText(self.ID_BASENAME, c4d.BFH_SCALEFIT)
            self.GroupEnd()

            self.GroupBegin(5002, c4d.BFH_RIGHT, cols=1)
            self.AddStaticText(2009, c4d.BFH_CENTER, name="Preset:")
            self.AddComboBox(self.ID_PRESET, c4d.BFH_LEFT, initw=100)
            self.AddChild(self.ID_PRESET, 0, "Default")
            self.AddChild(self.ID_PRESET, 1, "_Low")
            self.AddChild(self.ID_PRESET, 2, "_High")
            self.AddChild(self.ID_PRESET, 3, "_LP")
            self.AddChild(self.ID_PRESET, 4, "_HP")
            self.GroupEnd()

            self.GroupEnd()
            self.AddSeparatorH(5)

            # Main grid
            self.GroupBegin(3000, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=2)
            self.GroupBorderSpace(10, 10, 10, 10)

            # Row 1
            self.AddStaticText(2006, c4d.BFH_LEFT, name="Numbering:")
            self.AddStaticText(2003, c4d.BFH_LEFT, name="Rename Mode:")

            self.AddComboBox(self.ID_NUMERATE, c4d.BFH_SCALEFIT)
            self.AddChild(self.ID_NUMERATE, 1, "Yes")
            self.AddChild(self.ID_NUMERATE, 0, "No")

            self.AddComboBox(self.ID_MODE, c4d.BFH_SCALEFIT)
            self.AddChild(self.ID_MODE, 0, "Replace name (All)")
            self.AddChild(self.ID_MODE, 1, "Replace & Prefix/Postfix")

            # Row 2
            self.AddStaticText(2002, c4d.BFH_LEFT, name="Separator:")
            self.AddStaticText(2007, c4d.BFH_LEFT, name="Name Prefix:   ___name")

            self.AddComboBox(self.ID_SEPARATOR, c4d.BFH_SCALEFIT)
            self.AddChild(self.ID_SEPARATOR, 0, "_ (Underscore)")
            self.AddChild(self.ID_SEPARATOR, 1, "- (Dash)")
            self.AddChild(self.ID_SEPARATOR, 2, "Space")
            self.AddChild(self.ID_SEPARATOR, 3, "(No Separator)")
            self.AddChild(self.ID_SEPARATOR, 4, "Custom")

            self.AddEditText(self.ID_PREFIX, c4d.BFH_SCALEFIT)

            # Row 3
            self.AddStaticText(self.ID_CUSTOM_SEPARATOR_LABEL, c4d.BFH_LEFT, name="Custom Separator:")
            self.AddStaticText(2008, c4d.BFH_LEFT, name="Name Postfix:   name___")

            self.AddEditText(self.ID_CUSTOM_SEPARATOR, c4d.BFH_SCALEFIT)
            self.AddEditText(self.ID_POSTFIX, c4d.BFH_SCALEFIT)

            # Row 4
            self.AddStaticText(2000, c4d.BFH_LEFT, name="Start Number (e.g. 1):")
            self.AddStaticText(2004, c4d.BFH_LEFT, name="Replace in Name:")

            self.AddEditText(self.ID_START_NUMBER, c4d.BFH_SCALEFIT)
            self.AddEditText(self.ID_REPLACE_FROM, c4d.BFH_SCALEFIT)

            # Row 5
            self.AddStaticText(2100, c4d.BFH_LEFT, name="Number Direction:")
            self.AddStaticText(2005, c4d.BFH_LEFT, name="With:")

            self.AddComboBox(self.ID_NUMBER_DIRECTION, c4d.BFH_SCALEFIT)
            self.AddChild(self.ID_NUMBER_DIRECTION, 0, "Top to Bottom (default)")
            self.AddChild(self.ID_NUMBER_DIRECTION, 1, "Bottom to Top")

            self.AddEditText(self.ID_REPLACE_TO, c4d.BFH_SCALEFIT)

            # Row 6 - Number Position and Remove Symbols
            self.AddStaticText(2101, c4d.BFH_LEFT, name="Number Position:")
            self.AddStaticText(3100, c4d.BFH_LEFT, name="Remove Symbols:")

            self.AddComboBox(self.ID_NUMBER_POSITION, c4d.BFH_SCALEFIT)
            self.AddChild(self.ID_NUMBER_POSITION, 0, "After name (default)")
            self.AddChild(self.ID_NUMBER_POSITION, 1, "Before name")

            self.AddComboBox(self.ID_REMOVE_MODE, c4d.BFH_SCALEFIT)
            self.AddChild(self.ID_REMOVE_MODE, 0, "Off")
            self.AddChild(self.ID_REMOVE_MODE, 1, "Remove from Start")
            self.AddChild(self.ID_REMOVE_MODE, 2, "Remove from End")

            # Row 7 - Cleanup Mode and Remove Count + Del button
            self.AddStaticText(2102, c4d.BFH_LEFT, name="Cleanup Mode:")
            self.AddStaticText(3101, c4d.BFH_LEFT, name="Remove Count:")

            self.AddComboBox(self.ID_CLEANUP_MODE, c4d.BFH_SCALEFIT)
            self.AddChild(self.ID_CLEANUP_MODE, 0, "Off")
            self.AddChild(self.ID_CLEANUP_MODE, 1, "From end (default)")
            self.AddChild(self.ID_CLEANUP_MODE, 2, "From start")

            # Group for Remove Count and Del button
            self.GroupBegin(3200, c4d.BFH_SCALEFIT, cols=2)
            self.AddEditText(self.ID_REMOVE_COUNT, c4d.BFH_SCALEFIT)
            self.AddButton(self.ID_BUTTON_REMOVE, c4d.BFH_LEFT, initw=50, name="Del")
            self.GroupEnd()

            self.GroupEnd()
            
            # Reset to Default button separately under grid - centered
            self.GroupBegin(3300, c4d.BFH_CENTER, cols=1)
            self.GroupBorderSpace(10, 5, 10, 5)
            self.AddButton(self.ID_BUTTON_RESET, c4d.BFH_CENTER, initw=150, name="Reset to Default")
            self.GroupEnd()
            
            self.AddSeparatorH(10)

            # Buttons
            self.GroupBegin(4000, c4d.BFH_CENTER, cols=2)
            self.AddButton(self.ID_BUTTON_CLEANUP, c4d.BFH_SCALE, name="Cleanup Names")
            self.AddButton(self.ID_BUTTON_RENAME, c4d.BFH_SCALE, name="Rename Selected")
            self.GroupEnd()

            self.AddSeparatorH(10)

            # Preview
            self.AddStaticText(1600, c4d.BFH_LEFT, name="Preview (up to 3 objects):")
            self.AddMultiLineEditText(self.ID_PREVIEW, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, initw=600, inith=90)
            self.AddSeparatorH(10)

            self.GroupBegin(4001, c4d.BFH_RIGHT, cols=1)
            self.AddStaticText(1602, c4d.BFH_RIGHT, name="Simple Rename by R2K-3D v1.07 (Beta) thx github.com/SPluzh ")
            self.GroupEnd()

            print("CreateLayout completed successfully")
            return True
        except Exception as e:
            print(f"Error in CreateLayout: {e}")
            import traceback
            traceback.print_exc()
            return False

    def InitValues(self):
        settings = self.LoadSettings()
        if settings:
            self.SetInt32(self.ID_NUMERATE, settings.get('numerate', 1))
            self.SetInt32(self.ID_SEPARATOR, settings.get('separator', 1))
            self.SetString(self.ID_CUSTOM_SEPARATOR, settings.get('custom_separator', '-'))
            self.SetString(self.ID_START_NUMBER, settings.get('start_number', '1'))
            self.SetInt32(self.ID_MODE, settings.get('mode', 0))
            self.SetString(self.ID_PREFIX, settings.get('prefix', ''))
            self.SetString(self.ID_BASENAME, settings.get('basename', 'NewName'))
            self.SetString(self.ID_POSTFIX, settings.get('postfix', ''))
            self.SetString(self.ID_REPLACE_FROM, settings.get('replace_from', ''))
            self.SetString(self.ID_REPLACE_TO, settings.get('replace_to', ''))
            self.SetInt32(self.ID_NUMBER_DIRECTION, settings.get('number_direction', 0))
            self.SetInt32(self.ID_NUMBER_POSITION, settings.get('number_position', 0))
            self.SetInt32(self.ID_CLEANUP_MODE, settings.get('cleanup_mode', 0))
            self.SetInt32(self.ID_PRESET, settings.get('preset', 0))
            self.SetInt32(self.ID_REMOVE_MODE, settings.get('remove_mode', 0))
            self.SetString(self.ID_REMOVE_COUNT, settings.get('remove_count', '1'))
        else:
            self.SetInt32(self.ID_NUMERATE, 1)
            self.SetInt32(self.ID_SEPARATOR, 1)
            self.SetString(self.ID_CUSTOM_SEPARATOR, "-")
            self.SetString(self.ID_START_NUMBER, "1")
            self.SetInt32(self.ID_MODE, 0)
            self.SetString(self.ID_PREFIX, "")
            self.SetString(self.ID_BASENAME, "NewName")
            self.SetString(self.ID_POSTFIX, "")
            self.SetString(self.ID_REPLACE_FROM, "")
            self.SetString(self.ID_REPLACE_TO, "")
            self.SetInt32(self.ID_NUMBER_DIRECTION, 0)
            self.SetInt32(self.ID_NUMBER_POSITION, 0)
            self.SetInt32(self.ID_CLEANUP_MODE, 0)
            self.SetInt32(self.ID_PRESET, 0)
            self.SetInt32(self.ID_REMOVE_MODE, 0)
            self.SetString(self.ID_REMOVE_COUNT, "1")

        self.UpdateControls()
        self.UpdatePreview()
        return True

    def UpdateControls(self):
        mode = self.GetInt32(self.ID_MODE)
        numerate = self.GetInt32(self.ID_NUMERATE)
        sep_index = self.GetInt32(self.ID_SEPARATOR)
        cleanup_mode = self.GetInt32(self.ID_CLEANUP_MODE)
        remove_mode = self.GetInt32(self.ID_REMOVE_MODE)

        self.Enable(self.ID_REPLACE_FROM, mode == 1)
        self.Enable(self.ID_REPLACE_TO, mode == 1)
        self.Enable(self.ID_PREFIX, mode in (0, 1))
        self.Enable(self.ID_POSTFIX, mode in (0, 1))
        self.Enable(self.ID_BASENAME, mode == 0)
        self.Enable(self.ID_SEPARATOR, numerate == 1)
        self.Enable(self.ID_START_NUMBER, numerate == 1)
        self.Enable(self.ID_CUSTOM_SEPARATOR, numerate == 1 and sep_index == 4)
        self.Enable(self.ID_CUSTOM_SEPARATOR_LABEL, numerate == 1 and sep_index == 4)
        self.Enable(self.ID_NUMBER_DIRECTION, numerate == 1)
        self.Enable(self.ID_NUMBER_POSITION, numerate == 1)
        self.Enable(self.ID_CLEANUP_MODE, True)
        self.Enable(self.ID_BUTTON_CLEANUP, cleanup_mode != 0)
        
        # Remove controls - inactive when Off
        self.Enable(self.ID_REMOVE_COUNT, remove_mode != 0)
        self.Enable(self.ID_BUTTON_REMOVE, remove_mode != 0)

        self.UpdatePreview()
        self.SaveSettings()

    def CleanupName(self, name, mode):
        if mode == 1:
            matches = list(re.finditer(r"[A-Za-zА-Яа-я]", name))
            if matches:
                return name[:matches[-1].start() + 1]
        elif mode == 2:
            matches = list(re.finditer(r"[A-Za-zА-Яа-я]", name))
            if matches:
                return name[matches[0].start():]
        return name

    def RemoveSymbols(self, name, mode, count):
        """Remove specified number of characters from start or end"""
        if mode == 0 or count <= 0:
            return name
        
        if count >= len(name):
            return name  # Don't remove entire name
        
        if mode == 1:  # Remove from Start
            return name[count:]
        elif mode == 2:  # Remove from End
            return name[:-count]
        
        return name

    def DoRemove(self):
        """Execute symbol removal on selected objects"""
        remove_mode = self.GetInt32(self.ID_REMOVE_MODE)
        if remove_mode == 0:
            gui.MessageDialog("Remove mode is Off!")
            return
        
        try:
            remove_count = int(self.GetString(self.ID_REMOVE_COUNT).strip())
        except:
            gui.MessageDialog("Invalid remove count! Please enter a valid number.")
            return
        
        if remove_count <= 0:
            gui.MessageDialog("Remove count must be greater than 0!")
            return
        
        objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not objects:
            gui.MessageDialog("No objects selected!")
            return
        
        # Check if there are objects with names shorter than count
        too_short = [obj for obj in objects if len(obj.GetName()) <= remove_count]
        if too_short:
            result = gui.MessageDialog(
                f"Warning: {len(too_short)} object(s) have names shorter than or equal to {remove_count} characters.\n"
                "These names will not be changed. Continue?",
                c4d.GEMB_YESNO
            )
            if result == c4d.GEMB_R_NO:
                return
        
        doc.StartUndo()
        try:
            changed = 0
            for obj in objects:
                old_name = obj.GetName()
                new_name = self.RemoveSymbols(old_name, remove_mode, remove_count)
                
                if new_name != old_name:
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                    obj.SetName(new_name)
                    changed += 1
            
            doc.EndUndo()
            gui.MessageDialog(f"Successfully modified {changed} object(s)!")
        except:
            doc.EndUndo()
            raise
        
        c4d.EventAdd()
        self.UpdatePreview()

    def UpdatePreview(self):
        start_str = self.GetString(self.ID_START_NUMBER).strip()
        prefix = self.GetString(self.ID_PREFIX).strip()
        base_name = self.GetString(self.ID_BASENAME).strip()
        postfix = self.GetString(self.ID_POSTFIX).strip()
        sep_index = self.GetInt32(self.ID_SEPARATOR)
        mode = self.GetInt32(self.ID_MODE)
        numerate = self.GetInt32(self.ID_NUMERATE)
        replace_from = self.GetString(self.ID_REPLACE_FROM)
        replace_to = self.GetString(self.ID_REPLACE_TO)
        custom_sep = self.GetString(self.ID_CUSTOM_SEPARATOR).strip()
        direction = self.GetInt32(self.ID_NUMBER_DIRECTION)
        number_position = self.GetInt32(self.ID_NUMBER_POSITION)
        cleanup_mode = self.GetInt32(self.ID_CLEANUP_MODE)

        separator = {0: "_", 1: "-", 2: " ", 3: "", 4: custom_sep}.get(sep_index, "-")

        m = re.match(r"^(0*)(\d+)$", start_str)
        if m:
            leading_zeros = len(m.group(1))
            start_number = int(m.group(2))
        else:
            leading_zeros = 0
            try:
                start_number = int(start_str)
            except:
                start_number = 1

        objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not objects:
            self.SetString(self.ID_PREVIEW, "<No objects selected>")
            return

        objs_for_preview = objects[:3]
        if direction == 1:
            objs_for_preview = list(reversed(objs_for_preview))

        preview_lines = []
        for i, obj in enumerate(objs_for_preview):
            old_name = obj.GetName()
            clean_name = self.CleanupName(old_name, cleanup_mode)
            num = start_number + i
            num_str = f"{num:0{len(start_str)}d}" if leading_zeros > 0 else str(num)

            if mode == 1:
                new_name = clean_name.replace(replace_from, replace_to) if replace_from else clean_name
                new_name = f"{prefix}{new_name}{postfix}"
                if numerate:
                    if number_position == 1:
                        new_name = f"{num_str}{separator}{new_name}"
                    else:
                        new_name = f"{new_name}{separator}{num_str}"
            else:
                new_name = base_name
                new_name = f"{prefix}{new_name}{postfix}"
                if numerate:
                    if number_position == 1:
                        new_name = f"{num_str}{separator}{new_name}"
                    else:
                        new_name = f"{new_name}{separator}{num_str}"

            preview_lines.append(f"{old_name}  >>>  {new_name}")

        self.SetString(self.ID_PREVIEW, "\n-----------------------------\n".join(preview_lines))

    def DoRename(self):
        start_str = self.GetString(self.ID_START_NUMBER).strip()
        prefix = self.GetString(self.ID_PREFIX).strip()
        base_name = self.GetString(self.ID_BASENAME).strip()
        postfix = self.GetString(self.ID_POSTFIX).strip()
        sep_index = self.GetInt32(self.ID_SEPARATOR)
        mode = self.GetInt32(self.ID_MODE)
        numerate = self.GetInt32(self.ID_NUMERATE)
        replace_from = self.GetString(self.ID_REPLACE_FROM)
        replace_to = self.GetString(self.ID_REPLACE_TO)
        custom_sep = self.GetString(self.ID_CUSTOM_SEPARATOR).strip()
        direction = self.GetInt32(self.ID_NUMBER_DIRECTION)
        number_position = self.GetInt32(self.ID_NUMBER_POSITION)
        cleanup_mode = self.GetInt32(self.ID_CLEANUP_MODE)

        separator = {0: "_", 1: "-", 2: " ", 3: "", 4: custom_sep}.get(sep_index, "-")

        m = re.match(r"^(0*)(\d+)$", start_str)
        if m:
            leading_zeros = len(m.group(1))
            start_number = int(m.group(2))
        else:
            leading_zeros = 0
            try:
                start_number = int(start_str)
            except:
                start_number = 1

        objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not objects:
            gui.MessageDialog("No objects selected!")
            return

        if direction == 1:
            objects = list(reversed(objects))

        doc.StartUndo()
        try:
            for i, obj in enumerate(objects):
                old_name = obj.GetName()
                clean_name = self.CleanupName(old_name, cleanup_mode)
                num = start_number + i
                num_str = f"{num:0{len(start_str)}d}" if leading_zeros > 0 else str(num)

                if mode == 1:
                    new_name = clean_name.replace(replace_from, replace_to) if replace_from else clean_name
                    new_name = f"{prefix}{new_name}{postfix}"
                    if numerate:
                        if number_position == 1:
                            new_name = f"{num_str}{separator}{new_name}"
                        else:
                            new_name = f"{new_name}{separator}{num_str}"
                else:
                    new_name = base_name
                    new_name = f"{prefix}{new_name}{postfix}"
                    if numerate:
                        if number_position == 1:
                            new_name = f"{num_str}{separator}{new_name}"
                        else:
                            new_name = f"{new_name}{separator}{num_str}"

                doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                obj.SetName(new_name)
            doc.EndUndo()
        except:
            doc.EndUndo()
            raise
        c4d.EventAdd()

    def DoCleanup(self):
        cleanup_mode = self.GetInt32(self.ID_CLEANUP_MODE)
        if cleanup_mode == 0:
            return

        objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
        if not objects:
            gui.MessageDialog("No objects selected!")
            return

        doc.StartUndo()
        try:
            for obj in objects:
                old_name = obj.GetName()
                new_name = self.CleanupName(old_name, cleanup_mode)
                if new_name != old_name:
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
                    obj.SetName(new_name)
            doc.EndUndo()
        except:
            doc.EndUndo()
            raise
        c4d.EventAdd()
        self.UpdatePreview()

    def CoreMessage(self, id, msg):
        if id == c4d.EVMSG_CHANGE:
            current_selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
            if current_selection != self.last_selection:
                self.last_selection = current_selection
                self.UpdatePreview()
        return True

    def Command(self, id, msg):
        if id == self.ID_PRESET:
            preset_value = self.GetInt32(self.ID_PRESET)
            # New mapping: 0=Default, 1=_Low, 2=_High, 3=_LP, 4=_HP
            preset_map = {0: "", 1: "_Low", 2: "_High", 3: "_LP", 4: "_HP"}
            if preset_value == 0:
                self.SetInt32(self.ID_NUMERATE, 1)
                self.SetString(self.ID_POSTFIX, "")
            else:
                self.SetString(self.ID_POSTFIX, preset_map[preset_value])
                self.SetInt32(self.ID_NUMERATE, 0)
            self.UpdateControls()
            self.SaveSettings()
            return True
        elif id in [self.ID_NUMERATE, self.ID_SEPARATOR, self.ID_MODE, self.ID_CLEANUP_MODE, self.ID_NUMBER_DIRECTION, self.ID_NUMBER_POSITION, self.ID_REMOVE_MODE]:
            self.UpdateControls()
            return True
        elif id in [self.ID_START_NUMBER, self.ID_PREFIX, self.ID_BASENAME, self.ID_POSTFIX, self.ID_REPLACE_FROM, self.ID_REPLACE_TO, self.ID_CUSTOM_SEPARATOR, self.ID_REMOVE_COUNT]:
            self.UpdatePreview()
            self.SaveSettings()
            return True
        elif id == self.ID_BUTTON_RENAME:
            self.DoRename()
            return True
        elif id == self.ID_BUTTON_CLEANUP:
            self.DoCleanup()
            return True
        elif id == self.ID_BUTTON_REMOVE:
            self.DoRemove()
            return True
        elif id == self.ID_BUTTON_RESET:
            result = gui.MessageDialog("Are you sure you want to reset all settings to default values?", c4d.GEMB_YESNO)
            if result == c4d.GEMB_R_YES:
                self.ResetToDefaults()
            return True
        return False

def main():
    dlg = RenameDialog()
    dlg.Open(c4d.DLG_TYPE_ASYNC, defaultw=0, defaulth=0)

if __name__ == '__main__':
    main()
