import tkinter

button_width: int = 7
button_height: int = 1
windows_width = 500
windows_height = 314
edge_distance = 20

crawl_button_anchor_x: int = 100
crawl_button_anchor_y: int = 283
import_xlsx_button_anchor_x: int = 300
import_xlsx_button_anchor_y: int = 283


root_windows: tkinter.Tk
crawl_button: tkinter.Button
import_xlsx_button: tkinter.Button


def render_ui():

    global button_height
    global button_width

    global root_windows
    global crawl_button
    global import_xlsx_button

    root_windows = tkinter.Tk()
    root_windows.title("短视频播放量爬虫（0.0）")
    root_windows.geometry(f"{windows_width}x{windows_height}")

    crawl_button = tkinter.Button(root_windows,
                                  text="Begin crawl",
                                  height=button_height,
                                  width=button_width)
    crawl_button.place(x=crawl_button_anchor_x, y=crawl_button_anchor_y)

    import_xlsx_button = tkinter.Button(root_windows,
                                        text="Import form",
                                        height=button_height,
                                        width=button_width)
    import_xlsx_button.place(x=import_xlsx_button_anchor_x, y=import_xlsx_button_anchor_y)

    root_windows.mainloop()


