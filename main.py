from tkinter import * 
from tkinter import messagebox
import time
import requests
import random
import threading


End_POINT = "https://type.fit/api/quotes"


class TypeSpeed:
    def __init__(self):
        self.window = Tk()
        self.window.title("QuickFingers")
        self.window.geometry("800x600")

        self.text = self.random_sentence()

        self.frame = Frame(self.window)

        self.sample_label = Label(self.frame, text=self.text, font=("Helvetica", 24))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyPress>", self.start)

        self.speed_label = Label(self.frame, text="Speed: \n0.00 CPS\n0.00 CPM", font=("Helvetica", 24))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.rest_button = Button(self.frame, text="Rest", command=self.rest)
        self.rest_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False

        self.window.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()

        if not self.sample_label.cget("text").startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        
        if self.input_entry.get() == self.sample_label.cget("text")[:-1]:
            self.running = False
            self.input_entry.config(fg="green")


    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM")
    
    def rest(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0.00 CPS\n0.00 CPM")
        self.text = self.random_sentence()
        self.sample_label.config(self.text)
        self.input_entry.delete(0, END)


    def random_sentence(self):
        response = requests.get(End_POINT)
        sentence = random.choice(response.json())["text"]
        return sentence

TypeSpeed()