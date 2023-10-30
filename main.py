import smtplib
import imaplib
from email.message import EmailMessage
from tkinter import *


class MailApp:
    def __init__(self, master):
        self.master = master
        master.title("Mail Application")

        # Create GUI elements
        self.to_label = Label(master, text="To:")
        self.to_entry = Entry(master)
        self.subject_label = Label(master, text="Subject:")
        self.subject_entry = Entry(master)
        self.body_label = Label(master, text="Body:")
        self.body_text = Text(master)
        self.send_button = Button(master, text="Send", command=self.send_email)
        self.refresh_button = Button(master, text="Refresh", command=self.refresh_emails)
        self.email_listbox = Listbox(master)

        # Grid layout
        self.to_label.grid(row=0, column=0, sticky="E")
        self.to_entry.grid(row=0, column=1, columnspan=2, sticky="W")
        self.subject_label.grid(row=1, column=0, sticky="E")
        self.subject_entry.grid(row=1, column=1, columnspan=2, sticky="W")
        self.body_label.grid(row=2, column=0, sticky="NE")
        self.body_text.grid(row=2, column=1, columnspan=2, sticky="W")
        self.send_button.grid(row=3, column=0)
        self.refresh_button.grid(row=3, column=1)
        self.email_listbox.grid(row=4, column=0, columnspan=3)

    def send_email(self):
        # Get email details from GUI elements
        to = self.to_entry.get()
        subject = self.subject_entry.get()
        body = self.body_text.get("1.0", END)

        # Create email message
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = 'your_email@gmail.com'
        msg['To'] = to

        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('your_email@gmail.com', 'password')
            smtp.send_message(msg)

    def refresh_emails(self):
        # Clear email listbox
        self.email_listbox.delete(0, END)

        # Connect to email server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('your_email@gmail.com', 'password')
        mail.select('inbox')

        # Search for emails
        status, data = mail.search(None, 'ALL')

        # Retrieve email details and add to listbox
        for i in data[0].split():
            status, data = mail.fetch(i.decode(), '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
            raw_email = data[0][1].decode("utf-8")
            lines = raw_email.split('\r\n')
            from_line = lines[1]
            subject_line = lines[2]
            from_line_parts = from_line.split(': ')
            subject_line_parts = subject_line.split(': ')
            from_field = from_line_parts[1]
            subject_field = subject_line_parts[1]
            self.email_listbox.insert(END, f"From: {from_field}, Subject: {subject_field}")

        # Close connection
        mail.logout()


root = Tk()
app = MailApp(root)
root.mainloop()
