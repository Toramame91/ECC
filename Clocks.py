import tkinter as tk
import time
from datetime import datetime


class EorzeanClock(object):
    def __init__(self, frame):
        self._hour = 0
        self._minute = 0
        self._second = 0
        self._eorzeanHour = 0
        self._eorzeanMinute = 0
        self._frame = frame

    @property
    def getHour(self):
        return self._hour

    @property
    def getMinute(self):
        return self._minute

    @property
    def getSecond(self):
        return self._second

    # Function for calculating Eorzea time and displaying on a label
    def EorzeaTimeDisplay(self):
        localEpoch = int(time.time() * 1000)  # local epoch time
        epoch = localEpoch * 20.57142857142857  # local epoch times 3600/175 for eorzea time conversion
        minutes = int((epoch / (1000 * 60)) % 60)  # ticks from epoch calculated into minutes
        hours = int((epoch / (1000 * 60 * 60)) % 24)  # ticks from epoch calculated into hours
        self._eorzeanHour = f'{hours:02d}'  # format hours to display 2 digits
        self._eorzeanMinute = f'{minutes:02d}'  # format minutes to display 2 digits
        display = str(self._eorzeanHour) + ":" + str(self._eorzeanMinute)  # combine hours and minutes into one string
        # label for time placement
        timerLbl = tk.Label(self._frame, text="E.T.  " + display, bg='#443E3E', fg='white', font=('calibri', 20, 'bold'))
        timerLbl.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        timerLbl.after(2550, self.EorzeaTimeDisplay)

    # Function for local time
    def LocalTimeDisplay(self):
        now = datetime.now()  # get current local time
        current_time = now.strftime("%H:%M:%S")  # display local time in Hour:Minute:Second format
        # label for time placement
        ctLabel = tk.Label(self._frame, text="L.T.  " + current_time, bg='#443E3E', fg='white',
                           font=('calibri', 20, 'bold'))
        ctLabel.grid(row=1, column=3, columnspan=2, sticky=tk.W)
        ctLabel.after(1000, self.LocalTimeDisplay)

    def FindEorzeaTime(self):
        localEpoch = int(time.time() * 1000)  # local epoch time
        epoch = localEpoch * 20.57142857142857  # local epoch times 3600/175 for eorzea time conversion

        return epoch
