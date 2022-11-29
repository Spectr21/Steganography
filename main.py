from tkinter.messagebox import showinfo
from tkinter import *
from tkinter import filedialog as fd

def enc(fn):
    for i in range(100000000):
        k=i//1024

def info():
    showinfo("Information", "Данное приложение позволять кодировать и декодировать сообщение в аудио файле с помощью стеганографии, для этого нажмите на соответствующую кнопку в основном окне. ")

def back(*p):
    global root
    for i in p:
        i.destroy()
    frame_top.place(relx=0.05, rely=0.25, relwidth=0.4, relheight=0.4)
    frame_bottom.place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.4)
    root['bg'] = 'grey'
    root.title('Steganography')


def open_file(tx):
    #if tx=='':
        #showinfo("ERROR", 'Вы должны что-то ввести')
        #return 0
    global root
    fn=''
    fn = fd.askopenfilename()
    if fn == '':
        showinfo("ERROR", "Файл не выбран")
        return 0
    frame_mid = Frame(root)
    frame_mid.place(relx=0.3, rely=0, relheight=0.7, relwidth=0.4)
    lbl = Label(frame_mid, text= f'Work with file {fn} in process\n\n\n\n\n')
    btn = Button(frame_mid, text='OK', command=lambda: frame_mid.destroy(), height=10, width=10)
    lbl.pack()
    btn.pack()

def encode():
    global root, btn, frame_top, frame_bottom
    frame_top.place_forget()
    frame_bottom.place_forget()
    root['bg'] = 'white'
    root.title('Steganography_encode')
    tx = Label(text='Введите текст закодированного сообщения')
    tx.pack()
    ent = Entry()
    ent.pack()
    btn = Button(root, text='Choose file', command=lambda:open_file(ent.get()), height=20, width=20)
    btn.pack()
    frame_back = Frame(root, bg='white', bd=5)
    frame_back.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)
    btn1 = Button(frame_back,text="Back", command=lambda: back(btn, btn1, frame_back, tx, ent), height=2, width=10)
    btn1.pack()
    root.mainloop()


def decode():
    global root, btn, frame_top, frame_bottom
    frame_top.place_forget()
    frame_bottom.place_forget()
    root['bg'] = 'white'
    root.title('Steganography_decode')
    tx = Label(text='Введите ключ')
    tx.pack()
    ent = Entry()
    ent.pack()
    btn = Button(root, text='Choose file', command=lambda: open_file(ent.get()), height=20, width=20)
    btn.pack()
    frame_back = Frame(root, bg='white', bd=5)
    frame_back.place(relx=0, rely=0.9, relwidth=0.1, relheight=0.1)
    btn1 = Button(frame_back, text="Back", command=lambda: back(btn, btn1, frame_back, ent, tx), height=2, width=10)
    btn1.pack()
    root.mainloop()


root = Tk()
root['bg'] = 'grey'
root.title('Steganography')
root.geometry('900x550')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.05, rely=0.25, relwidth=0.4, relheight=0.4)

frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.4)

btn = Button(frame_top, text='Decode', command=decode, height=20, width=200)
btn.pack()

btn = Button(frame_bottom, text='Encode', command=encode, height=20, width=200)
btn.pack()

frame_info = Frame(root)
frame_info.place(relx=0.88, rely=0.95, relwidth=0.12, relheight=0.05)

btn = Button(frame_info, text='Programme info', command=info)
btn.pack()

root.mainloop()
