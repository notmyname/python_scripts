import dbus

session = dbus.SessionBus()

proxy = session.get_object('org.gnome.evince.ApplicationService', '/org/gnome/evince/Evince')

proxy.OpenURI('file:///home/john/Desktop/UserManual.pdf', dbus.Dictionary({'': dbus.String('',variant_level=1)}), dbus.UInt32(0))
proxy.OpenWindow(dbus.Dictionary({'': dbus.String('',variant_level=1)}), dbus.UInt32(0))
