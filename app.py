import tkinter as tk
from playsound import playsound
from win11toast import toast
import threading
import time
import os
import sys

WORK_TIME = 10   # 10 seconds for testing
BREAK_TIME = 5   # 5 seconds for testing

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏱ Pomodoro Timer")
        self.root.geometry("320x180")
        self.root.resizable(False, False)

        self.running = False
        self.remaining = WORK_TIME
        self.is_work_session = True

        # UI
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Arial", 16))
        self.label.pack(pady=10)

        self.timer_label = tk.Label(root, text="00:10", font=("Arial", 28))
        self.timer_label.pack()

        self.start_button = tk.Button(root, text="Start", width=18, command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", width=18, command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack()

    def get_sound_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "beep.wav")

    def play_sound(self):
        try:
            wav_path = self.get_sound_path()
            playsound(wav_path)
        except Exception as e:
            print("Sound Error:", e)

    def notify(self, title, message):
        try:
            toast(title=str(title), body=str(message), duration="short")
        except Exception as e:
            print("Notification Error:", e)

    def start_timer(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.timer_loop, daemon=True).start()

    def stop_timer(self):
        self.running = False
        self.remaining = WORK_TIME
        self.is_work_session = True
        self.update_timer_label()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def timer_loop(self):
        while self.running:
            if self.remaining > 0:
                mins = self.remaining // 60
                secs = self.remaining % 60
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                time.sleep(1)
                self.remaining -= 1
            else:
                # Session finished
                self.play_sound()
                if self.is_work_session:
                    self.notify("Work Session Complete", "Take a short break! 🌿")
                    self.remaining = BREAK_TIME
                else:
                    self.notify("Break Over", "Time to get back to work! 💪")
                    self.remaining = WORK_TIME
                self.is_work_session = not self.is_work_session
        self.update_timer_label()

    def update_timer_label(self):
        mins = self.remaining // 60
        secs = self.remaining % 60
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
