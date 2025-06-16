Проект по литература - Кръстословица (в случая за мотива за смъртта)
(Да, базата данни е качена нарочно. Така си пращам думите за кръстословицата. Не, не правете като мен моля. Тук има само 10 въпроса с автор, произведение, година, информация и отговор)

Setup:
1. Make sure you have Docker and Docker Compose installed on your system.

2. Build and start the containers:
```bash
docker-compose up --build
```

3. In a new terminal, initialize the database:
```bash
docker-compose exec web python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

The application will be available at `http://localhost:5000`
