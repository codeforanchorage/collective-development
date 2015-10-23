# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box_url = "https://opscode-vm.s3.amazonaws.com/vagrant/opscode_ubuntu-12.04_provisionerless.box"
  config.vm.box = "opscode-12.04"

  config.vm.provider(:virtualbox) do |vb|
    vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
    vb.customize ['modifyvm', :id, '--natdnsproxy1', 'on']
  end

  config.vm.network 'private_network', ip: '192.168.61.2'

  config.vm.provision(:shell) do |s|
    s.path = "vagrant-bootstrap.sh"
  end

end
