[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![wakatime](https://wakatime.com/badge/github/LorezV/crm-django-and-bot.svg)](https://wakatime.com/badge/github/LorezV/crm-django-and-bot)
![License: Private](https://img.shields.io/badge/License-Private-black.svg)

# crm-django-and-bot

Requirements:

- [Docker >= 20.10.3](https://docs.docker.com/engine/install/)
- [Docker Compose >= 1.28.2](https://docs.docker.com/compose/install/)

### Development

#### 1. Download or clone (`git clone https://github.com/LorezV/crm-django-and-bot.git`) the repository

#### 2. Change directory

```cd crm-django-and-bot```

#### 3. Create local environment files
e.x:
- .envs/.local/nginx.env
```env
SERVER_NAME=localhost
SERVE_FILES=no
DISABLE_DEFAULT_SERVER=yes
USE_REVERSE_PROXY=yes
REVERSE_PROXY_URL_1=/
REVERSE_PROXY_HOST_1=http://django:8000/
PROXY_REAL_IP=yes
USE_GZIP=yes
USE_BROTLI=yes
```
- .envs/.local/django.env
```env
DJANGO_DEBUG=True
DJANGO_SETTINGS_MODULE=crm.settings.local
DJANGO_SECRET_KEY="dev_secret"
DJANGO_ADMINS=Full Name <email-with-name@example.com>,anotheremailwithoutname@example.com
DJANGO_STAFF=Full Name <email-with-name@example.com>,anotheremailwithoutname@example.com
DJANGO_ALLOWED_HOSTS=localhost
DJANGO_DATABASE_MAIN_URL=postgres://dev_user:dev_password@postgres:5432/dev_database
```
- .envs/.local/telegram.env
```env
TELEGRAM_MAIN_BOT_TOKEN="!!!SET TELEGRAM_MAIN_BOT_TOKEN!!!"
```
- .envs/.local/postgres/main.env
```env
POSTGRES_USER=dev_user
POSTGRES_PASSWORD="dev_password"
POSTGRES_DB=dev_database
```

#### 4. Start containers

```docker-compose -f docker-compose-dev.yml up -d```

#### 5. Start the dev server with interactive mode

```sh
docker-compose -f docker-compose-dev.yml exec django sh
poetry shell
./entrypoint.sh
```

#### 6. Open http://localhost in your browser

### Configuration notes

#### Generating your personal ssh key

On your local computer, generate SSH key pair by typing:

```bash
ssh-keygen -b 4096
```
```bash
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):
```

The utility will prompt you to select a location for the keys that will be generated. By default, the keys will be stored in the ~/.ssh directory within your user’s home directory. The private key will be called id_rsa and the associated public key will be called id_rsa.pub.

A passphrase is an optional addition. If you enter one, you will have to provide it every time you use this key (unless you are running SSH agent software that stores the decrypted key). We recommend using a passphrase, but if you do not want to set a passphrase, you can simply press ENTER to bypass this prompt.

```bash
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.
The key fingerprint is:
a9:49:2e:2a:5e:33:3e:a9:de:4e:77:11:58:b6:90:26 username@remote_host
The key's randomart image is:
+--[ RSA 2048]----+
|     ..o         |
|   E o= .        |
|    o. o         |
|        ..       |
|      ..S        |
|     o o.        |
|   =o.+.         |
|. =++..          |
|o=++.            |
+-----------------+
```

You now have a public and private key that you can use to authenticate. The next step is to place the public key on your server so that you can use SSH key authentication to log in.

#### Copying your Public Key Using SSH-Copy-ID

```bash
ssh-copy-id username@remote_host
```
```bash
The authenticity of host '111.111.11.111 (111.111.11.111)' can't be established.
ECDSA key fingerprint is fd:fd:d4:f9:77:fe:73:84:e1:55:00:ad:d6:6d:22:fe.
Are you sure you want to continue connecting (yes/no)? yes
```

This just means that your local computer does not recognize the remote host. This will happen the first time you connect to a new host. Type “yes” and press ENTER to continue.

```bash
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
username@111.111.11.111's password:
```

Type in the password (your typing will not be displayed for security purposes) and press ENTER.

```bash
Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'username@111.111.11.111'"
and check to make sure that only the key(s) you wanted were added.
```

At this point, your id_rsa.pub key has been uploaded to the remote account. You can continue onto the next section.

#### Connecting to server via ssh key

```bash
ssh -p 22 usernam@host
```

source: https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server

#### Setting the DJANGO_DATABASE_MAIN_URL environment variable
In order to use unsafe characters you have to encode with urllib.parse.encode before you set into .env file.
```python
import urllib.parse
urllib.parse.quote_plus('.9.nZ+DNK?-%j?d^')
'.9.nZ%2BDNK%3F-%25j%3Fd%5E'  # use that password in DJANGO_DATABASE_MAIN_URL
```

```bash
# .envs/.production/postgres/main.envs
POSTGRES_PASSWORD=".9.nZ+DNK?-%j?d^"

# .envs/.production/django.env
DJANGO_DATABASE_MAIN_URL=postgres://user:.9.nZ%2BDNK%3F-%25j%3Fd%5E@127.0.0.1:5432/database
```

#### Pre-deploying
Don't forget to add .production folder with a requirement .env files to `/opt/services/crm-django-and-bot/src/`, 
because this folder added to .gitignore for security reasons.
```
/opt/services/crm-django-and-bot/src/
├── ...
├── manage.py
├── pyproject.toml
├── .envs
│   ├── .example
│   ├── .production # CREATE THIS FOLDER ON YOUR SERVER!!!
│   │   ├── postgres
│   │   │   └── main.env # EDIT THAT FILE!!!
│   │   ├── django.env # EDIT THAT FILE!!!
│   │   ├── nginx.env # EDIT THAT FILE!!!
│   │   └── telegram.env # EDIT THAT FILE!!!
└── ...
```
