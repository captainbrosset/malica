import os
import sys

geaargs = ""
for arg in sys.argv:
	if arg == 'empty':
		geaargs += "--clear_datastore "
	if arg == 'mate':
		os.system("mate ..")

os.system("dev_appserver.py " + geaargs + " ..")