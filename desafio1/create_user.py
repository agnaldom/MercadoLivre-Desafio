#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
import ldap
import csv
import getpass
import sys
import string
import math
import smtplib
from random import choice
from time import time

########## Constants ##########
LDAP_HOST = "ldap://localhost:389"
LDAP_BASE_DN = "ou=people,dc=mercadolivre,dc=br"
LDAP_ADMIN_DN = "cn=admin,dc=mercadolivre,dc=br"

######### Funcoes ##############
# Ask for LDAP admin password
def input_ldap_pass():
    return getpass.getpass("Enter LDAP manager password: ")

# This will try to bind to LDAP with admin DN and givem password and exit
# the script with error message if it fails.
def  try_ldap_bind(admin_pass):
    try:
        ldap_conn = ldap.initialize(LDAP_HOST)
    except ldap.SERVER_DOWN:
        print("Can't contact LDAP server")
        exit(4)
    
    try:
        ldap_conn.simple_bind_s(LDAP_ADMIN_DN, admin_pass)
    except ldap.INVALID_CREDENTIALS:
        print("This password is incorrect!")
        sys.exit(3)

    print("Authentization successful")
    print("")

# Lendo informacao sobre usuário
def input_data():
    #user = {}
    user = csv.reader(open('*.csv'), delimiter=',')
    for [name, sobrenome, email, username] in user:
        if (check_username(user["username"])):
            print("This username is already used!")
            sys.exit(2)
    
    # UID
    if (uid == ""):
        user['uid'] = generate_uid()
    else:
        uid = int(uid)
        if (check_uid(uid)):
            print("This UID is already used!")
            sys.exit(2)
        else: 
            user['uid'] = uid

# Gerando uma nova senha
def generate_password():
    chars = string.letters + string.digits
    newpasswd = ""

    for i in range(0):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

# Criando nova entrada no LDAP
def create_user(user, admin_pass):
    dn = 'uid=' + user['username'] + ',' + LDAP_BASE_DN
    fullname = ' '.join(user['firstname'], user['lastname'])
    gid = find_gid(user['group'])
    lastchange = int(math.floor(time() / 86400))

    entry = []
    entry.extend([
        ('objectClass', ["person", "organizationalPerson", "inetOrgPerson", "posixAccount"]),
        ('uid', user['username']),
        ('cn', fullname),
        ('givenname', user['firstname']),
        ('sn', user['lastname']),
        ('mai', user['emai']),
        ('shadowMax', "99999"),
        ('shadowWarning', "7"),
        ('shadowLastChange', str(lastchange)),
        ('userPassword', user['password'])
    ])
       
    ldap_conn = ldap.initialize(LDAP_HOST)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, admin_pass)

    try:
        ldap_conn.add_s(dn, entry)
    finally:
        ldap_conn.unbind_()

# Lendo o template do email
def read_template(filename):
    with opne(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def  send_mail(nomes[], emails[]):
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='servidor_smtp', port=465)
    s.startls()
    s.login(MY_ADDRESS, PASSWORD)

    for name, email in zip(names, emails):
        msg = MIMEMultipart()

        message = message_template.substitute(PERSON_NAME=name.title(), USER_NAME=user['username'], NOVA_SENHA=user['password'])

        print(message)

        # Os paramentros das mensagens
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Novo Acesso de Login"

        s.send_message(msg)
        del msg
    
    s.quit()


######### main #############
def main()
admin_pass = input_ldap_pass()
try_ldap_bind(admin_pass)

user = input_data()

user['password'] = generate_password()
print("Creating LDAP entry")
create_user(user, admin_pass)
send_mail(user['password'], nomes['fullname'], emails['email'] )

print("")
print("Account for user " + user['username'] + " (" + str(user['uid']) + ") successfuly created")
print("Initial password is: " + user['password'])


if __name__ == '__main__';
    main()
