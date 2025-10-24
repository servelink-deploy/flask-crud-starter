# Flask CRUD Starter - API Utilisateurs

Application Flask professionnelle avec architecture Blueprint, rate limiting, et pagination pour la gestion d'utilisateurs.

## 🚀 Fonctionnalités

- **Architecture Blueprint** : Organisation modulaire du code
- **CRUD complet** : Créer, Lire, Mettre à jour et Supprimer des utilisateurs
- **Pagination** : Support de limit/offset pour les listes
- **Recherche** : Recherche d'utilisateurs par nom ou email
- **Rate Limiting** : Protection contre les abus (Flask-Limiter)
- **Validation** : Validation stricte avec Pydantic
- **Gestion d'erreurs** : Handlers personnalisés pour toutes les erreurs
- **Base de données PostgreSQL** : Avec indexation pour les performances
- **CORS** : Support des requêtes cross-origin
- **Health check** : Monitoring de l'état de l'application

## 📋 Prérequis

- Python 3.8+
- PostgreSQL (hébergé en ligne)
- Variables d'environnement configurées

## 🔧 Installation

1. Cloner le projet
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
```

4. Modifier le fichier `.env` :
```
DATABASE_URL=postgresql://user:password@host:port/database
PORT=8000
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

## 🏃 Démarrage

### Développement local
```bash
python main.py
```

### Production (avec Gunicorn)
```bash
gunicorn -w 3 -b 0.0.0.0:8000 main:app
```

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Vérifie l'état de l'application et la connexion à la base de données.

**Réponse** :
```json
{
  "status": "healthy",
  "database": "connected",
  "service": "flask-crud-api"
}
```

### Créer un utilisateur
```http
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+33612345678"
}
```

**Rate limit** : 10 requêtes/minute

### Récupérer tous les utilisateurs (avec pagination)
```http
GET /api/users?limit=20&offset=0
```

**Paramètres** :
- `limit` : Nombre d'utilisateurs (max 100, défaut 100)
- `offset` : Position de départ (défaut 0)

**Réponse** :
```json
{
  "users": [...],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

### Rechercher des utilisateurs
```http
GET /api/users/search?q=john
```

**Paramètres** :
- `q` : Terme de recherche (nom ou email)

### Récupérer un utilisateur par ID
```http
GET /api/users/{id}
```

### Mettre à jour un utilisateur
```http
PUT /api/users/{id}
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+33698765432"
}
```

**Rate limit** : 20 requêtes/minute

### Supprimer un utilisateur
```http
DELETE /api/users/{id}
```

**Rate limit** : 10 requêtes/minute

## 📦 Structure du projet

```
flask-crud-starter/
├── app/
│   ├── __init__.py          # Factory pattern et configuration
│   ├── config.py            # Configuration et variables d'environnement
│   ├── database.py          # Gestion PostgreSQL
│   ├── models.py            # Modèles Pydantic
│   ├── services.py          # Logique métier
│   ├── routes.py            # Blueprints et routes
│   └── errors.py            # Gestionnaires d'erreurs
├── main.py                  # Point d'entrée
├── requirements.txt         # Dépendances
├── .env.example            # Template des variables
├── .gitignore              # Fichiers à ignorer
└── README.md               # Documentation
```

## 🛡️ Sécurité et Performance

### Rate Limiting
- **Limite globale** : 200 requêtes/jour, 50 requêtes/heure
- **POST /api/users** : 10 requêtes/minute
- **PUT /api/users/{id}** : 20 requêtes/minute
- **DELETE /api/users/{id}** : 10 requêtes/minute

### Base de données
- Index sur la colonne `email` pour des recherches rapides
- Transactions automatiques avec rollback en cas d'erreur
- Requêtes préparées contre les injections SQL

### Validation
- Validation stricte des emails avec `email-validator`
- Limites de longueur sur tous les champs
- Validation des types avec Pydantic

## 🎯 Gestion des erreurs

L'API retourne des réponses JSON structurées pour toutes les erreurs :

- **400** : Erreur de validation
- **404** : Ressource non trouvée
- **405** : Méthode non autorisée
- **409** : Conflit (email déjà existant)
- **429** : Trop de requêtes (rate limit)
- **500** : Erreur serveur

## 📝 Best Practices

- **Architecture Blueprint** : Séparation modulaire des routes
- **Factory Pattern** : Fonction `create_app()` pour l'initialisation
- **Séparation des responsabilités** : Routes → Services → Database
- **Rate Limiting** : Protection contre les abus
- **Pagination** : Performance optimisée pour les grandes listes
- **Indexation DB** : Recherches rapides sur les champs clés
- **Validation stricte** : Pydantic pour l'intégrité des données
- **Gestion des erreurs** : Handlers centralisés
- **Code propre** : Auto-documenté sans commentaires superflus

## 🌐 Déploiement

Configuration pour votre plateforme :
- **Build command** : `pip install -r requirements.txt`
- **Start command** : `gunicorn -w 3 -b 0.0.0.0:8000 main:app`

Variables d'environnement requises :
- `DATABASE_URL` : URL de connexion PostgreSQL
- `SECRET_KEY` : Clé secrète pour Flask (production)
- `PORT` : Port d'écoute (optionnel, défaut 8000)
- `FLASK_ENV` : Environnement (production/development)

## 🔍 Différences avec le projet Python de base

Ce projet Flask offre :
- Architecture Blueprint modulaire
- Rate limiting intégré
- Pagination des résultats
- Fonctionnalité de recherche
- Champ téléphone supplémentaire
- Gestion d'erreurs plus complète
- Structure plus professionnelle et scalable
