# EventBooking
Sports event booking system. Django project

## Uruchomienie
```sh
docker compose up
```
## Korzystanie z pg admina

1. Wejdz i zaloguj się http://localhost:8080
username: admin@admin.com
pass: admin
2. Dodaj bazę danych1

Servers -> Register -> Name ustawiamy dowolnie
Przejdz do zakładki Connections
![Alt text](image.png)

hasło to: postgres


## Wchodzenie do środka kontenera
```sh
docker exec -it eventbooking-web-1 /bin/bash
```

## Odpalanie stronki
http://localhost:8000

## Przydatne komendy:
docker compose down - usuwa kontenery, ale volume zostaje => baza danych nie zostanie usunięta dopóki nie usuniesz volume'a