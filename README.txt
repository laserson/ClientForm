   [1]SourceForge.net Logo

                                   ClientForm

   ClientForm is a Python module for handling HTML forms on the client
   side, useful for parsing HTML forms, filling them in and returning the
   completed forms to the server. It developed from a port of Gisle Aas'
   Perl module HTML::Form, from the [2]libwww-perl library, but the
   interface is not the same.

   Simple working example:
from urllib2 import urlopen
from ClientForm import ParseResponse

response = urlopen("http://wwwsearch.sourceforge.net/ClientForm/example.html")
forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
print form
form["comments"] = "Thanks, Gisle"

# form.click() returns a urllib2.Request object
# (see HTMLForm.click.__doc__ if you don't have urllib2)
print urlopen(form.click()).read()

   A more complicated working example (Note: this example makes use of the
   ClientForm 0.2 API; refer to the README.html file in the latest 0.1
   release for the corresponding code for that version.):
import ClientForm
import urllib2
request = urllib2.Request(
    "http://wwwsearch.sourceforge.net/ClientForm/example.html")
response = urllib2.urlopen(request)
forms = ClientForm.ParseResponse(response, backwards_compat=False)
response.close()
## f = open("example.html")
## forms = ClientForm.ParseFile(f, "http://example.com/example.html",
##                              backwards_compat=False)
## f.close()
form = forms[0]
print form  # very useful!

# A 'control' is a graphical HTML form widget: a text entry box, a
# dropdown 'select' list, a checkbox, etc.

# Indexing allows setting and retrieval of control values
original_text = form["comments"]  # a string, NOT a Control instance
form["comments"] = "Blah."

# Controls that represent lists (checkbox, select and radio lists) are
# ListControl instances.  Their values are sequences of list item names.
# They come in two flavours: single- and multiple-selection:
form["favorite_cheese"] = ["brie"]  # single
form["cheeses"] = ["parmesan", "leicester", "cheddar"]  # multi
#  equivalent, but more flexible:
form.set_value(["parmesan", "leicester", "cheddar"], name="cheeses")

# Add files to FILE controls with .add_file().  Only call this multiple
# times if the server is expecting multiple files.
#  add a file, default value for MIME type, no filename sent to server
form.add_file(open("data.dat"))
#  add a second file, explicitly giving MIME type, and telling the server
#   what the filename is
form.add_file(open("data.txt"), "text/plain", "data.txt")

# All Controls may be disabled (equivalent of greyed-out in browser)...
control = form.find_control("comments")
print control.disabled
#  ...or readonly
print control.readonly
#  readonly and disabled attributes can be assigned to
control.disabled = False
#  convenience method, used here to make all controls writable (unless
#   they're disabled):
form.set_all_readonly(False)

# A couple of notes about list controls and HTML:

# 1. List controls correspond to either a single SELECT element, or
# multiple INPUT elements.  Items correspond to either OPTION or INPUT
# elements.  For example, this is a SELECT control, named "control1":

#    <select name="control1">
#     <option>foo</option>
#     <option value="1">bar</option>
#    </select>

# and this is a CHECKBOX control, named "control2":

#    <input type="checkbox" name="control2" value="foo" id="cbe1">
#    <input type="checkbox" name="control2" value="bar" id="cbe2">

# You know the latter is a single control because all the name attributes
# are the same.

# 2. Item names are the strings that go to make up the value that should
# be returned to the server.  These strings come from various different
# pieces of text in the HTML.  The HTML standard and the ClientForm
# docstrings explain in detail, but playing around with an HTML file,
# ParseFile() and 'print form' is very useful to understand this!

# You can get the Control instances from inside the form...
control = form.find_control("cheeses", type="select")
print control.name, control.value, control.type
control.value = ["mascarpone", "curd"]
# ...and the Item instances from inside the Control
item = control.get("curd")
print item.name, item.selected, item.id, item.attrs
item.selected = False

# Controls may be referred to by label:
#  find control with label that has a *substring* "Cheeses"
#  (eg., a label "Please select a cheese" would match).
control = form.find_control(label="select a cheese")

