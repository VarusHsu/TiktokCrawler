import tkinter
from tkinter import filedialog

# widget size
button_width: int = 7
button_height: int = 1
windows_width = 500
windows_height = 314
edge_distance = 20
log_list_box_width: int = 60
log_list_box_height: int = 13

# widget anchor
crawl_button_anchor_x: int = 100
crawl_button_anchor_y: int = 283
import_xlsx_button_anchor_x: int = 300
import_xlsx_button_anchor_y: int = 283
log_list_box_anchor_x = 7
log_list_box_anchor_y = 20

# widget instance
root_windows: tkinter.Tk
crawl_button: tkinter.Button
import_xlsx_button: tkinter.Button
log_list_box: tkinter.Listbox

# global
file_name: str = ""
log_list: [] = ["[WELCOME] QAQ"]


def render_ui():
    global button_height
    global button_width

    global root_windows
    global crawl_button
    global import_xlsx_button
    global log_list_box

    global log_list

    root_windows = tkinter.Tk()
    root_windows.title("短视频播放量爬虫（0.0）")
    root_windows.geometry(f"{windows_width}x{windows_height}")
    root_windows.resizable(False, False)

    crawl_button = tkinter.Button(root_windows,
                                  text="Begin crawl",
                                  height=button_height,
                                  width=button_width)
    crawl_button.place(x=crawl_button_anchor_x, y=crawl_button_anchor_y)

    import_xlsx_button = tkinter.Button(root_windows,
                                        text="Import form",
                                        height=button_height,
                                        width=button_width,
                                        command=handle_import_xlsx_button_click)
    import_xlsx_button.place(x=import_xlsx_button_anchor_x, y=import_xlsx_button_anchor_y)

    log_list_box = tkinter.Listbox(root_windows,
                                   height=log_list_box_height,
                                   width=log_list_box_width)
    log_list_box.place(x=log_list_box_anchor_x, y=log_list_box_anchor_y)
    log_list_box.insert("end", log_list[0])
    root_windows.mainloop()


def handle_import_xlsx_button_click() -> int:
    """
    :return:
        1: import successful
        0: import cancel
        -1: file isn't xlsx or file already corrupted
    """
    global file_name
    file = tkinter.filedialog.askopenfilename(title="import xlsx file", filetypes=[('xlsx', '*.xlsx')])
    if type(file) is tuple or file_name == file:
        return 0
