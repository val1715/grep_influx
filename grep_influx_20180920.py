#!/usr/bin/env python3

from influxdb import InfluxDBClient
import json
from multiprocessing import Pool as pool

myuser = ""
mypass = ""
myhost = ""
myport = 8086

maxconnections = 7

container = {}
report_file = 'report_influx.html'

html_startpart = """
    <html>
    	<head>
    		<title>Influxdb structure</title>
    		<style type="text/css">
    			.nav {
    				position: fixed;
                    width:99%;
    				top:0;
    				font: 1.3em arial, sans-serif;
    				text-align: center;
                    background-color:#ffffff;
    			}
    			.content {
    				margin-top:5em;
    			}
    			.row {
    				border: 1px solid black;
    				margin: 3px 0px 3px 0px;
    				background-color: #f2f2f2;
    			}
    			.data_db {
    				float: left;
    				width: 15%;
    				overflow: hidden;
    				background-color: #eeffcc;
    				text-align: center;
    				box-sizing: border-box;
    				vertical-align: middle;
    			}
    			.data_meas {
    				float: left;
    				width: 15%;
    				box-sizing: border-box;
    				text-align: center;
    				overflow: hidden;
    				background-color: #d4d8cc;
    			}
                .content .data_db, .content .data_meas  {
    				font: 1.4em arial, sans-serif;
                }
    			.data_tags {
    				float: left;
    				width: 13%;
    				box-sizing: border-box;
    				text-align: center;
    				background-color: #aee0ff;
    			}
    			.data_fields {
    				float: left;
    				width: 30%;
    				box-sizing: border-box;
    				text-align: center;
    				background-color: #fffdb9;
    			}
    			.field_last_record {
    				float: left;
    				width: 27%;
    				box-sizing: border-box;
    				text-align: center;
    				background-color: #facd49;
    			}
                .content .data_tags span, .content .data_fields span, .content .field_last_record span {
                    border-bottom: 1px dotted #333333;
                }
    			.data_fields span, .data_tags span, .field_last_record span {
    				display: block;
    			}
    			.row::after {
    				content: "";
    				clear: both;
    				display: block;
    			}
    		</style>
    	</head>
    	<body>
    		<div class='nav'> InlfluxDB structure
    			<div class="row">
    				<div class="data_db">
    					<span>DATABASE</span>
    				</div>
    				<div class="data_meas">
    					<span>MEASUREMENT</span>
    				</div>
    				<div class="data_tags">
    					<span>TAGS</span>
    				</div>
    				<div class="data_fields">
    					<span>FIELDS</span>
    				</div>
                    <div class="field_last_record">
                        <span>LAST</span>
                    </div>
    			</div>
            </div>
    		<div class="content">
"""

html_endpart = """
    		</div>
    	</body>
    </html>
"""
################################################################################


'''
### Container dict has next structure:

    container_scheme = {
        database_name = {
            measure_name = {
                "fields_list" = [ list of all fields in measurement (strings) ],
                "fields" = {
                    field_name = {
                        "name" = "field_name",
                        "type" = "field_type",
                        "last_time" = "timestamp of last record to field",
                        "last_value" = "last written value to field",
                        ...
                    }
                },
                "tags" = {
                    "tags_list" = [ list of all tags in measurement (strings) ],
                    tag_name = {
                        name = "tag_name",
                        ...
                    }
                }
            }
        }
    }
'''

'''
### Structure of temporary storage dict:

    working_list = {
        'host' : '',
        'port' : '',
        'user' : '',
        'pass' : '',
        'database' : '',
        'measure' : '',
        'field' : '',
        'tag' : ''
    }
'''
################################################################################




################################################################################
def call_fields(object_call):
    '''
    This function make a call to influxdb and return list of received fields according
    to the input parameters. One function execution make one connection to influx server
    so it can be used paralell.
    '''
    # ''' set local variables from input dict'''
    f_host = object_call['host'];
    f_port = object_call['port'];
    f_user = object_call['user'];
    f_pass = object_call['pass'];
    f_db = object_call['database'];
    f_measure = object_call['measure'];

    # ''' initialize common influxdb connection '''
    f_client = InfluxDBClient(host=f_host, port=f_port, username=f_user, password=f_pass, ssl=True, verify_ssl=True)
    f_client.switch_database(f_db)

    # ''' get fields from measurement '''
    try:
        print(f'Get fields for [{f_measure}] in [{f_db}] database')
        fields_list = f_client.query(f'SHOW FIELD KEYS from "{f_measure}"')
        fields_test = fields_list.raw.get('series', None)
    except Exception as e: # typically if query can not be parsed:
        print(e)
        # break
        return {f_db : {f_measure : []}} # return empty list if erron in query processing
    if fields_test:
        return {f_db : {f_measure : fields_test[0]['values']}} # return list of fields
    else:
        return {f_db : {f_measure : []}} # return empty list if no fields
