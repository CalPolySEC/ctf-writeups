# PicoCTF 2019 - Irish-Name-Repo 1
Author: PinkNoize

Web Exploitation - 300

> There is a website running at https://2019shell1.picoctf.com/problem/4162/ (link) or http://2019shell1.picoctf.com:4162. Do you think you can log us in? Try to see if you can login!

## TL;DR

This challenge provides a website with an admin panel. SQLi the admin panel for the flag.

# Writeup

Upon loading the supplied webpage, we see a "List 'o the Irish!" We can click the 'hamburger bars' in the top left to find an admin login page. As this is an admin login page, we should try logging as user `admin`. You can guess passwords but it probably won't work.

Typically, users credentials (hopefully some kind of hash) are stored in databases. One class of databases are SQL databases. If the users are stored in a SQL database,  checking if the password is correct will require a query to the database. If this query is not done securely it could be vulnerable to code injection. This is known as [SQL Injection (SQLi)](https://owasp.org/www-community/attacks/SQL_Injection).

If we consider the query that checks the login, it would be something like...

```sql
SELECT * FROM users where user = '<username here>' and pass = '<password here>';
```

To exploit this we could inject code that is always true. For example, let user = `admin` and pass = `' or '1'='1`. When this is added to the query it would look like...

```sql
SELECT * FROM users where user = 'admin' and pass = '' or '1'='1';
```

As `'1' = '1'` is always true, this bypasses the password check. We can do this on the admin login to get the flag, `picoCTF{s0m3_SQL_96ab211c}`.