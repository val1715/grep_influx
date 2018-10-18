
# install influxdb module for python3:

# get pip for python3 (not included to base AMI)
apt_package 'python3-all'
apt_package 'python3-pip'

# fix locale error of base ubuntu AMI:
execute 'prepare_python3_modules' do
  command 'export LC_ALL="en_US.UTF-8" && python3 -m pip install influxdb'
end
