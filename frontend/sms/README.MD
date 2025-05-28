#file.io for StarSon

file.io is a temorary file sharing API that allows you to upload files(like receipt) and reserve a secure public download link. 
#It is usefull for;
- Gnerating instant links to PDF receipts
-Sending those links via SMS or email
-Avoiding the need for hosting infrastracture during development.
#How It Works
1. your receipt_generator  creates the PDF file.
2. link_generator.py uploads the file to htttps;//file.io
3. send_sms.py uses the link to send an sms
