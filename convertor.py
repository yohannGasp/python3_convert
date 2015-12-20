#!/usr/bin/python3
#===================================================================================================
#  Convertor Bank 
#===================================================================================================
import time
import json
import os
import sys
import glob
import threading
import sqlite3
import shutil
#===================================================================================================
#  Global parameters
#===================================================================================================

PATH_IN   = ''
PATH_OUT  = ''
mask      = ''
# SLEEP     = 50

#===================================================================================================
#  Class convertor_sbrf3_to_front
#===================================================================================================
class convertor_sbrf3_to_front:

	SHABLON   =  ''
	delimeter = ''

	def __init__(self):
		pass
		
	def m(self, x):
		print(self.attr * self.arg * x)
		
	#===================================================================================================
	# function convert 
	#===================================================================================================
	def convert(self, file_in, file_out):
		try:
			f = open(str(file_in),'r')
			f_out = open(str(file_out),'w')		
			for line in f:
				if not line.find("PR2:") == -1: # need line
					#===================================================================================
					#  parsing tags
					#===================================================================================
					start = 0
					while not line.find("|", start) == -1:
						st = line.find("|", start) + 1
						elem = line[st:line.find("|", st)]
						elem = elem.split(":")
						tag = elem[0]
						if len(elem) == 2:
							val = elem[1]
						
						if tag == 'RT4':
							RT4 = val
						if tag == 'SD1':
							SD1 = val
						if tag == 'PR2':
							PR2 = val
			
						start = line.find("|", start) + 1
					#===================================================================================
					#  stroka
					#===================================================================================
					# SHABLON = "#NUMPP#DOC#RT4#SD1#PR2#PR2#"
	
					stroka = ""
					start1 = 0
					SHABLON = self.SHABLON
					delimeter = self.delimeter					
					while not SHABLON.find("#", start1) == -1:
						st1 = SHABLON.find("#", start1) + 1
						elem1 = SHABLON[st1:SHABLON.find("#", st1)]
				
						if elem1 == 'RT4':
							stroka += RT4 + delimeter
						if elem1 == 'SD1':
							stroka += SD1 + delimeter
						if elem1 == 'PR2':
							stroka += PR2 + delimeter
						
						start1 = SHABLON.find("#", start1) + 1
					#===================================================================================
					#  stroka write to file check doubl !!!!
					#===================================================================================
					f_out.write(stroka + '\n')
	
		except Exception:
			print("#==================================")
			print(type(Exception.args))
			print("#==================================")
	
		finally:
			f.close()
			f_out.close()
		
cnv = convertor_sbrf3_to_front()
#===================================================================================================
#  Settings 
#===================================================================================================
try:

	conf = open('sett.conf','r')
	param = conf.read()
	js_param = json.loads(param)

	cnv.SHABLON   = js_param['SHABLON']
	cnv.delimeter = js_param['delimeter']

	PATH_IN  = js_param['path_in']
	PATH_OUT = js_param['path_out']
	mask     = js_param['mask']	
	SLEEP    = js_param['sleep']
	LOG      = js_param['log']
	SQLITE3  = js_param['sqlite3']
	ARHIV    = js_param['arhiv']
	
	connection = sqlite3.connect(SQLITE3)
	cursor = connection.cursor()
	
	# print(PATH_IN)
	# print(PATH_OUT)
	# print(SHABLON)
	
	# f = open(str(PATH_IN),'r')

except ValueError:
	print("#==================================")
	print("#  error json")
	print("#==================================")

except FileNotFoundError :
	print("#==================================")
	print("# not file sett.conf")
	print("#==================================")
#===================================================================================================
# function find_files 
#===================================================================================================
def find_files(x):
	logs('start thread: ' + str(x))
	names = glob.glob(PATH_IN + mask)     # все файлы и поддиректории в "с:\home"
	for name in names:
		if os.path.isfile(name):  # если это файл (а не директория)
			logs(str(x) + name)            # делаем что-нибудь с ним
			cnv.convert(name, PATH_OUT)
			shutil.move(name, ARHIV) # переместить

			
#===================================================================================================
# function logs 
#===================================================================================================
def logs(msg):
	try:
		log = open(str(LOG),'a')
		log.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + msg + '\n')
	finally:
		log.close()
#===================================================================================================
# function checksDouble 
#===================================================================================================
def checksDouble(num,sum_):
	cursor.execute('select num from name where num = ' + num + ' and sum = ' + sum_)
	for r in cursor:
		if r == num:
			return True
		else:
			return False
	cursor.close()
			
#===================================================================================================
#  Loops 
#===================================================================================================
while True:	

# dir1 = PATH_IN
# names = os.listdir(dir1)   # список файлов и поддиректорий в данной директории
# for name in names:
#     fullname = os.path.join(dir1, name)  # получаем полное имя
#     if os.path.isfile(fullname):        # если это файл...
#         print(fullname)                  # делаем что-нибудь с ним
	t1 = threading.Thread(target=find_files, args=(0,))
	t1.start()
	t1.join()
	print('ok')

	time.sleep(int(SLEEP))