# Script to uninstall nitkcaa

service_root="/etc/systemd/system""/nitkcaa.service"

systemctl stop nitkcaa.service
[ $? -ne 0 ] && { echo "Could not stop the service."; exit 1; }
systemctl disable nitkcaa.service
[ $? -ne 0 ] && { echo "Could not disable the service."; exit 1; }

rm nitkcaa.conf nitkcaa.service
[ $? -ne 0 ] && { echo "Could not cleanup."; exit 1; }