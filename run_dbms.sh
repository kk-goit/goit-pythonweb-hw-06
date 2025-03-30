#!/bin/bash

sudo docker run --name goit -p 5432:5432 -e POSTGRES_PASSWORD=qwerty -d postgres

