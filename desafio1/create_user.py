#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
import ldap
import csv
import getpass
import sys
import string

########## Constants ##########
LDAP_HOTS = "ldap://localhost"
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

######### main #############
admin_pass = input_ldap_pass()
try_ldap_bind(admin_pass)
