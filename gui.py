# import tkinter as tk
# window = tk.Tk()
# window.title("Example for Tkinter")  # to define the title
# window.mainloop()
#
# canvas = tk.Canvas(window, width=450, height=500)  # define the size
# canvas.pack()
#
# frame = tk.Frame(window, bg="red")
# frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
#
# menu = tk.Menu(window)
# window.config(menu=menu)
# subMenu_exit = tk.Menu(menu)
# menu.add_cascade(label="Exit_menu", menu=subMenu_exit)
# subMenu_exit.add_command(label="Exit", command=window.destroy())


#from indicators import get_indicator_plots
import tkinter as tk

root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300)
canvas1.pack()


def hello():
    label1 = tk.Label(root, text='Hello World!', fg='blue', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 200, window=label1)


button1 = tk.Button(text='Click Me', command=hello(), bg='brown', fg='white')
canvas1.create_window(150, 150, window=button1)

root.mainloop()

text = input('write something: ')
print('This is your text:'+text)