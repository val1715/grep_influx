
# Inxlux_report

#### Creating and using python3 script to generate html report about structure of given influxdb database:

This cookbook generate python script from input parameters and create a cron job on instance to run generated script (daily).
Main script when running connects to given influxdb server and retrives information from that server as:
- each database name;
- measurements for each database;
- fields for each measurement in every database;
- tags for each measurement in every database;
- time of last write for each field (every measurement, every database);

#### Resulting html report has next structure:

| DATABASE | MEASUREMENT | TAG   | FIELD | time of last write to field |
| -------- | ----------- | ---   | ----- | --------------------------- |
| (name)   | (name)      | (name)| (name)| (time)                      |

#### Password for database:

Use encrypted databag to store your password for infxluxdb.
If you don't have one - create it.
```
knife data bag from file users influxdbuser-private.json --secret-file /tmp/encrypted_data_bag_secret
```
See details at: https://docs.chef.io/data_bags.html

Cookbook configured to look for databag as `databags/users/#{username}-private.json` databag for password but you can update it according to personal needs.

## Check attribute file to set your own input parameters

#### Number of processes:
One python3 process for this script typically use 307 MB of virtual memory. So don't make number of connections more than instance can supply with memory size (my proposal = not more than 40 % of RAM).
So:
 * for 4gb instance = 4 connections;
 * for 8gb instance = 8 connections;
 * for 16gb instance = 16 connections;

See details about memory usage:
https://stackoverflow.com/questions/23369937/python-memory-consumption-on-linux-physical-and-virtual-memory-are-growing-whil/23402745#23402745
