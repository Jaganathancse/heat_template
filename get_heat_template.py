#!/usr/bin/python

import subprocess
import json

#To run a command and returns the command line output
def run_command(cmd):
        return subprocess.check_output(cmd,shell=True)

#To run introspection commands and captures node json hardware data using uid
def get_introspection_json_data(node_uid):
        cmd='source ~/stackrc;token=$(openstack token issue -f value -c id);curl -H "X-Auth-Token: $token" http://127.0.0.1:5050/v1/introspection/'+node_uid+'/data | jq .'
        output=subprocess.check_output(cmd,shell=True)
        data=json.loads(output)
        return data

#To capture the required data as tokens and creates dictinary
def read_required_data(json_data):
        dict_data={}
        #if json_data['all_interfaces']['eth0']['ip']=="null":
        dict_data['token1']=json_data['all_interfaces']['eth0']['ip']
        #else:
        #       dict_data['token1']=json_data['all_interfaces']['eth1']['ip']
        return dict_data

#To read heat template file
def read_heat_template_file():
        file_content="";
        with open('heat_template_file') as file:
                file_content = file.readlines()
        return file_content

#To create heat template file
def write_heat_template_file(file_name,file_content):
        fh = open(file_name, "w")
        fh.writelines(file_content)
        fh.close()
        return
#To update the heat template file content
def update_heat_template_content(dict,file_lines):
        list_lines=[]
        for line in file_lines:
                for key,val in dict.items():
                        if val:
                                list_lines.append(line.replace('<'+key+'>',val));
                        else:
                                list_lines.append(line.replace('<'+key+'>',""));
        return list_lines;

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
        dict_data=read_required_data(data)
        lines=read_heat_template_file();
        updated_lines=update_heat_template_content(dict_data,lines);
        write_heat_template_file('node_'+uid+'.yaml',updated_lines);

        #print dict_data['token1']