################################################################################

def call_tags(object_call):
    '''
    This function make a call to influxdb and return list of received tags according
    to the input parameters. One function execution make one connection to influx server
    so it can be used paralell.
    '''
    # ''' set local variables from input dict'''
    f_host = object_call['host'];
    f_port = object_call['port'];
    f_user = object_call['user'];
    f_pass = object_call['pass'];
    f_db = object_call['database'];
    f_measure = object_call['measure'];

    # ''' initialize common influxdb connection '''
    f_client = InfluxDBClient(host=f_host, port=f_port, username=f_user, password=f_pass, ssl=True, verify_ssl=True)
    f_client.switch_database(f_db)

    # ''' get tags from measurement '''
    try:
        print(f'Get tags for [{f_measure}] in [{f_db}] database')
        tags_list = f_client.query(f'SHOW TAG KEYS from "{f_measure}"')
        # print("Tags_list: "+str(tags_list))
        tags_test = tags_list.raw.get('series', None)
        # print('###raw' + str(tags_list.raw))
        # print("Tags_test: "+str(tags_test))

    except Exception as e: # typically if query can not be parsed:
        print(e)
        # break
        return {f_db : {f_measure : []}} # return empty list if error in query processing
    if tags_test:
        return {f_db : {f_measure : tags_test[0]['values']}} # return list of fields
    else:
        return {f_db : {f_measure : []}} # return empty list if no tags
################################################################################

def call_query(obj):
    '''
    This function make a call to influxdb and return list of LAST time and value according
    to the input field-mesurement-database. One function execution make one connection to influx server
    so it can be used paralell.
    '''
    # ''' set local variables from input dict'''
    f_host = obj['host'];
    f_port = obj['port'];
    f_user = obj['user'];
    f_pass = obj['pass'];
    f_db = obj['database'];
    f_measure = obj['measure'];
    f_field = obj['field']
    # ''' initialize common influxdb connection '''
    f_client = InfluxDBClient(host=f_host, port=f_port, username=f_user, password=f_pass, ssl=True, verify_ssl=True)
    f_client.switch_database(f_db)
    try:
        print(f'Get info of last write to db [{f_db}] to measurement [{f_measure}] in field [{f_field}]')
        query_list = f_client.query(f'SELECT LAST("{f_field}") from "{f_measure}"')
        query_list_test = query_list.raw.get('series', None)
    except Exception as e:
        print(e)
    if query_list_test:
        return {f_db : { f_measure : { f_field : { 'time' : query_list_test[0]['values'][0][0],
                                                'value' : query_list_test[0]['values'][0][1] }}}}

