import tkinter as tk
import tkinter.ttk as ttk

#class for window
class Win(tk.Tk):

    #window configuation and initiation
    def __init__(self):
        #basic window configurations
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.overrideredirect(True)
        self.grid_propagate(False)
        self.wm_geometry("1280x800")   #window size
        self.configure(background="#858585") #window background color
        self.minsize(400, 400) #minimum size for window

        #set starting position of window to be 0,0
        self.x = 0  
        self.y = 0

        #create and configure custom title bar
        title_bar = tk.Frame(self, height=25, bg='#443E3E', relief='raised', bd=1)
        title_bar.grid(row=0, column=0, sticky='ew')
        tk.Button(title_bar, text='x', command=self.destroy).pack(fill='x', side="right")
             
        #bind mouse button 1 to move window using title bar
        title_bar.bind('<ButtonPress-1>', self.button_press)
        title_bar.bind('<B1-Motion>', self.move_window)

        #initialize navigation bar frame
        sideBarFrame = tk.Frame(self, height=800,width= 250, bg='#443E3E', relief='raised', bd=1)   
        mainConsoleFrame = tk.Frame(self, height=800,width= 1300, bg='#443E3E', relief='raised', bd=1)

        #configure grid layout        
        sideBarFrame.grid(row=1,column=0,rowspan=4, sticky='w') 
        mainConsoleFrame.grid(row=1,column=1)
        

    #FRAMES

   
    #function for moving window
    def move_window(self, event):
        x = self.winfo_pointerx() - self.x
        y = self.winfo_pointery() - self.y
        self.geometry('+{}+{}'.format(x, y))

    #function for button press
    def button_press(self, event):
        self.x = event.x
        self.y = event.y


win = Win()


win.mainloop()