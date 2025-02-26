![png](show.png)
# About this tool

The tool has 0 false postives its a fast username or can be real name search what i mainly use this stuff for it has a built in duckduckgo search and a brute force username runs fron a .txt so does the duckduckgo brute force.

## Installation 
Clone the repository and install the required dependencies:  
```yaml
git clone https://github.com/vbiskit/oneRise

cd oneRise

pip3 install -r requirements.txt

cd

sudo mv oneRise/oneRise /usr/local/bin/

sudo chmod +x /usr/local/bin/oneRise/onerise.py

sudo ln -s /usr/local/bin/oneRise/onerise.py /usr/local/bin/onerise
```
# Run the tool:
```yaml
onerise
```
# onerise -h

```yaml
Arguments:
  -sf  Save the output to a file
  -bf brute-force usernames from a .txt file
  -all Search With Duckduckgo And Userlinks
  -bd brute-force usernames with duckduckgo
  -bf name,name2
  -bd name,name2
Usage:
  - python3 onerise.py <example> -sf example.txt
  - python3 onerise.py <example> for just links
  - python3 onerise.py -bf usernames.txt
  - python3 onerise.py <example> -all
  - python3 onerise.py -bd example.txt
  - python3 onerise.py example -all -sf some.txt
  - python3 onerise.py -bf name,name2
  - python3 onerise.py -bd name,name2
```



# can't install tool because of error: externally-managed-environment: fix in 14 seconds
```
sudo apt install virtualenv

virtualenv python

cd python

source bin/activate

now you can install and run the tool just follow the steps at the top in Installation.
```
