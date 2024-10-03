Hosting Date : 03/10/2024

Reference : https://www.youtube.com/watch?v=LaoYcQsPyD8&t=2s
https://www.linkedin.com/pulse/deploy-django-application-ec2-postgresql-s3-domain-ssl-rashid-xcepf/

Render is used for Database Service : 30 day free service.
Your database will expire on November 2, 2024. The database will be deleted unless 
you upgrade to a paid instance type.

S3 Bucket is used to store media files.
S3 Bucket is connected.

To connect ec2 with our cmd
ssh -i "footprimeEcommerce.pem" ubuntu@ec2-3-91-87-198.compute-1.amazonaws.com

sudo apt update -> To update the package index, it fetches the latest package lists from 
the repositories configured on your system. This allows your package manager to know about 
the newest versions of packages and their dependencies.

apt stands for Advanced Package Tool. It is a package management utility used in Debian-based 
Linux distributions, such as Ubuntu, to manage the installation, upgrade, and removal of software 
packages.

sudo apt install python3-pip python3-dev nginx -> This will install python, pip, and Nginx server


sudo pip3 install virtualenv
sudo apt install python3-virtualenv  -> Creating a python virtual environment




