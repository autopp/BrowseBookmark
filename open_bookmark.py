import sublime
import sublime_plugin

SETTINGS_FILE_NAME = "OpenBookmark.sublime-settings"
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

class OpenFoldedBookmarkCommand(sublime_plugin.WindowCommand):
    def run(self, bookmarks = None):
        pass

class OpenUnfoldedBookmarkCommand(sublime_plugin.WindowCommand):
    def run(self):
        bookmarks = unfold_bookmarks(load_bookmarks())
        
