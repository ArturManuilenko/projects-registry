# projects-registry
Automation of collecting information about current projects and keeping track of employees' time 

## Global requirements
- Bash
- Make
- Python ```3.8.6```
- Pipenv
- Pyenv
- Docker ```19.03.15```
- Docker-compose ```1.27.4```
- Pipenv ```2020.11.15```
- *Packages requirements in Pipfile*

## Environment

### Environment variables for deployment
- Jira:
    - JIRA_TOKEN
    - JIRA_EMAIL
- Tempo:
   - TEMPO_TOKEN

## Commands

### How to update repository to the latest state in the branch
```bash
make build
```