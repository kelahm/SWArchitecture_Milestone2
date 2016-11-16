from mailboxLayer import MailboxLayer


#Valid Email Testing
m1 = MailboxLayer("mcfarland.kelah@gmail.com")
print(m1.verifyEmail())

m2 = MailboxLayer("imkelah@yahoo.com")
print(m2.verifyEmail())

#Invalid Email Testing
w = MailboxLayer("me@example.com")
print(w.verifyEmail())

w1 = MailboxLayer("abc@gmail.com")
print(w1.verifyEmail())

##Testing emails with msstate.edu domain requires the use of the catch_all protocol
##which is not a part of the free subscription to the Mailboxlayer API.