# You can explicitly say that you're referring to a ListControl:
#  set value of "cheeses" ListControl
form.set_value(["gouda"], name="cheeses", kind="list")
#  equivalent:
form.find_control(name="cheeses", kind="list").value = ["gouda"]
#  the first example is also almost equivalent to the following (but
#  insists that the control be a ListControl -- so it will skip any
#  non-list controls that come before the control we want)
form["cheeses"] = ["gouda"]
# The kind argument can also take values "multilist", "singlelist", "text",
# "clickable" and "file":
#  find first control that will accept text, and scribble in it
form.set_value("rhubarb rhubarb", kind="text", nr=0)
#  find, and set the value of, the first single-selection list control
form.set_value(["spam"], kind="singlelist", nr=0)

# You can find controls with a general predicate function:
def control_has_caerphilly(control):
    for item in control.items:
        if item.name == "caerphilly": return True
form.find_control(kind="list", predicate=control_has_caerphilly)

# HTMLForm.controls is a list of all controls in the form
for control in form.controls:
    if control.value == "inquisition": sys.exit()

# Control.items is a list of all Item instances in the control
for item in form.find_control("cheeses").items:
    print item.name

# To remove items from a list control, remove it from .items:
cheeses = form.find_control("cheeses")
curd = cheeses.get("curd")
del cheeses.items[cheeses.items.index(curd)]
# To add items to a list container, instantiate an Item with its control
# and attributes:
# Note that you are responsible for getting the attributes correct here,
# and these are not quite identical to the original HTML, due to
# defaulting rules and a few special attributes (e.g. Items that represent
# OPTIONs have a special "contents" key in their .attrs dict).  In future
# there will be an explicitly supported way of using the parsing logic to
# add items and controls from HTML strings without knowing these details.
ClientForm.Item(cheeses, {"contents": "mascarpone",
                          "value": "mascarpone"})

# You can specify list items by label using set/get_value_by_label() and
# the label argument of the .get() method.  Sometimes labels are easier to
# maintain than names, sometimes the other way around.
form.set_value_by_label(["Mozzarella", "Caerphilly"], "cheeses")

# Which items are present, selected, and successful?
#  is the "parmesan" item of the "cheeses" control successful (selected
#   and not disabled)?
print "parmesan" in form["cheeses"]
#  is the "parmesan" item of the "cheeses" control selected?
print "parmesan" in [
    item.name for item in form.find_control("cheeses").items if item.selected]
#  does cheeses control have a "caerphilly" item?
print "caerphilly" in [item.name for item in form.find_control("cheeses").items]

# Sometimes one wants to set or clear individual items in a list, rather
# than setting the whole .value:
#  select the item named "gorgonzola" in the first control named "cheeses"
form.find_control("cheeses").get("gorgonzola").selected = True
# You can be more specific:
#  deselect "edam" in third CHECKBOX control
form.find_control(type="checkbox", nr=2).get("edam").selected = False
#  deselect item labelled "Mozzarella" in control with id "chz"
form.find_control(id="chz").get(label="Mozzarella").selected = False

# Often, a single checkbox (a CHECKBOX control with a single item) is
# present.  In that case, the name of the single item isn't of much
# interest, so it's a good idea to check and uncheck the box without
# using the item name:
form.find_control("smelly").items[0].selected = True  # check
form.find_control("smelly").items[0].selected = False  # uncheck

# Items may be disabled (selecting or de-selecting a disabled item is
# not allowed):
control = form.find_control("cheeses")
print control.get("emmenthal").disabled
control.get("emmenthal").disabled = True
#  enable all items in control
control.set_all_items_disabled(False)

request2 = form.click()  # urllib2.Request object
try:
    response2 = urllib2.urlopen(request2)
except urllib2.HTTPError, response2:
    pass

print response2.geturl()
print response2.info()  # headers
print response2.read()  # body
response2.close()

   All of the standard control types are supported: TEXT, PASSWORD,
   HIDDEN, TEXTAREA, ISINDEX, RESET, BUTTON (INPUT TYPE=BUTTON and the
   various BUTTON types), SUBMIT, IMAGE, RADIO, CHECKBOX, SELECT/OPTION
   and FILE (for file upload). Both standard form encodings
   (application/x-www-form-urlencoded and multipart/form-data) are
   supported.

   The module is designed for testing and automation of web interfaces,
   not for implementing interactive user agents.

   Security note: Remember that any passwords you store in HTMLForm
   instances will be saved to disk in the clear if you pickle them
   (directly or indirectly). The simplest solution to this is to avoid
   pickling HTMLForm objects. You could also pickle before filling in any
   password, or just set the password to "" before pickling.

   Python 2.0 or above is required. To run the tests, you need the
   unittest module (from [3]PyUnit). unittest is a standard library module
   with Python 2.1 and above.

   For full documentation, see the docstrings in ClientForm.py.

   Note: this page describes the 0.2 (stable release) interface. See
   [4]here for the old 0.1 interface.

