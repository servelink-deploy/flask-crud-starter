from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Route non trouvée',
            'status': 404
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Méthode non autorisée',
            'status': 405
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Erreur interne du serveur',
            'status': 500
        }), 500

    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify({
            'error': 'Trop de requêtes. Veuillez réessayer plus tard.',
            'status': 429
        }), 429
