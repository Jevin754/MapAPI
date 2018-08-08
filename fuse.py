import os
import glob
import pandas as pd
import argparse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def fuse_all(res_dir):
	files = glob.glob(os.path.join(res_dir, '*.csv'))
	files.sort()
	n_files = len(files)
	total_list = []
	for f in files:
		total_list.append(pd.read_csv(f, sep=','))
	total = pd.concat(total_list)
	tar_file = os.path.join(res_dir, 'total.csv')
	total.to_csv(tar_file,index=False,sep=',')


if __name__ == "__main__":
	parse = argparse.ArgumentParser()
	parse.add_argument('--resdir', type = str, default = './results', 
		help = 'result path')

	res_dir = parse.parse_args().resdir
	fuse_all(res_dir)