Parsers

   ClientForm contains two parsers. See [5]the FAQ entry on XHTML for
   details.

   [6]mxTidy or [7]µTidylib can be useful for dealing with bad HTML.

   I think it would be nice to have an implementation of ClientForm based
   on [8]BeautifulSoup (i.e. all methods and attributes implemented using
   the BeautifulSoup API), since that module does tolerant HTML parsing
   with a nice API for doing non-forms stuff. (I'm not about to do this,
   though. For anybody interested in doing this, note that the ClientForm
   tests would need making constructor-independent first.)

Backwards-compatibility mode

   ClientForm 0.2 includes three minor backwards-incompatible interface
   changes from version 0.1.

   To make upgrading from 0.1 easier, and to allow me to stop supporting
   version 0.1 sooner, version 0.2 contains support for operating in a
   backwards-compatible mode, under which code written for 0.1 should work
   without modification. This is done on a per-HTMLForm basis via the
   .backwards_compat attribute, but for convenience the ParseResponse()
   and ParseFile() factory functions accept backwards_compat arguments.
   These backwards-compatibility features will be removed in version 0.3.
   The default is to operate in backwards-compatible mode. To run with
   backwards compatible mode turned OFF (strongly recommended):
from urllib2 import urlopen
from ClientForm import ParseResponse
forms = ParseResponse(urlopen("http://example.com/"), backwards_compat=False)
# ...

   The backwards-incompatible changes are:
     * Ambiguous specification of controls or items now results in
       AmbiguityError. If you want the old behaviour, explicitly pass nr=0
       to indicate you want the first matching control or item.
     * Item label matching is now done by substring, not by strict
       string-equality (but note leading and trailing space is always
       stripped). (Control label matching is always done by substring.)
     * Handling of disabled list items has changed. First, note that
       handling of disabled list items in 0.1 (and in 0.2's
       backwards-compatibility mode!) is buggy: disabled items are
       successful (ie. disabled item names are sent back to the server).
       As a result, there was no distinction to be made between successful
       items and selected items. In 0.2, the bug is fixed, so this is no
       longer the case, and it is important to note that list controls'
       .value attribute contains only the successful item names; items
       that are selected but not successful (because disabled) are not
       included in .value. Second, disabled list items may no longer be
       deselected: AttributeError is raised in 0.2, whereas deselection
       was allowed in 0.1. The bug in 0.1 and in 0.2's
       backwards-compatibility mode will not be fixed, to preserve
       compatibility and to encourage people to upgrade to the new 0.2
       backwards_compat=False behaviour.

Credits

   Apart from Gisle Aas for allowing the original port from libwww-perl,
   particular credit is due to Gary Poster and Benji York, and their
   employer, Zope Corporation, for their contributions which led to
   ClientForm 0.2 being released. Thanks also to the many people who have
   contributed bug reports.

Download

   For installation instructions, see the INSTALL.txt file included in the
   distribution.

   Stable release There have been three fairly minor
   backwards-incompatible interface changes since version 0.1 (see
   [9]above), but by default the code operates in a backwards-compatible
   mode so that code written for 0.1 should work without changes.

   0.2 includes better support for labels, and a simpler interface (all
   the old methods are still there, but some have been deprecated and a
   few added).
     * [10]ClientForm-0.2.10.tar.gz
     * [11]ClientForm-0.2.10.zip
     * [12]Change Log (included in distribution)
     * [13]Older releases.

   Old release No longer maintained. I recommend upgrading from 0.1 to
   0.2.

   There were many interface changes between 0.0 and 0.1, so you should
   take care if upgrading old code from 0.0.

   0.1 includes FILE control support for file upload, handling of disabled
   list items, and a redesigned interface.
     * [14]ClientForm-0.1.17.tar.gz
     * [15]ClientForm-0_1_17.zip
     * [16]Change Log (included in distribution)
     * [17]Older releases.

   Ancient release No longer maintained. You don't want this.
     * [18]ClientForm-0.0.16.tar.gz
     * [19]ClientForm-0_0_16.zip
     * [20]Change Log (included in distribution)
     * [21]Older releases.

Subversion

   The [22]Subversion (SVN) trunk is
   [23]http://codespeak.net/svn/wwwsearch/ClientForm/trunk, so to check
   out the source:
