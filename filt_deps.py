import sys
import re
import os

up = 0
if len(sys.argv) > 1 :
	if not sys.argv[1].isdigit() :
		print('filt_deps [#] [N]')
		print(' #  -- Number of directories up to root')
		print(' N  -- Do not check that file exists')
		exit()
	up = int(sys.argv[1])

check = 1
if len(sys.argv) > 2 and sys.argv[2].upper() == 'N' :
	check = 0

pwd= os.getcwd()

fpath = pwd.split("/")
#print(fpath)
pathlen=len(fpath)-1

#print('Up '+str(up))

pfxix = pathlen - up if pathlen >= up else 0

home='/' + '/'.join(fpath[1:pfxix+1])+'/'

pfx=""
if up > 0 :
	for ix in range(up) :
		pfx = pfx + '../'
	#print('Pfx '+pfx)

relpath='/'.join(fpath[pfxix+1:])
#print(' Relpath ' + relpath)

in_dep=0

for line in sys.stdin :
	if in_dep == 0 :
		mo = re.search('^([a-z-_.0-9]+):', line)
		if mo == None :
#			print('Not ' + line)
			continue
		tgt = mo.group(1)
		rhs = line[mo.end():]
#		print('Tgt '+tgt)
		in_dep = 1
	else:
		if line[0] != ' ' :
			in_dep = 0
			continue
		rhs = line[1:]

#	print('<< '+rhs)

	while True:
		mo = re.search(' ([^ ]*)',rhs)
		if mo == None : 
			break
		try:
			val = str(mo.group(1)) 
			if len(val) > 0 and val[0] != '\\' and val[0] != '\n' :
				res = val.lstrip().rstrip()
				res = re.sub(home,'',res)
				while True :
					sl = len(res)
					res = re.sub('[^/]+/[.][.]/','', res)
					if len(res) == sl :
						break
				if up > 0 :
					pflen = 0
					while pflen*3+3 < len(res) and res[pflen*3:pflen*3+3] == '../' :
						pflen = pflen + 1
					
#					print(res + ' Now '+str(pfxix)+ ' to ' + str(pathlen-pflen)+ ' '+str(pflen))
					mo_ = re.search('/', res)
					if mo_ == None :
						res = relpath + '/' + res
					else :
						res = res[pflen*3:]
						if pflen > 0 and pfxix+1 < pathlen-pflen :
							res = '/'.join(fpath[pfxix+1:pathlen-pflen]) + '/' + res
#					print('Eny '+res)

				got = 1
				try :
					if check > 0 :
						f = open(val.rstrip(),"r")
						f.close()
				except :
					got = 0

				if got > 0 :
					res = re.sub('[^/]+/[.][.]/','', res)
					res = re.sub('[^/]+/[.][.]/','', res)
					print(res)
		except :
			print('Failure')
			break
		rhs = rhs[mo.end():]

exit()
