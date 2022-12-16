from tkinter.messagebox import showinfo
from tkinter import *
from tkinter import filedialog as fd
import Functions


def long_func(flag, fn, tx, frame, arr):
    showinfo("Work", "Work in progress")
    """
    :param flag:
    :param fn:
    :param tx:
    :param frame:
    :param arr:
    :return:
    """
    if flag:
        # encode
        try:
            new_source, segment_width = Functions.hide(fn, tx)
        except:
            showinfo("ERROR", "ERROR")
            frame.destroy()
            for i in arr:
                i.pack()
            return 0
        frame.destroy()
        for i in arr:
            i.pack()
        if segment_width is None:
            showinfo("ERROR", "Unknown symbols")
            return 0
        showinfo("Key", "Your key is: " + str(segment_width))
    else:
        # decode
        try:
            msg = Functions.recover(fn, int(tx))
        except:
            showinfo("ERROR", "ERROR")
            frame.destroy()
            for i in arr:
                i.pack()
            return 0
        frame.destroy()
        for i in arr:
            i.pack()
        showinfo('Message', 'Your message is: ' + str(msg))
    '''for i in range(1000000000):
        pass'''
    frame.destroy()
    for i in arr:
        i.pack()


def info():
    showinfo("Information",
             "This program allows the user to encode a secret message in an audio file and decode it from a resulting audio file using steganography by pressing a corresponding button in the main menu.")


def back(p):
    global root
    for i in p:
        i.destroy()
    frame_top.place(relx=0.05, rely=0.25, relwidth=0.4, relheight=0.4)
    frame_bottom.place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.4)
    root['bg'] = 'grey'
    root.title('Steganography')


def open_file(flag, tx, arr):
    if tx == '':
        showinfo("ERROR", 'Вы должны что-то ввести')
        return 0
    global root, frame_mid
    fn = ''
    fn = fd.askopenfilename()
    if fn == '':
        showinfo("ERROR", "Файл не выбран")
        return 0
    for i in arr:
        i.pack_forget()
    frame_mid = Frame(root)
    frame_mid.place(relx=0.3, rely=0, relheight=0.7, relwidth=0.4)
    back_array.append(frame_mid)
    lbl = Label(frame_mid, text=f'Start working with file {fn}\n\n\n\n\n')
    btn1 = Button(frame_mid, text='START', command=lambda: long_func(flag, fn, tx, frame_mid, arr), height=10, width=10)
    lbl.pack()
    btn1.pack()


def encode():
    global root, btn, frame_top, frame_bottom, back_array
    frame_top.place_forget()
    frame_bottom.place_forget()
    root['bg'] = 'white'
    root.title('Steganography_encode')
    tx = Label(text='Enter secret message', font='50')
    tx.pack()
    ent = Entry()
    ent.pack()
    btn = Button(root, text='Choose file', font='50', command=lambda: open_file(1, ent.get(), [tx, ent, btn]), height=20, width=20)
    btn.pack()
    frame_back = Frame(root, bg='white', bd=5)
    frame_back.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)
    btn1 = Button(frame_back, text="Back", command=lambda: back(back_array), height=2, width=10)
    btn1.pack()
    back_array = [btn, btn1, frame_back, tx, ent]
    root.mainloop()


def decode():
    global root, btn, frame_top, frame_bottom, back_array
    frame_top.place_forget()
    frame_bottom.place_forget()
    root['bg'] = 'white'
    root.title('Steganography_decode')
    tx1 = Label(text='Enter key', font='50')
    tx1.pack()
    ent1 = Entry()
    ent1.pack()
    btn = Button(root, text='Choose file', font='50', command=lambda: open_file(0, ent1.get(), [tx1, ent1, btn]), height=20,
                 width=20)
    btn.pack()
    frame_back = Frame(root, bg='white', bd=5)
    frame_back.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)
    btn1 = Button(frame_back, text="Back", font='50', command=lambda: back(back_array), height=2, width=10)
    btn1.pack()
    back_array = [btn, btn1, frame_back, ent1, tx1]
    root.mainloop()


back_array = []
root = Tk()
root['bg'] = 'grey'
root.title('Steganography')
root.geometry('900x300')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.05, rely=0.25, relwidth=0.4, relheight=0.4)

frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.4)

btn = Button(frame_top, text='Decode', font='50', command=decode, height=20, width=200)
btn.pack()

btn = Button(frame_bottom, text='Encode', font='50', command=encode, height=20, width=200)
btn.pack()

frame_info = Frame(root)
frame_info.place(relx=0.88, rely=0.92, relwidth=0.12, relheight=0.08)

btn = Button(frame_info, text='Programme info', command=info)
btn.pack()

root.mainloop()