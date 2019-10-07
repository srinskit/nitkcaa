# Script to install nitkcaa
[ $# -lt 2 ] && { echo "Usage: $0 username password [service-folder]"; exit 1; }

username=$1
password=$2
ping_host="1.1.1.1"

if [ $3 ]; then
    service_root=$3
else
    service_root="/etc/systemd/system"
fi

echo "Installing python package"
pip3 install nitkcaa/ --user
[ $? -ne 0 ] && { echo "Could not install nitkcaa."; exit 1; }

service_path=$service_root"/nitkcaa.service"
conf_path=$HOME"/.nitkcaa.conf"
unit_path=$PWD"/nitkcaa.service"

cat << EOF > $conf_path
$username
$password
$ping_host
EOF
[ $? -ne 0 ] && { echo "Could not generate config file."; exit 1; }

cat << EOF > $unit_path
# nitkcaa.service

[Unit] 
Description= NITK Client Auth Agent Service

[Service] 
Type= simple 
User=$USER
ExecStart= $(which nitkcaa) $conf_path --service 

[Install]
WantedBy=multi-user.target
EOF
[ $? -ne 0 ] && { echo "Could not generate service unit file."; exit 1; }

sudo ln -nsf $unit_path $service_path
[ $? -ne 0 ] && { echo "Could not generate link in service folder."; exit 1; }
sudo systemctl enable nitkcaa.service
[ $? -ne 0 ] && { echo "Could not enable service."; exit 1; }
sudo systemctl start nitkcaa.service
[ $? -ne 0 ] && { echo "Could not start service."; exit 1; }

echo "Done."
