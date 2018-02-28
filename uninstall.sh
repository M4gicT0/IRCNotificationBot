#! /bin/sh
#
# uninstall.sh
# Copyright (C) 2018 transpalette <transpalette@translaptop>
#
# Distributed under terms of the MIT license.
#

rm -Rf ~/.config/IRCNotificationBot/

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

systemctl stop IRCNotificationBot.service
systemctl disable IRCNotificationBot.service
rm /etc/systemd/system/IRCNotificationBot.service
rm -Rf /opt/IRCNotificationBot
