import os
from fabric import task, Connection
from invoke import Exit
from dotenv import load_dotenv
load_dotenv()
load_dotenv(dotenv_path='./prod.env', verbose=True)

my_hosts = ["root@165.22.122.187"]
deployment_hosts = ["deployer@165.22.122.187"]
user_group = 'deployers'
spoon = os.getenv("SPOON")

full_name_user = 'chris wedgwood'
user_group = 'deployers' 
user_name = 'deployer'

print(spoon) 
# initialize the base directory
abs_dir_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))


@task(hosts=my_hosts)
def start_provision(c):
    """
    Start server provisioning
    """
    

    install_ansible_dependencies(c)
    #create_deployer_group()
    #create_deployer_user()
    #upload_keys()
    #set_selinux_permissive()
    #run('service sshd reload')
    
    #upgrade_server(c)
    create_deployer_group(c)
    create_deployer_user(c)


def create_deployer_group(c):
    """
    Create a user group for all project developers
    """
    groups = c.run('getent group | cut -d: -f1',hide=True)
    groups = str(groups).split('\n')
    if user_group not in groups:
        c.run('groupadd {}'.format(user_group))
    
    
    c.run('mv /etc/sudoers /etc/sudoers-backup')
    c.run('(cat /etc/sudoers-backup; echo "%' +
    user_group + ' ALL=(ALL) ALL") > /etc/sudoers')
    c.run('chmod 440 /etc/sudoers')


def create_deployer_user(c):
    """
    Create a user for the user group
    """
    user = c.run(f'getent passwd {user_name}')
    if not user:
        c.run(f'useradd -c "{full_name_user}" -m -g {user_group} {user_name}')
        c.run(f'passwd {user_name}')
    c.run(f'usermod -a -G {user_group} {user_name}')
    c.run(f'mkdir -p /home/{user_name}/.ssh')
    c.run(f'chown -R {user_name} /home/{user_name}/.ssh')
    c.run(f'chgrp -R {user_group} /home/{user_name}/.ssh')
    c.run(f'cp .ssh/authorized_keys /home/{user_name}/.ssh/authorized_keys')

def upload_keys():
    """
    Upload the SSH public/private keys to the remote server via scp
    """
    scp_command = 'scp {} {}/authorized_keys {}@{}:~/.ssh'.format(
        ssh_keys_name + '.pub',
        ssh_keys_dir,
        user_name,
        host_string
    )
    local(scp_command)

@task
def install_ansible_dependencies(c):
    """
    Install the python-dnf module so that Ansible
    can communicate with Fedora's Package Manager
    """
    c.run('sudo apt update')
    c.run('sudo apt install software-properties-common')
    c.run('sudo apt-add-repository --yes --update ppa:ansible/ansible')
    c.run('sudo apt install ansible')
        
    
def upgrade_server(c):
    """
    Upgrade the server as a root user
    """
    c.run('sudo apt update')
    c.run('sudo apt -y upgrade')
    c.run('python3 -V')
    c.run('sudo apt install -y python3-pip')
    c.run('sudo apt install build-essential libssl-dev libffi-dev python3-dev')
    
@task(hosts=deployment_hosts)
def create_git_ssh(c):
   
    c.run("whoami")
    c.run('''ssh-keygen -t rsa -b 4096 -C "wedgemail@gmail.com"''')
    c.run(f'''eval $(ssh-agent -s);ssh-add /home/{user_name}/.ssh/id_rsa;ssh-add /home/{user_name}/.ssh/id_rsa''')
    c.run(f'cat /home/{user_name}/.ssh/id_rsa.pub')
    c.run('ssh -T git@github.com')
