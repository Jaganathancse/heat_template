#!/usr/bin/python

import subprocess
import json
import csv

#To run a command and returns the command line output
def run_command(cmd):
        return subprocess.check_output(cmd,shell=True)

#To run introspection commands and captures node json hardware data using uid
def get_introspection_json_data(node_uid):
        cmd='source ~/stackrc;token=$(openstack token issue -f value -c id);curl -H "X-Auth-Token: $token" http://127.0.0.1:5050/v1/introspection/'+node_uid+'/data | jq .'
        output=subprocess.check_output(cmd,shell=True)
        data=json.loads(output)
        return data

#To generate the csv file with introspection hardware information
def generate_template_content(json_data,file_name):
        csvfile = open(file_name+'.csv', 'wt')
        try:
                writer=csv.writer(csvfile)
                writer.writerow(['NIC Information'])
                writer.writerow(['NIC','IP','MAC']);
                for key in json_data['all_interfaces']:
                        writer.writerow([key,json_data['all_interfaces'][key]['ip'],json_data['all_interfaces'][key]['mac']])
                writer.writerow([])

                writer.writerow(['Memory MB',json_data['memory_mb']])
                writer.writerow(['ipmi_address',json_data['ipmi_address']])
                writer.writerow([])
                writer.writerow(['CPU Information'])
                writer.writerow(['Count','Model Name','Architecture','Frequency'])
                writer.writerow([json_data['inventory']['cpu']['count'],json_data['inventory']['cpu']['model_name'],json_data['inventory']['cpu']['architecture'],
                        json_data['inventory']['cpu']['frequency']])
                writer.writerow([])
                writer.writerow(['Disks Information'])
                writer.writerow(['Name','Vendor','Size'])
                for disk in json_data['inventory']['disks']:
                        writer.writerow([disk['name'],disk['vendor'],disk['size']])

        finally:
                csvfile.close()
        return

#To reads all the nodes uid and returns list
def get_nodes_list():
        uid_list=[]
        node_list=run_command('source ~/stackrc;ironic node-list');
        nodes_data=node_list.split('\n');
        for i in range(3,(len(nodes_data)-2)):
                cols=nodes_data[i].split('|');
                uid_list.append(cols[1].strip());
        return uid_list;

uid_list=get_nodes_list();

for uid in uid_list:
        dict_dat={}
        data=get_introspection_json_data(uid)
        #dict_data=read_required_data(data)
        updated_lines=generate_template_content(data,'nodes_'+uid);

