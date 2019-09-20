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

service_path=$service_root"/nitkcaa.service"
conf_path=$PWD"/nitkcaa.conf"
unit_path=$PWD"/nitkcaa.service"

python_path=$(which python3)

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
ExecStart= $python_path $PWD/main.py $conf_path service

[Install]
WantedBy=multi-user.target
EOF
[ $? -ne 0 ] && { echo "Could not generate service unit file."; exit 1; }

ln -s $unit_path $service_path
[ $? -ne 0 ] && { echo "Could not generate link in service folder."; exit 1; }
systemctl enable nitkcaa.service
[ $? -ne 0 ] && { echo "Could not enable service."; exit 1; }
systemctl start nitkcaa.service
[ $? -ne 0 ] && { echo "Could not start service."; exit 1; }

echo -e "Add the following alias to your .rc file\n"
echo alias nitkcaa=\"$python_path $PWD/main.py $conf_path oneoff\"