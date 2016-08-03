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

#To generate the introspection hardware data in csv file for a node
def generate_introspection_hw_data(json_data,file_name):
        csvfile = open(file_name+'.csv', 'wt')
        try:
                writer=csv.writer(csvfile)
                writer.writerow(['System Information'])
                writer.writerow(['CPU\'s',json_data['cpus']])
                writer.writerow(['Memory MB',json_data['memory_mb']])
                writer.writerow(['ipmi_address',json_data['ipmi_address']])
                writer.writerow(['Boot Interface',json_data['boot_interface']])

                if json_data['extra']:
                        writer.writerow(['OS Version',json_data['extra']['system']['os']['version']])
                        writer.writerow(['OS Vendor',json_data['extra']['system']['os']['vendor']])
                        writer.writerow(['Product Name',json_data['extra']['system']['product']['name']])
                        writer.writerow(['Product UUID',json_data['extra']['system']['product']['uuid']])
                        writer.writerow(['Product Vendor',json_data['extra']['system']['product']['vendor']])
                        writer.writerow(['Product Version',json_data['extra']['system']['product']['version']])
                        writer.writerow(['Kernel Arch',json_data['extra']['system']['kernel']['arch']])
                        writer.writerow(['Kernel Version',json_data['extra']['system']['kernel']['version']])
                        writer.writerow(['Bios Vendor',json_data['extra']['firmware']['bios']['vendor']])
                        writer.writerow(['Bios Version',json_data['extra']['firmware']['bios']['version']])
                        writer.writerow(['Bios Date',json_data['extra']['firmware']['bios']['date']])
                        writer.writerow([])
                        writer.writerow(['System Vendor Information'])
                        writer.writerow(['Manufacturer',json_data['inventory']['system_vendor']['manufacturer']])
                        writer.writerow(['Product Name',json_data['inventory']['system_vendor']['product_name']])
                        writer.writerow(['Serial Number',json_data['inventory']['system_vendor']['serial_number']])
                        writer.writerow([])
                        writer.writerow(['NIC Information'])
                        writer.writerow(['NIC','IP','MAC']);
                        for key in json_data['all_interfaces']:
                                writer.writerow([key,json_data['all_interfaces'][key]['ip'],json_data['all_interfaces'][key]['mac']])
                        writer.writerow([])
  			writer.writerow(['CPU Information'])
                        for cpu_key,cpu_value in json_data['inventory']['cpu'].iteritems():
                                writer.writerow([cpu_key,cpu_value])
                        writer.writerow([])
                        writer.writerow(['CPU Extra Information'])
                        writer.writerow(['Physical Count',json_data['extra']['cpu']['physical']['number']])
                        writer.writerow(['Logical Count',json_data['extra']['cpu']['logical']['number']])
                        writer.writerow(['Physid','Product','Vendor','Frequency'])
                        for cpu_key,cpu_value in json_data['extra']['cpu'].iteritems():
                                if cpu_key.startswith('physical_'):
                                        writer.writerow([cpu_value['physid'],cpu_value['product'],cpu_value['vendor'],cpu_value['frequency']])
                        writer.writerow([])
                        writer.writerow(['Disks Information'])
                        writer.writerow(['Name','Vendor','Size','Rotational','Serial','model'])
                        for disk in json_data['inventory']['disks']:
                                writer.writerow([disk['name'],disk['vendor'],disk['size'],disk['rotational'],disk['serial'],disk['model']])
                        writer.writerow([])
                        writer.writerow(['Disks Extra Information'])
                        writer.writerow(['Logical Count',json_data['extra']['disk']['logical']['count']])
                        for disks_key,disks_value in json_data['extra']['disk'].iteritems():
                                if disks_key !='logical':
                                        writer.writerow([disks_key])
                                        for disk_key,disk_value in disks_value.iteritems() :
                                                writer.writerow([disk_key,disk_value])

                        writer.writerow([])
                        writer.writerow(['Root Disk Information'])
                        for rdisk_key,rdisk_value in json_data['root_disk'].iteritems():
                                writer.writerow([rdisk_key,rdisk_value])
                        writer.writerow([])
                        writer.writerow(['Network Information'])
                        for nw_key,nw_value in json_data['extra']['network'].iteritems():
                                writer.writerow([nw_key])
                                for nic_key, nic_value in nw_value.iteritems():
                                        writer.writerow([nic_key,nic_value])
                        writer.writerow([])

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
        data=get_introspection_json_data(uid)
        generate_introspection_hw_data(data,'node_'+uid);

