import tkinter
from tkinter import ttk

button_width: int = 7
button_height: int = 1


root_windows: tkinter.Tk
crawl_button: tkinter.Button
import_xlsx_button: tkinter.Button

pixel_virtual: tkinter.PhotoImage


def render_ui():

    global button_height
    global button_width

    global root_windows
    global crawl_button
    global import_xlsx_button

    global pixel_virtual

    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    root_windows = tkinter.Tk()
    root_windows.title("短视频播放量爬虫（0.0）")
    root_windows.geometry("500x314")

    pixel_virtual = tkinter.PhotoImage(width=1, height=1)

    crawl_button = tkinter.Button(root_windows,
                                  text="Begin crawl",
                                  height=button_height,
                                  width=button_width)
    crawl_button.pack()




    root_windows.mainloop()


