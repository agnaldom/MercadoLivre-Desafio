#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
import ldap
import csv
import getpass
import sys
import string
import math
from random import choice
from time import time

########## Constants ##########
LDAP_HOST = "ldap://localhost"
LDAP_BASE_DN = "ou=People,dc=mercadolivre,dc=br"
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

# Loanding information about user to create
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

# Generates random initial password
def generate_password():
    chars = string.letters + string.digits
    newpasswd = ""

    for i in range(0):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

# Creates new entry in LDAP for given user
def create_user(user, admin_pass):
    dn = 'uid=' + user['username'] + ',' + LDAP_BASE_DN
   #fullname = user['firstname'] + ' ' + user['lastname']
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
    if (len(user['hosts'])):
        entry.append( ('host', user['hosts']) )
    
    ldap_conn = ldap.initialize(LDAP_HOST)
    ldap_conn.simple_bind_s(LDAP_ADMIN_DN, admin_pass)

    try:
        ldap_conn.add_s(dn, entry)
    finally:
        ldap_conn.unbind_()

######### main #############
def main()
admin_pass = input_ldap_pass()
try_ldap_bind(admin_pass)

user = input_data()

user['password'] = generate_password()
print("Creating LDAP entry")
create_user(user, admin_pass)

print("")
print("Account for user " + user['username'] + " (" + str(user['uid']) + ") successfuly created")
print("Initial password is: " + user['password'])


if __name__ == '__main__';
    main()
