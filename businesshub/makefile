# ⚙️ Ambiente di default (dev). Sovrascrivibile con make up ENV=prod
ENV ?= .env

up:
	@echo "🚀 Avvio ambiente con $(ENV)"
	docker compose --env-file $(ENV) up -d --build

down:
	@echo "🛑 Arresto ambiente con $(ENV)"
	docker compose --env-file $(ENV) down

down-volumes:
	@echo "🧨 Arresto + Rimozione volumi con $(ENV)"
	docker compose --env-file $(ENV) down -v

status:
	@echo "📊 Stato container con $(ENV)"
	docker compose --env-file $(ENV) ps

logs:
	@echo "📜 Log del container web"
	docker compose --env-file $(ENV) logs -f web

migrate:
	docker compose --env-file $(ENV) exec web python manage.py migrate

createsuperuser:
	docker compose --env-file $(ENV) exec web python manage.py createsuperuser

collectstatic:
	docker compose --env-file $(ENV) exec web python manage.py collectstatic --noinput
