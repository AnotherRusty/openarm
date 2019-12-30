echo -e "\033[1;32m Setup openarm udev rules."
echo " "
sudo cp udev_rules/openarm.rules  /etc/udev/rules.d
echo " "
echo "Restarting udev ..."
echo ""

sudo udevadm control --reload-rules
sudo udevadm trigger