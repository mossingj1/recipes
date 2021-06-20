# Getting Started

# Ubuntu Server on FreeNAS VM #
## Step 1 - Setting up Freenas Zvol ##
First of all, a dedicated storage space will need to be allocated for the virtual machines. You should have already created a storage pool from one or more drives for file-sharing over the network. Add a new Zvol (ZFS volume) to the preferred pool by clicking the vertical ellipsis menu button (⋮).

![image](https://user-images.githubusercontent.com/52215012/122658673-2f7f9500-d13e-11eb-8cb2-c673d0d5afb6.png)

Specify the size of Zvol, after giving a name to it. Make sure the disk is larger than the minimum requirement of your installed OS. For example, Microsoft Windows 10 and Ubuntu Desktop will need at least 32 GB and 25 GB respectively.

![image](https://user-images.githubusercontent.com/52215012/122658692-51791780-d13e-11eb-8757-e7fff0670122.png)

## Step 2 - Setting up a VM ##
### Create VM ###
Go to the “Virtual Machines” section and click “Add” to create a new VM. Use the settings detailed below.
1) Operating System
>* Guest operating system: Linux
>* Name: UBUDocker (or whatever you want it to be)
>* System Clock: Local
>* Boot method: UEFI
>* Start on boot enabled
>* Enable VNC enabled
>* Bind: 0.0.0.0

![image](https://user-images.githubusercontent.com/52215012/122658774-2a6f1580-d13f-11eb-96e2-03bbcea0b565.png)

2) CPU and Memory
>* Virtual CPUs: 2
>* Memory Size: 4 GiB

![image](https://user-images.githubusercontent.com/52215012/122658980-e2e98900-d140-11eb-93b0-256e533cfb9c.png)

3) Disks
>- Select "Use existing disk Image"
>   - You will use the Zvol created in Step 1
>- Select Jail_V</UBUDocker

![image](https://user-images.githubusercontent.com/52215012/122659017-35c34080-d141-11eb-93ac-361c7ab8915b.png)

4) Network Interface
>* Adaptor Type: VirtIO

![image](https://user-images.githubusercontent.com/52215012/122659031-61462b00-d141-11eb-8a3b-1a2584c6a8cb.png)

5) Instalation Method
>- Choose instalation media image: Select location of Ubuntu image 
>   - /mnt/myVol/ShareDrive/09 - NAS/ubuntu-20.04-desktop-amd64.iso

![image](https://user-images.githubusercontent.com/52215012/122659069-acf8d480-d141-11eb-91bc-90157440df0c.png)

6) Confirm Options
>- Review and confirm options

### Finish setup install ###
Now its time to setup Ubuntu. Go to "Virtual Machines" in FreeNAS and select the newly created VM.

Click the toggle switch to start up the virtual machine. Then select the “VNC” button will take you to the web viewer window, that allows you to remotely control and see the graphical output of the VM. Continue using the VNC to set up Ubuntu on the VM.

Once you are finished setting up Ubuntu go back to FreeNAS -> Virual Machines. Select the Virtual Machine ("UBUDocker") and select POWER OFF. Once shut down, select Devices and remove the CDROM device by clicking the vertical ellipsis menu button (⋮) and selecting DELETE. 

Now restart then Virtual Machine.

### Enabling SSH ###
By default, when Ubuntu is first installed, remote access via SSH is not allowed. Enabling SSH on Ubuntu is fairly straightforward.
Open the terminal with Ctrl+Alt+T and install the openssh-server package:
```
sudo apt update
sudo apt install openssh-server
```
When prompted, enter your password and press Enter to continue with the installation.

Once the installation is complete, the SSH service will start automatically. You can verify that SSH is running by typing:
```
sudo systemctl status ssh
```
The output should tell you that the service is running and enabled to start on system boot. Press q or Ctl-C to get back to the command line prompt.

Ubuntu ships with a firewall configuration tool called UFW. If the firewall is enabled on your system, make sure to open the SSH port:
```
sudo ufw allow ssh
```
As the firewall is currently blocking all connections except for SSH, if you install and configure additional services, you will need to adjust the firewall settings to allow traffic in. You can learn some common UFW operations in our [UFW Essentials guide.](https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands)

Start the firewall by typing.
```
ufw enable
```

To avoid having to log out of our normal user and log back in as the root account, we can set up what is known as superuser or root privileges for our normal account. This will allow our normal user to run commands with administrative privileges by putting the word sudo before each command.

To add these privileges to our new user, we need to add the user to the sudo group. By default, on Ubuntu 20.04, users who are members of the sudo group are allowed to use the sudo command.

```
usermod -aG sudo jcm
```

That’s it! You can now connect to your Ubuntu system via SSH from any remote machine.
*Resources*
- https://www.youtube.com/watch?v=8oMAEBUOPQ0
- https://www.unbxtech.com/2020/04/howto-create-vm-freenas-11.html
- https://linuxize.com/post/how-to-enable-ssh-on-ubuntu-20-04/
- https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04
- https://getmethegeek.com/blog/2021-01-07-add-docker-capabilities-to-truenas-core/
   - https://www.youtube.com/watch?v=XBVjuwgz0Cg


## Step 4 - Installing Docker ##
The Docker installation package available in the official Ubuntu repository may not be the latest version. To ensure we get the latest version, we’ll install Docker from the official Docker repository. To do that, we’ll add a new package source, add the GPG key from Docker to ensure the downloads are valid, and then install the package.

First, update your existing list of packages:
```
sudo apt update
 ```
Next, install a few prerequisite packages which let apt use packages over HTTPS:
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
 ```
Then add the GPG key for the official Docker repository to your system:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
 ```
Add the Docker repository to APT sources:
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
 ```
Next, update the package database with the Docker packages from the newly added repo:
```
sudo apt update
 ```
Make sure you are about to install from the Docker repo instead of the default Ubuntu repo:
```
apt-cache policy docker-ce
 ```
You’ll see output like this, although the version number for Docker may be different:
```
Output of apt-cache policy docker-ce
docker-ce:
  Installed: (none)
  Candidate: 5:19.03.9~3-0~ubuntu-focal
  Version table:
     5:19.03.9~3-0~ubuntu-focal 500
        500 https://download.docker.com/linux/ubuntu focal/stable amd64 Packages
 ```
Notice that docker-ce is not installed, but the candidate for installation is from the Docker repository for Ubuntu 20.04 (focal).

Finally, install Docker:
```
sudo apt install docker-ce
 ```
Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running:
```
sudo systemctl status docker
 ```
The output should be similar to the following, showing that the service is active and running:
```
Output
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2020-05-19 17:00:41 UTC; 17s ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 24321 (dockerd)
      Tasks: 8
     Memory: 46.4M
     CGroup: /system.slice/docker.service
             └─24321 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```
Installing Docker now gives you not just the Docker service (daemon) but also the docker command line utility, or the Docker client. We’ll explore how to use the docker command later in this tutorial.

### Executing the Docker Command Without Sudo (Optional) ###
By default, the docker command can only be run the root user or by a user in the docker group, which is automatically created during Docker’s installation process. If you attempt to run the docker command without prefixing it with sudo or without being in the docker group, you’ll get an output like this:

```
Output
docker: Cannot connect to the Docker daemon. Is the docker daemon running on this host?.
See 'docker run --help'.
```
If you want to avoid typing sudo whenever you run the docker command, add your username to the docker group:
```
sudo usermod -aG docker ${USER}
 ```
To apply the new group membership, log out of the server and back in, or type the following:
```
su - ${USER}
 ```
You will be prompted to enter your user’s password to continue.

Confirm that your user is now added to the docker group by typing:
```
id -nG
 ```
```
Output
jcm sudo docker
```
If you need to add a user to the docker group that you’re not logged in as, declare that username explicitly using:
```
sudo usermod -aG docker username
 ```

### Using the Docker Command ###
Using docker consists of passing it a chain of options and commands followed by arguments. The syntax takes this form:
```
docker [option] [command] [arguments]
 ```
To view all available subcommands, type:
```
docker
 ```
As of Docker 19, the complete list of available subcommands includes:
```
Output
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  images      List images
  import      Import the contents from a tarball to create a filesystem image
  info        Display system-wide information
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  login       Log in to a Docker registry
  logout      Log out from a Docker registry
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  ps          List containers
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  run         Run a command in a new container
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  search      Search the Docker Hub for images
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  version     Show the Docker version information
  wait        Block until one or more containers stop, then print their exit codes
```
To view the options available to a specific command, type:
```
docker docker-subcommand --help
 ```
To view system-wide information about Docker, use:
```
docker info
```
Let’s explore some of these commands. We’ll start by working with images.

### Working with Docker Images ###
```
docker run -d \
    -v ./staticfiles:/opt/recipes/staticfiles \
    -v ./mediafiles:/opt/recipes/mediafiles \
    -p 80:8080 \
    -e SECRET_KEY=YOUR_SECRET_KEY \
    -e DB_ENGINE=django.db.backends.postgresql \
    -e POSTGRES_HOST=db_recipes \
    -e POSTGRES_PORT=5432 \
    -e POSTGRES_USER=djangodb \
    -e POSTGRES_PASSWORD=YOUR_POSTGRES_SECRET_KEY \
    -e POSTGRES_DB=djangodb \
    --name recipes_1 \
    vabene1111/recipes
```
sudo apt install docker-compose
wget https://raw.githubusercontent.com/vabene1111/recipes/develop/.env.template -O .env
docker-compose up -d




Docker containers are built from Docker images. By default, Docker pulls these images from Docker Hub, a Docker registry managed by Docker, the company behind the Docker project. Anyone can host their Docker images on Docker Hub, so most applications and Linux distributions you’ll need will have images hosted there.

To check whether you can access and download images from Docker Hub, type:
```
docker run hello-world
```
The output will indicate that Docker in working correctly:
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b8dfde127a29: Pull complete
Digest: sha256:9f6ad537c5132bcce57f7a0a20e317228d382c3cd61edae14650eec68b2b345c
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Docker was initially unable to find the hello-world image locally, so it downloaded the image from Docker Hub, which is the default repository. Once the image downloaded, Docker created a container from the image and the application within the container executed, displaying the message.

You can search for images available on Docker Hub by using the docker command with the search subcommand. For example, to search for the Ubuntu image, type:
```
docker search ubuntu
 ```
The script will crawl Docker Hub and return a listing of all images whose name match the search string. In this case, the output will be similar to this:
```
Output
NAME                                                      DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
ubuntu                                                    Ubuntu is a Debian-based Linux operating sys…   10908               [OK]
dorowu/ubuntu-desktop-lxde-vnc                            Docker image to provide HTML5 VNC interface …   428                                     [OK]
rastasheep/ubuntu-sshd                                    Dockerized SSH service, built on top of offi…   244                                     [OK]
consol/ubuntu-xfce-vnc                                    Ubuntu container with "headless" VNC session…   218                                     [OK]
ubuntu-upstart                                            Upstart is an event-based replacement for th…   108                 [OK]
ansible/ubuntu14.04-ansible                               Ubuntu 14.04 LTS with 
```

In the OFFICIAL column, OK indicates an image built and supported by the company behind the project. Once you’ve identified the image that you would like to use, you can download it to your computer using the pull subcommand.

Execute the following command to download the official ubuntu image to your computer:

docker pull ubuntu
 
You’ll see the following output:

Output
Using default tag: latest
latest: Pulling from library/ubuntu
d51af753c3d3: Pull complete
fc878cd0a91c: Pull complete
6154df8ff988: Pull complete
fee5db0ff82f: Pull complete
Digest: sha256:747d2dbbaaee995098c9792d99bd333c6783ce56150d1b11e333bbceed5c54d7
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest
After an image has been downloaded, you can then run a container using the downloaded image with the run subcommand. As you saw with the hello-world example, if an image has not been downloaded when docker is executed with the run subcommand, the Docker client will first download the image, then run a container using it.

To see the images that have been downloaded to your computer, type:

docker images
 
The output will look similar to the following:

Output
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              1d622ef86b13        3 weeks ago         73.9MB
hello-world         latest              bf756fb1ae65        4 months ago        13.3kB
As you’ll see later in this tutorial, images that you use to run containers can be modified and used to generate new images, which may then be uploaded (pushed is the technical term) to Docker Hub or other Docker registries.

Let’s look at how to run containers in more detail.



Select Language
![image](https://user-images.githubusercontent.com/52215012/122659210-96537d00-d143-11eb-9bb0-96baedc9cc17.png)

Keyboard Layout
![image](https://user-images.githubusercontent.com/52215012/122659214-a4a19900-d143-11eb-8c45-5959770387e1.png)
![image](https://user-images.githubusercontent.com/52215012/122659264-49bc7180-d144-11eb-8855-5e2317f6d2ed.png)

## Prerequisites
In order to complete this guide, you should have a fresh Ubuntu 20.04 server instance with a basic firewall and a non-root user with sudo privileges configured. You can learn how to set this up by running through our initial server setup guide.

We will be installing Django within a virtual environment. Installing Django into an environment specific to your project will allow your projects and their requirements to be handled separately.

Once we have our database and application up and running, we will install and configure the Gunicorn application server. This will serve as an interface to our application, translating client requests from HTTP to Python calls that our application can process. We will then set up Nginx in front of Gunicorn to take advantage of its high performance connection handling mechanisms and its easy-to-implement security features.

Let’s get started.

# Docker Install #
## Step 1 — Installing Docker ##
First, update your existing list of packages:
``` 
sudo apt update
 ```
Next, install a few prerequisite packages which let apt use packages over HTTPS:
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
 ```
Then add the GPG key for the official Docker repository to your system:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
 ```
Add the Docker repository to APT sources:
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
 ```
Next, update the package database with the Docker packages from the newly added repo:
```
sudo apt update
 ```
Make sure you are about to install from the Docker repo instead of the default Ubuntu repo:
```
apt-cache policy docker-ce
```
Finally, install Docker:
```
sudo apt install docker-ce
 ```
Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running:
```
sudo systemctl status docker
```

## Step 2 — Install Docker Compose ##
First, confirm the latest version available in their [releases page.] (https://github.com/docker/compose/releases) At the time of this writing, the most current stable version is 1.29.2.

The following command will download the 1.29.2 release and save the executable file at /usr/local/bin/docker-compose, which will make this software globally accessible as docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Next, set the correct permissions so that the docker-compose command is executable:
```
sudo chmod +x /usr/local/bin/docker-compose
```
To verify that the installation was successful, you can run:
```
docker-compose --version
 ```
You’ll see output similar to this:
```
Output
docker-compose version 1.27.4, build 40524192
Docker Compose is now successfully installed on your system. In the next section, we’ll see how to set up a docker-compose.yml file and get a containerized environment up and running with this tool.
```

### Step 3 - Setting up Portainer ###
Now that Docker and Docker Composer are installed, follow the steps below to get Portainer setup.

You can use Docker command to deploy the Portainer Server; note the agent is not needed on standalone hosts, however, it does provide additional functionality if used.

To get the server installed, run the commands below.
```
cd ~/
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer
```
You’ll just need to access the port 9000 of the Docker engine where Portainer is running using your browser.
At this point, all you need to do is access Portainer portal to manage Docker. Open your web browser and browse to the server’s hostname or IP address followed by port #9000

http://localhost:9000

### Resources ###
- https://docs.fuga.cloud/how-to-install-portainer-docker-ui-manager-on-ubuntu-20.04-18.04-16.04
- https://getmethegeek.com/blog/2020-04-20-installing-docker-and-portainer-on-proxmox/
- https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04
- docker system prune

### Next ###
We now need to create an area for Portainer to have data.
```
mkdir ~/mealplanner
cd ~/mealplanner
 ```
In this directory, set up an application folder to serve as the document root for your Nginx environment:
```
mkdir app
```
Using your preferred text editor, create a new index.html file within the app folder:
```
nano app/index.html
```
Place the following content into this file:
```
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Docker Compose Demo</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/dark.min.css">
</head>
<body>

    <h1>This is a Docker Compose Demo Page.</h1>
    <p>This content is being served by an Nginx container.</p>

</body>
</html>
```
Save and close the file when you’re done. If you are using nano, you can do that by typing CTRL+X, then Y and ENTER to confirm.

Next, create the docker-compose.yml file:
```
wget https://raw.githubusercontent.com/vabene1111/recipes/develop/docs/install/docker/nginx-proxy/docker-compose.yml
```
### Step 4 — Running Docker Compose ###
With the docker-compose.yml file in place, we can now execute Docker Compose to bring our environment up. The following command will download the necessary Docker images, create a container for the web service, and run the containerized environment in background mode:

```
wget https://raw.githubusercontent.com/vabene1111/recipes/develop/docs/install/docker/plain/docker-compose.yml
```
```
wget https://raw.githubusercontent.com/vabene1111/recipes/develop/.env.template -O .env
```
```
docker network create nginx-proxy
```
```
docker-compose run -d
```
```
docker-compose ps
```


```
docker run -d \
    -v "/$(pwd)/staticfiles:/opt/recipes/staticfiles" \
    -v "{pwd}/mediafiles:/opt/recipes/mediafiles" \
    -p 80:8080 \
    -e SECRET_KEY=YOUR_SECRET_KEY \
    -e DB_ENGINE=django.db.backends.postgresql \
    -e POSTGRES_HOST=db_recipes \
    -e POSTGRES_PORT=5432 \
    -e POSTGRES_USER=djangodb \
    -e POSTGRES_PASSWORD=YOUR_POSTGRES_SECRET_KEY \
    -e POSTGRES_DB=djangodb \
    --name recipes_1 \
    vabene1111/recipes
```
Docker Compose will first look for the defined image on your local system, and if it can’t locate the image it will download the image from Docker Hub. You’ll see output like this:

Your environment is now up and running in the background. To verify that the container is active, you can run:
```
docker-compose ps
 ```
This command will show you information about the running containers and their state, as well as any port redirections currently in place:

Output
       Name                     Command               State          Ports        
----------------------------------------------------------------------------------
compose-demo_web_1   /docker-entrypoint.sh ngin ...   Up      0.0.0.0:8000->80/tcp
You can now access the demo application by pointing your browser to either localhost:8000 if you are running this demo on your local machine, or your_server_domain_or_IP:8000 if you are running this demo on a remote server.

You’ll see a page like this:




We now need to create an area for Portainer to have data.
 ```
sudo mkdir /portainer
sudo mkdir /portainer/data
 ```
Now we will do a Docker run Portainer
 ```
sudo docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always --pull=always -v /var/run/docker.sock:/var/run/docker.sock -v /portainer/data:/data portainer/portainer-ce
 ```
# Manual Install #
### Installing the Packages from the Ubuntu Repositories

To begin the process, we’ll download and install all of the items we need from the Ubuntu repositories. We will use the Python package manager pip to install additional components a bit later.

We need to update the local apt package index and then download and install the packages. The packages we install depend on which version of Python your project will use.
```shell script
$ sudo apt update
$ sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl git
```

## Creating the PostgreSQL Database and User
Log into an interactive Postgres session by typing:

``` shell script
$ sudo -u postgres psql
```
In the psql console:
```
CREATE DATABASE djangodb;
CREATE USER djangouser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE djangodb TO djangouser;
ALTER DATABASE djangodb OWNER TO djangouser;

--Maybe not necessary, but should be faster:
ALTER ROLE djangouser SET client_encoding TO 'utf8';
ALTER ROLE djangouser SET default_transaction_isolation TO 'read committed';
ALTER ROLE djangouser SET timezone TO 'UTC';

--Grant superuser right to your new user, it will be removed later
ALTER USER djangouser WITH SUPERUSER;
```
When you are finished, exit out of the PostgreSQL prompt by typing:

``` shell script
\q
```

## Creating a Python Virtual Environment for your Project
Now that we have our database, we can begin getting the rest of our project requirements ready. We will be installing our Python requirements within a virtual environment for easier management.

To do this, we first need access to the virtualenv command. We can install this with pip.

If you are using Python 3, upgrade pip and install the package by typing:

``` shell script
$ sudo -H pip3 install --upgrade pip
$ sudo -H pip3 install virtualenv
```
With virtualenv installed, we can start forming our project. Create and move into a directory where we can keep our project files:

``` shell script
$ mkdir ~/recipes
$ cd ~/recipes
```
Within the project directory, create a Python virtual environment by typing:
``` shell script
virtualenv recipesenv
```
This will create a directory called recipesenv within your recipes directory. Inside, it will install a local version of Python and a local version of pip. We can use this to install and configure an isolated Python environment for our project.

Before we install our project’s Python requirements, we need to activate the virtual environment. You can do that by typing:
``` shell script
$ source recipesenv/bin/activate
```
Your prompt should change to indicate that you are now operating within a Python virtual environment. It will look something like this: (recipesenv)user@host:~/recipes$.

*With your virtual environment active, install Django, Gunicorn, and the psycopg2 PostgreSQL adaptor with the local instance of pip:
Note: When the virtual environment is activated (when your prompt has (myprojectenv) preceding it), use pip instead of pip3, even if you are using Python 3. The virtual environment’s copy of the tool is always named pip, regardless of the Python version.*

``` shell script
$ pip install django gunicorn psycopg2-binary
 ```
You should now have all of the software needed to start a Django project.

## Installing Django Project
Get the last version from the repository: 
``` shell script
$ git clone https://github.com/vabene1111/recipes.git -b master
```
Download the .env configuration file and edit it accordingly.
```
wget https://raw.githubusercontent.com/vabene1111/recipes/develop/.env.template -O .env
```
edit .env template line 
Load variables from POSTGRES_HOST=db_recipes to POSTGRES_HOST=localhost

``` shell script
$ export $(cat .env |grep "^[^#]" | xargs) 
```

Execute
```
python3.8 manage.py migrate
```
Log into an interactive Postgres session by typing:
```
sudo -u postgres psql
```
revert superuser from postgres
```
ALTER USER djangouser WITH NOSUPERUSER;
```
Generate static files:
```
python3.8 manage.py collectstatic
```

Test to see everything worked by typing:
``` 
python3.8 manage.py runserver
```


## Creating systemd Socket and Service Files for Gunicorn

The Gunicorn socket will be created at boot and will listen for connections. When a connection occurs, systemd will automatically start the Gunicorn process to handle the connection.

Start by creating and opening a systemd socket file for Gunicorn with sudo privileges:
```
sudo nano /etc/systemd/system/gunicorn.socket
```
Inside, we will create a [Unit] section to describe the socket, a [Socket] section to define the socket location, and an [Install] section to make sure the socket is created at the right time:
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Next, create and open a systemd service file for Gunicorn with sudo privileges in your text editor. The service filename should match the socket filename with the exception of the extension:
```
sudo nano /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=jcm
Group=www-data
WorkingDirectory=/home/jcm/recipes/recipes
EnvironmentFile=/home/jcm/recipes/recipes/.env
ExecStart=/home/jcm/recipes/recipesenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          recipes.wsgi:application

[Install]
WantedBy=multi-user.target
```


We can now start and enable the Gunicorn socket. This will create the socket file at /run/gunicorn.sock now and at boot. When a connection is made to that socket, systemd will automatically start the gunicorn.service to handle it:
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
Check the status of the process to find out whether it was able to start:
```
sudo systemctl status gunicorn.socket
```
You should receive an output like this:
```
Output
● gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor prese>
     Active: active (listening) since Fri 2020-06-26 17:53:10 UTC; 14s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
      Tasks: 0 (limit: 1137)
     Memory: 0B
     CGroup: /system.slice/gunicorn.socket
```
Next, check for the existence of the gunicorn.sock file within the /run directory:
```
$ file /run/gunicorn.sock
```
```
Output
/run/gunicorn.sock: socket
```

Check the Gunicorn socket’s logs by typing:
```
$ sudo journalctl -u gunicorn.socket
```

sudo systemctl daemon-reload
sudo systemctl restart gunicorn


## Configure Nginx to Proxy Pass to Gunicorn
ow that Gunicorn is set up, we need to configure Nginx to pass traffic to the process.

Start by creating and opening a new server block in Nginx’s sites-available directory:

```
sudo nano /etc/nginx/sites-available/recipes
```

```
server {
    listen 8002;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static {
        alias /home/jcm/recipes/recipes/staticfiles;
    }

    location /media {
        alias /home/jcm/recipes/recipes/mediafiles;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Save and close the file when you are finished. Now, we can enable the file by linking it to the sites-enabled directory:
```
sudo ln -s /etc/nginx/sites-available/recipes /etc/nginx/sites-enabled
```

Test your Nginx configuration for syntax errors by typing:
```
sudo nginx -t
```
If no errors are reported, go ahead and restart Nginx by typing:
```
sudo systemctl restart nginx
```

Finally, we need to open up our firewall to normal traffic on port 80. Since we no longer need access to the development server, we can remove the rule to open port 8000 as well:
```
sudo ufw delete allow 8002
sudo ufw allow 'Nginx Full'
```
























Create a service that will start gunicorn at boot:
```
sudo nano /etc/systemd/system/gunicorn_recipes.service
```
And enter these lines:
```
[Unit]
Description=gunicorn daemon for recipes
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=3
Group=www-data
WorkingDirectory=/media/data/recipes
EnvironmentFile=/media/data/recipes/.env
ExecStart=/opt/.pyenv/versions/3.8.5/bin/gunicorn --error-logfile /tmp/gunicorn_err.log --log-level debug --capture-output --bind unix:/media/data/recipes/recipes.sock recipes.wsgi:application

[Install]
WantedBy=multi-user.target
```

sudo systemctl enable gunicorn_recipes.service
sudo systemctl start gunicorn_recipes.service
systemctl status gunicorn_recipes.service








 --error-logfile /tmp/gunicorn_err.log --log-level debug --capture-output --bind unix:/run/guinicorn.sock recipes.wsgi:application




### Resources VM
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

### Creating a Ubuntu VM
- https://www.unbxtech.com/2020/04/howto-create-vm-freenas-11.html
- https://www.youtube.com/watch?v=8oMAEBUOPQ0

### Initial Server Setup with Ubuntu 20.04
https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04

### How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 20.04
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04

**Installing the Packages from the Ubuntu Repositories**




sudo -u postgres psql




iocage setup
New Jail
DCHP

 create a dataset in the FreeNAS WebUI where you'll store the app
mkdir /mnt/myVol/apps/recipes/postgresql/

mount dataset 
iocage fstab -a postgresql /mnt/Data/apps/postgresql /mnt/postgres/data nullfs rw 0 0

The first thing you need to do is to update and upgrade packages:
pkg update
pkg upgrade

*Install Packages*
pkg install sudo
pkg install git
pkg install python38

*Install Pip*
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.8 get-pip.py

*Upgrading PIP*
python -m pip install -U pip

*Install PostgreSQL*
pkg install postgresql12-server

#autostart service with jail
sysrc postgresql_enable=YES

sudo pip install -r requirements.txt

pip install cryptography-2.8-cp38-cp38-win_amd64 (1)


Get the last version from the repository:
git clone https://github.com/vabene1111/recipes.git -b master


<h1 align="center">
  <br>
  <a href="https://app.tandoor.dev"><img src="https://github.com/vabene1111/recipes/raw/develop/docs/logo_color.svg" height="256px" width="256px"></a>
  <br>
  Tandoor Recipes
  <br>
</h1>

<h4 align="center">The recipe manager that allows you to manage your ever growing collection of digital recipes.</h4>

<p align="center">

<img src="https://github.com/vabene1111/recipes/workflows/Continous%20Integration/badge.svg?branch=develop" >
<img src="https://img.shields.io/github/stars/vabene1111/recipes" >
<img src="https://img.shields.io/github/forks/vabene1111/recipes" >
<img src="https://img.shields.io/docker/pulls/vabene1111/recipes" >

</p>

<p align="center">
<a href="https://docs.tandoor.dev/install/docker/" target="_blank" rel="noopener noreferrer">Installation</a> •
<a href="https://docs.tandoor.dev/" target="_blank" rel="noopener noreferrer">Documentation</a> •
<a href="https://app.tandoor.dev/" target="_blank" rel="noopener noreferrer">Demo</a>
</p>

![Preview](docs/preview.png)

# Your Feedback

Share some information on how you use Tandoor to help me improve the application [Google Survey](https://forms.gle/qNfLK2tWTeWHe9Qd7)

## Features

- 📦 **Sync** files with Dropbox and Nextcloud (more can easily be added)
- 🔍 Powerful **search** with Djangos [TrigramSimilarity](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#trigram-similarity)
- 🏷️ Create and search for **tags**, assign them in batch to all files matching certain filters
- 📄 **Create recipes** locally within a nice, standardized web interface
- ⬇️ **Import recipes** from thousands of websites supporting [ld+json or microdata](https://schema.org/Recipe)
- 📱 Optimized for use on **mobile** devices like phones and tablets
- 🛒 Generate **shopping** lists from recipes
- 📆 Create a **Plan** on what to eat when
- 👪 **Share** recipes with friends and comment on them to suggest or remember changes you made
- ➗ automatically convert decimal units to **fractions** for those who like this
- 🐳 Easy setup with **Docker** and included examples for Kubernetes, Unraid and Synology
- 🎨 Customize your interface with **themes**
- ✉️ Export and import recipes from other users
- 🌍 localized in many languages thanks to the awesome community
- ➕ Many more like recipe scaling, image compression, cookbooks, printing views, ...

This application is meant for people with a collection of recipes they want to share with family and friends or simply
store them in a nicely organized way. A basic permission system exists but this application is not meant to be run as 
a public page.
Documentation can be found [here](https://docs.tandoor.dev/).

While this application has been around for a while and is actively used by many (including myself), it is still considered
**beta** software that has a lot of rough edges and unpolished parts.
## License

Beginning with version 0.10.0 the code in this repository is licensed under the [GNU AGPL v3](https://www.gnu.org/licenses/agpl-3.0.de.html) license with an
[common clause](https://commonsclause.com/) selling exception. See [LICENSE.md](https://github.com/vabene1111/recipes/blob/develop/LICENSE.md) for details.

> NOTE: There appears to be a whole range of legal issues with licensing anything else then the standard completely open licenses.
> I am in the process of getting some professional legal advice to sort out these issues. 
> Please also see [Issue 238](https://github.com/vabene1111/recipes/issues/238) for some discussion and **reasoning** regarding the topic.

**Reasoning**  
**This software and *all* its features are and will always be free for everyone to use and enjoy.**

The reason for the selling exception is that a significant amount of time was spend over multiple years to develop this software.
A payed hosted version which will be identical in features and code base to the software offered in this repository will
likely be released in the future (including all features needed to sell a hosted version as they might also be useful for personal use).
This will not only benefit me personally but also everyone who self-hosts this software as any profits made trough selling the hosted option
allow me to spend more time developing and improving the software for everyone. Selling exceptions are [approved by Richard Stallman](http://www.gnu.org/philosophy/selling-exceptions.en.html) and the
common clause license is very permissive (see the [FAQ](https://commonsclause.com/)).
