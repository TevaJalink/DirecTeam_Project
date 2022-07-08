#this is a step by step guide to create the producer-sqs-consumer-s3 pipeline

1)login to your aws console
2) navigate to sqs and create your sqs quueue
3) navigate to s3 and create an s3 bucket
4) navigae to IAM and create 2 policies with the iam policies json files in the consumer and producer folders
5) create 2 users, one for the producer and one for the consumer and save thier access id files
6) open the .env file in producer inorder to add the enviroment variables
7) open the .env file in consumer inorder to add the enviroment variables
8) navigate to the directory where the producer docker file is and build the image using docker-build command, call the image 'Producer_image'
9) navigate to the directory where the consumer docker file is and build the image using docker-build command, call the image 'Consumer_image'
10) run docker-compose --env-file, each with the relevent env file inorder to run the docker with the relevent env variables
11) download postman to test the API