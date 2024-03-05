#!/usr/bin/env python
# coding: utf-8

# In[5]:


import tkinter as tk
import smtplib
import firebase_admin
from firebase_admin import credentials, firestore
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Initialize Firebase app
cred = credentials.Certificate('D:\IFT 520\emailencryption-45057-firebase-adminsdk-srix3-87fd26d942.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Create GUI window
root = tk.Tk()
root.title('Compose Email')
root.geometry('500x400')

# Email field
email_label = tk.Label(root, text='Recipient Email:')
email_label.place(x=50, y=50)
email_entry = tk.Entry(root, width=30)
email_entry.place(x=200, y=50)

# Subject field
subject_label = tk.Label(root, text='Subject:')
subject_label.place(x=50, y=100)
subject_entry = tk.Entry(root, width=30)
subject_entry.place(x=200, y=100)

# Message field
message_label = tk.Label(root, text='Message:')
message_label.place(x=50, y=150)
message_text = tk.Text(root, height=10, width=40)
message_text.place(x=100, y=175)

def rsa_encrypt(message):
    # Generate RSA key pair
    key_pair = RSA.generate(2048)

    # Encrypt message with public key
    public_key = key_pair.publickey()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())

    # Encode encrypted message in base64 for storage
    encoded_message = base64.b64encode(encrypted_message)

    return encoded_message, key_pair.export_key()

def send_email():
    recipient = email_entry.get()
    subject = subject_entry.get()
    message = message_text.get('1.0', 'end-1c')

    try:
        # RSA encryption
        encoded_message, public_key = rsa_encrypt(message)

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('emailencryptionift520@gmail.com','mpgastfwvfemjqwm')
        server.sendmail('your_email@gmail.com', recipient, f'Subject: {subject}\n\n{encoded_message}')
        server.quit()

        # Save email to Firebase
        doc_ref = db.collection('sent_emails').document()
        doc_ref.set({
            'recipient': recipient,
            'subject': subject,
            'message': encoded_message,
            'public_key': public_key.decode()
        })

        # Reset fields
        email_entry.delete(0, 'end')
        subject_entry.delete(0, 'end')
        message_text.delete('1.0', 'end')

        # Show success message
        success_label = tk.Label(root, text='Email sent successfully!', fg='green')
        success_label.place(x=180, y=320)
    except Exception as e:
        # Show error message
        error_label = tk.Label(root, text=f'Error: {e}', fg='red')
        error_label.place(x=220, y=320)

# Send button
send_button = tk.Button(root, text='Send', command=send_email)
send_button.place(x=200, y=350, width=100)

root.mainloop()


# In[ ]:




