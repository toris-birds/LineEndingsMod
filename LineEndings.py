import sublime, sublime_plugin
import os
import threading

Pref = {}
s = {}

def plugin_loaded():
	global s, Pref
	s = sublime.load_settings('LineEndings.sublime-settings')
	Pref = Pref()
	Pref.load()
	s.clear_on_change('reload')
	s.add_on_change('reload', lambda:Pref.load())

class Pref:
	def load(self):
		Pref.show_line_endings_on_status_bar          = s.get('show_line_endings_on_status_bar', True)
		Pref.alert_when_line_ending_is                = [l.lower() for l in s.get('alert_when_line_ending_is', [])]
		Pref.auto_convert_line_endings_to             = s.get('auto_convert_line_endings_to', '')

class StatusBarLineEndings(sublime_plugin.EventListener):

	def on_load(self, view):
		if view.line_endings().lower() in Pref.alert_when_line_ending_is:
			sublime.message_dialog(view.line_endings()+' line endings detected on file:\n\n'+view.file_name());

	def on_pre_save(self, view):
		if Pref.auto_convert_line_endings_to != '' and view.line_endings().lower() != Pref.auto_convert_line_endings_to.lower():
			view.set_line_endings(Pref.auto_convert_line_endings_to)

class SetLineEndingWindowCommand(sublime_plugin.TextCommand):

	def run(self, view, type):
		for view in sublime.active_window().views():
			view.set_line_endings(type)
		StatusBarLineEndings().on_load(sublime.active_window().active_view())

	def is_enabled(self):
		return len(sublime.active_window().views()) > 0

class SetLineEndingViewCommand(sublime_plugin.TextCommand):

	def run(self, view, type):
		view = sublime.active_window().active_view()
		view.set_line_endings(type)
		StatusBarLineEndings().on_load(view)

	def is_enabled(self):
		return len(sublime.active_window().views()) > 0

	def is_checked(self, type):
		if self.view.line_endings().lower() == type:
			return True
		else:
			return False

class ConvertIndentationWindowCommand(sublime_plugin.TextCommand):

	def run(self, view, type):
		for view in sublime.active_window().views():
			if type == 'spaces':
				view.run_command('expand_tabs', {"set_translate_tabs":True})
			else:
				view.run_command('unexpand_tabs', {"set_translate_tabs":True})
		StatusBarLineEndings().on_load(sublime.active_window().active_view())

	def is_enabled(self):
		return len(sublime.active_window().views()) > 0

class GetLineEndingsProjectFilesCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		GetLineEndingsProjectFilesThread().start()

	def is_enabled(self):
		return len(sublime.active_window().folders()) > 0

class GetLineEndingsProjectFilesThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		folders = sublime.active_window().folders()
		line_endings = []
		for path in folders:
			self.recurse(path, line_endings)
		line_endings.sort()
		view = sublime.active_window().new_file()
		view.settings().set('word_wrap', False)
		view.set_scratch(True)
		view.run_command('insert', {'characters' : "\n".join(line_endings)})

	def recurse(self, path, line_endings):
		if os.path.isfile(path):
			line_endings.append('"'+self.line_ending_file(path)+'" '+path)
		elif not os.path.islink(path):
			for content in os.listdir(path):
				file = os.path.join(path, content)
				if os.path.isfile(file):
					line_endings.append('"'+self.line_ending_file(file)+'"  '+file)
				elif not os.path.islink(file):
					self.recurse(file, line_endings)

	def line_ending_file(self, file):
		try:
			with open(file, 'r', newline='') as f:
				f.readline()
			return str(repr(f.newlines))
		except:
			return 'Unknown'