#! python3

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from config import themes
from config import currentTheme
import tkinter.filedialog
import tkinter.messagebox as tmb
import os
import pprint

#-----------------------------------------------------------------------------------------------------------#

# Image directories

images_dir = "images\\"
config_dir = "config\\"

# Under file menu
new_file_image_dir  = os.path.join(os.getcwd(), images_dir + "new_file.png")
open_file_image_dir = os.path.join(os.getcwd(), images_dir + "open_file.png")
save_file_image_dir = os.path.join(os.getcwd(), images_dir + "save.png")

# Under edit menu 
undo_image_dir      = os.path.join(os.getcwd(), images_dir + "undo.png")
redo_image_dir      = os.path.join(os.getcwd(), images_dir + "redo.png")
cut_image_dir       = os.path.join(os.getcwd(), images_dir + "cut.png")
copy_image_dir      = os.path.join(os.getcwd(), images_dir + "copy.png")
paste_image_dir     = os.path.join(os.getcwd(), images_dir + "paste.png")
find_image_dir      = os.path.join(os.getcwd(), images_dir + "find_text.png")
replace_image_dir   = os.path.join(os.getcwd(), images_dir + "replace_text.png")

# Under about menu
about_image_dir     = os.path.join(os.getcwd(), images_dir + "about.png")
help_image_dir      = os.path.join(os.getcwd(), images_dir + "help.png")


#-----------------------------------------------------------------------------------------------------------#

# Global Variables
file_name = None
PROGRAM_NAME = "Blueprint text editor"

#-----------------------------------------------------------------------------------------------------------#

# Initiate root
root = Tk()
root.title("Untitled - {}".format(PROGRAM_NAME))
tabs = ttk.Notebook(master = root)

#-----------------------------------------------------------------------------------------------------------#

# Open all images
new_file_image = Image.open(fp=new_file_image_dir)
new_file_ph = ImageTk.PhotoImage(image=new_file_image)
open_file_image = Image.open(fp=open_file_image_dir)
open_file_ph = ImageTk.PhotoImage(image=open_file_image)
save_file_image = Image.open(fp=save_file_image_dir)
save_file_ph = ImageTk.PhotoImage(image=save_file_image)
undo_image = Image.open(fp=undo_image_dir)
undo_ph = ImageTk.PhotoImage(image=undo_image)
redo_image = Image.open(fp=redo_image_dir)
redo_ph = ImageTk.PhotoImage(image=redo_image)
cut_image = Image.open(fp=cut_image_dir)
cut_ph = ImageTk.PhotoImage(image=cut_image)
copy_image = Image.open(fp=copy_image_dir)
copy_ph = ImageTk.PhotoImage(image=copy_image)
paste_image = Image.open(fp=paste_image_dir)
paste_ph = ImageTk.PhotoImage(image=paste_image)
find_image = Image.open(fp=find_image_dir)
find_ph = ImageTk.PhotoImage(image=find_image)
replace_image = Image.open(fp=replace_image_dir)
replace_ph = ImageTk.PhotoImage(image=replace_image)
about_image = Image.open(fp=about_image_dir)
about_ph = ImageTk.PhotoImage(image=about_image)
help_image = Image.open(fp=help_image_dir)
help_ph = ImageTk.PhotoImage(image=help_image)

icons = ("new_file", "open_file", "save", "cut", "copy",
         "paste", "undo", "redo", "find_text", "replace_text")

#-----------------------------------------------------------------------------------------------------------#

# UI Variables
content = ""
show_line_number = IntVar()
show_line_number.set(1)
show_cursor_info = BooleanVar()
to_highlight_line = BooleanVar()
word_wrap = BooleanVar()
get_theme = StringVar()

#-----------------------------------------------------------------------------------------------------------#

# Define all callbacks

def change_title(event = None):
    if not file_name:
        root.title("* Untitled - {}".format(PROGRAM_NAME))
    else:
        root.title("* {} - {}".format(os.path.basename(file_name), PROGRAM_NAME))

