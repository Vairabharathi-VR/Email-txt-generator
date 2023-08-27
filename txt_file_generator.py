import imaplib
import email
import ssl

# Define your email settings
imap_email = 'vairabharathi.vr@gmail.com'  # Replace with your email
imap_password = 'dlajeckttmsbwsby'      # Replace with your password

# Initialize IMAP connection
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(imap_email, imap_password)
imap.select('inbox')

# Fetch all unread emails
status, email_ids = imap.search(None, 'ALL')
email_id_list = email_ids[0].split()

# Create a text file to save the email conversations
text_file_path = 'email_conversations.txt'
with open(text_file_path, 'w') as f:
    for email_id in email_id_list:
        status, msg_data = imap.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        sender_email = msg['From']
        email_subject = msg['Subject']

        if msg.is_multipart():
            email_body = ''
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    email_body += part.get_payload(decode=True).decode()
        else:
            email_body = msg.get_payload(decode=True).decode()

        # Write the email conversation to the text file
        f.write(f"Question : {email_subject}\n")
        f.write(f"{email_body}\n\n")

    # Fetch sent emails
    status, sent_email_ids = imap.search(None, 'SENTBEFORE "25-Aug-2023"')
    sent_email_id_list = sent_email_ids[0].split()

    for sent_email_id in sent_email_id_list:
        status, sent_msg_data = imap.fetch(sent_email_id, '(RFC822)')
        sent_msg = email.message_from_bytes(sent_msg_data[0][1])
        recipient_email = sent_msg['To']
        sent_email_subject = sent_msg['Subject']

        if sent_msg.is_multipart():
            sent_email_body = ''
            for part in sent_msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    sent_email_body += part.get_payload(decode=True).decode()
        else:
            sent_email_body = sent_msg.get_payload(decode=True).decode()

        # Write the sent email conversation to the text file
        f.write(f"Answer : {sent_email_subject}\n")
        f.write(f"{sent_email_body}\n\n")

imap.logout()

print("Email conversations saved to:", text_file_path)
