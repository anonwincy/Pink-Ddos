<h3 align=center>
    Anonymous Vibes Bangladesh Ddos - Distributed Denial-of-Service.
</h3>

<h6 align=center>
    <a href="">Usage</a>
    ·
    <a href="">Install</a>
    ·
    <a href="">Disclaimer</a>
    ·
    <a href="">References</a>
</h6>

<p align=center>
	A script that can determine whether a website is vulnerable to Pink Ddos.
</p>

<p align=center>
    <a href="">
		<img alt="Version" src="https://img.shields.io/github/v/tag/wannabewastaken/xmlrpc-dos?style=for-the-badge&label=release&logo=verdaccio&color=526D82&logoColor=DDE6ED&labelColor=27374D&sort=semver">
    </a>
    <a href="">
		<img alt="Stargazers" src="https://img.shields.io/github/stars/wannabewastaken/xmlrpc-dos?style=for-the-badge&logo=starship&color=526D82&logoColor=DDE6ED&labelColor=27374D">
    </a>
</p>

&nbsp;

### Usage
> <code> python3 Pink-Ddos.py -target <target_ip_or_domain> -port <target_port> -method <mode> -threads <threads> -proxy <proxy_file> -useragents <user_agents_file> -retry <retries> -time <timeout> </code> <br/> <br/>
> <code> example: python3 Pink-Ddos.py -target example.com -port 80 -method http -threads 20 -useragents random-user.txt </code>

<h3> Method: TCP & HTTP</h3>

### How to install
<details>
<summary>Termux</summary>
	
<span>Make sure you have already installed `git` if you don't, run the code above.</span>
```bash
> pkg update -y
> pkg upgrade -y
> pkg install pip
> pkg install python
> pkg install python2
> pkg install git -y
> pip install requests
> pip install tqdm
> pip install HTTPAdapter
> pip install signal
> pip install sys
> pip install Retry

```

<span>Let's cloning it into your computer.</span>
```bash
> git clone https://github.com/anonwincy/Pink-Ddos.git
```
```bash
cd Pink-Ddos
python3 Pink-Ddos.py -h
```
</details>

<details>
<summary>Kali-Linux</summary>
	
<span>Run as root</span>
```bash
> apt update -y
> apt install git -y
> apt update -y
> apt upgrade -y
> apt install pip
> apt install python
> apt install python2
> apt install git -y
> pip install requests
> pip install tqdm
> pip install HTTPAdapter
> pip install signal
> pip install sys
> pip install Retry
> pip install os

```

<span>Let's cloning it into your computer.</span>
```bash
> git clone https://github.com/anonwincy/Pink-Ddos.git
```
```bash
cd Pink-Ddos
python3 Pink-Ddos.py -h
```
</details>
	
### Disclaimer
The use of the xmlrpc-dos is COMPLETE RESPONSIBILITY of the END-USER. Developers assume NO liability and are NOT responsible for any misuse or damage caused by this program.
