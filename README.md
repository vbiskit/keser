<p align="center">
  <a href="https://github.com/vbiskit/keser">
    <img alt="Minimum Python version required: 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=flat-square" />
  </a>
  <a href="https://github.com/vbiskit/keser/blob/main/LICENSE">
    <img alt="License badge for Keser" src="https://img.shields.io/github/license/vbiskit/keser?style=flat-square" />
  </a>
  <a href="https://github.com/vbiskit/keser">
    <img alt="View count for Keser" src="https://komarev.com/ghpvc/?username=vbiskit&color=brightgreen&label=views&style=flat-square" />
  </a>
 <a href="https://twitter.com/sillybiskit">
  <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-sillybiskit-FF5733?style=flat-square&logo=twitter&logoColor=white" />
</a>

## 😁 Description
everything you need in a username tool very fast 0 false positives searches through over 670 sites and with duckduckgo

## 🤔 Why use it
find people with there last names on websites, usernames pointless

## 📦 Installation 
```yaml
git clone https://github.com/vbiskit/keser

cd keser

pip3 install -r requirements.txt

cd

echo 'export PATH="$HOME/keser:$PATH"' >> ~/.bashrc && source ~/.bashrc

chmod +x ~/keser/keser.py

mv ~/keser/keser.py ~/keser/keser
```
## 🚀 Run the tool:
```yaml
keser
```
## 🥺 keser -h

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
   keser <example> -sf example.txt
   keser <example> for just links
   keser -bf usernames.txt
   keser <example> -all
   keser -bd example.txt
   keser example -all -sf some.txt
   keser -bf name,name2
   keser -bd name,name2
   keser -bsn <user>
```
## 😡 can't install tool because of error: externally-managed-environment fix in 14 seconds.
```yaml
sudo apt install virtualenv

virtualenv python

cd python

source bin/activate
```
**now you can install and run the tool just follow the steps here**
https://github.com/vbiskit/keser/blob/main/README.md#installation

# 🤖  how to uninstall the tool:
```yaml
rm -rf keser
