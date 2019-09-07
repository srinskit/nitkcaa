# Script to uninstall nitkcaa

service_root="/etc/systemd/system""/nitkcaa.service"

systemctl stop nitkcaa.service
systemctl disable nitkcaa.service

rm nitkcaa.conf nitkcaa.service