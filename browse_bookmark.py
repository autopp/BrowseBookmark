import sublime
import sublime_plugin

import webbrowser

SETTINGS_FILE_NAME = "BrowseBookmark.sublime-settings"
def load_bookmarks():
    return sublime.load_settings(SETTINGS_FILE_NAME).get('bookmarks', [])

def is_page(b):
    return 'url' in b

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
    ret = [b['prefix'] + b['title'], b['url']]
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
    
    return ret

class BrowseFoldedBookmarkCommand(sublime_plugin.WindowCommand):
    def run(self, backtrace = None):
        if backtrace == None:
            self.backtrace = []
        else:
            self.backtrace = backtrace
            
        if len(self.backtrace) == 0:
            self.bookmarks = load_bookmarks()
            top_item = ["** TOP LEVEL **", "cancel browsing"]
        else:
            self.bookmarks = backtrace[-1]['bookmarks']
            top_item = ["** " + "/".join(b['title'] for b in self.backtrace) + " **", "go back previous folder"]
        
        items = [top_item]
        items.extend(make_folded_item(b) for b in self.bookmarks)
        self.window.show_quick_panel(items, self.on_done, 0, 1)
        
    def on_done(self, idx):
        if idx < 0:
            return
        elif idx == 0:
            if len(self.backtrace) == 0:
                return
            else:
                self.backtrace.pop()
                sublime.set_timeout(lambda: self.window.run_command('browse_folded_bookmark', args = {'backtrace': self.backtrace}), 0)
        else:
            b = self.bookmarks[idx-1]
            if is_page(b):
                webbrowser.open_new_tab(b['url'])
            else:
                self.backtrace.append(b)
                sublime.set_timeout(lambda: self.window.run_command('browse_folded_bookmark', args = {'backtrace': self.backtrace}), 0)
            

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
