# Based on Package/Default/sort.py

import sublime, sublime_plugin

# Uglyness needed until SelectionRegions will happily compare themselves
def srcmp(a, b):
    aa = a.begin();
    ba = b.begin();

    if aa < ba:
        return -1;
    elif aa == ba:
        return cmp(a.end(), b.end())
    else:
        return 1;

def length_sort(txt):
    txt.sort(lambda a, b: cmp(len(a), len(b)))
    return txt

def reverse_list(l):
    l.reverse()
    return l

def uniquealise_list(l):
    table = {}
    res = []
    for x in l:
        if x not in table:
            table[x] = x
            res.append(x)
    return res

def shrink_wrap_region( view, region ):
    a, b = region.begin(), region.end()

    for a in xrange(a, b):
        if not view.substr(a).isspace():
            break

    for b in xrange(b-1, a, -1):
        if not view.substr(b).isspace():
            b += 1
            break

    return sublime.Region(a, b)

def shrinkwrap_and_expand_non_empty_selections_to_entire_line(v):
    sw = shrink_wrap_region
    regions = []

    for sel in v.sel():
        if not sel.empty():
            regions.append(v.line(sw(v, v.line(sel))))
            v.sel().subtract(sel)

    for r in regions:
        v.sel().add(r)

def permute_lines(f, v, e):
    shrinkwrap_and_expand_non_empty_selections_to_entire_line(v)

    regions = [s for s in v.sel() if not s.empty()]
    if not regions:
        regions = [sublime.Region(0, v.size())]

    regions.sort(srcmp, reverse=True)

    for r in regions:
        txt = v.substr(r)
        lines = txt.splitlines()
        lines = f(lines)

        v.replace(e, r, u"\n".join(lines))

class SortLinesByLengthCommand(sublime_plugin.TextCommand):
    def run(self, edit, reverse=False, remove_duplicates=False):
        view = self.view

        permute_lines(length_sort, view, edit)

        if reverse:
            permute_lines(reverse_list, view, edit)

        if remove_duplicates:
            permute_lines(uniquealise_list, view, edit)
