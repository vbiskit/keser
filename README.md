## About this tool

The tool has 0 false postives its a very fast username or can be real name search what i mainly use this stuff for it has a built in duckduckgo search and a brute force username runs fron a .txt so does the duckduckgo brute force,: its also scans through 676 sites

## Installation 
Clone the repository and install the required dependencies:  
```yaml
git clone https://github.com/vbiskit/oneRise

cd oneRise

pip3 install -r requirements.txt

cd

sudo mv oneRise /usr/local/bin/

sudo chmod +x /usr/local/bin/oneRise/oneRise/onerise.py

echo '#!/bin/bash' | sudo tee /usr/local/bin/onerise > /dev/null

echo 'cd /usr/local/bin/oneRise/oneRise && python3 onerise.py "$@"' | sudo tee -a /usr/local/bin/onerise > /dev/null

sudo chmod +x /usr/local/bin/onerise
```
## Run the tool:
```yaml
onerise
```
## onerise -h

```yaml
Arguments:
  -sf  Save the output to a file
  -bf brute-force usernames from a .txt file
  -all Search With Duckduckgo And Userlinks
  -bd brute-force usernames with duckduckgo
  -bsn brute-force similar names 
  -bf name,name2
  -bd name,name2
  -bsn search similar names of that user
Usage:
   onerise <example> -sf example.txt
   onerise <example> for just links
   onerise -bf usernames.txt
   onerise <example> -all
   onerise -bd example.txt
   onerise example -all -sf some.txt
   onerise -bf name,name2
   onerise -bd name,name2
   onerise -bsn <user>
```
## can't install tool because of error: externally-managed-environment fix in 14 seconds.
```yaml
sudo apt install virtualenv

virtualenv python

cd python

source bin/activate
```
**now you can install and run the tool just follow the steps here**
https://github.com/vbiskit/oneRise/tree/main?tab=readme-ov-file#installation

# how to uninstall the tool:
```yaml
sudo rm -f /usr/local/bin/onerise

sudo rm -rf /usr/local/bin/oneRise
