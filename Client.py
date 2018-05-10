from Tkinter import *
from socket import *
from threading import *
from ScrolledText import*
class Receive():
  def __init__(self, server, gettext):
    #self.server = server
    #self.gettext = gettext
    while 1:
      try:
        text = server.recv(1024)
        if not text: break
        gettext.configure(state='normal')
        gettext.insert(END,'Server >> %s\n'%text)
        gettext.configure(state='disabled')
        gettext.see(END)
      except:
        break
class App(Thread):
  client = socket()
  client.connect(('localhost', input("Port: ")))
  def __init__(self, master):
    Thread.__init__(self)
    frame = Frame(master)
    frame.pack()
    self.gettext = ScrolledText(frame, height=10,width=100)
    self.gettext.pack()
    self.gettext.insert(END,'Welcome to Chat\n')
    self.gettext.configure(state='disabled')
    sframe = Frame(frame)
    sframe.pack(anchor='w')
    self.pro = Label(sframe, text="Client>>");
    self.sendtext = Entry(sframe,width=80)
    self.sendtext.focus_set()
    self.sendtext.bind(sequence="<Return>", func=self.Send)
    self.pro.pack(side=LEFT)
    self.sendtext.pack(side=LEFT)
  def Send(self, args):
    self.gettext.configure(state='normal')
    text = self.sendtext.get()
    if text=="": text=" "
    self.gettext.insert(END,'Me >> %s\n'%text)
    self.sendtext.delete(0,END)
    self.client.send(text)
    self.sendtext.focus_set()
    self.gettext.configure(state='disabled')
    self.gettext.see(END)
  def run(self):
    Receive(self.client, self.gettext)
root = Tk()
root.title('Client Chat')
app = App(root).start()
root.mainloop()
