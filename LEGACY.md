# LEGACY uninstall

The legacy installation procedure was deprecated due to the fact that
root privileges were needed. Something a user not doesn't always have.
Plus getting the DB was a heachache because the old installScript
worked until it didn't... So I'm going against my old self (better?)
judgement and commited the DB to the repo. The DB is not really that
large and it changes rarely if at all. So I'm favoring practicality
and mental sanity over the "good" practices my old self held.

Run with sudo the uninstall script via:

```
$ sudo ./uninstallLegacy.sh
```

If you have an Mac computer and you managed to install isonav via the
legacy deprecated method you may get an "Operation not permitted"
error there is a work around, you'll need to disable the System
Integrity Protection. Simply reboot and press Cmd-R then open a
terminal and type "csrutil disable" (without the quotes) reboot and
run the install script again. It is encouraged to reenable it after
the installation is done.

For the new install instructions see the [README](README.md).