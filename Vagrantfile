# vagrantfile for CS 1660/2060 Docker Lecture
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "docker-demo"

  # forward ports for demos
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    # update system
    apt-get update
    apt-get install -y curl jq tree

    # install Docker
    apt-get install -y docker.io
    usermod -aG docker vagrant

    # pull common images ahead of time
    docker pull python:3.12-slim
    docker pull nginx:latest
    docker pull alpine:latest

    # clone starter repo (update URL to your actual repo)
    # git clone https://github.com/YOUR_ORG/docker-starter.git /home/vagrant/docker-starter
    # chown -R vagrant:vagrant /home/vagrant/docker-starter

    echo "docker demo VM ready!"
    echo "run: vagrant ssh"
  SHELL
end
