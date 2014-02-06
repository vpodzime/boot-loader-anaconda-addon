#
# Copyright (C) 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Vratislav Podzimek <vpodzime@redhat.com>
#

# will be translated in the future
_ = lambda x: x
N_ = lambda x: x

# the path to addons is in sys.path so we can import things from org_fedora_hello_world
from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.gui.categories.system import SystemCategory

from gi.repository import Gtk

# export only the spoke, no helper functions, classes or constants
__all__ = ["BootLoaderSpoke"]

class BootLoaderSpoke(NormalSpoke):
    ### class attributes defined by API ###

    # list all top-level objects from the .glade file that should be exposed
    # to the spoke or leave empty to extract everything
    builderObjects = ["bootLoaderSpokeWindow"]

    # the name of the main window widget
    mainWidgetName = "bootLoaderSpokeWindow"

    # name of the .glade file in the same directory as this source
    uiFile = "boot_loader.glade"

    # category this spoke belongs to
    category = SystemCategory

    # spoke icon (will be displayed on the hub)
    # preferred are the -symbolic icons as these are used in Anaconda's spokes
    icon = "face-cool-symbolic"

    # title of the spoke (will be displayed on the hub)
    title = N_("_BOOT LOADER CONFIGURATION")

    ### methods defined by API ###
    def __init__(self, data, storage, payload, instclass):
        NormalSpoke.__init__(self, data, storage, payload, instclass)
        self._pw_changed = False

    def initialize(self):
        NormalSpoke.initialize(self)
        self._pwEntry = self.builder.get_object("pwEntry")
        self._confirmEntry = self.builder.get_object("confirmEntry")

        self._pwEntry.set_tooltip_text(_("Enter password here or leave empty for no password"))

    def refresh(self):
        if self.data.bootloader.password:
            self._pwEntry.set_placeholder_text(_("Boot loader pasword set, you can change it here"))
        else:
            self._pwEntry.set_placeholder_text(_("You can set boot loader password here."))

        self._confirmEntry.set_sensitive(False)
        self._pw_changed = False

    def apply(self):
        if self._pw_changed:
            self.data.bootloader.password = self._pwEntry.get_text()
            self.data.bootloader.isCrypted = False

    def execute(self):
        # nothing to do here
        pass

    @property
    def ready(self):
        # this spoke is always ready
        return True

    @property
    def completed(self):
        # this spoke is always completed
        return True

    @property
    def mandatory(self):
        # this is an optional spoke that is not mandatory to be completed
        return False

    @property
    def status(self):
        if self.data.bootloader.password:
            return _("Boot loader password set")
        else:
            return _("Boot loader password not set")


    ### handlers ###
    def on_pw_focus_in(self, *args):
        self._pw_changed = True
        self._pwEntry.set_placeholder_text("")

    def on_pw_confirm_changed(self, *args):
        self._confirmEntry.set_sensitive(True)

        pw = self._pwEntry.get_text()
        if not pw:
            self._confirmEntry.set_text("")
        confirm = self._confirmEntry.get_text()

        if pw != confirm:
            self._confirmEntry.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY,
                                                   "gtk-dialog-error")
            self.clear_info()
        else:
            self._confirmEntry.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, "")

    def on_back_clicked(self, *args):
        pw = self._pwEntry.get_text()
        confirm = self._confirmEntry.get_text()

        if pw != confirm:
            self.set_error(_("Passwords do not match"))
            self.window.show_all()
            self._confirmEntry.grab_focus()
            return

        NormalSpoke.on_back_clicked(self, *args)
