#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
import ldap
import csv
import getpass

########## Constants ##########
LDAP_HOTS = "ldap://localhost"
LDAP_BASE_DN = "ou=People,dc=mercadolivre,dc=br"
LDAP_ADMIN_DN = "cn=admin,dc=mercadolivre,dc=br"

######### Funcoes ##############
# Ask for LDAP admin password
def input_ldap_pass():
    return getpass.getpass("Enter LDAP manager password: ")


######### main #############
admin_pass = input_ldap_pass()