"""
DEVELOPED AT : 07 June 2024
DEVELOPED BY : SCIHACK/POWERPIZZA
PURPOSE : I developed it for a friend.
"""

import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from datetime import datetime
from pandas import DataFrame, Series, read_csv
import matplotlib.pyplot as plt
import os

root = tkinter.Tk()
root.title("Digital Library")
root.geometry("1100x600")
root.state("zoomed")
root.iconphoto(False, PhotoImage(file="software_icon_PNG.png"))

# DATAFRAME STRUCTURES (NOTE : THEY ARE JUST STRUCTURES NOT REAL DF)
GBL_books_data_df = DataFrame(columns=["ACC NO.","AUTHOR","TITLE","VOLUME","PLACE AND PUBLISHER","YEAR OF PUBLISH","PAGES","BOOK NO.","COST"])
GBL_issued_books_df = DataFrame(columns=["SNO.", "BOOK ACC. NO.", "CLIENT NAME", "CLIENT PHONE NO.", "ISSUE DATE", "RETURN DATE", "IS RETURNED"])
GBL_returned_books_df = DataFrame(columns=["SNO.", "BOOK ACC. NO.", "CLIENT NAME", "CLIENT PHONE NO.", "ISSUED DATE", "RETURN DATE", "RETURNING AT"])
# ----------- END ---------------

# ------------------- CREATING FILE STRUCTURE -------------------
print("CREATING FILE STRUCTURE")
if "db" not in os.listdir():
    os.mkdir("db")
if len(os.listdir("db")) != 3:
    GBL_books_data_df.to_csv("db/books_data.csv", index=False)
    GBL_issued_books_df.to_csv("db/issued_books_data.csv", index=False)
    GBL_returned_books_df.to_csv("db/returned_books_data.csv", index=False)
    print("FILE STRUCTURE CREATED SUCCESSFULLY.")
print("DONE\nStaring Software......")
# ------------------- (END) CREATING FILE STRUCTURE -------------------

