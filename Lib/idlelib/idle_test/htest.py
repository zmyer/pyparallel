'''Run human tests of Idle's window, dialog, and popup widgets.

run(test): run *test*, a callable that causes a widget to be displayed.
runall(): run all tests defined in this file.

Let X be a global name bound to a widget callable. End the module with

if __name__ == '__main__':
    <unittest, if there is one>
    from idlelib.idle_test.htest import run
    run(X)

The X object must have a .__name__ attribute and a 'parent' parameter.
X will often be a widget class, but a callable instance with .__name__
or a wrapper function also work. The name of wrapper functions, like
'_editor_Window', should start with '_'.

This file must contain a matching instance of the folling template,
with X.__name__ prepended, as in '_editor_window_spec ...'.

_spec = {
    'file': '',
    'kwds': {'title': ''},
    'msg': ""
    }

file (no .py): used in runall() to import the file and get X.
kwds: passed to X (**kwds), after 'parent' is added, to initialize X.
title: an example; used for some widgets, delete if not.
msg: displayed in a master window. Hints as to how the user might
  test the widget. Close the window to skip or end the test.
'''
from importlib import import_module
import tkinter as tk

AboutDialog_spec = {
    'file': 'aboutDialog',
    'kwds': {'title': 'aboutDialog test',
             '_htest': True,
             },
    'msg': "Test every button. Ensure Python, TK and IDLE versions "
           "are correctly displayed.\n [Close] to exit.",
     }

_calltip_window_spec = {
    'file': 'CallTipWindow',
    'kwds': {},
    'msg': "Typing '(' should display a calltip.\n"
           "Typing ') should hide the calltip.\n"
    }

_class_browser_spec = {
    'file': 'ClassBrowser',
    'kwds': {},
    'msg': "Inspect names of module, class(with superclass if "
           "applicable), methods and functions.\nToggle nested items.\n"
           "Double clicking on items prints a traceback print a traceback "
            "for an exception that is ignored."
     }

_color_delegator_spec = {
    'file': 'ColorDelegator',
    'kwds': {},
    'msg': "The text is sample Python code.\n"
           "Ensure components like comments, keywords, builtins,\n"
           "string, definitions, and break are correctly colored.\n"
           "The default color scheme is in idlelib/config-highlight.def"
    }

_dyn_option_menu_spec = {
    'file': 'dynOptionMenuWidget',
    'kwds': {},
    'msg': "Select one of the many options in the 'old option set'.\n"
           "Click the button to change the option set.\n"
           "Select one of the many options in the 'new option set'."
    }

_editor_window_spec = {
   'file': 'EditorWindow',
    'kwds': {},
    'msg': "Test editor functions of interest."
    }

GetCfgSectionNameDialog_spec = {
    'file': 'configSectionNameDialog',
    'kwds': {'title':'Get Name',
             'message':'Enter something',
             'used_names': {'abc'},
             '_htest': True},
    'msg': "After the text entered with [Ok] is stripped, <nothing>, "
           "'abc', or more that 30 chars are errors.\n"
           "Close 'Get Name' with a valid entry (printed to Shell), "
           "[Cancel], or [X]",
    }

GetHelpSourceDialog_spec = {
    'file': 'configHelpSourceEdit',
    'kwds': {'title': 'Get helpsource',
             '_htest': True},
    'msg': "Enter menu item name and help file path\n "
           "<nothing> and more than 30 chars are invalid menu item names.\n"
           "<nothing>, file does not exist are invalid path items.\n"
           "Test for incomplete web address for help file path.\n"
           "A valid entry will be printed to shell with [0k].\n"
           "[Cancel] will print None to shell",
    }

# Update once issue21519 is resolved.
GetKeysDialog_spec = {
    'file': 'keybindingDialog',
    'kwds': {'title': 'Test keybindings',
             'action': 'find-again',
             'currentKeySequences': [''] ,
             '_htest': True,
             },
    'msg': "Test for different key modifier sequences.\n"
           "<nothing> is invalid.\n"
           "No modifier key is invalid.\n"
           "Shift key with [a-z],[0-9], function key, move key, tab, space"
           "is invalid.\nNo validitity checking if advanced key binding "
           "entry is used."
    }

_help_dialog_spec = {
    'file': 'EditorWindow',
    'kwds': {},
    'msg': "If the help text displays, this works.\n"
           "Text is selectable. Window is scrollable."
    }

_io_binding_spec = {
    'file': 'IOBinding',
    'kwds': {},
    'msg': "Test the following bindings\n"
           "<Control-o> to display open window from file dialog.\n"
           "<Control-s> to save the file\n"
    }

