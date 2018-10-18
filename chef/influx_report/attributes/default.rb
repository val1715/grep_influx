# set below name and full path for generated report (html page)
default['influx_report']['report_name'] = "influx_report.html"
default['influx_report']['report_path'] = "/var/www/influx_report" # do not add last slash, will be added in recipe

# set below name and full path for main python script
default['influx_report']['script_fullpath'] = "/opt/influx_report/influx_report.py"
default['influx_report']['script_path'] = "/opt/influx_report"

# name of os user which is used to create files and run script
default['influx_report']['default_exec_user'] = 'ubuntu'
# hour for cron wher run main script
default['influx_report']['run_time_hour'] = '10'
# minute for cron when run main script
default['influx_report']['run_time_minute'] = '15'

# number of proceses for parallel retriving of information (set it from 3 to 9 for best results)
default['influx_report']['subprocesses'] = 6

# port to open for report hosting via nginx
default['influx_report']['hosted_port'] = 8080
# path and full path of nginx config file for this cookbook (to host generated report)
default['influx_report']['nginx_config_dir'] = '/etc/nginx/conf.d'
default['influx_report']['nginx_config_file'] = '/etc/nginx/conf.d/influx_report.conf'

# host address of influxdb
default['influx_report']['database_host'] = ''
# port number of inxluxdb
default['influx_report']['database_port'] = 8086
# username (login) to use with influxdb
default['influx_report']['database_username'] = ''
