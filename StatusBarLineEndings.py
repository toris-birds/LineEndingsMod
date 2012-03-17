import sublime, sublime_plugin

s = sublime.load_settings('LineEndings.sublime-settings')

class StatusBarLineEndings(sublime_plugin.EventListener):

	def on_load(self, view):
		if s.get('show_line_endings_on_status_bar'):
			self.show(view)

	def on_activated(self, view):
		if s.get('show_line_endings_on_status_bar'):
			self.show(view)

	def show(self, view):
		if view is not None:
			if view.is_loading():
				sublime.set_timeout(lambda:self.show(view), 100)
			else:
				view.set_status('line_endings', view.line_endings())
				sublime.set_timeout(lambda:view.set_status('line_endings',  view.line_endings()), 400)