svn co http://codespeak.net/svn/wwwsearch/ClientForm/trunk ClientForm

FAQs

     * Doesn't the standard Python library module, cgi, do this?
       No: the cgi module does the server end of the job. It doesn't know
       how to parse or fill in a form or how to send it back to the
       server.
     * Which version of Python do I need?
       2.0 or above (ClientForm 0.2; version 0.1 requires Python 1.5.2 or
       above).
     * Is urllib2 required?
       No.
     * How do I use it without urllib2?
       Use .click_request_data() instead of .click().
     * Which urllib2 do I need?
       You don't. It's convenient, though. If you have Python 2.0, you
       need to upgrade to the version from Python 2.1 (available from
       [24]www.python.org). Otherwise, you're OK.
     * Which license?
       ClientForm is dual-licensed: you may pick either the [25]BSD
       license, or the [26]ZPL 2.1 (both are included in the
       distribution).
     * Is XHTML supported?
       Yes. You must pass
       form_parser_class=ClientForm.XHTMLCompatibleFormParser to
       ParseResponse() / ParseFile(). Note this parser is less tolerant of
       bad HTML than the default, ClientForm.FormParser
     * How do I figure out what control names and values to use?
       print form is usually all you need. In your code, things like the
       HTMLForm.items attribute of HTMLForm instances can be useful to
       inspect forms at runtime. Note that it's possible to use item
       labels instead of item names, which can be useful -- use the
       by_label arguments to the various methods, and the
       .get_value_by_label() / .set_value_by_label() methods on
       ListControl.
     * What do those '*' characters mean in the string representations of
       list controls?
       A * next to an item means that item is selected.
     * What do those parentheses (round brackets) mean in the string
       representations of list controls?
       Parentheses (foo) around an item mean that item is disabled.
     * Why doesn't <some control> turn up in the data returned by
       .click*() when that control has non-None value?
       Either the control is disabled, or it is not successful for some
       other reason. 'Successful' (see HTML 4 specification) means that
       the control will cause data to get sent to the server.
     * Why does ClientForm not follow the HTML 4.0 / RFC 1866 standards
       for RADIO and multiple-selection SELECT controls?
       Because by default, it follows browser behaviour when setting the
       initially-selected items in list controls that have no items
       explicitly selected in the HTML. Use the select_default argument to
       ParseResponse if you want to follow the RFC 1866 rules instead.
       Note that browser behaviour violates the HTML 4.01 specification in
       the case of RADIO controls.
     * Why does .click()ing on a button not work for me?
          + Clicking on a RESET button doesn't do anything, by design -
            this is a library for web automation, not an interactive
            browser. Even in an interactive browser, clicking on RESET
            sends nothing to the server, so there is little point in
            having .click() do anything special here.
          + Clicking on a BUTTON TYPE=BUTTON doesn't do anything either,
            also by design. This time, the reason is that that BUTTON is
            only in the HTML standard so that one can attach callbacks to
            its events. The callbacks are functions in SCRIPT elements
            (such as Javascript) embedded in the HTML, and their execution
            may result in information getting sent back to the server.
            ClientForm, however, knows nothing about these callbacks, so
            it can't do anything useful with a click on a BUTTON whose
            type is BUTTON.
          + Generally, embedded script may be messing things up in all
            kinds of ways. See the answer to the next question.
     * Embedded script is messing up my form filling. What do I do?
       See the [27]General FAQs page and the next FAQ entry for what to do
       about this.
     * How do I change INPUT TYPE=HIDDEN field values (for example, to
       emulate the effect of JavaScript code)?
       As with any control, set the control's readonly attribute false.
form.find_control("foo").readonly = False  # allow changing .value of control fo
o
form.set_all_readonly(False)  # allow changing the .value of all controls
     * I'm having trouble debugging my code.
       The [28]ClientCookie package makes it easy to get .seek()able
       response objects, which is convenient for debugging. See also
       [29]here for few relevant tips. Also see [30]General FAQs.
     * I have a control containing a list of integers. How do I select the
       one whose value is nearest to the one I want?
import bisect
def closest_int_value(form, ctrl_name, value):
    values = map(int, [item.name for item in form.find_control(ctrl_name).items]
)
    return str(values[bisect.bisect(values, value) - 1])

