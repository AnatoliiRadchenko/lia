sudo apt-get install -y apt-transport-https software-properties-common wget
Import the GPG key:

bash
Copy code to clipboard
Copy
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
To add a repository for stable releases, run the following command:

bash
Copy code to clipboard
Copy
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
To add a repository for beta releases, run the following command:

bash
Copy code to clipboard
Copy
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com beta main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
Run the following command to update the list of available packages:

bash
Copy code to clipboard
Copy
# Updates the list of available packages
sudo apt-get update
To install Grafana OSS, run the following command:

bash
Copy code to clipboard
Copy
# Installs the latest OSS release:
sudo apt-get install grafana
