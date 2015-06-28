[Sublime Text 2+](http://www.sublimetext.com/) Package. 

# Status

Just rewritten.

# Description

Original tree is  https://github.com/titoBouzout/LineEndings

This branch is a customized version for Sublime Text 2+

Provides line endings information and convert them for Sublime Text.
Sublime Text: see http://www.sublimetext.com/

# Functions

* Display line endings on status bar.
* Display an alert when loading a file whose line_ending is not some you expect.
* Convert line endings for current view.
	Use right click menu to convert line endings.
	'Auto convert on save' is disabled for this version.


# Settings
Preferences > Package Settings > LineEndingsMod > Setting - User

Setting keys are same as LineEndings.
example: (Setting - User)

	{
		// If you want to see an alert dialog for CRLF line endings
		// (Shown on file loading)
		"alert_when_line_endings_is":
		[
			"Windows"
		]
	}

example: (Setting - Default)

	{
		// line ending types are
		// "Windows", "CRLF",
		// "Unix", "LF",
		// "Mac", "CR" 
		// ("CRLF", "LF" and "Mac" are for LineEndingsMod)
	
		
		// Show line ending on status bar
		// Set true or false
		// Default: true
		"show_line_endings_on_status_bar": true,
		
		// Show an alert when the line ending is on the list.
		// Set line ending types.
		// Default: []
		// example: "alert_when_line_ending_is":["Windows","Unix","CR"]
		"alert_when_line_ending_is" : [],
		
		// // Disable this option and
		// //  try right click and 'change all line endings ...'
		// // It's safer, I think.
		// //
		// // (This option is disabled internally for this branch.)
		// // If set, auto convert line endings on save.
		// // Set "" for no convresion.
		// // Default: ""
		"auto_convert_line_endings_to" : ""
	}

# Notes

No undo for line endings conversion.

# Todo

* Use threads.
* Command pallet

# Contributors