form["distance"] = [closest_int_value(form, "distance", 23)]
     * Where can I find out more about the HTML and HTTP standards?
          + W3C [31]HTML 4.01 Specification.
          + [32]RFC 1866 - the HTML 2.0 standard.
          + [33]RFC 1867 - Form-based file upload.
          + [34]RFC 2616 - HTTP 1.1 Specification.

   I prefer questions and comments to be sent to the [35]mailing list
   rather than direct to me.

   [36]John J. Lee, July 2008.

   [37]Home
   [38]General FAQs
   [39]mechanize
   [40]mechanize docs
   ClientForm
   [41]ClientCookie
   [42]ClientCookie docs
   [43]pullparser
   [44]DOMForm
   [45]python-spidermonkey
   [46]ClientTable
   [47]1.5.2 urllib2.py
   [48]1.5.2 urllib.py
   [49]Other stuff
   [50]Example
   [51]Notes
   [52]Parsers
   [53]Compatibility
   [54]Credits
   [55]Download
   [56]FAQs

References

   1. http://sourceforge.net/
   2. http://www.linpro.no/lwp/
   3. http://pyunit.sourceforge.net/
   4. file://localhost/tmp/tmpwWhv19/src/README-0_1_17.html
   5. file://localhost/tmp/tmpwWhv19/#faq
   6. http://www.egenix.com/files/python/mxTidy.html
   7. http://utidylib.berlios.de/
   8. http://www.crummy.com/software/BeautifulSoup/
   9. file://localhost/tmp/tmpwWhv19/#compat
  10. file://localhost/tmp/tmpwWhv19/src/ClientForm-0.2.10.tar.gz
  11. file://localhost/tmp/tmpwWhv19/src/ClientForm-0.2.10.zip
  12. file://localhost/tmp/tmpwWhv19/src/ChangeLog.txt
  13. file://localhost/tmp/tmpwWhv19/src/
  14. file://localhost/tmp/tmpwWhv19/src/ClientForm-0.1.17.tar.gz
  15. file://localhost/tmp/tmpwWhv19/src/ClientForm-0_1_17.zip
  16. file://localhost/tmp/tmpwWhv19/src/ChangeLog.txt
  17. file://localhost/tmp/tmpwWhv19/src/
  18. file://localhost/tmp/tmpwWhv19/src/ClientForm-0.0.16.tar.gz
  19. file://localhost/tmp/tmpwWhv19/src/ClientForm-0_0_16.zip
  20. file://localhost/tmp/tmpwWhv19/src/ChangeLog.txt
  21. file://localhost/tmp/tmpwWhv19/src/
  22. http://subversion.tigris.org/
  23. http://codespeak.net/svn/wwwsearch/ClientForm/trunk#egg=ClientForm-dev
  24. http://www.python.org/
  25. http://www.opensource.org/licenses/bsd-license.php
  26. http://www.zope.org/Resources/ZPL
  27. file://localhost/tmp/bits/GeneralFAQ.html
  28. file://localhost/tmp/ClientCookie/
  29. file://localhost/tmp/ClientCookie/doc.html#debugging
  30. file://localhost/tmp/bits/GeneralFAQ.html
  31. http://www.w3.org/TR/html401/
  32. http://www.ietf.org/rfc/rfc1866.txt
  33. http://www.ietf.org/rfc/rfc1867.txt
  34. http://www.ietf.org/rfc/rfc2616.txt
  35. http://lists.sourceforge.net/lists/listinfo/wwwsearch-general
  36. mailto:jjl@pobox.com
  37. file://localhost/tmp
  38. file://localhost/tmp/bits/GeneralFAQ.html
  39. file://localhost/tmp/mechanize/
  40. file://localhost/tmp/mechanize/doc.html
  41. file://localhost/tmp/ClientCookie/
  42. file://localhost/tmp/ClientCookie/doc.html
  43. file://localhost/tmp/pullparser/
  44. file://localhost/tmp/DOMForm/
  45. file://localhost/tmp/python-spidermonkey/
  46. file://localhost/tmp/ClientTable/
  47. file://localhost/tmp/bits/urllib2_152.py
  48. file://localhost/tmp/bits/urllib_152.py
  49. file://localhost/tmp/#other
  50. file://localhost/tmp/tmpwWhv19/#example
  51. file://localhost/tmp/tmpwWhv19/#notes
  52. file://localhost/tmp/tmpwWhv19/#parsers
  53. file://localhost/tmp/tmpwWhv19/#compat
  54. file://localhost/tmp/tmpwWhv19/#credits
  55. file://localhost/tmp/tmpwWhv19/#download
  56. file://localhost/tmp/tmpwWhv19/#faq
