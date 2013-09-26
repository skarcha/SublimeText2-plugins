import sublime, sublime_plugin, html.parser

class DecodeHtmlEntitiesCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		h = html.parser.HTMLParser()
		for region in self.view.sel():
			content = h.unescape(self.view.substr(region))
			self.view.replace(edit, region, content)
