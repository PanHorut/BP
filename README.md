# Bachelor's Thesis
## Basic school math drill platform with entering answers by voice
**Author:** Dominik Horut (`xhorut01`)

This file describes the directory structure of the implementation part of the thesis and provides a setup guide for running the application.

## Directory structure
<pre>.
├── be
│   ├── api ................. Application logic and endpoints
│   ├── be  ................. Server setup
│   ├── db_init ............. Seed data
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md ........... Guide to run server in development mode
├── fe
│   ├── index.html
│   ├── src ................. Frontend source code
│   │   ├── api
│   │   ├── components
│   │   ├── router
│   │   ├── stores
│   │   ├── utils
│   │   └── views 
│   ├── README.md ........... Guide to run frontend in developer mode
├── LICENSE ................. License (GNU GPL v3)
└── README.md ............... General project overview and setup guide
</pre>



## Application build and run guide
This section provides instructions to build and run the application locally.
Alternatively, you can access the deployed version [here](https://drillovacka.applikuapp.com/).

### Requirements

This application uses Docker to build and run its services. Before you begin, ensure the following are installed on your machine:
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/


### 1. Navigate to the `be` directory
Assuming you are in root directory of application:
```bash
cd be
```

### 2. Environment setup

Configure the required environment variables in your `.env` file:

```sh
MYSQLDATABASE=drillovacka-demo
MYSQLUSER=root
MYSQLPASSWORD=secret
MYSQLHOST=localhost
MYSQLPORT=3307
```

Additionally, the application uses **Azure Speech-to-Text** and **Gemini** services. To authenticate these services, add your respective API keys to the `.env` file:
```sh
AZURE_API_KEY=YOUR_AZURE_API_KEY
AZURE_REGION=YOUR_AZURE_REGION
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 3. Build the containers
Build the server and database containers:

```bash
docker-compose build --no-cache
```
### 4. Start the containers
Start the server and MySQL database:

```bash
docker-compose up
```
### 5. Access the application
Visit http://localhost:8000/ to access the application. 

To use admin part of application, login with these credentials:
- **Username:** admin1
- **Password:** kockanenipes

### 6. Clean up
Stop and remove containers, volumes, and networks used by docker-compose:
```bash
docker-compose down --volumes --remove-orphans
```
Remove the `be_web` image
```bash
docker rmi be_web
```

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
See the [LICENSE](./LICENSE) file for details.