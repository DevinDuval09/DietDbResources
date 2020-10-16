#form to select user
import tkinter
from tkinter import ttk as ttk
from WidgetUtility import SQL_ComboBox
from WidgetUtility import User
import pyodbc
class SelectUser(tkinter.Frame):
    '''Provides a frame and a combobox with users from DB listed.
        Use the.GetUser() method to retrun the currently selected UserId.
        Use the .remove(root) method to destroy the combobox and frame'''
    def __init__(self, parent):

        tkinter.Frame.__init__(self, parent)

        conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
        cursor = conx.cursor()
        ldirections = ttk.Label(self, text='Select a user').grid(column=0)
        self.cmbuser = SQL_ComboBox(self, "SELECT UserID,FirstName,LastName FROM Users")
        self.cmbuser.grid(column=0)

    def remove(self, parent):
        for w in parent.winfo_children():
            w.destroy()

    def GetUser(self):
        return self.cmbuser.get().split(',')[0][1:]

if __name__=='__main__':
    root = tkinter.Tk()
    user = None
    userbox = SelectUser(root)
    userbox.grid(column=1)
    lblUser = tkinter.Label(root)
    lblUser.grid(column=1)

    def SetUser():
        user = User(userbox.GetUser())
        userbox.remove(root)
        print(user.FirstName)

    bSubmit = ttk.Button(root, text='select user', command=SetUser).grid(column=0)


    root.mainloop()