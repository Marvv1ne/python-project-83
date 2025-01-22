### Page analizer


### Hexlet tests and linter status:
[![Actions Status](https://github.com/Marvv1ne/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Marvv1ne/python-project-83/actions)

[![Python CI](https://github.com/Marvv1ne/python-project-83/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Marvv1ne/python-project-83/actions/workflows/python-ci.yml)

[![Maintainability](https://api.codeclimate.com/v1/badges/77a9eee1bdca69cffd8d/maintainability)](https://codeclimate.com/github/Marvv1ne/python-project-83/maintainability)

[Project on Render](https://python-project-83-2wp1.onrender.com/)

### Description
Check websites for SEO suitability for free

## Technologies Used
- Python 3.x
- Flask 3.x
- PostgreSQL
- HTML/Bootstrap for frontend
- Docker for containerization

## Local Setup
**After cloning the repository and setting up PostgreSQL DB**

1. **Install dependencies:**
```
make install
```
2. **Set up environment variables:** Create `.env` file and define:
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://page_analyser_user:your-password@localhost/page_analyser
where page_analyser_user is your logit to database
your-password is your password to database

P.S.
before connecting to your database (if it`s installed locally on your machine)
do not forget start PostgreSql with command: 'sudo service postgresql start'
```

3. **Build tables in DB:**
```
make build
```
4. **Run server in developer mode:**
```
make dev
```