#
# Cookbook:: influx_report
# Recipe:: set_influx_report_script
#
# Copyright:: 2018, Valerii Olefir

influx_host = node['influx_report']['database_host']
influx_port = node['influx_report']['database_port']
influx_user = node['influx_report']['database_username']
influx_pass = Chef::EncryptedDataBagItem.load(:users, "#{influx_user}-private")['password']

script_file = node['influx_report']['script_fullpath']
full_name_report = "#{node['influx_report']['report_path']}/#{node['influx_report']['report_name']}"

Chef::Log.info('Starting influx_report_script recipe from influx_report')

# creating directory for generated report
directory "#{node['influx_report']['report_path']}" do
  mode                  '0755'
  owner                 node['influx_report']['default_exec_user']
  recursive             true
  action                :create
end

# creating directory for script
directory "#{node['influx_report']['script_path']}" do
  mode                  '0755'
  owner                 node['influx_report']['default_exec_user']
  recursive             true
  action                :create
end

# create main script from template and put it to script directory
template script_file do
  source                "grep_script.py.erb"
  owner                 node['influx_report']['default_exec_user']
  mode                  '0755'
  variables(
    :host               => influx_host,
    :port               => influx_port,
    :user               => influx_user,
    :password           => influx_pass,
    :num_of_connections => node['influx_report']['subprocesses'],
    :num_of_threads     => node['influx_report']['threads'],
    :out_file_name      => full_name_report
  )
end

# create cron record to run generated script periodically
cron 'generate_influxdb_report' do
  action                :create
  hour                  node['influx_report']['run_time_hour']
  minute                node['influx_report']['run_time_minute']
  user                  node['influx_report']['default_exec_user']
  command               "python3 #{script_file}"
end

Chef::Log.info('Finished influx_report_script recipe from influx_report')
