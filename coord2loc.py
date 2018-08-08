#-*- coding: utf-8 -*-

import os
import urllib2
import json
import pandas as pd
import xlrd
from tqdm import tqdm
import argparse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# user_key = 'YourKey'


def trans_from_excel(src_file, tar_file, start, end):
	print("Loading data from %s" % src_file)
	workbook = xlrd.open_workbook(src_file)
	booksheet = workbook.sheet_by_index(0)
	total_records = []
	list_lon = [] # 经度
	list_lat = [] # 纬度
	list_formatted_address = [] # 结构化地址
	list_district = [] # 所在区
	list_township = [] # 所在街道
	column = [u'经度', u'纬度', u'结构化地址', u'所在区', u'乡镇或街道', u'社区名称', u'建筑物名称', u'门牌信息']
	# column = ['Lon', 'Lat', 'Formatted Address', 'District', 'Township', 'Neighborhood Name', 'Building', 'Street Number']
	print("Start processing...")
	idx = []
	for i in tqdm(range(start, end+1)):
		row_data = booksheet.row_values(i)
		lon = row_data[1] # 经度
		lat = row_data[0] # 纬度
		open_success, res_data = trans_single_list(lon, lat)
		if open_success & (res_data['status']=='1'):
			idx.append(i)
			record = []
			record.append(lon)
			record.append(lat)
			regeo_info = res_data['regeocode']
			record.append(regeo_info['formatted_address'])
			addComponent = regeo_info['addressComponent']
			record.append(addComponent['district'])
			record.append(addComponent['township'])
			record.append(addComponent['neighborhood']['name'])
			record.append(addComponent['building']['name'])
			record.append('%s %s' % (addComponent['streetNumber']['street'], addComponent['streetNumber']['number']))
			total_records.append(record)
	dataframe = pd.DataFrame(total_records, columns=column, index=range(start, end+1))
	dataframe.to_csv(tar_file,index=False,sep=',')
	return dataframe



def trans_single_list(lon, lat):
	tmp_url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location=%.6f,%.6f&key=%s&radius=1000&extensions=all' % (lon, lat, user_key)
	try:
		response = urllib2.urlopen(tmp_url)
	except urllib2.URLError, e:
		open_success = False
		# print("\n F_CDN_____>%s_____"%e.code)
	else:
		open_success = True
		response_data = response.read()
	data_json = json.loads(response_data)
	return open_success, data_json
	# if data_json['status'] == '1':
	# 	return data_json
	# 	# address = data_json['regeocode']['formatted_address']
	# else:
	# 	print("Fail to transfer...")
	# 	print("Info: %s" % data_json['info'])
	# 	exit()

if __name__ == "__main__":
	parse = argparse.ArgumentParser()
	parse.add_argument('--locfile', type = str, default = 'loc.xlsx', 
		help = 'source file')
	parse.add_argument('--s', type = int, default = None, help = 'start')
	parse.add_argument('--e', type = int, default = None, help = 'end')

	loc_file = parse.parse_args().locfile
	start = parse.parse_args().s
	end = parse.parse_args().e

	tar_file = './results/output_%08d-%08d.csv' % (start, end)

	trans_from_excel(loc_file, tar_file, start, end)
