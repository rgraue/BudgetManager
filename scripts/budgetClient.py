from tkinter import *
import analysis
import account

def loginPage(window, user):
    clearWindow(window)
    fields = "Username", "Password"
    ents = makeform(window, fields)
    Button(window, text = "Submit", command = lambda: retrieveCred(window, ents, user)).pack()
    return


def retrieveCred (window, entry, user):
    credentials = []
    for i in entry:
        credentials.append(i[1].get())
    user.setUser(credentials[0], credentials[1])
    if (user.verifyUser()):
        buildHome(window, user)
    else:
        print("no user found")
    return credentials

# Builds home page of budget app
def buildHome (window, user) :
    clearWindow(window)
    Button(
        window,
        text = "Add Receipt",
        width = 20,
        height = 10,
        bg = "tomato",
        fg = "black",
        command = lambda: addPage(window, user.getFields(), user)
    ).pack(fill = Y, side = LEFT, pady = 5, padx = 5)
    Button(
        text = "View",
        width = 20,
        height = 10,
        bg = "lavender",
        fg = "black",
        command = lambda: viewPage(window, user)
        ).pack(fill = Y, side = LEFT, pady = 5, padx = 5)
    window.update()

### TODO
def viewPage (window, user):
    clearWindow(window)
    window.title("View")
    print(user.getFinances())
    window.update()

# creates add page to input financial details
def addPage (window, fields, user):
    varb = StringVar(window)
    varb.set(user.getCategories())
    clearWindow(window)
    window.title("Add Receipt")
    ents = makeform(window, fields)
    OptionMenu(window, varb, *user.getCategories()).pack()
    #window.bind('<Return>', (lambda event, e=ents: addData(e, varb.get(), user)))
    Button(window, text = "back" , command = lambda: buildHome(window, user)).pack()
    Button(window, text = "Submit", command = lambda: (addData(ents, varb.get(), user), buildHome(window, user))).pack()
    window.update()

# Clears the window of all current widgets
def clearWindow (window):
    wid = window.winfo_children()
    for i in wid:
        i.destroy()
    window.update()

# creates entry form depending on input fields
def makeform(window, fields):
    entries = []
    for field in fields:
        row = Frame(window)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries

#fetches and adds data to data frame
def addData (entry, cat, user):
    info = []
    for i in entry:
        info.append(i[1].get())
    info.append(cat)
    user.addReceipt(info)
    print(user.getFinances())

def main() :

    window = Tk()
    user = account.account()
    loginPage(window, user)
    window.mainloop()
    


    



if __name__ == '__main__':
    main()