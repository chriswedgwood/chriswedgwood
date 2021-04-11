# AWS Deployment Guide

# SSH into Server

chmod 400 connect.pem

ssh -i connet.pem  user@ipaddress 

# Ansible Vault
The following files are encrypted with ansible-vault
For ssh:
sudo ansible-vault encrypt .ansible/production/connect.pem 

For ansible variables:
sudo ansible-vault encrypt .ansible/production/group_vars/all 

For environment variables on the app server:
sudo ansible-vault encrypt .ansible/production/roles/common/templates/env.j2 

OR 
ansible-vault encrypt .ansible/production/roles/common/templates/env.j2  .ansible/production/group_vars/all .ansible/production/connect.pem 

DECRYPT

ansible-vault decrypt .ansible/production/roles/common/templates/env.j2  .ansible/production/group_vars/all .ansible/production/connect.pem 


# Run playbook from local

ansible-playbook ./production/deploy.yml --private-key=./production/connect.pem  -u ubuntu -i ./production/hosts -v


# Connect to AWS RD Postgres

Make sure it can be publically accessed. Click Modify , expand configurations 


psql --host=mypostgresql.c6c8mwvfdgv0.us-west-2.rds.amazonaws.com --port=5432 --username=awsuser --password --dbname=mypgdb 

# NGINX

Find nginx folders
`find / -xdev 2>/dev/null -name "nginx"`

# LOGS IN UBUNTU


systemctl status nginx.service 
sudo journalctl -xe

#TODO MUST ADD permissions into deployment 



# CERTBOT

TODO need to automate this but in the mean time these can be run after first deployment 

sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx

sudo certbot --nginx -d chriswedgwood.com -d www.chriswedgwood.com

sudo ufw enable
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'


sudo certbot renew --dry-run


# DIGITAL OCEAN

Create droplet
Change .ansible/production/hosts to be ip

#Create deployer user

ansible-playbook ./.ansible/production/provision.yml --private-key=./.ansible/production/connect.pem  -u root -i ./.ansible/production/hosts -v

#Run deployment

ansible-playbook ./.ansible/production/deploy.yml --private-key=./.ansible/production/connect.pem  -u root -i ./.ansible/production/hosts -v

# TROUBLESHOOTUNG

#502 Bad Gateway

systemctl status nginx.service 
sudo journalctl -xe
read gunicorn logs in app root and you should discover the issue in one of them

# DATABASE CONNECTIVITY FROM OUTSIDE SERVER FOR PG_DUMP
pg_dump: error: connection to database "chriswedgwood" failed: could not connect to server: Operation timed out
        Is the server running on host "ip" and accepting
        TCP/IP connections on port 5432?

You need to check the firewall and open acces to port 5432. SSH onto the box and run:

cat /etc/postgresql/10/main/postgresql.conf
vi /etc/postgresql/10/main/postgresql.conf
i
make change
esc
:wq
sudo systemctl restart postgresql
vi /etc/postgresql/10/main/pg_hba.conf
host    all             all              0.0.0.0/0                            md5























