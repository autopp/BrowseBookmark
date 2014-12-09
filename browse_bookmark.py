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
    ret = [b['prefix'] + b['title'], b['url'], str(b.get('desc', '<no description>'))]
    return ret

def make_entry_text(n):
    n = int(n)
    if n == 0:
        return "no entry"
    elif n == 1:
        return "1 entry"
    else:
        return "%d entries" % n

def make_folded_item(b):
    ret = [b['title']]
    
    if is_page(b):
        ret.append(b['url'])
    else:
        ret[0] = ret[0] + '/'
        ret.append("folder (%s)" % make_entry_text(len(b['bookmarks'])))
    
    ret.append(str(b.get('desc', '<no description>')))
    
    return ret

class BrowseFoldedBookmarkCommand(sublime_plugin.WindowCommand):
    def run(self, bookmarks = None):
        if bookmarks == None:
            self.bookmarks = load_bookmarks()
        else:
            self.bookmarks = bookmarks
        
        items = [make_folded_item(b) for b in self.bookmarks]
        self.window.show_quick_panel(items, self.on_done)
        
    def on_done(self, idx):
        if idx < 0:
            return
        
        b = self.bookmarks[idx]
        if is_page(b):
            webbrowser.open_new_tab(b['url'])
        else:
            sublime.set_timeout(lambda: self.window.run_command('browse_folded_bookmark', args = {'bookmarks': b['bookmarks']}), 1)
            

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
