### Homework Serverless with Python

#### Setup

  start localstack
  ```bash
    docker-compose up
  ```

  create resources
  ```bash
    sh ./script.sh
  ```

  #### Resources
  sqs queues
    - em-preparacao-pizzaria
    - pronto-pizzaria

  dynamodb table
    - pedidos-pizzaria

#### Deploy
  run: 
  ```bash
    npm run deploy
  ```


