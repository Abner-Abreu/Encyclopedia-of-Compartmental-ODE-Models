import tkinter as tk
from gui.app import App

import services as ser
import database as data

def main():
    data.init_db()
    root = tk.Tk()
    service = ser.ServiceHandler()  
    app = App(root, service)
    root.mainloop()
    
if __name__ == '__main__':
    main()