_multi_call_spec = {
    'file': 'MultiCall',
    'kwds': {},
    'msg': "The following actions should trigger a print to console or IDLE"
           " Shell.\nEntering and leaving the text area, key entry, "
           "<Control-Key>,\n<Alt-Key-a>, <Control-Key-a>, "
           "<Alt-Control-Key-a>, \n<Control-Button-1>, <Alt-Button-1> and "
           "focusing out of the window\nare sequences to be tested."
    }

_multistatus_bar_spec = {
    'file': 'MultiStatusBar',
    'kwds': {},
    'msg': "Ensure presence of multi-status bar below text area.\n"
           "Click 'Update Status' to change the multi-status text"
    }

_object_browser_spec = {
    'file': 'ObjectBrowser',
    'kwds': {},
    'msg': "Double click on items upto the lowest level.\n"
           "Attributes of the objects and related information "
           "will be displayed side-by-side at each level."
    }

_path_browser_spec = {
    'file': 'PathBrowser',
    'kwds': {},
    'msg': "Test for correct display of all paths in sys.path.\n"
           "Toggle nested items upto the lowest level.\n"
           "Double clicking on an item prints a traceback\n"
           "for an exception that is ignored."
    }

_percolator_spec = {
    'file': 'Percolator',
    'kwds': {},
    'msg': "There are two tracers which can be toggled using a checkbox.\n"
           "Toggling a tracer 'on' by checking it should print tracer"
           "output to the console or to the IDLE shell.\n"
           "If both the tracers are 'on', the output from the tracer which "
           "was switched 'on' later, should be printed first\n"
           "Test for actions like text entry, and removal."
    }

_scrolled_list_spec = {
    'file': 'ScrolledList',
    'kwds': {},
    'msg': "You should see a scrollable list of items\n"
           "Selecting (clicking) or double clicking an item "
           "prints the name to the console or Idle shell.\n"
           "Right clicking an item will display a popup."
    }

_stack_viewer_spec = {
    'file': 'StackViewer',
    'kwds': {},
    'msg': "A stacktrace for a NameError exception.\n"
           "Expand 'idlelib ...' and '<locals>'.\n"
           "Check that exc_value, exc_tb, and exc_type are correct.\n"
    }

_tabbed_pages_spec = {
    'file': 'tabbedpages',
    'kwds': {},
    'msg': "Toggle between the two tabs 'foo' and 'bar'\n"
           "Add a tab by entering a suitable name for it.\n"
           "Remove an existing tab by entering its name.\n"
           "Remove all existing tabs.\n"
           "<nothing> is an invalid add page and remove page name.\n"
    }

TextViewer_spec = {
    'file': 'textView',
    'kwds': {'title': 'Test textView',
             'text':'The quick brown fox jumps over the lazy dog.\n'*35,
             '_htest': True},
    'msg': "Test for read-only property of text.\n"
           "Text is selectable. Window is scrollable.",
     }

_tooltip_spec = {
    'file': 'ToolTip',
    'kwds': {},
    'msg': "Place mouse cursor over both the buttons\n"
           "A tooltip should appear with some text."
    }

_tree_widget_spec = {
    'file': 'TreeWidget',
    'kwds': {},
    'msg': "You should see two canvases side-by-side.\n"
           "The left canvas is scrollable.\n"
           "The right canvas is not scrollable.\n"
           "Click on folders upto to the lowest level."
    }

_widget_redirector_spec = {
    'file': 'WidgetRedirector',
    'kwds': {},
    'msg': "Every text insert should be printed to the console."
           "or the IDLE shell."
    }

def run(*tests):
    root = tk.Tk()
    test_list = [] # List of tuples of the form (spec, callable widget)
    if tests:
        for test in tests:
            test_spec = globals()[test.__name__ + '_spec']
            test_spec['name'] = test.__name__
            test_list.append((test_spec,  test))
    else:
        for k, d in globals().items():
            if k.endswith('_spec'):
                test_name = k[:-5]
                test_spec = d
                test_spec['name'] = test_name
                mod = import_module('idlelib.' + test_spec['file'])
                test = getattr(mod, test_name)
                test_list.append((test_spec, test))

    help_string = tk.StringVar('')
    test_name = tk.StringVar('')
    callable_object = None
    test_kwds = None


    def next():
        nonlocal help_string, test_name, callable_object, test_kwds
        if len(test_list) == 1:
            next_button.pack_forget()
        test_spec, callable_object = test_list.pop()
        test_kwds = test_spec['kwds']
        test_kwds['parent'] = root
        help_string.set(test_spec['msg'])
        test_name.set('Test ' + test_spec['name'])


    def run_test():
        widget = callable_object(**test_kwds)
        try:
            print(widget.result)
        except AttributeError:
            pass

    label = tk.Label(root, textvariable=help_string, justify='left')
    label.pack()
    button = tk.Button(root, textvariable=test_name, command=run_test)
    button.pack()
    next_button = tk.Button(root, text="Next", command=next)
    next_button.pack()

    next()

    root.mainloop()

if __name__ == '__main__':
    run()
