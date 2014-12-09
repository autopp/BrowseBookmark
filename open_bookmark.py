import sublime
import sublime_plugin

import webbrowser

SETTINGS_FILE_NAME = "BrowseBookmark.sublime-settings"
def load_bookmarks():
    return sublime.load_settings(SETTINGS_FILE_NAME).get('bookmarks', [])

def is_page(b):
    return b['kind'] == 'page'

def unfold_bookmarks(bookmarks, prefix = ""):
    ret = []
    for b in bookmarks:
        if is_page(b):
            b['prefix'] = prefix
            ret.append(b)
        else:
            ret.extend(unfold_bookmarks(b['bookmarks'], prefix + b['title'] + "/"))
            
    return ret

def make_unfolded_item(b):
    ret = [b['title'], b['url']]
    if 'desc' in b :
        desc = b['desc']
        if type(desc) == list:
            ret.extend([str(d) for d in desc])
        else:
            ret.apped(str(desc))
    return ret

class BrowseFoldedBookmarkCommand(sublime_plugin.WindowCommand):
    def run(self, bookmarks = None):
        pass

class BrowseUnfoldedBookmarkCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.bookmarks = unfold_bookmarks(load_bookmarks())
        items = [make_unfolded_item(b) for b in self.bookmarks]
        self.window.show_quick_panel(items, self.on_done)
        
    def on_done(self, idx):
        if idx < 0:
            return
        
        b = self.bookmarks[idx]
        webbrowser.open_new_tab(b['url'])