################################################################################
def main():
    client = InfluxDBClient(host=myhost, port=myport, username=myuser, password=mypass, ssl=True, verify_ssl=True)
    databases = client.get_list_database()


    for every_db in databases:
        container[every_db['name']] = {} # assign database name - 1-st level;
        client.switch_database(every_db['name'])
        try:
            print(f'Get measurements for [{every_db}] database')
            measurements = client.get_list_measurements();
            # print(measurements)
        except Exception as e:
            print(f'ERROR for database [{every_db}] of get measurements as: [{e}]')
            continue

        for every_meas in measurements:
            container[every_db['name']][every_meas['name']] = {} # assign measure name - 2-nd level;

    # create temporary working object to obtain fields:
    working_list = []
    for each_db in container:
        for each_meas in container[each_db]:
            temp_object = {
                'host' : myhost,
                'port' : myport,
                'user' : myuser,
                'pass' : mypass,
                'database' : each_db,
                'measure' : each_meas
            }
            working_list.append(temp_object)

    ############################################################################
    # get all fields of influx and put them into temporary storage
    with pool(len(working_list) if len(working_list) < maxconnections else maxconnections) as p:
        get_fields_list = p.map(call_fields, working_list)
        get_tags_list = p.map(call_tags, working_list)
    del p # remove pool of workers


    # move info about fields into main storage variable
    for each_record in get_fields_list:
        db_name = list(each_record.keys())[0]
        # print("f> "+db_name) # debug
        meas_name = list(each_record.get(db_name))[0]
        # print("f>> "+meas_name) # debug
        container[db_name][meas_name]['fields_list'] = [] # set empty array for received fields
        container[db_name][meas_name]['fields'] = {} # set empty dict for store info separately
        try:
            for field in each_record[db_name][meas_name]:
                field_name = field[0]
                # print("f>>> "+field_name) # debug
                container[db_name][meas_name]['fields_list'].append(field[0])
                container[db_name][meas_name]['fields'][field_name] = {}
                container[db_name][meas_name]['fields'][field_name]['name'] = field[0]
                container[db_name][meas_name]['fields'][field_name]['type'] = field[1]
        except Exception as e:
            print(f'ERROR - catch during field iteration in working_list for field [{field}]')
            print(e)
            continue

    del get_fields_list # clean temporary storage;

    # move info about tags into main storage variable
    for each_record in get_tags_list:
        db_name = list(each_record.keys())[0]
        # print("t> "+db_name) # debug
        meas_name = list(each_record.get(db_name))[0]
        # print("t>> "+meas_name) # debug
        container[db_name][meas_name]['tags_list'] = [] # set empty array for received tags
        container[db_name][meas_name]['tags'] = {} # set empty dict for store info separately
        try:

            for tag in each_record[db_name][meas_name]:
                tag_name = tag[0]
                # print("t>>> "+tag_name) # debug
                container[db_name][meas_name]['tags_list'].append(tag_name)
                container[db_name][meas_name]['tags'][tag_name] = {}
                container[db_name][meas_name]['tags'][tag_name]['name'] = tag[0]

        except Exception as e:
            print(f'ERROR - catch during tags iteration in working_list for tag [{tag}]')
            print(e)
            continue

    del get_tags_list # clean temporary storage;

    # fill temporary storage for retrive last record to fields
    working_list = []
    for each_db in container:
        # print(">"+str(container[each_db])) # debug
        for each_meas in container[each_db]:
            # print(">>"+str(container[each_db][each_meas])) # debug
            # print(each_db + " > " + each_meas)
            # print(container[each_db][each_meas])
            for each_field in container[each_db][each_meas]['fields_list']:
                # print('## each_ms = '+str(each_ms))
                # print(">>>"+str(container[each_db][each_meas]['fields_list'])) # debug
                temp_object = {
                    'host' : myhost,
                    'port' : myport,
                    'user' : myuser,
                    'pass' : mypass,
                    'database' : each_db,
                    'measure' : each_meas,
                    'field' : each_field
                }
                working_list.append(temp_object)

    # get info about last record to every field time/value:
    with pool(len(working_list) if len(working_list) < maxconnections else maxconnections) as p:
        get_last_records = p.map(call_query, working_list)

    # move received info into main storage:
    for each_record in get_last_records:
        db_name = list(each_record.keys())[0]
        meas_name = list(each_record.get(db_name))[0]
        # print(db_name)  # debug
        # print(meas_name)  # debug
        try:
            for field in each_record[db_name][meas_name]:
                # print(field) # debug
                field_last_time = each_record[db_name][meas_name][field]['time'];
                field_last_value = each_record[db_name][meas_name][field]['value'];
                # move it to CONTAINER
                container[db_name][meas_name]['fields'][field]['last_time'] = field_last_time
                container[db_name][meas_name]['fields'][field]['last_value'] = field_last_value
        except Exception as e:
            print(f'ERROR - parsing working_list for last time record = field [{field}]')
            print(e)
            continue
    del get_last_records # clean temporary storage

    # create and fill html report of all this stuff:
    report = open(report_file, 'w')
    report.write(html_startpart) # write first part for all css style and basic stuff;
    for db in container:
        print(db)
        for meas in container[db]:
            print(meas)
            report.write('<div class="row">')
            report.write(f'<div class="data_db"><span>{db}</span></div>') # end of database block (1-st column);
            report.write(f'<div class="data_meas"><span>{meas}</span></div><div class="data_tags">') # end of measurement block (2-nd column)

            try:
                for tag in container[db][meas]['tags_list']:
                    report.write(f'<span>{tag}</span>')
            except Exception as e:
                print(f'ERROR - Processing [{meas}] in [{db}] and try iterate over ["tags_list"] and catch [{e}]')

            report.write('</div><div class="data_fields">') # end of tags block (3-rd column);

            try:
                for field in container[db][meas]['fields_list']:
                    report.write(f'<span>{field}</span>')
            except Exception as e:
                print(f'Processing [{meas}] in [{db}] and try iterate over ["fields_list"] and catch [{e}]')

            report.write('</div><div class="field_last_record">') # end for fields block (4-th column);
            # report.write('</div>') # end for fields block (4-th column);

            try:
                for field in container[db][meas]['fields_list']:
                    last_time = container[db][meas]['fields'][field]['last_time']
                    last_value = container[db][meas]['fields'][field]['last_value']
                    # report.write(f'<span>[{field}]=>[{last_time}]=[{last_value}]</span>')
                    report.write(f'<span>[{last_time}]</span>')
            except Exception as e:
                print(f'Processing [{meas}] in [{db}] and try iterate over ["fields_list"] to put LAST time/value and catch [{e}]')

            report.write('</div>') # end of last record block
            report.write('</div>') # end for row block

    report.write(html_endpart) # write final closed tags;
    report.close()

    ############################################################################
    # json_file = open('container.json','w')
    # json_file.write(str(container))
    # json_file.close()
    # json_workfile = open('working_list.json','w')
    # json_workfile.write(str(working_list))
    # json_workfile.close()
    ############################################################################

if __name__ == "__main__":
    main()
