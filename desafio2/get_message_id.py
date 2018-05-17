import email
import getpass
import imaplib
import os
import sys

detach_dir = '.' # directory where to save attachments (default: current)
user = input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select("INBOX") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

#resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
resp, items = m.uid('search', None, "(SUBJECT Devops SUBJECT DevOps)")
items = items[0].split() # getting the mails id

for mail in items:
    #resp, data = m.fetch(emailid, "`(RFC822)`") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    resp, data = m.fetch(mail, "`(RFC822)`")
    email_body = data[0][1] # getting the mail content
    mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

    #Check if any attachments at all
    if mail.get_content_maintype() != 'multipart':
        continue

    print ("["+mail["From"]+"] :" + mail["Subject"])

    # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
    for part in mail.walk():
        # multipart are just containers, so we skip them
        if part.get_content_maintype() == 'multipart':
            continue

        # is this part an attachment ?
        if part.get('Content-Disposition') is None:
            continue

        #filename = part.get_filename()

        filename = mail["From"] + "_hw1answer"
        
        att_path = os.path.join(detach_dir, filename)

        #Check if its already there
        if not os.path.isfile(att_path) :
            # finally write the stuff
            fp = open(att_path+".csv", 'wb')
            fp.write(part.get_payload(decode=True))
fp.close()