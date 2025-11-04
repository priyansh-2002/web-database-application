# DevOps Assignment - Flask + MySQL + Docker Compose + Jenkins

## Run locally
1. Build & start:
  docker-compose up --build -d

2. Test:
  curl http://localhost:5000/
  
  curl http://localhost:5000/init
  
  curl -X POST http://localhost:5000/add
   -H "Content-Type: application/json" -d '{"message":"hi"}'
  curl http://localhost:5000/notes

3. Stop:
  docker-compose down -v

## CI/CD
- Jenkinsfile included; configure Jenkins with Docker and credentials `dockerhub-creds`.