def onManageBooks():
    books_df = read_csv("db/books_data.csv")  # contains 9 columns

    def saveToDB():
        nonlocal books_df
        books_df.to_csv("db/books_data.csv", index=False)
        books_df = read_csv("db/books_data.csv")
        loadTable()
        lbl_total_count.config(text=f"{len(books_df.index)} BOOKS PRESENT")

    manage_book_canvas = Canvas(root, bg="#ffffff")
    root.title("Digital Library [MANAGE BOOKS]")

    # ------------------------- HEADER OF THIS WINDOW ---------------------------
    top_options = Frame(manage_book_canvas, bg="#ffffff", highlightthickness=1, highlightbackground="#000000")

    def onAddBooks():
        addBookWin = Toplevel(root)
        addBookWin.transient(root)
        addBookWin.title("Add Book")
        addBookWin.resizable(False, False)

        addBookCanvas = Canvas(addBookWin, bg="#FFFFFF", bd=0)
        def createBookEntry(master, lbl_text, default_value=""):
            ent_text_var = StringVar(master=addBookWin, value=default_value)
            f_entry = Frame(master, bg='#ffffff', highlightthickness=1, highlightbackground="#fcba03")
            l1 = Label(f_entry, text=lbl_text, font=("Bahnschrift", 18), bg="#ffffff", anchor=W)
            l1.pack(side=LEFT, fill=X, expand=True)
            e1 = Entry(f_entry, font=("Bahnschrift", 16), textvariable=ent_text_var, highlightthickness=1, highlightbackground="blue")
            e1.pack(side=LEFT, fill=X, expand=True)
            f_entry.pack(fill=X, expand=True)
            return ent_text_var

        fr_acc_no_entry = Frame(addBookCanvas, bg="#ffffff")
        fr_acc_entry_holder = Frame(fr_acc_no_entry, bg="#ffffff")
        acc_no_val = createBookEntry(fr_acc_entry_holder, "Acc. No.", str(int(([0]+books_df["ACC NO."].tolist())[-1])+1))
        fr_acc_entry_holder.pack(side=LEFT, fill=X, expand=True)
        def onClickAuto():
            acc_no_val.set(str(int(([0]+books_df["ACC NO."].tolist())[-1])+1))
        btn_auto_acc = Button(fr_acc_no_entry, text="AUTO", font=("Helvetica", 12, "bold"), bg="#ffe2db", relief="groove", command=onClickAuto)
        btn_auto_acc.pack(side=LEFT)
        fr_acc_no_entry.pack(fill=X, padx=2)

        df_columns_vars = []  # excluding acc no.
        fr_entries = Frame(addBookCanvas, bg="#ffffff")
        for col_df in books_df.columns[1:]:
            df_columns_vars.append(createBookEntry(fr_entries, str(col_df).capitalize()))
        fr_entries.pack(fill=X, padx=2)

        Frame(addBookCanvas).pack(pady=10)  # just for gapping

        def onSubmitBook():
            # 2, 4, 5, 7
            if not str(acc_no_val.get()).isnumeric():
                messagebox.showerror("Non-Int Value", f"ACC. NO. should be integer")
                return

            if int(acc_no_val.get()) in books_df["ACC NO."].values:
                messagebox.showerror("Already Exists", f"Please choose a different acc no. entry with this acc no. already exists.")
                return

            for check in [2, 4, 5, 7]:  # VOLUME, YEAR OF PUBLISH, PAGES, COST
                if not str(df_columns_vars[check].get()).isnumeric():
                    messagebox.showerror("Non-Int Value", f"{books_df.columns[1:][check]} should be integer")
                    return

            books_df.loc[len(books_df.index)] = list(map(lambda x: x.get(), [acc_no_val]+df_columns_vars))
            saveToDB()
            addBookWin.destroy()
            messagebox.showinfo("Saved", "Saved Successfully!")

        btnSubmit = Button(addBookCanvas, text="Add Book & Save", font=("Helvetica", 14), bg="#c2ffc5", relief="ridge", command=onSubmitBook)
        btnSubmit.pack(fill=X, expand=True, padx=2, pady=2)
        addBookCanvas.pack(fill=BOTH, expand=True)
        addBookWin.mainloop()
    btn_add_books = Button(top_options, text="Add Books", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onAddBooks)
    btn_add_books.pack(side=LEFT, padx=1)

    def onDeleteBook():
        # -------------------------- DELETE BOOK FUNCTION ------------------------------
        deleteBookWin = Toplevel(root)
        deleteBookWin.transient(root)
        deleteBookWin.resizable(False, False)
        deleteBookWin.title("Delete Book")

        acc_no_to_del = IntVar()
        fr_entry_holder = Frame(deleteBookWin, bg="#ffffff")
        lbl_acc_no = Label(fr_entry_holder, text="Acc. No.", font=("Bahnschrift", 18), bg="#ffffff", anchor=W)
        lbl_acc_no.pack(side=LEFT, fill=X, expand=True)
        entry_acc_no = Entry(fr_entry_holder, font=("Bahnschrift", 16), textvariable=acc_no_to_del, highlightthickness=1, highlightbackground="blue")
        entry_acc_no.pack(side=LEFT, fill=X, expand=True)
        fr_entry_holder.pack()

        def onDelete():
            if acc_no_to_del.get() in books_df["ACC NO."].values:
                books_df.drop(books_df[books_df["ACC NO."] == acc_no_to_del.get()].index[0], axis=0, inplace=True)
                saveToDB()
                deleteBookWin.destroy()
                messagebox.showinfo("Deleted", "Successfully deleted 1 entry!")
            else:
                messagebox.showerror("Failed", f"Acc No {acc_no_to_del.get()} not found in database.")
        btn_delete = Button(deleteBookWin, text="Delete !", bg="#ffbac7", font=("Helvetica", 14), command=onDelete)
        btn_delete.pack(fill=X, padx=2)
        deleteBookWin.mainloop()
        # ----------------------------- (END) DELETE BOOK FUNCTION -------------------------
    btn_delete_book = Button(top_options, text="Delete Book", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onDeleteBook)
    btn_delete_book.pack(side=LEFT, padx=1)

    def onExportBooks():
        file_ = filedialog.asksaveasfilename(filetypes=(("CSV file", "*.csv"), ("Excel file", "*.xlsx")), defaultextension="csv")
        if not file_:
            return
        if file_.endswith(".csv"):
            books_df.to_csv(file_, index=False)
        elif file_.endswith(".xlsx"):
            books_df.to_excel(file_, index=False)
        else:
            messagebox.showerror("Unknown File", "File types provided is unsupported.")
            return
        messagebox.showinfo("Saved", f"File saved successfully at {file_}")

    btn_export_books = Button(top_options, text="Export Books", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onExportBooks)
    btn_export_books.pack(side=LEFT, padx=1)

    def onClose():
        root.unbind("<MouseWheel>", scrollBindID)
        manage_book_canvas.destroy()
        root.title("Digital Library")
    btn_close = Button(top_options, text="Close", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onClose)
    btn_close.pack(side=LEFT, padx=1, pady=1)

    lbl_total_count = Label(top_options, text=f"{len(books_df.index)} BOOKS PRESENT", bg="#ffffff", font=("Calibri", 14, "bold", "underline"), fg="#ff0000")
    lbl_total_count.pack(side=RIGHT, padx=4, anchor=NE, pady=2)

    top_options.pack(fill=X)

    # ------------------------- (END) HEADER OF THIS WINDOW ---------------------------

    table_frame = Frame()  # just initializing for later use...

    def loadTable():
        nonlocal table_frame
        if table_frame:
            table_frame.destroy()

        table_frame = Frame(book_view_canvas, bg="#ffffff")
        for i, item in enumerate(books_df.columns):
            lbl_th = Label(table_frame, text=item, font=("Helvetica", 16, "bold"), highlightthickness=1, highlightbackground="#000000")
            lbl_th.grid(row=1, column=i, sticky=NSEW, ipadx=20)

        for row_ in range(len(books_df.index)):
            for idxr, col_ in enumerate(books_df.iloc[row_]):
                lbl_td = Label(table_frame, text=col_, font=("Helvetica", 16, "bold"), highlightthickness=1, highlightbackground="#000000")
                lbl_td.grid(row=row_+2, column=idxr, sticky=NSEW, ipadx=20)
        table_frame.pack()

        table_frame.bind("<Configure>", lambda eve: book_view_canvas.configure(scrollregion=book_view_canvas.bbox("all")))
        book_view_canvas.create_window((0, 0), window=table_frame, anchor=NW)

    # -------------- TABLE VIEW AND Y ORIENT SCROLLBAR --------
    fr_bi_layout = Frame(manage_book_canvas, bg="#ffffff")
    frame_table_holder = Frame(fr_bi_layout)
    book_view_canvas = Canvas(frame_table_holder, bg="#ffffff")
    book_view_canvas.pack(fill=BOTH, expand=True)
    frame_table_holder.pack(fill=BOTH, expand=True, side=LEFT)

    scroll_bar_Y = Scrollbar(fr_bi_layout, orient="vertical", command=book_view_canvas.yview)
    scroll_bar_Y.pack(side=RIGHT, fill=Y, pady=2)
    book_view_canvas.configure(yscrollcommand=scroll_bar_Y.set)
    fr_bi_layout.pack(fill=BOTH, expand=True)
    def onMouseScroll(eve):
        if table_frame.winfo_height() < book_view_canvas.winfo_height():
            return
        book_view_canvas.yview_scroll((eve.delta//100)*-1, 'units')
    scrollBindID = root.bind("<MouseWheel>", onMouseScroll)
    # -------------- TABLE VIEW AND Y ORIENT SCROLLBAR END --------

    # -------------- X ORIENT SCROLLBAR + TABLE LOADING --------
    scroll_bar_X = Scrollbar(manage_book_canvas, orient="horizontal", command=book_view_canvas.xview)
    scroll_bar_X.pack(fill=X)
    book_view_canvas.configure(xscrollcommand=scroll_bar_X.set)
    loadTable()
    # -------------- (END) X ORIENT SCROLLBAR + TABLE LOADING --------
    manage_book_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)


def onIssuedBooks():
    issued_books_df = read_csv("db/issued_books_data.csv")

    def saveToDB():
        nonlocal issued_books_df
        issued_books_df.to_csv("db/issued_books_data.csv", index=False)
        issued_books_df = read_csv("db/issued_books_data.csv")
        loadTable()
        lbl_total_count.config(text=f"{len(issued_books_df.index)} ENTRIES PRESENT")

    issued_books_canvas = Canvas(root, bg="#ffffff")
    root.title("Digital Library [ISSUED BOOKS]")

    # ------------------------- HEADER OF THIS WINDOW ---------------------------
    top_options = Frame(issued_books_canvas, bg="#ffffff", highlightthickness=1, highlightbackground="#000000")

    def for_issue_new_book():
        issueBookWin = Toplevel(root)
        issueBookWin.title("Issue Book")
        issueBookWin.transient(root)
        issueBookWin.resizable(False, False)

        issueBookCanvas = Canvas(issueBookWin, bg="#FFFFFF")

        # ------------------------ TEXT VARIABLES ----------------------
        acc_no_var = IntVar(issueBookWin)
        client_name_var = StringVar(issueBookWin)
        client_phone_no_var = StringVar(issueBookWin)
        issue_date_var = StringVar(issueBookWin, value=str(datetime.now().date()))
        return_date_var = StringVar(issueBookWin)
        # ------------------------ (END) TEXT VARIABLES ----------------------

        # ------------------------ FORM GUI ---------------------------
        fr_row1 = Frame(issueBookCanvas, bg="#ffffff")
        lbl_acc_no = Label(fr_row1, text="ACC. NO. (book to be issued)", font=("Arial", 14), anchor=W, bg="#ffffff")
        lbl_acc_no.pack(fill=X, side=LEFT, expand=True)
        entry_acc_no = Entry(fr_row1, textvariable=acc_no_var, highlightthickness=1, highlightbackground="#000000", font=("Arial", 14))
        entry_acc_no.pack(fill=BOTH, expand=True, side=LEFT)
        fr_row1.pack(fill=X, expand=True, padx=3, pady=1)

        fr_row2 = Frame(issueBookCanvas, bg="#ffffff")
        lbl_client_name = Label(fr_row2, text="Client Name", font=("Arial", 14), anchor=W, bg="#ffffff")
        lbl_client_name.pack(fill=X, side=LEFT)
        entry_client_name = Entry(fr_row2, textvariable=client_name_var, highlightthickness=1, highlightbackground="#000000", font=("Arial", 14))
        entry_client_name.pack(fill=BOTH, expand=True, side=LEFT)
        fr_row2.pack(fill=X, expand=True, padx=3, pady=1)

        fr_row3 = Frame(issueBookCanvas, bg="#ffffff")
        lbl_client_phno = Label(fr_row3, text="Client Phone No.", font=("Arial", 14), anchor=W, bg="#ffffff")
        lbl_client_phno.pack(fill=X, side=LEFT)
        entry_client_phno = Entry(fr_row3, textvariable=client_phone_no_var, highlightthickness=1, highlightbackground="#000000", font=("Arial", 14))
        entry_client_phno.pack(fill=BOTH, expand=True, side=LEFT)
        fr_row3.pack(fill=X, expand=True, padx=3, pady=1)

        fr_row4 = Frame(issueBookCanvas, bg="#ffffff")
        lbl_issue_date = Label(fr_row4, text="Issue Date", font=("Arial", 14), anchor=W, bg="#ffffff")
        lbl_issue_date.pack(fill=X, side=LEFT)
        entry_issue_date = Entry(fr_row4, textvariable=issue_date_var, highlightthickness=1, highlightbackground="#000000", font=("Arial", 14), state=DISABLED)
        entry_issue_date.pack(fill=BOTH, expand=True, side=LEFT)
        fr_row4.pack(fill=X, expand=True, padx=3, pady=1)

        fr_row5 = Frame(issueBookCanvas, bg="#ffffff")
        lbl_return_date = Label(fr_row5, text="Return Date", font=("Arial", 14), anchor=W, bg="#ffffff")
        lbl_return_date.pack(fill=X, side=LEFT)
        entry_return_date = Entry(fr_row5, textvariable=return_date_var, highlightthickness=1, highlightbackground="#000000", font=("Arial", 14), state=DISABLED)
        entry_return_date.pack(fill=BOTH, expand=True, side=LEFT)
        def onSetReturnDate(*eve):
            cal_win = Toplevel(root)
            cal_win.transient(root)
            cal_win.resizable(False, False)
            cal_win.title("Calender")
            my_calender = Calendar(cal_win)
            my_calender.pack()

            def on_day_select(*eve):
                return_date_var.set(value=my_calender.selection_get())
                cal_win.destroy()
            my_calender.bind("<<CalendarSelected>>", on_day_select)
        entry_return_date.bind("<Button-1>", onSetReturnDate)
        fr_row5.pack(fill=X, expand=True, padx=3, pady=1)
        # ------------------------ (END) FORM GUI ---------------------------

        def onIssueNow():
            new_sno = int(([0]+issued_books_df["SNO."].tolist())[-1])+1

            df_book_data = read_csv("db/books_data.csv")
            if acc_no_var.get() not in df_book_data["ACC NO."].values:
                messagebox.showerror("Book not found", f"Book with acc no. {acc_no_var.get()} not found in database.")
                return

            if len(return_date_var.get()) < 3:
                messagebox.showerror("Invalid Return Date", f"Return date is required")
                return
            data_to_add = [new_sno, acc_no_var.get(), client_name_var.get(), client_phone_no_var.get(), issue_date_var.get(), return_date_var.get(), False]
            issued_books_df.loc[len(issued_books_df.index)] = data_to_add
            saveToDB()
            messagebox.showinfo("Done", "Successfully issue new book!")

        btn_issue_now = Button(issueBookCanvas, text="Issue Now!", font=("Calibri", 14, "bold"), bg="#c5ffbf", relief="groove", command=onIssueNow)
        btn_issue_now.pack(side=RIGHT, padx=2, pady=3, ipadx=10)
        issueBookCanvas.pack(fill=BOTH, expand=True)
        issueBookWin.mainloop()
    btn_issue_a_book = Button(top_options, text="Issue a Book", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=for_issue_new_book)
    btn_issue_a_book.pack(side=LEFT, padx=1)

    def for_return_book_now():
        returnBookWin = Toplevel(root)
        returnBookWin.transient(root)
        returnBookWin.resizable(False, False)
        returnBookWin.title("Return Book")

        returning_sno_var = IntVar()

        fr_entry_holder = Frame(returnBookWin, bg="#FFFFFF")
        lbl_entry_sno = Label(fr_entry_holder, text="SNO.\n(of book to be returned)", font=("Helvetica", 16), bg="#FFFFFF")
        lbl_entry_sno.pack(side=LEFT)
        entry_sno = Entry(fr_entry_holder, textvariable=returning_sno_var, font=("Helvetica", 16), highlightthickness=1, highlightbackground="#000000", width=12)
        entry_sno.pack(side=LEFT, fill=BOTH, expand=True)
        fr_entry_holder.pack(fill=BOTH, expand=True)

        def onReturnNow():
            if returning_sno_var.get() not in issued_books_df["SNO."].values:
                messagebox.showerror("Failed", "Failed to return book because book with this SNO. has no issued records.")
                return
            if issued_books_df.loc[issued_books_df["SNO."] == returning_sno_var.get(), "IS RETURNED"].values[0]:
                messagebox.showerror("Failed", "The book at this SNO. has already been returned.")
                return

            df_returned_books = read_csv("db/returned_books_data.csv")

            issued_books_df.loc[issued_books_df["SNO."] == returning_sno_var.get(), "IS RETURNED"] = True
            selected_row = issued_books_df.loc[issued_books_df["SNO."] == returning_sno_var.get(), "BOOK ACC. NO.": "RETURN DATE"]
            new_sno_ = int(([0] + df_returned_books["SNO."].to_list())[-1]) + 1
            data_to_add = [new_sno_] + list(selected_row.values[0]) + [str(datetime.now().date())]
            df_returned_books.loc[len(df_returned_books.index)] = data_to_add

            saveToDB()  # saving to issued_books_data.csv
            df_returned_books.to_csv("db/returned_books_data.csv", index=False)
            messagebox.showinfo("Done", "Book has been returned successfully.")
        btn_return = Button(returnBookWin, text="Return Now!", font=("Calibri", 14, "bold"), relief="groove", bg="#fcb6b1", command=onReturnNow)
        btn_return.pack(anchor=E, padx=1, pady=1)
        returnBookWin.mainloop()
    btn_return_book = Button(top_options, text="Return Book", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=for_return_book_now)
    btn_return_book.pack(side=LEFT, padx=1)

    def onExportBooks():
        file_ = filedialog.asksaveasfilename(filetypes=(("CSV file", "*.csv"), ("Excel file", "*.xlsx")), defaultextension="csv")
        if not file_:
            return
        if file_.endswith(".csv"):
            issued_books_df.to_csv(file_, index=False)
        elif file_.endswith(".xlsx"):
            issued_books_df.to_excel(file_, index=False)
        else:
            messagebox.showerror("Unknown File", "File types provided is unsupported.")
            return
        messagebox.showinfo("Saved", f"File saved successfully at {file_}")
    btn_export = Button(top_options, text="Export", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onExportBooks)
    btn_export.pack(side=LEFT, padx=1)

    def onClose():
        root.unbind("<MouseWheel>", scrollBindID)
        issued_books_canvas.destroy()
        root.title("Digital Library")
    btn_close = Button(top_options, text="Close", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onClose)
    btn_close.pack(side=LEFT, padx=1, pady=1)

    lbl_total_count = Label(top_options, text=f"{len(issued_books_df.index)} ENTRIES PRESENT", bg="#ffffff", font=("Calibri", 14, "bold", "underline"), fg="#ff0000")
    lbl_total_count.pack(side=RIGHT, padx=4, anchor=NE, pady=2)

    top_options.pack(fill=X)
    # ------------------------- (END) HEADER OF THIS WINDOW ---------------------------

    table_frame = Frame()  # just initializing for latter use.

    def loadTable():
        nonlocal table_frame
        if table_frame:
            table_frame.destroy()

        table_frame = Frame(issued_view_canvas, bg="#FFFFFF")
        for i, item in enumerate(issued_books_df.columns):
            lbl_th = Label(table_frame, text=item, font=("Helvetica", 16, "bold"), highlightthickness=1, highlightbackground="#000000")
            lbl_th.grid(row=1, column=i, sticky=NSEW, ipadx=20)

        for row_ in range(len(issued_books_df.index)):
            for idxr, col_ in enumerate(issued_books_df.iloc[row_]):
                if idxr == 1:
                    def createClickableTD():
                        col_cpy = col_

                        def openBookViewer():
                            viewer_win = Toplevel(root)
                            viewer_win.transient(root)
                            viewer_win.title(f"Book Viewer (ACC NO. : {col_cpy})")

                            df_book_data = read_csv("db/books_data.csv")
                            selected_view = df_book_data[df_book_data["ACC NO."] == col_cpy]
                            for idxr, col_name in enumerate(selected_view.columns):
                                lbl_view = Label(viewer_win, text=f"{col_name} : {selected_view[col_name].values[0]}", font=("Helvetica", 14, "bold"), anchor=W, justify=LEFT)
                                lbl_view.pack(fill=X, padx=2)
                            viewer_win.mainloop()
                        clickable_td = Button(table_frame, text=col_, font=("Helvetica", 14, "bold"), bg="#c6e8c3", relief="ridge", cursor="sizing", command=openBookViewer)
                        clickable_td.grid(row=row_ + 2, column=idxr, sticky=NSEW, ipadx=20, padx=1, pady=1)
                    createClickableTD()
                else:
                    lbl_td = Label(table_frame, text=col_, font=("Helvetica", 16, "bold"), highlightthickness=1, highlightbackground="#000000")
                    lbl_td.grid(row=row_+2, column=idxr, sticky=NSEW, ipadx=20)

        table_frame.pack()

        table_frame.bind("<Configure>", lambda eve: issued_view_canvas.configure(scrollregion=issued_view_canvas.bbox("all")))
        issued_view_canvas.create_window((0, 0), window=table_frame, anchor=NW)

    # -------------- TABLE VIEW AND Y ORIENT SCROLLBAR --------
    fr_bi_layout = Frame(issued_books_canvas, bg="#ffffff")
    frame_table_holder = Frame(fr_bi_layout)
    issued_view_canvas = Canvas(frame_table_holder, bg="#ffffff")
    issued_view_canvas.pack(fill=BOTH, expand=True)
    frame_table_holder.pack(fill=BOTH, expand=True, side=LEFT)

    scroll_bar_Y = Scrollbar(fr_bi_layout, orient="vertical", command=issued_view_canvas.yview)
    scroll_bar_Y.pack(side=RIGHT, fill=Y, pady=2)
    issued_view_canvas.configure(yscrollcommand=scroll_bar_Y.set)
    fr_bi_layout.pack(fill=BOTH, expand=True)

    def onMouseScroll(eve):
        if table_frame.winfo_height() < issued_view_canvas.winfo_height():
            return
        issued_view_canvas.yview_scroll((eve.delta//100)*-1, 'units')
    scrollBindID = root.bind("<MouseWheel>", onMouseScroll)
    # -------------- TABLE VIEW AND Y ORIENT SCROLLBAR END --------

    # -------------- X ORIENT SCROLLBAR + TABLE LOADING --------
    scroll_bar_X = Scrollbar(issued_books_canvas, orient="horizontal", command=issued_view_canvas.xview)
    scroll_bar_X.pack(fill=X)
    issued_view_canvas.configure(xscrollcommand=scroll_bar_X.set)
    loadTable()
    # -------------- (END) X ORIENT SCROLLBAR + TABLE LOADING --------
    issued_books_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)


def onReturnedBooks():
    returned_book_df = read_csv("db/returned_books_data.csv")

    def saveToDB():
        nonlocal returned_book_df
        returned_book_df.to_csv("db/returned_books_data.csv", index=False)
        returned_book_df = read_csv("db/returned_books_data.csv")
        loadTable()
        lbl_total_count.config(text=f"{len(returned_book_df.index)} ENTRIES PRESENT")

    returned_book_canvas = Canvas(root, bg="#ffffff")
    root.title("Digital Library [RETURNED BOOKS]")

    # ------------------------- HEADER OF THIS WINDOW ---------------------------
    top_options = Frame(returned_book_canvas, bg="#ffffff", highlightthickness=1, highlightbackground="#000000")

    def onDeleteEntry():
        deleteBookWin = Toplevel(root)
        deleteBookWin.transient(root)
        deleteBookWin.resizable(False, False)
        deleteBookWin.title("Delete Entry (Returned Book)")

        sno_to_del = IntVar()
        fr_entry_holder = Frame(deleteBookWin, bg="#ffffff")
        lbl_sno_no = Label(fr_entry_holder, text="SNO. (of entry to delete)", font=("Bahnschrift", 18), bg="#ffffff", anchor=W)
        lbl_sno_no.pack(side=LEFT, fill=X, expand=True)
        entry_sno_no = Entry(fr_entry_holder, font=("Bahnschrift", 16), textvariable=sno_to_del, highlightthickness=1, highlightbackground="blue")
        entry_sno_no.pack(side=LEFT, fill=X, expand=True)
        fr_entry_holder.pack()

        def onDelete():
            if sno_to_del.get() in returned_book_df["SNO."].values:
                returned_book_df.drop(returned_book_df[returned_book_df["SNO."] == sno_to_del.get()].index[0], axis=0, inplace=True)
                saveToDB()
                deleteBookWin.destroy()
                messagebox.showinfo("Deleted", "Successfully deleted 1 entry!")
            else:
                messagebox.showerror("Failed", f"SNO. {sno_to_del.get()} not found in database.")

        btn_delete = Button(deleteBookWin, text="Delete !", bg="#ffbac7", font=("Helvetica", 14), command=onDelete)
        btn_delete.pack(fill=X, padx=2)
        deleteBookWin.mainloop()
    btn_delete_entry = Button(top_options, text="Delete Entry", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onDeleteEntry)
    btn_delete_entry.pack(side=LEFT, padx=1)

    def onExportBooks():
        file_ = filedialog.asksaveasfilename(filetypes=(("CSV file", "*.csv"), ("Excel file", "*.xlsx")), defaultextension="csv")
        if not file_:
            return
        if file_.endswith(".csv"):
            returned_book_df.to_csv(file_, index=False)
        elif file_.endswith(".xlsx"):
            returned_book_df.to_excel(file_, index=False)
        else:
            messagebox.showerror("Unknown File", "File types provided is unsupported.")
            return
        messagebox.showinfo("Saved", f"File saved successfully at {file_}")
    btn_export = Button(top_options, text="Export", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onExportBooks)
    btn_export.pack(side=LEFT, padx=1)

    def onClose():
        root.unbind("<MouseWheel>", scrollBindID)
        returned_book_canvas.destroy()
        root.title("Digital Library")
    btn_close = Button(top_options, text="Close", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onClose)
    btn_close.pack(side=LEFT, padx=1, pady=1)

    lbl_total_count = Label(top_options, text=f"{len(returned_book_df.index)} ENTRIES PRESENT", bg="#ffffff", font=("Calibri", 14, "bold", "underline"), fg="#ff0000")
    lbl_total_count.pack(side=RIGHT, padx=4, anchor=NE, pady=2)

    top_options.pack(fill=X)
    # ------------------------- (END) HEADER OF THIS WINDOW ---------------------------

    table_frame = Frame()  # just initializing for later uses...

    def loadTable():
        nonlocal table_frame
        if table_frame:
            table_frame.destroy()

        table_frame = Frame(returnedBooks_view_canvas, bg="#FFFFFF")
        for i, item in enumerate(returned_book_df.columns):
            lbl_th = Label(table_frame, text=item, font=("Helvetica", 16, "bold"), highlightthickness=1, highlightbackground="#000000")
            lbl_th.grid(row=1, column=i, sticky=NSEW, ipadx=20)

        for row_ in range(len(returned_book_df.index)):
            for idxr, col_ in enumerate(returned_book_df.iloc[row_]):
                if idxr == 1:
                    def createClickableTD():
                        col_cpy = col_

                        def openBookViewer():
                            viewer_win = Toplevel(root)
                            viewer_win.transient(root)
                            viewer_win.title(f"Book Viewer (ACC NO. : {col_cpy})")

                            df_book_data = read_csv("db/books_data.csv")
                            selected_view = df_book_data[df_book_data["ACC NO."] == col_cpy]
                            for idxr, col_name in enumerate(selected_view.columns):
                                lbl_view = Label(viewer_win, text=f"{col_name} : {selected_view[col_name].values[0]}", font=("Helvetica", 14, "bold"), anchor=W, justify=LEFT)
                                lbl_view.pack(fill=X, padx=2)
                            viewer_win.mainloop()
                        clickable_td = Button(table_frame, text=col_, font=("Helvetica", 14, "bold"), bg="#c6e8c3", relief="ridge", cursor="sizing", command=openBookViewer)
                        clickable_td.grid(row=row_ + 2, column=idxr, sticky=NSEW, ipadx=20, padx=1, pady=1)
                    createClickableTD()
                else:
                    lbl_td = Label(table_frame, text=col_, font=("Helvetica", 16, "bold"), highlightthickness=1, highlightbackground="#000000")
                    lbl_td.grid(row=row_+2, column=idxr, sticky=NSEW, ipadx=20)

        table_frame.pack()

        table_frame.bind("<Configure>", lambda eve: returnedBooks_view_canvas.configure(scrollregion=returnedBooks_view_canvas.bbox("all")))
        returnedBooks_view_canvas.create_window((0, 0), window=table_frame, anchor=NW)

    # -------------- TABLE VIEW AND Y ORIENT SCROLLBAR --------
    fr_bi_layout = Frame(returned_book_canvas, bg="#ffffff")
    frame_table_holder = Frame(fr_bi_layout)
    returnedBooks_view_canvas = Canvas(frame_table_holder, bg="#ffffff")
    returnedBooks_view_canvas.pack(fill=BOTH, expand=True)
    frame_table_holder.pack(fill=BOTH, expand=True, side=LEFT)

    scroll_bar_Y = Scrollbar(fr_bi_layout, orient="vertical", command=returnedBooks_view_canvas.yview)
    scroll_bar_Y.pack(side=RIGHT, fill=Y, pady=2)
    returnedBooks_view_canvas.configure(yscrollcommand=scroll_bar_Y.set)
    fr_bi_layout.pack(fill=BOTH, expand=True)

    def onMouseScroll(eve):
        if table_frame.winfo_height() < returnedBooks_view_canvas.winfo_height():
            return
        returnedBooks_view_canvas.yview_scroll((eve.delta // 100) * -1, 'units')

    scrollBindID = root.bind("<MouseWheel>", onMouseScroll)
    # -------------- TABLE VIEW AND Y ORIENT SCROLLBAR END --------

    # -------------- X ORIENT SCROLLBAR + TABLE LOADING --------
    scroll_bar_X = Scrollbar(returned_book_canvas, orient="horizontal", command=returnedBooks_view_canvas.xview)
    scroll_bar_X.pack(fill=X)
    returnedBooks_view_canvas.configure(xscrollcommand=scroll_bar_X.set)
    loadTable()
    # -------------- (END) X ORIENT SCROLLBAR + TABLE LOADING --------
    returned_book_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)


# ------------------------- HOMEPAGE BEGIN -----------------------
home_canvas = Canvas(root, bg="#efe3ff")
heading_lbl = Label(home_canvas, text="Digital Library", bg="#efe3ff", font=("Bahnschrift SemiBold", 34, "bold", "underline"))
heading_lbl.pack(pady=5)

# ------------------------- HOME PAGE OPTIONS ----------------------
fr_options = Frame(home_canvas, highlightthickness=2, highlightbackground="#000000", bg="#e3f5ff")
opt_title_lbl = Label(fr_options, text="OPTIONS", font=("Bahnschrift SemiBold", 16, "underline"), bg="#e3f5ff")
opt_title_lbl.pack()

row_1_fr = Frame(fr_options, bg="#e3f5ff")
btn_manage_books = Button(row_1_fr, text="Manage Books", font=("Cascadia Code", 18), width=20, bg="#dbffd9", relief="ridge", command=onManageBooks)
btn_manage_books.pack(side=LEFT)

fr_centre_btn = Frame(row_1_fr, bg="#e3f5ff")
btn_issued_books = Button(fr_centre_btn, text="Issued Books", font=("Cascadia Code", 18), width=20, bg="#dbffd9", relief="ridge", command=onIssuedBooks)
btn_issued_books.pack()
fr_centre_btn.pack(side=LEFT, fill=X, expand=True)

btn_returned_books = Button(row_1_fr, text="Returned Books", font=("Cascadia Code", 18), width=20, bg="#dbffd9", relief="ridge", command=onReturnedBooks)
btn_returned_books.pack(side=RIGHT)
row_1_fr.pack(fill=X, expand=True, padx=50, pady=30)

row_2_fr = Frame(fr_options, bg="#e3f5ff")
def onClickGraphs():
    graph_canvas = Canvas(root, bg="#ffffff")
    root.title("Digital Library [Graphs]")

    # ----------------------- HEADER -------------------
    top_options = Frame(graph_canvas, bg="#ffffff", highlightthickness=1, highlightbackground="#000000")
    def onClose():
        root.title("Digital Library")
        graph_canvas.destroy()
    btn_close = Button(top_options, text="Close", font=("Arial", 16), bg="#d9ebff", relief="ridge", width=12, command=onClose)
    btn_close.pack(side=LEFT, padx=1, pady=1)
    top_options.pack(fill=X)
    # ----------------------- (END) HEADER -------------------

    # --------------------- SOME FUNCTIONS ---------------------
    def createGraphCard(master, title, description, function):
        # This function is responsible for the cards u see on this page.
        card_ = Frame(master, bg="#dbfffe", relief="ridge", bd=2, width=350, height=300)
        lbl_card_title = Label(card_, text=title, font=("Calibri", 18), bg="#3853ff", fg="#05fcf8")
        lbl_card_title.pack(fill=X)
        lbl_card_desc = Label(card_, text=description, bg="#dbfffe", font=("Calibri", 18), anchor=W, justify=LEFT, wraplength=340)
        lbl_card_desc.pack(fill=X)
        btn_plot_graph = Button(card_, text="Show", font=("Calibri", 14), bg="#ffb8c5", relief="groove", command=function)
        btn_plot_graph.pack(fill=X, padx=2, pady=2, side=BOTTOM)
        card_.pack()
        card_.propagate(False)

    def plotGraph1():
        df_ = read_csv("db/books_data.csv")
        x_axis_labels = []
        y_axis_labels = []
        for year_ in sorted(df_["YEAR OF PUBLISH"].drop_duplicates()):
            x_axis_labels.append(str(year_))
            y_axis_labels.append(len(df_[df_["YEAR OF PUBLISH"] == year_].index))
        plt.figure("Graph 1")
        plt.plot(x_axis_labels, y_axis_labels)
        plt.xticks(rotation=315)
        plt.xlabel("YEARS")
        plt.ylabel("No. of Books")
        plt.title("GRAPH : No. of books published each year")
        plt.show()

    def plotGraph2():
        df_ = read_csv("db/books_data.csv")
        x_axis_labels = []
        y_axis_labels = []
        print(df_[df_["YEAR OF PUBLISH"] == 2005])
        for year_ in sorted(df_["YEAR OF PUBLISH"].drop_duplicates()):
            x_axis_labels.append(str(year_))
            y_axis_labels.append(df_[df_["YEAR OF PUBLISH"] == year_]["COST"].sum())
        plt.figure("Graph 2")
        plt.bar(x_axis_labels, y_axis_labels)
        plt.xticks(rotation=315)
        plt.xlabel("YEARS")
        plt.ylabel("Cost")
        plt.title("GRAPH : cost of books each year")
        plt.show()

    def plotGraph3():
        df_ = read_csv("db/issued_books_data.csv")
        df_["ISSUE_YEAR"] = df_["ISSUE DATE"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").date().year)
        x_axis_labels = []
        y_axis_labels = []
        for year_ in sorted(df_["ISSUE_YEAR"].drop_duplicates()):
            x_axis_labels.append(str(year_))
            y_axis_labels.append(len(df_[df_["ISSUE_YEAR"] == year_]))
        plt.figure("Graph 3")
        plt.bar(x_axis_labels, y_axis_labels)
        plt.xticks(rotation=315)
        plt.xlabel("YEARS")
        plt.ylabel("No. of Books")
        plt.title("GRAPH : No. of books issued each year")
        plt.show()

    def plotGraph4():
        df_ = read_csv("db/issued_books_data.csv")
        df_["RETURN DATE"] = df_["RETURN DATE"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        df_["ISSUE DATE"] = df_["ISSUE DATE"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
        plt.figure("Graph 4")
        plt.bar(df_["SNO."], Series(df_["RETURN DATE"] - df_["ISSUE DATE"]).dt.days)
        plt.xticks(rotation=0)
        plt.xlabel("SNO. of clients")
        plt.ylabel("Days")
        plt.title("GRAPH : No. of days up to which book kept by each client")
        plt.show()

    def plotGraph5():
        df_ = read_csv("db/issued_books_data.csv")
        plt.figure("Graph 5")
        bars_ = plt.bar(["STILL ISSUED", "RETURNED"], [len(df_[df_["IS RETURNED"] == False]), len(df_[df_["IS RETURNED"]])])
        bars_[0].set_color("red")
        bars_[1].set_color("green")
        plt.xticks(rotation=0)
        plt.xlabel("ISSUED/RETURNED")
        plt.ylabel("No. of books")
        plt.title("GRAPH : No. of issued and returned books")
        plt.show()
    # --------------------- (END) SOME FUNCTIONS ---------------------


    fr_graphs_cards = Frame(graph_canvas, bg="#FFFFFF")
    # ---------------------- ROW 1 STARTS ---------------------
    cards_row_1 = Frame(fr_graphs_cards)
    card_1 = Frame(cards_row_1, bg="#FFFFFF")
    createGraphCard(card_1, "Graph 1", "Plot shows number of books published each year.\n\nX-AXIS : Year\nY-AXIS : No. of books\nTYPE : PLOT", plotGraph1)
    card_1.pack(fill=X, side=LEFT, expand=True)

    card_2 = Frame(cards_row_1, bg="#FFFFFF")
    createGraphCard(card_2, "Graph 2", "Bar graph shows money invested on books each year.\n\nX-AXIS : YEAR\nY-AXIS : Cost\nTYPE : BAR-GRAPH", plotGraph2)
    card_2.pack(fill=X, side=LEFT, expand=True)

    card_3 = Frame(cards_row_1, bg="#FFFFFF")
    createGraphCard(card_3, "Graph 3", "Plot shows number of books issued each year.\n\nX-AXIS : YEAR\nY-AXIS : No. of books\nTYPE : PLOT", plotGraph3)
    card_3.pack(fill=X, side=LEFT, expand=True)
    cards_row_1.pack(fill=X, pady=5)
    # ---------------------- ROW 1 END ---------------------

    # ---------------------- ROW 2 START ---------------------
    cards_row_2 = Frame(fr_graphs_cards)
    card_4 = Frame(cards_row_2, bg="#FFFFFF")
    createGraphCard(card_4, "Graph 4", "Bar graph shows no. of days up to which each client has kept the book.\n\nX-AXIS : SNO. of clients\nY-AXIS : Days\nTYPE : BAR-GRAPH", plotGraph4)
    card_4.pack(fill=X, side=LEFT, expand=True)

    card_5 = Frame(cards_row_2, bg="#FFFFFF")
    createGraphCard(card_5, "Graph 5", "Bar graph shows total no. of issued and returned books till now.\n\nX-AXIS : Issued/Returned\nY-AXIS : No. of books.\nTYPE : BAR-GRAPH", plotGraph5)
    card_5.pack(fill=X, side=LEFT, expand=True)
    cards_row_2.pack(fill=X, pady=5)
    # ---------------------- ROW 2 END ---------------------

    fr_graphs_cards.pack(fill=BOTH, expand=True)
    graph_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

btn_graphs = Button(row_2_fr, text="Graphs", font=("Cascadia Code", 18), width=20, bg="#dbffd9", relief="ridge", command=onClickGraphs)
btn_graphs.pack(side=LEFT)

def onAbout():
    btn_about.config(state="disabled")
    aboutWin = Toplevel(root)
    aboutWin.title("About")
    aboutWin.transient(root)
    aboutWin.resizable(False, False)
    def onCloseAbout():
        btn_about.config(state="normal")
        aboutWin.destroy()
    aboutWin.protocol("WM_DELETE_WINDOW", onCloseAbout)

    lbl_about = Label(aboutWin, text="About", font=("Bahnschrift SemiBold", 20, "underline"), bg="#7d97ff", fg="#0000ff")
    lbl_about.pack(fill=X, anchor=N)

    lbl_para1 = Label(aboutWin, text="Project : Digital Library Software\nPurpose : To keepup library management work with era of IT.\nYear of Development : 2024", font=("Cascadia Code", 16), anchor=W, justify=LEFT, wraplength=500)
    lbl_para1.pack(fill=X, anchor=N, padx=5, pady=8)

    lbl_para1 = Label(aboutWin, text="Developed By : ______\nGrade : _____", font=("Cascadia Code", 16), anchor=W, justify=LEFT, wraplength=500, bg="#212121", fg="#ffffff")
    lbl_para1.pack(fill=X, anchor=N)
    aboutWin.mainloop()

btn_about = Button(row_2_fr, text="About", font=("Cascadia Code", 18), width=20, bg="#dbffd9", relief="ridge", command=onAbout)
btn_about.pack(side=RIGHT)
row_2_fr.pack(fill=X, expand=True, padx=50, pady=30)
fr_options.pack(fill=X, padx=10, pady=10)
# --------------------- END HOME PAGE OPTIONS ----------------------

home_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
# ------------------------- HOMEPAGE END -----------------------

root.mainloop()
