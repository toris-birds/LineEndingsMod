import sublime, sublime_plugin

CR="CR"
LF="Unix"
CRLF="Windows"
# map line ending types in settings to CR, LF or CRLF
# key:from, value:to
# Use upper case for keys.
map_LineEndType={
	"CR":CR,	"MAC":CR,
	"LF":LF,	"UNIX":LF,
	"CRLF":CRLF,"WINDOWS":CRLF
}
d_LineEndType={CR:"CR (mac) ", LF:"LF (unix) ", CRLF:"CRLF (windows) "}

k_Pref_ShowStatus="show_line_endings_on_status_bar"
k_Pref_Alert="alert_when_line_ending_is"
k_Pref_AutoConv="auto_convert_line_endings_to"
d_Pref={k_Pref_ShowStatus:True, k_Pref_Alert:set(), k_Pref_AutoConv:""}

#view.set_status("LineEndType","plugin loading...")

def show_LineEndType_in_Status(view):
	Pref().load_Pref_ShowStatus()
	if not d_Pref[k_Pref_ShowStatus]:
		clear_LineEndType_in_Status(view)
		return
	line_end_type=view.line_endings()
	view.set_status("LineEndType",d_LineEndType[line_end_type])
def clear_LineEndType_in_Status(view):
	view.erase_status("LineEndType")
def show_LineEndType_Alert(view):
	Pref().load_Pref_ShowStatus()
	Pref().load_Pref_Alert()
	line_end_type=view.line_endings()
	if line_end_type not in d_Pref[k_Pref_Alert]:
		return
	sublime.message_dialog("Warn: line ending:"+d_LineEndType[line_end_type]+" detected.")
def auto_convert_all_line_ends_on_save(view):
	##### Better to use threads #####
	# Seems to be blocked of slowdown after save...
	Pref().load_Pref_AutoConv()
	line_end_type=d_Pref[k_Pref_AutoConv]
	if not line_end_type:
		return
	#edit=view.begin_edit()
	if line_end_type == CRLF:
		edit=view.begin_edit()
		view.run_command('all_line_ends_to_crlf')
		view.end_edit(edit)
	elif line_end_type == CR:
		edit=view.begin_edit()
		view.run_command('all_line_ends_to_cr')
		view.end_edit(edit)
	elif line_end_type == LF:
		edit=view.begin_edit()
		view.run_command('all_line_ends_to_lf')
		view.end_edit(edit)
	#view.end_edit(edit)


#class LineChecker:
#	line_type_used={CR:False, LF:False, CRLF:False}
#	def reset():
#		self.line_type_used={CR:False, LF:False, CRLF:False}
#	def check_all_line_endings(self, view):
#		##### NOT efficient #####
#		s=view.size()
#		r=sublime.Region(0, s)
#		r_arr=view.split_by_newlines(r)
#		for x in xrange(len(r_arr)):
#			r2=view.full_line(r_arr[x])
#			l=view.substr(r2)[-2:]
#			## allways ends with '\n'...
#			if l[-1]=='\r':
#				self.line_type_used[CR]=True
#				if self.line_type_used[LF] and self.line_type_used[CRLF]:
#					break
#				else:
#					continue
#			if l[-1]=='\n':
#				if (len(l) > 1) and (l[-2]=='\r'):
#					self.line_type_used[CRLF]=True
#					if self.line_type_used[CR] and self.line_type_used[LF]:
#						break
#					else:
#						continue
#				else:
#					self.line_type_used[LF]=True
#					if self.line_type_used[CR] and self.line_type_used[CRLF]:
#						break
#					else:
#						continue
#		msg="CR:"+str(self.line_type_used[CR])
#		msg+=", LF:"+str(self.line_type_used[LF])
#		msg+=", CRLF:"+str(self.line_type_used[CRLF])
#		view.set_status("Test", msg)
#		pass

class Pref:
	def get_LineEndType(self, k):
		if not k:
			return None
		k=k.upper()
		if k not in map_LineEndType:
			return None
		return map_LineEndType[k]
	def load_from_file(self):
		return sublime.load_settings("LineEndingsMod.sublime-settings")
	def load(self):
		s=self.load_from_file()
		self.load_Pref_ShowStatus(s)
		self.load_Pref_Alert(s)
		self.load_Pref_AutoConv(s)
	def load_Pref_ShowStatus(self, s=None):
		# default: True
		d_Pref[k_Pref_ShowStatus]=True
		if not s:
			s=self.load_from_file()
		if not s.get(k_Pref_ShowStatus):
			d_Pref[k_Pref_ShowStatus]=False
			return
		#d_Pref[k_Pref_ShowStatus]=True
	def load_Pref_Alert(self, s=None):
		# default: set()
		d_Pref[k_Pref_Alert].clear()
		if not s:
			s=self.load_from_file()
		arr=s.get(k_Pref_Alert)
		if not arr:
			return
		for k in arr:
			v=self.get_LineEndType(k)
			if not v:
				continue
			d_Pref[k_Pref_Alert].add(v)
	def load_Pref_AutoConv(self, s=None):
		# default: ""
		d_Pref[k_Pref_AutoConv]=""
		if not s:
			s=self.load_from_file()
		k=s.get(k_Pref_AutoConv)
		v=self.get_LineEndType(k)
		if not v:
			return
		d_Pref[k_Pref_AutoConv]=v
		
class EventCatcher(sublime_plugin.EventListener):
	def on_load(self, view):
		show_LineEndType_in_Status(view)
		show_LineEndType_Alert(view)
	#	#LineChecker().check_all_line_endings(view)
	def on_pre_save(self, view):
		clear_LineEndType_in_Status(view)
		##### Disabled auto convert on save #####
		# auto_convert_all_line_ends_on_save(view)
	def on_post_save(self, view):
		show_LineEndType_in_Status(view)
	def on_activated(self, view):
		# When a view gains input focus.
		# (When tab is switched)
		# .. or (When touched sublime window...)
		### DO NOT call show_LineEndType_Alert here.   ###
		### Dialog loop forever ...                    ###
		### If accidentally falled into infinite loop, ###
		### Stop sublime from task manager and         ###
		### edit this file with another editor.        ###
		show_LineEndType_in_Status(view)
		#LineChecker().check_all_line_endings(view)

class StatusBarUpdateLineEndsStatusCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=self.view
		show_LineEndType_in_Status(view)
class AllLineEndsToCrlfCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=self.view
		view.set_line_endings(CRLF)
		show_LineEndType_in_Status(view)
class AllLineEndsToCrCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=self.view
		view.set_line_endings(CR)
		show_LineEndType_in_Status(view)
class AllLineEndsToLfCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=self.view
		view.set_line_endings(LF)
		show_LineEndType_in_Status(view)

##### Main #####
Pref().load()
