Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "functional/deploy.yml"
    ansible.verbose  = true
  end
  config.vm.synced_folder ".", "/home/vagrant/chriswedgwood"
end

