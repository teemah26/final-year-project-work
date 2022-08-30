from asyncore import read
from tkinter import*
from tkinter import filedialog
window =Tk()
window.title ('syntax error checker')
window.geometry("600x600")
def open_text():
    text_file=filedialog.askopenfilename(title="open text file",filetypes=(("text files","*.py"), ))
    text_file=open(text_file,'r')
    stuff=text_file.read()
    my_text.insert(END,stuff)
    text_file.close()  
                    
                                         
my_text=Text(window,width=40,height=10,font=("helvetica",16))                                   
my_text.pack(pady=20)    

open_button=Button(window,text="choose python file to open",command=open_text)
open_button.pack(pady=20)


scan_text=Button(window,text="scan text",command=)
scan_text.pack(pady=40)

window.mainloop()
