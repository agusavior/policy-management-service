# PMS API

PMS means Policy Management Service.

## Getting started

### Run it without docker

You may use an IDE as IntelliJ.
Open the folder with your IDE and run it with the green start button.

Now you may go to your browser and open https://localhost

### Run it with Docker

```bash
cd api
docker build . -t pms && docker run -p 80:80 pms
```

Now you may go to your browser and open https://localhost

## Deploy it to AWS

Read this [README](infrastructure).

## Endpoints

There are three endpoints. We use only POSTs methods because the specifications kinda imply that.
* POST `/policy/creation`
* POST `/policy/modification`
* POST `/policy/information`

Read the specifications [HERE](docs/EMBEA_PMS_Specifications.pdf).