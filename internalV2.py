import tkinter

button_width: int = 7
button_height: int = 1
windows_width = 500
windows_height = 314
edge_distance = 20


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
    crawl_button.place(x=int(windows_width / 3 * 2), y=int(windows_height - edge_distance - button_height))

    import_xlsx_button = tkinter.Button(root_windows,
                                        text="Import form",
                                        height=button_height,
                                        width=button_width)
    import_xlsx_button.place(x=int(windows_width / 3), y=int(windows_height - edge_distance - button_height))


    root_windows.mainloop()


