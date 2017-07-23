#!/usr/bin/env python3

import censys.ipv4
import sqlite3
import pandas as pd
import censys.export
import requests

c = censys.ipv4.CensysIPv4(api_id="XXXXXXX", api_secret="XXXXXXXX")

fields = ["autonomous_system.name", "443.https.tls.certificate.parsed.subject.organization", "ip", "protocols", "autonomous_system.routed_prefix", "location.city"]
count = 0


def main():
    d = int(0)
    while(1):
        print(" ")
        print('Choose the Input:')
        print('1. Organization name')
        print('2. A subnet/IP')
        print('3. Organization name AND a subnet')
        print('4. Store in a database')
        print('5. Print exsiting Database')
        print('6. Select from exsiting Database [sqlquery]')
        ch = int(input('Select(1/2/3/4/5/6): '))

        if ch == 1:
            org_name = input('Input the name of Organization: ')
            input_org(org_name, d)

        elif ch == 2:
            subnet = input('Input the subnet or ip address (xxx.xxx.xxx.xxx/xx): ')
            input_subnet(subnet, d)

        elif ch == 3:
            org_name = input('Input the name of Organization: ')
            subnet = input('Input the subnet (xxx.xxx.xxx.xxx/xx): ')
            input_both(org_name, subnet, d)

        elif ch == 4:
            d = int(1)

        elif ch == 5:
            db = input('Name of Database:')
            conn = sqlite3.connect(db + '.db')
            print("Database opened!!")
            print(pd.read_sql_query("SELECT IP, CERT_NAME, AUTO_NAME, SUBNET, LOCATION, PORTS from HOSTS", conn))

            conn.close()

        elif ch == 6:
            db = input('Name of Database:')
            conn1 = sqlite3.connect(db + '.db')
            print("Database opened!!")
            print("Column names: IP, CERT_NAME, AUTO_NAME, SUBNET, LOCATION, PORTS | Table: Hosts ")
            sqlquery = input("Enter the query: ")
            print(" ")
            print(pd.read_sql_query(sqlquery, conn1))

            conn1.close()

        elif ch == 7:
            export(1)

        else:
            print('Try Again!!')


def input_org(org_name, d):
    count = 0

    if d == 1:
        conn = create_table()

    try:

        for i in c.search("autonomous_system.name:\"" + org_name + "\"or 443.https.tls.certificate.parsed.subject.organization:\"" + org_name + "\"", fields=fields):
            try:
                for x in i["443.https.tls.certificate.parsed.subject.organization"]:
                    print("Cert_Org_Name: {}".format(x))
                    x_db = x
            except:
                print("Cert_Org_name: Not found!!")
                x_db = "Not Found"
                pass
            try:
                print("Autonomous_system_name: {}".format(i["autonomous_system.name"]))
                auto_db = i["autonomous_system.name"]
            except:
                print("Autonomous_system_name: Not Found!!")
                auto_db = "Not found"
                pass
            print("IP:{}".format(i["ip"]), "")
            print("Subnet:{}".format(i["autonomous_system.routed_prefix"]), "")
            print("Host Location:{}".format(i["location.city"]), "")
            ports_db = ""
            for port in i["protocols"]:
                print("{}|".format(port), end=" ")
                ports_db += port + " "
            print("\n")
            count += 1

            if d == 1:
                insert_table(conn, i["ip"], x_db, auto_db, i["autonomous_system.routed_prefix"], i["location.city"], ports_db)

        print("Number of Hosts found: {}".format(count))

        if d == 1:
            conn.close()

    except:
        print('More than 10,000 results found! API only allows 10,000')


def input_subnet(subnet, d):
    count = 0

    if d == 1:
        conn = create_table()

    for i in c.search("ip:\"" + subnet + "\"", fields=fields):
        try:
            for x in i["443.https.tls.certificate.parsed.subject.organization"]:
                print("Cert_Org_Name: {}".format(x))
                x_db = x
        except:
            print("Cert_Org_name: Not found!!")
            x_db = "Not Found"
            pass

        try:
            print("Autonomous_system_name: {}".format(i["autonomous_system.name"]))
            auto_db = i["autonomous_system.name"]
        except:
            print("Autonomous_system_name: Not Found!!")
            auto_db = "Not found"
            pass

        print("IP:{}".format(i["ip"]), "")
        print("Subnet:{}".format(i["autonomous_system.routed_prefix"]), "")
        print("Host Location:{}".format(i["location.city"]), "")
        ports_db = ""
        for port in i["protocols"]:
            print("{}|".format(port), end=" ")
            ports_db += port + " "
        print("\n")
        count += 1

        if d == 1:
            insert_table(conn, i["ip"], x_db, auto_db, i["autonomous_system.routed_prefix"], i["location.city"], ports_db)

    print("Number of Hosts found: {}".format(count))


def input_both(org_name, subnet, d):

    count = 0

    if d == 1:
        conn = create_table()

    for i in c.search("autonomous_system.name:\"" + org_name + "\" or 443.https.tls.certificate.parsed.subject.organization:\"" + org_name + "\" and ip:\"" + subnet + "\"", fields=fields):
        try:
            for x in i["443.https.tls.certificate.parsed.subject.organization"]:
                print("Cert_Org_Name: {}".format(x))
                x_db = x
        except:
            print("Cert_Org_name: Not found!!")
            x_db = "Not Found"
            pass

        try:
            print("Autonomous_system_name: {}".format(i["autonomous_system.name"]))
            auto_db = i["autonomous_system.name"]
        except:
            print("Autonomous_system_name: Not Found!!")
            auto_db = "Not found"
            pass

        print("IP:{}".format(i["ip"]), "")
        print("Subnet:{}".format(i["autonomous_system.routed_prefix"]), "")
        print("Host Location:{}".format(i["location.city"]), "")
        ports_db = ""
        for port in i["protocols"]:
            print("{}|".format(port), end=" ")
            ports_db += port + " "
        print("\n")
        count += 1

        if d == 1:
            insert_table(conn, i["ip"], x_db, auto_db, i["autonomous_system.routed_prefix"], i["location.city"], ports_db)

    print("Number of Hosts found: {}".format(count))


def create_table():

    db = input('Name of Database:')
    conn = sqlite3.connect(db + '.db')
    print("Database created!!")
    conn.execute('''CREATE TABLE HOSTS
    (IP TEXT PRIMARY KEY     NOT NULL,
    CERT_NAME           TEXT,
    AUTO_NAME           TEXT,
    SUBNET              TEXT NOT NULL,
    LOCATION            TEXT,
    PORTS               TEXT NOT NULL);''')

    return conn


def insert_table(conn, IP, CERT_NAME, AUTO_NAME, SUBNET, LOCATION, PORTS):

    with conn:
        cur = conn.cursor()
        cur.execute("""INSERT OR IGNORE INTO HOSTS (IP,CERT_NAME,AUTO_NAME,SUBNET,LOCATION,PORTS) VALUES (?,?,?,?,?,?)""", (IP, CERT_NAME, AUTO_NAME, SUBNET, LOCATION, PORTS))
        print("Records created successfully")


if __name__ == '__main__':
    main()

    # print(i["443.https.tls.certificate.parsed.subject.organization"], i["protocols"])
