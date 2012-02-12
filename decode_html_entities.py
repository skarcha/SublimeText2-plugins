import sublime, sublime_plugin, HTMLParser

class DecodeHtmlEntitiesCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		h = HTMLParser.HTMLParser()
		for region in self.view.sel():
			content = h.unescape(self.view.substr(region))
			self.view.replace(edit, region, content)