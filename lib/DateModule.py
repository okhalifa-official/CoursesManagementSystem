import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
class DatePicker(ttk.Frame):
    """
    Simple DatePicker: an Entry + button. Clicking the button opens a Toplevel
    with a tkcalendar.Calendar. Selecting a date writes it to the entry.
    Avoids DateEntry popup/focus issues.
    """
    def __init__(self, master, date_pattern="yyyy-mm-dd", initial_date=None, **kwargs):
        super().__init__(master, **kwargs)
        self.date_pattern = date_pattern

        # Make the entry readonly so user cannot type
        self.entry = ttk.Entry(self, width=20, state="readonly")
        self.entry.pack(side="left", fill="x", expand=False)

        btn = ttk.Button(self, text="📅", width=3, command=self._open_calendar)
        btn.pack(side="left", padx=(6, 0))

        if initial_date:
            # initial_date expected as "YYYY-MM-DD" or datetime.date
            if isinstance(initial_date, str):
                self.entry.configure(state="normal")
                self.entry.delete(0, tk.END)
                self.entry.insert(0, initial_date)
                self.entry.configure(state="readonly")
            else:
                self.entry.configure(state="normal")
                self.entry.delete(0, tk.END)
                self.entry.insert(0, initial_date.strftime("%Y-%m-%d"))
                self.entry.configure(state="readonly")

        self._cal_win = None

    def _open_calendar(self):
        if self._cal_win:
            return  # Already open

        self._cal_win = tk.Toplevel(self)
        self._cal_win.title("Select Date")

        cal = Calendar(self._cal_win, date_pattern="yyyy-mm-dd")
        cal.pack(padx=10, pady=10)

        def on_select(event):
            date_str = cal.get_date()
            self._set_date(date_str)
            self._cal_win.destroy()
            self._cal_win = None

        ttk.Button(self._cal_win, text="Select", command=on_select).pack(pady=5)

        cal.bind("<<CalendarSelected>>", on_select)

        # bind ESC to close safely
        self._cal_win.bind("<Escape>", lambda e: self._cal_win.destroy())
    
    def _set_date(self, date_str):
        """Safely update the readonly entry."""
        self.entry.configure(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, date_str)
        self.entry.configure(state="readonly")