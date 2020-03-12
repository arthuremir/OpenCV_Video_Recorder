import time
import tkinter as tk
from tkinter import font
from tkinter import Label, StringVar, Entry, Button, IntVar, OptionMenu, filedialog
from PIL import Image, ImageTk

import cv2

from utils.config_initializer import get_cameras

location = ""
save_path = ""
cameras = get_cameras()


class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.bind('<Escape>', lambda e: self.quit())

        window_size = (640, 520)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.args = {}

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        x_shift = int(self.winfo_screenwidth() / 2 - window_size[0] / 2)
        y_shift = int(self.winfo_screenheight() / 2 - window_size[1] / 2)

        self.geometry("{}x{}+{}+{}".format(window_size[0], window_size[1], x_shift, y_shift))

        self.frames = dict()
        self.frames["StartPage"] = StartPage(args=self.args, parent=self.container, controller=self)
        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):

        if page_name in self.frames:
            self.frames[page_name].tkraise()
            if page_name == "RecordPage":
                self.frames[page_name].init_capture()
        else:
            # TODO refactor this
            frame = globals()[page_name](args=self.args, parent=self.container, controller=self)

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, args, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.configure(background='#2D303D')
        self.controller.title("CMC Video Recorder")

        camera_options = cameras.keys()

        global location
        location = StringVar()

        location.set('hall')

        loc_label = Label(self,
                          text="Choose a camera location",
                          background="#2D303D",
                          foreground="#ffffff",
                          padx="20",
                          pady="10",
                          font="16")

        loc_menu = OptionMenu(self, location, *camera_options)
        loc_menu.config(background="#21232d",
                        foreground="#ffffff",
                        activebackground="#E95420",
                        padx="20",
                        pady="10",
                        font="16")

        loc_label.place(relx=.25, rely=.25, anchor="c")
        loc_menu.place(relx=.25, rely=.35, anchor="c")

        path_label = Label(self,
                           text="Choose a path to save video",
                           background="#2D303D",
                           foreground="#ffffff",
                           padx="20",
                           pady="10",
                           font="16")

        button_path = Button(self,
                             text="Choose",
                             command=self.get_path,
                             bd=0,
                             highlightthickness=0,
                             background="#21232d",
                             foreground="#ffffff",
                             activebackground="#E95420",
                             padx="20",
                             pady="10",
                             font="16")

        path_label.place(relx=.75, rely=.25, anchor="c")
        button_path.place(relx=.75, rely=.35, anchor="c")

        def change_dropdown(*args):
            print(location.get())

        # link function to change dropdown
        location.trace('w', change_dropdown)

        button_record = Button(self,
                               text="Load camera",
                               command=self.load_camera,
                               bd=0,
                               highlightthickness=0,
                               background="#21232d",
                               foreground="#ffffff",
                               activebackground="#E95420",
                               padx="20",
                               pady="10",
                               font="16")
        button_record.place(relx=.5, rely=.5, anchor="c")

    def load_camera(self):
        self.controller.show_frame('RecordPage')

    def get_path(self):
        global save_path
        save_path = filedialog.askdirectory(initialdir="", title="Select file")


class RecordPage(tk.Frame):

    def __init__(self, args, parent, controller):
        # print(location.get(), save_path)
        tk.Frame.__init__(self, parent)
        self.args = args

        self.controller = controller

        self.cam_wrapper = Label(self)
        self.cam_wrapper.pack()

        button_start = Button(self,
                              text="Start recording",
                              command=self.start_recording,
                              bd=0,
                              highlightthickness=0,
                              background="green",
                              foreground="#ffffff",
                              padx="90",
                              pady="4",
                              font="16")
        button_start.place(relx=0.25, rely=0.961, anchor="c")

        button_end = Button(self,
                            text="Finish recording",
                            command=self.finish_recording,
                            bd=0,
                            highlightthickness=0,
                            background="#C60000",
                            foreground="#ffffff",
                            padx="90",
                            pady="4",
                            font="16")
        button_end.place(relx=0.75, rely=0.961, anchor="c")

        self.init_capture()

    def init_capture(self):
        camera_rtsp = cameras[location.get()]
        print(camera_rtsp)
        self.cap = cv2.VideoCapture(camera_rtsp)
        self.stop_flag = 0

        self.update_cam()

    def update_cam(self):
        res, frame = self.cap.read()
        # frame = cv2.flip(frame, 1)
        if res:
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            self.cam_wrapper.imgtk = img_tk
            self.cam_wrapper.configure(image=img_tk)
        if self.stop_flag:
            self.disable_frame()
            return
        self.cam_wrapper.after(1, self.update_cam)

    def start_recording(self):
        pass

    def finish_recording(self):
        self.controller.show_frame("StartPage")
