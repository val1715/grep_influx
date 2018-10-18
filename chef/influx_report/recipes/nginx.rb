#
# Cookbook:: influx_report
# Recipe:: set_nginx
#
# Copyright:: 2018, Valerii Olefir

# add this recipe to test access and view of report as hosted page:
Chef::Log.info('Start install nginx as testing influx_report script')

package 'nginx' do
  action :install
end

directory "#{node['influx_report']['nginx_config_dir']}" do
  mode                  '0755'
  recursive             true
  action                :create
end

template node['influx_report']['nginx_config_file'] do
  source 'default.conf.erb'
  variables(
    :nginx_port => node['influx_report']['hosted_port'],
    :root_folder => node['influx_report']['report_path'],
    :index_page => node['influx_report']['report_name']
  )
  # notifies :restart, resources(:service => 'nginx')
end

service 'nginx' do
  action %i[start enable]
  subscribes :restart, "template[#{node['influx_report']['nginx_config_file']}]", :immediately
end


Chef::Log.info('Finished install nginx as testing influx_report script')
