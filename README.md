## Description
**everything you need in a username tool very fast 0 false positives searches through over 670 sites**

## Installation 
Clone the repository and install the required dependencies:  
```yaml
git clone https://github.com/vbiskit/keser

cd keser

pip3 install -r requirements.txt

cd

sudo mv keser /usr/local/bin/

sudo chmod +x /usr/local/bin/keser/keser/keser.py

echo '#!/bin/bash' | sudo tee /usr/local/bin/keser > /dev/null

echo 'cd /usr/local/bin/keser/keser && python3 onerise.py "$@"' | sudo tee -a /usr/local/bin/keser > /dev/null

sudo chmod +x /usr/local/bin/onerise
```
## Run the tool:
```yaml
keser
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
sudo rm -f /usr/local/bin/keser

sudo rm -rf /usr/local/bin/keser
