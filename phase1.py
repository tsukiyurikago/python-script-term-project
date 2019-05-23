import tkinter as tk # Python 3

timer = 5.0
opacity = 1.0

def myupdate():
    global opacity
    global root
    opacity -=0.01
    root.attributes('-alpha', opacity)
    root.after(16,myupdate)

root = tk.Tk()
root.attributes('-alpha',opacity)
# The image must be stored to Tk or it will be garbage collected.
root.image = tk.PhotoImage(file='res\img\logosample0.png')
label = tk.Label(root, image=root.image, bg='white')
root.overrideredirect(True)
root.geometry("+250+250")
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")
label.pack()
myupdate()
root.mainloop()