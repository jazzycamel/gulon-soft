import imaplib
import smtplib
import getpass

def checkmail():
    #Connect to server via SSL
    conn=imaplib.IMAP4_SSL("imap.gmail.com", 993)

    #Login
    conn.login("jazzycamel", getpass.getpass())

    #List mailboxes
    typ,data=conn.list()
    print "Response Code: ", typ
    print "Response", data

    conn.select()
    typ,data=conn.search(None, 'ALL')
    for num in data[0].split():
        typ,data=conn.fetch(num,'(RFC822)')
        print("Message: %s\n%s\n" % (num,data[0][1]))

    conn.close()
    conn.logout()

def sendmail():
    conn=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    conn.login("jazzycamel", getpass.getpass())
    conn.sendmail("jazzycamel@googlemail.com", "rob@gulon.co.uk", "From: jazzycamel@googlemail.com\r\nTo: rob@gulon.co.uk\r\n\r\nHello World")
    conn.set_debuglevel(1)
    conn.quit()

sendmail()
