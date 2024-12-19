# Server Setup and Deployment Instructions

This guide outlines the steps to set up the server environment, install dependencies, and deploy the chatbot demo project.

## Accessing the EC2 Instance  
1. Ensure your .pem key file has the correct permissions:  
    ```bash
    chmod 400 chatbot-ec2.pem
    ```

2.  Connect to your EC2 instance via SSH:
    ```bash
    ssh -i "chatbot-ec2.pem" ec2-user@<EC2_PUBLIC_IP>
    ```
## Installing Python 3.12 and Dependencies  

Run the following commands inside your EC2 instance:  
Update and Install Required Tools:  
```bash
sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget -y
```
Download and Install Python 3.12:  
```bash
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar xzf Python-3.12.0.tgz
cd Python-3.12.0
./configure --enable-optimizations
make -j 4
sudo make altinstall
```
Make Python 3.12 the default version:  
```bash
sudo ln -sf /usr/local/bin/python3.12 /usr/bin/python3
sudo ln -sf /usr/local/bin/pip3.12 /usr/bin/pip3
```
Install pip:  
```bash
curl -O https://bootstrap.pypa.io/get-pip.py
python3.12 get-pip.py
python3.12 -m pip install --upgrade pip
```
Verify Python Installation:  
```bash
python3.12 --version
pip3.12 --version
```
## Setting Up the Project

Navigate to the Project Directory:
```bash
cd ~/chatbot_demo
```
Install Python Dependencies:
```bash
python3.12 -m pip install --upgrade pip
pip3.12 install -r requirements.txt
```
Set Environment Variables:

Replace YOUR_OPENAI_API_KEY with your OpenAI API key.
```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
