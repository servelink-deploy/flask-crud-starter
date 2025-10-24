from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    try:
        Config.validate()
        app.run(host='0.0.0.0', port=Config.PORT, debug=False)
    except Exception as e:
        print(f"Erreur au démarrage: {e}")
        exit(1)
