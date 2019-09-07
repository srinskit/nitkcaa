# Script to install nitkcaa

username=$1
password=$2
ping_host="1.1.1.1"

conf_path=$PWD"/nitkcaa.conf"
service_path=$PWD"/nitkcaa.service"

python_path=$(which python3)

cat << EOF > $conf_path
$username
$password
$ping_host
EOF

cat << EOF > $service_path
# nitkcaa.service

[Unit] 
Description= NITK Client Auth Agent Service

[Service] 
Type= simple 
ExecStart= $python_path $PWD/main.py $conf_path service

[Install]
WantedBy=multi-user.target
EOF

echo -e "Add the following alias to your .rc file\n"
echo alias nitkcaa=\"$python_path $PWD/main.py $conf_path oneoff\"