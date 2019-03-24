# Udacity Python Fullstack Project 5: Deploying Item Catalog App

> A deep understanding of exactly what your web applications are doing, how they are hosted, and the interactions between multiple systems are what define you as a Full Stack Web Developer. In this project, you’ll be responsible for turning a brand-new, bare bones, Linux server into the secure and efficient web application host your applications need.

#### Server
1. IPV4: `178.128.92.125`
2. Item Catalog URL: `http://178.128.92.125`

#### Software
1. Apache Server
2. Posgresql Database
3. Python libraries and frameworks: Flask, pip, sqlalchemy

#### Summary of configurations
1. Change SSH port from `22` to `2200`.
2. Set up Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).
3. Add, grant permission, and setup key based authentication for `grader` user.
4. Force users to use SSH to login.
5. Configure the local timezone to UTC.
6. Setup Item Catalog web app up and running with Apache using WSGI


#### Item Catalog
Visit `http://178.128.92.125`
