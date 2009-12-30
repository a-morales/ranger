import os
import sys

def main():
	"""initialize objects and run the filemanager"""
	try:
		import curses
	except ImportError as errormessage:
		print(errormessage)
		print('ranger requires the python curses module. Aborting.')
		sys.exit(1)

	from locale import setlocale, LC_ALL
	from optparse import OptionParser, SUPPRESS_HELP

	from ranger import __version__, USAGE
	from ranger.fm import FM
	from ranger.container.environment import Environment
	from ranger.shared.settings import SettingsAware
	from ranger.gui.defaultui import DefaultUI as UI
	from ranger.fsobject.file import File

	setlocale(LC_ALL, 'en_US.utf8')
	os.stat_float_times(True)

	# Parse options
	parser = OptionParser( usage = USAGE,
			version = 'ranger ' + __version__ )

	# Instead of using this directly, use the embedded
	# shell script by running ranger with:
	# source /path/to/ranger /path/to/ranger
	parser.add_option( '--cd-after-exit',
			action = 'store_true',
			dest = 'cd_after_exit',
			help = SUPPRESS_HELP )

	args, rest = parser.parse_args()

	if args.cd_after_exit:
		sys.stderr = sys.__stdout__
	
	# Initialize objects
	target = ' '.join(rest)
	if target:
		if not os.access(target, os.F_OK):
			print("File or directory doesn't exist: %s" % target)
			sys.exit(1)
		elif os.path.isfile(target):
			thefile = File(target)
			FM().execute_file(thefile)
			sys.exit(0)
		else:
			path = target
	else:
		path = '.'

	SettingsAware._setup()
	Environment(path)

	try:
		my_ui = UI()
		my_fm = FM(ui=my_ui)
		my_fm.stderr_to_out = args.cd_after_exit

		# Run the file manager
		my_fm.initialize()
		my_ui.initialize()
		my_fm.loop()
	finally:
		# Finish, clean up
		if 'my_ui' in vars():
			my_ui.destroy()
		if args.cd_after_exit:
			try: sys.__stderr__.write(my_fm.env.pwd.path)
			except: pass

if __name__ == '__main__':
	top_dir = os.path.dirname(sys.path[0])
	sys.path.insert(0, top_dir)
	main()