def search_output(needle, if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove("match", "1.0", END)
    matches_found = 0
    if needle:
        start_pos = "1.0"
        while True:
            start_pos = content_text.search(pattern = needle, index = start_pos, nocase = if_ignore_case, stopindex = END)
            if not start_pos:
                break
            end_pos = "{}+{}c".format(start_pos, len(needle))
            content_text.tag_add("match", start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config(tagName = "match", foreground = "red", background = "yellow")
    search_box.focus_set()
    search_toplevel.title("{} matches found.".format(matches_found))


def new_file(event = None):
    root.title(PROGRAM_NAME)
    global file_name
    file_name = None
    content_text.delete(1.0, END)

def open_file(event = None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension = ".txt",
        filetypes = [
            ("All Files", "*.*"),
            ("CSS Files", "*.css"),
            ("JavaScript Files", ".js"),
            ("JSON Files", "*.json"),
            ("HTML Files", "*.html"),
            ("Markdown Files", "*.md"),
            ("Python Files", "*.py"),
            ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title(string = "{} - {}".format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
            global content
            content = content_text.get(1.0, END)

def save(event = None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"

def save_as(event = None):
    input_file_name = tkinter.filedialog.asksaveasfilename(default = ".txt",
        filetypes = [
            ("All files", "*.txt"),
            ("CSS Files", "*.css"),
            ("JavaScript Files", ".js"),
            ("JSON Files", "*.json"),
            ("HTML Files", "*.html"),
            ("Markdown Files", "*.md"),
            ("Python Files", "*.py"),
            ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title("{} - {}".format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"

def write_to_file(file_name):
    try:
        global content
        content = content_text.get(1.0, END)
        with open(file_name, "w") as the_file:
            the_file.write(content)
    except IOError:
        pass

def exit_editor(event = None):
    if file_name and not (content == content_text.get(1.0, END)):    
        if tkinter.messagebox.askokcancel("Quit", "You are closing the editor. \nSave changes first?"):
            save()
        else:
            root.destroy()
    
def undo(event = None):
    content_text.event_generate(sequence = "<<Undo>>")
    
def redo(event = None):
    content_text.event_generate("<<Redo>>")
    return "break"

def cut(event = None):
    content_text.event_generate(sequence = "<<Cut>>")

def copy(event = None):
    content_text.event_generate(sequence = "<<Copy>>")

def paste(event = None):
    content_text.event_generate(sequence = "<<Paste>>")

def select_all(event = None):
    content_text.tag_add("sel", "1.0", "end")
    return "break"

def find_text(event = None):
    search_toplevel = Toplevel(master = root)
    search_toplevel.title(string = "Find text")
    search_toplevel.transient(master = root)
    search_toplevel.resizable(width = False, height = False)
    search_toplevel.wm_geometry(newGeometry = "275x70")
    Label(master = search_toplevel, text = "Find Text:").grid(row = 0, column = 0, sticky = "e")
    search_entry_widget = Entry(master = search_toplevel, width = 25)
    search_entry_widget.grid(row = 0, column = 1, padx = 2, pady = 2, sticky = "we")
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(master = search_toplevel, text = "Ignore Case", variable = ignore_case_value).grid(row = 1, column = 1, sticky = "e", padx = 2, pady = 2)
    Button(master = search_toplevel, text = "Find All", underline = 0, command = lambda: search_output(search_entry_widget.get(), ignore_case_value.get(), content_text, search_toplevel, search_entry_widget)).grid(row = 0, column = 2, sticky = "e" + "w", padx = 2, pady = 2)
    def close_search_window():
        content_text.tag_remove("match", "1.0", END)
        search_toplevel.destroy()
        search_toplevel.protocol(name = "WM_DELETE_WINDOW", func = close_search_window)
        return "break"

def replace_text(event = None):
    match_word_value = IntVar()
    match_case_value = IntVar()
    wrap_around_value = IntVar()
    direction_up = IntVar()
    direction_down = IntVar()
    replace_toplevel = Toplevel(master = root)
    replace_toplevel.title(string = "Replace Text")
    replace_toplevel.transient(master = root)
    replace_toplevel.resizable(width = False, height = False)
    Label(master = replace_toplevel, text = "Find Text:").grid(row = 0, column = 0, sticky = "e")
    find_entry_widget = Entry(master = replace_toplevel, width = 25)
    find_entry_widget.grid(row = 0, column = 1, padx = 2, pady = 2, sticky = "we", columnspan = 9)
    find_entry_widget.focus_set()
    Label(master = replace_toplevel, text = "Replace With:").grid(row = 1, column = 0, sticky = "e")
    replace_entry_widget = Entry(master = replace_toplevel, width = 25)
    replace_entry_widget.grid(row = 1, column = 1, padx = 2, pady = 2, sticky = "we", columnspan = 10)
    Checkbutton(master = replace_toplevel, text = "Match Whole Word Only", variable = match_word_value).grid(row = 2, column = 1, columnspan = 4, sticky = "w")
    Checkbutton(master = replace_toplevel, text = "Match Case", variable = match_case_value).grid(row = 3, column = 1, columnspan = 4, sticky = "w")
    Checkbutton(master = replace_toplevel, text = "Wrap Around", variable = wrap_around_value).grid(row = 4, column = 1, columnspan = 4, sticky = "w")
    Label(master = replace_toplevel, text = "Direction:").grid(row = 2, column = 6, sticky = "w")
    Radiobutton(master = replace_toplevel, text = "Up", variable = direction_up).grid(row = 3, column = 6, columnspan = 6, sticky = "w")
    Radiobutton(master = replace_toplevel, text = "Down", variable = direction_down).grid(row = 3, column = 7, columnspan = 3, sticky = "e")
    Button(master = replace_toplevel, text = "Find", underline = 0).grid(row = 0, column = 11, sticky = "e" + "w", padx = 2, pady = 2)
    Button(master = replace_toplevel, text = "Find All", underline = 0).grid(row = 1, column = 11, sticky = "e" + "w", padx = 2)
    Button(master = replace_toplevel, text = "Replace", underline = 0).grid(row = 2, column = 11, sticky = "e" + "w", padx = 2)
    Button(master = replace_toplevel, text = "Replace All", underline = 0).grid(row = 3, column = 11, sticky = "e" + "w", padx = 2)

def display_about_messagebox(event = None):
    tmb.showinfo(title = "About", 
        message = "{}{}".format(PROGRAM_NAME, "\nVersion: 0.0.1"))

def display_help_messagebox(event = None):
    tmb.showinfo(title = "Help", message = "This section is under construction.")

def on_content_changed(event = None):
    update_line_numbers()
    update_cursor_info_bar()

def get_line_numbers():
    output = ""
    if show_line_number.get():
        row, col = content_text.index("end").split(".")
        for i in range(1, int(row)):
            output += str(i) + "\n"
    return output

def update_line_numbers(event = None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state = "normal")
    line_number_bar.delete("1.0", "end")
    line_number_bar.insert("1.0", line_numbers)
    line_number_bar.config(state = "disabled")

def highlight_line(interval = 100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    content_text.after(ms = interval, func = toggle_highlight)
    
def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")

def toggle_highlight(event = None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()

def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand = "no", fill = None, side = "right", anchor = "se")
    else:
        cursor_info_bar.pack_forget()
    
def update_cursor_info_bar(event = None):
    row, col = content_text.index(INSERT).split(".")
    line_num, col_num = str(int(row)), str(int(col) + 1) # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text = infotext)

def show_popup_menu(event):
    popup_menu.tk_popup(x = event.x_root, y = event.y_root)

def change_theme(event = None):
    selected_theme = get_theme.get()
    theme_colors = themes.all_themes_data.get(selected_theme)
    shortcut_bar.config(
        background = themes.all_themes_data[selected_theme]["shortcut_bar_color"])
    for index, icon in enumerate(icons):
        tool_bar.config(background = themes.all_themes_data[selected_theme]["shortcut_button_color"])
    content_text.config(
        background = themes.all_themes_data[selected_theme]["text_editor_background_color"],
        foreground = themes.all_themes_data[selected_theme]["text_editor_background_color"])
    line_number_bar.config(
        background = themes.all_themes_data[selected_theme]["line_number_background_color"],
        foreground = themes.all_themes_data[selected_theme]["line_number_foreground_color"]
    )
    config_File = open(os.path.join(os.getcwd(), config_dir + "currentTheme.py"), "w+")
    config_File.write("current_theme_color = " + pprint.pformat(theme_colors))
    config_File.close()


#-----------------------------------------------------------------------------------------------------------#

# Initiate objects
shortcut_bar = Frame(
    master = root, 
    height = 25, 
    background = currentTheme.current_theme_color["shortcut_bar_color"])

for index, icon in enumerate(icons):
    icon_dir = os.path.join(os.getcwd(), images_dir + "{}.png".format(icon))
    icon_image = Image.open(fp = icon_dir)
    tool_bar_icon = ImageTk.PhotoImage(image = icon_image)
    cmd = eval(icon)
    tool_bar = Button(
        master = shortcut_bar, 
        image = tool_bar_icon, 
        command = cmd, 
        background = currentTheme.current_theme_color["shortcut_button_color"])
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side = "left")
    
line_number_bar = Text(
    master = root, 
    width = 4, 
    padx = 3, 
    takefocus = 0, 
    border = 0, 
    background = currentTheme.current_theme_color["line_number_background_color"],
    foreground = currentTheme.current_theme_color["line_number_foreground_color"], 
    state = "disabled", 
    wrap = "none")
content_text = Text(
    master = root, 
    wrap = "word", 
    undo = 1,
    background = currentTheme.current_theme_color["text_editor_background_color"],
    foreground = currentTheme.current_theme_color["text_editor_foreground_color"])
menu_bar    = Menu(master = root)
file_menu   = Menu(master = menu_bar, tearoff = 0)
edit_menu   = Menu(master = menu_bar, tearoff = 0)
view_menu   = Menu(master = menu_bar, tearoff = 0)
themes_menu = Menu(master = view_menu, tearoff = 0)
about_menu  = Menu(master = menu_bar, tearoff = 0)
scroll_bar = Scrollbar(master = content_text)
cursor_info_bar = Label(master = content_text, text = "Line: 1 | Column: 1")
popup_menu = Menu(master = content_text,
    background = currentTheme.current_theme_color["cursor_info_background_color"],
    foreground = currentTheme.current_theme_color["cursor_info_foreground_color"]
)
for index in ("cut", "copy", "paste", "undo", "redo"):
    cmd = eval(index)
    popup_menu.add_command(label = index, compound = "left", command = cmd)
popup_menu.add_separator()
popup_menu.add_command(label = "Select All", compound = "left", underline = 7, command = select_all)

#-----------------------------------------------------------------------------------------------------------#

# Add sub-menu and commands


# File Menu
file_menu.add_command(
    label = "New", 
    accelerator = "Ctrl+N", 
    compound = "left", 
    image = new_file_ph, 
    command = new_file)
file_menu.add_command(
    label = "Open", 
    accelerator = "Ctrl+O", 
    compound = "left", 
    image = open_file_ph, 
    command = open_file)
file_menu.add_command(
    label = "Save", 
    accelerator = "Ctrl+S", 
    compound = "left", 
    image = save_file_ph, 
    command = save)
file_menu.add_command(
    label = "Save As", 
    accelerator = "Ctrl+Shift+S", 
    compound = "left", 
    command = save_as)
file_menu.add_separator()
file_menu.add_command(
    label = "Exit", 
    accelerator = "Alt+F4", 
    compound = "left", 
    command = exit_editor)

# Edit Menu
edit_menu.add_command(
    label = "Undo", 
    accelerator = "Ctrl+Z", 
    image = undo_ph, 
    compound = "left",
    command = undo)
edit_menu.add_command(
    label = "Redo", 
    accelerator = "Ctrl+Y", 
    image = redo_ph, 
    compound = "left",
    command = redo)
edit_menu.add_separator()
edit_menu.add_command(
    label = "Cut", 
    accelerator = "Ctrl+X", 
    image = cut_ph, 
    compound = "left", 
    command = cut)
edit_menu.add_command(
    label = "Copy", 
    accelerator = "Ctrl+C", 
    image = copy_ph, 
    compound = "left", 
    command = copy)
edit_menu.add_command(
    label = "Paste", 
    accelerator = "Ctrl+V", 
    image = paste_ph, 
    compound = "left", 
    command = paste)
edit_menu.add_separator()
edit_menu.add_command(
    label = "Find", 
    accelerator = "Ctrl+F", 
    image = find_ph, 
    compound = "left",
    command = find_text)
edit_menu.add_command(
    label = "Replace",
    accelerator = "Ctrl+H",
    image = replace_ph,
    compound = "left",
    command = replace_text)
edit_menu.add_separator()
edit_menu.add_command(
    label = "Select All", 
    accelerator = "Ctrl+A", 
    compound = "left",
    command = select_all)

# View Menu

view_menu.add_checkbutton(
    label = "Show Line Number", 
    variable = show_line_number)
view_menu.add_checkbutton(
    label = "Show Cursor Location at Bottom", 
    variable = show_cursor_info,
    command = show_cursor_info_bar)
view_menu.add_checkbutton(
    label = "Highlight Current Line", 
    variable = to_highlight_line,
    command = toggle_highlight)
view_menu.add_checkbutton(
    label = "Word Wrap", 
    variable = word_wrap)
view_menu.add_separator()
view_menu.add_cascade(
    label = "Themes", 
    menu = themes_menu)

# Themes Menu
themes_menu.add_radiobutton(
    label = "Default", 
    compound = "left",
    variable = get_theme,
    command = change_theme)
themes_menu.add_radiobutton(
    label = "Aquamarine", 
    compound = "left",
    variable = get_theme,
    command = change_theme)
themes_menu.add_radiobutton(
    label = "Bold Beige", 
    compound = "left",
    variable = get_theme,
    command = change_theme)
themes_menu.add_radiobutton(
    label = "Cobalt Blue", 
    compound = "left",
    variable = get_theme,
    command = change_theme)
themes_menu.add_radiobutton(
    label = "Greyscale", 
    compound = "left",
    variable = get_theme,
    command = change_theme)
themes_menu.add_radiobutton(
    label = "Night Mode", 
    compound = "left",
    variable = get_theme,
    command = change_theme)
themes_menu.add_radiobutton(
    label="Olive Green", 
    compound="left",
    variable=get_theme,
    command=change_theme)


# About Menu
about_menu.add_command(
    label = "About", 
    image = about_ph, 
    compound = "left",
    command = display_about_messagebox)
about_menu.add_command(
    label = "Help", 
    accelerator = "F1", 
    image = help_ph, 
    compound = "left",
    command = display_help_messagebox)

#-----------------------------------------------------------------------------------------------------------#

# Add all menu items
menu_bar.add_cascade(label = "File", menu = file_menu)
menu_bar.add_cascade(label = "Edit", menu = edit_menu)
menu_bar.add_cascade(label = "View", menu = view_menu)
menu_bar.add_cascade(label = "About", menu = about_menu)
root.config(menu = menu_bar)


#-----------------------------------------------------------------------------------------------------------#

# content_text bindings

content_text.tag_configure('active_line', background='#eeeee0')
content_text.bind(sequence = "<Any-KeyPress>", func = change_title)
content_text.bind(sequence = "<Any-KeyPress>", func = on_content_changed)
content_text.bind(sequence = "<Control-n>", func = new_file)
content_text.bind(sequence = "<Control-N>", func = new_file)
content_text.bind(sequence = "<Control-o>", func = open_file)
content_text.bind(sequence = "<Control-O>", func = open_file)
content_text.bind(sequence = "<Control-s>", func = save)
content_text.bind(sequence = "<Control-S>", func = save)
content_text.bind(sequence = "<Control-Shift-s>", func = save_as)
content_text.bind(sequence = "<Control-Shift-S>", func = save_as)
content_text.bind(sequence = "<Alt-F4>", func = exit_editor)
content_text.bind(sequence = "<Control-z>", func = undo)
content_text.bind(sequence = "<Control-Z>", func = undo)
content_text.bind(sequence = "<Control-y>", func = redo)
content_text.bind(sequence = "<Control-Y>", func = redo)
content_text.bind(sequence = "<Control-x>", func = cut)
content_text.bind(sequence = "<Control-X>", func = cut)
content_text.bind(sequence = "<Control-c>", func = copy)
content_text.bind(sequence = "<Control-C>", func = copy)
content_text.bind(sequence = "<Control-v>", func = paste)
content_text.bind(sequence = "<Control-V>", func = paste)
content_text.bind(sequence = "<Control-a>", func = select_all)
content_text.bind(sequence = "<Control-A>", func = select_all)
content_text.bind(sequence = "<Control-f>", func = find_text)
content_text.bind(sequence = "<Control-F>", func = find_text)
content_text.bind(sequence = "<Control-h>", func = replace_text)
content_text.bind(sequence = "<Control-H>", func = replace_text)
content_text.bind(sequence = "<KeyPress-F1>", func = display_help_messagebox)
content_text.bind(sequence = "<Button-3>", func = show_popup_menu)

#-----------------------------------------------------------------------------------------------------------#

# Pack the root

shortcut_bar.pack(expand = "no", fill = "x")
line_number_bar.pack(side = "left", fill = "y")
content_text.pack(expand="yes", fill="both")
content_text.focus_set()
content_text.configure(yscrollcommand = scroll_bar.set)
scroll_bar.config(command = content_text.yview)
scroll_bar.pack(side = "right", fill = "y")
cursor_info_bar.pack(expand = NO, fill = None, side = RIGHT, anchor = "se")
root.geometry(newGeometry = "900x600")
root.mainloop()
