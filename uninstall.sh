# Script to uninstall nitkcaa

service_root="/etc/systemd/system""/nitkcaa.service"
conf_path=$HOME"/.nitkcaa.conf"
unit_path=$PWD"/nitkcaa.service"

sudo systemctl stop nitkcaa.service
[ $? -ne 0 ] && { echo "Could not stop the service."; exit 1; }
sudo systemctl disable nitkcaa.service
[ $? -ne 0 ] && { echo "Could not disable the service."; exit 1; }

rm $conf_path $unit_path
[ $? -ne 0 ] && { echo "Could not cleanup."; exit 1; }

pip3 uninstall nitkcaa
[ $? -ne 0 ] && { echo "Could not uninstall python package."; exit 1; }

echo "Done."
