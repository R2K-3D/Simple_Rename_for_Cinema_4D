import c4d
from c4d import gui
import re

class RenameDialog(gui.GeDialog):
    ID_CLEANUP_MODE = 3005
    ID_NUMERATE = 1500
    ID_SEPARATOR = 1100
    ID_START_NUMBER = 1000
    ID_MODE = 1300
    ID_PREFIX = 1003
    ID_BASENAME = 1001
    ID_POSTFIX = 1002
    ID_REPLACE_FROM = 1400
    ID_REPLACE_TO = 1401
    ID_BUTTON_RENAME = 1200
    ID_BUTTON_CLEANUP = 1201
    ID_PREVIEW = 1601
    ID_CUSTOM_SEPARATOR = 2011
    ID_CUSTOM_SEPARATOR_LABEL = 2010
    ID_NUMBER_DIRECTION = 2020
    ID_NUMBER_POSITION = 2021
    ID_TIMER = 5000  # ID для таймера

    def CreateLayout(self):
        self.SetTitle("Simple Rename by R2K-3D v1.06 (Beta)")

        self.GroupBegin(3000, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=2, rows=1)

        # Левая колонка
        self.GroupBegin(3001, c4d.BFH_SCALEFIT | c4d.BFV_TOP, cols=1)
        self.AddStaticText(2006, c4d.BFH_LEFT, name="Numbering:")
        self.AddComboBox(self.ID_NUMERATE, c4d.BFH_SCALEFIT)
        self.AddChild(self.ID_NUMERATE, 1, "Yes")
        self.AddChild(self.ID_NUMERATE, 0, "No")

        self.AddStaticText(2002, c4d.BFH_LEFT, name="Separator:")
        self.AddComboBox(self.ID_SEPARATOR, c4d.BFH_SCALEFIT)
        self.AddChild(self.ID_SEPARATOR, 0, "_ (Underscore)")
        self.AddChild(self.ID_SEPARATOR, 1, "- (Dash)")
        self.AddChild(self.ID_SEPARATOR, 2, "Space")
        self.AddChild(self.ID_SEPARATOR, 3, "(No Separator)")
        self.AddChild(self.ID_SEPARATOR, 4, "Custom")

        self.AddStaticText(self.ID_CUSTOM_SEPARATOR_LABEL, c4d.BFH_LEFT, name="Custom Separator:")
        self.AddEditText(self.ID_CUSTOM_SEPARATOR, c4d.BFH_SCALEFIT)

        self.AddStaticText(2000, c4d.BFH_LEFT, name="Start Number (e.g. 1):")
        self.AddEditText(self.ID_START_NUMBER, c4d.BFH_SCALEFIT)

        self.AddStaticText(2100, c4d.BFH_LEFT, name="Number Direction:")
        self.AddComboBox(self.ID_NUMBER_DIRECTION, c4d.BFH_SCALEFIT)
        self.AddChild(self.ID_NUMBER_DIRECTION, 0, "Top to Bottom (default)")
        self.AddChild(self.ID_NUMBER_DIRECTION, 1, "Bottom to Top")

        self.AddStaticText(2101, c4d.BFH_LEFT, name="Number Position:")
        self.AddComboBox(self.ID_NUMBER_POSITION, c4d.BFH_SCALEFIT)
        self.AddChild(self.ID_NUMBER_POSITION, 0, "After name (default)")
        self.AddChild(self.ID_NUMBER_POSITION, 1, "Before name")

        self.AddStaticText(2102, c4d.BFH_LEFT, name="Cleanup Mode:")
        self.AddComboBox(self.ID_CLEANUP_MODE, c4d.BFH_SCALEFIT)
        self.AddChild(self.ID_CLEANUP_MODE, 0, "Off")
        self.AddChild(self.ID_CLEANUP_MODE, 1, "From end (default)")
        self.AddChild(self.ID_CLEANUP_MODE, 2, "From start")

        self.GroupEnd()

        # Правая колонка
        self.GroupBegin(3002, c4d.BFH_SCALEFIT | c4d.BFV_TOP, cols=1)
        self.AddStaticText(2003, c4d.BFH_LEFT, name="Rename Mode:")
        self.AddComboBox(self.ID_MODE, c4d.BFH_SCALEFIT)
        self.AddChild(self.ID_MODE, 0, "Replace name (All)")
        self.AddChild(self.ID_MODE, 1, "Replace & Prefix/Postfix")

        self.AddStaticText(2007, c4d.BFH_LEFT, name="Name Prefix:   ___name")
        self.AddEditText(self.ID_PREFIX, c4d.BFH_SCALEFIT)

        self.AddStaticText(2001, c4d.BFH_LEFT, name="Base Name:")
        self.AddEditText(self.ID_BASENAME, c4d.BFH_SCALEFIT)

        self.AddStaticText(2008, c4d.BFH_LEFT, name="Name Postfix:   name___")
        self.AddEditText(self.ID_POSTFIX, c4d.BFH_SCALEFIT)

        self.AddStaticText(2004, c4d.BFH_LEFT, name="Replace in Name:")
        self.AddEditText(self.ID_REPLACE_FROM, c4d.BFH_SCALEFIT)

        self.AddStaticText(2005, c4d.BFH_LEFT, name="With:")
        self.AddEditText(self.ID_REPLACE_TO, c4d.BFH_SCALEFIT)
        self.GroupEnd()

        self.GroupEnd()

        self.AddSeparatorH(10)

        # Кнопки Rename и Cleanup рядом
        self.GroupBegin(4000, c4d.BFH_CENTER, cols=2)
        self.AddButton(self.ID_BUTTON_CLEANUP, c4d.BFH_SCALE, name="Cleanup Names")
        self.AddButton(self.ID_BUTTON_RENAME, c4d.BFH_SCALE, name="Rename Selected")
        self.GroupEnd()

        self.AddSeparatorH(10)
        self.AddStaticText(1600, c4d.BFH_LEFT, name="Preview (up to 3 objects):")
        self.AddMultiLineEditText(self.ID_PREVIEW, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, initw=600, inith=90)
        self.AddSeparatorH(10)

        self.GroupBegin(4001, c4d.BFH_RIGHT, cols=1)
        self.AddStaticText(1602, c4d.BFH_RIGHT, name="Simple Rename by R2K-3D v1.06 (Beta) thx github.com/SPluzh ")
        self.GroupEnd()

        # Запускаем таймер обновления превью
        self.SetTimer(self.ID_TIMER, 500)  # обновлять каждые 500 мс

        return True

    def InitValues(self):
        self.SetInt32(self.ID_NUMERATE, 1)
        self.SetInt32(self.ID_SEPARATOR, 1)
        self.SetString(self.ID_CUSTOM_SEPARATOR, "-")
        self.SetString(self.ID_START_NUMBER, "1")  # С 1, без ведущих нулей
        self.SetInt32(self.ID_MODE, 0)
        self.SetString(self.ID_PREFIX, "")
        self.SetString(self.ID_BASENAME, "NewName")
        self.SetString(self.ID_POSTFIX, "")
        self.SetString(self.ID_REPLACE_FROM, "")
        self.SetString(self.ID_REPLACE_TO, "")
        self.SetInt32(self.ID_NUMBER_DIRECTION, 0)
        self.SetInt32(self.ID_NUMBER_POSITION, 0)
        self.SetInt32(self.ID_CLEANUP_MODE, 0)  # Off по умолчанию

        self.UpdateControls()
        self.UpdatePreview()
        return True

    def UpdateControls(self):
        mode = self.GetInt32(self.ID_MODE)
        numerate = self.GetInt32(self.ID_NUMERATE)
        sep_index = self.GetInt32(self.ID_SEPARATOR)
        cleanup_mode = self.GetInt32(self.ID_CLEANUP_MODE)

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

        # Кнопка Cleanup активна только если Cleanup Mode != Off
        self.Enable(self.ID_BUTTON_CLEANUP, cleanup_mode != 0)

        self.UpdatePreview()

    def CleanupName(self, name, mode):
        if mode == 1:  # From end - оставить от начала до последней буквы включительно
            matches = list(re.finditer(r"[A-Za-zА-Яа-я]", name))
            if matches:
                last_pos = matches[-1].start()
                return name[:last_pos + 1]
        elif mode == 2:  # From start - оставить от первой буквы до конца
            matches = list(re.finditer(r"[A-Za-zА-Яа-я]", name))
            if matches:
                first_pos = matches[0].start()
                return name[first_pos:]
        return name

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

        # Добавим разделитель в превью
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

    def Command(self, id, msg):
        if id == self.ID_NUMERATE or id == self.ID_SEPARATOR or id == self.ID_MODE or id == self.ID_CLEANUP_MODE or id == self.ID_NUMBER_DIRECTION or id == self.ID_NUMBER_POSITION:
            self.UpdateControls()
            self.UpdatePreview()
            return True
        elif id == self.ID_START_NUMBER or id == self.ID_PREFIX or id == self.ID_BASENAME or id == self.ID_POSTFIX or id == self.ID_REPLACE_FROM or id == self.ID_REPLACE_TO or id == self.ID_CUSTOM_SEPARATOR:
            self.UpdatePreview()
            return True
        elif id == self.ID_BUTTON_RENAME:
            self.DoRename()
            self.UpdatePreview()
            return True
        elif id == self.ID_BUTTON_CLEANUP:
            self.DoCleanup()
            return True
        elif id == self.ID_TIMER:
            # Автообновление превью
            self.UpdatePreview()
            return True

        return False

def main():
    dlg = RenameDialog()
    dlg.Open(c4d.DLG_TYPE_ASYNC, defaultw=0, defaulth=0)

if __name__ == '__main__':
    main()