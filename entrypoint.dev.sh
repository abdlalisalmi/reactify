#!/bin/sh

# CD to the server directory
until cd /app
do
    echo "Waiting for server volume..."
done

# Generate the database migrations
until ./manage.py makemigrations
do
	echo "Waiting for create migrations..."
	sleep 2
done

# Apply the database migrations
until ./manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

# Create the default superuser
until python create_superuser.py
do
	echo "Creating SuperUser..."
	sleep 2
done

# Collect static files
until ./manage.py collectstatic --noinput
do
	echo "Waiting for collectstatic..."
	sleep 2
done

# Run the server
until ./manage.py runserver 0.0.0.0:8000
do
	echo "Waiting for server..."
	sleep 2
done
