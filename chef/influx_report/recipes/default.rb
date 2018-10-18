#
# Cookbook:: influx_report
# Recipe:: default
#
# Copyright:: 2018, Valerii Olefir

include_recipe "influx_report::prerequsites"
include_recipe "influx_report::nginx"
include_recipe "influx_report::influx_report_script"
