#!/bin/bash
# Script pour installer les bonnes dépendances et lancer les tests

echo "📦 Mise à jour de bcrypt vers version compatible..."
pip uninstall -y bcrypt
pip install bcrypt==4.1.3

echo ""
echo "🧪 Lancement des tests..."
cd /Users/steph/go/src/opti-campaign/backend
pytest tests/test_campaigns.py -v

echo ""
echo "✅ Tests terminés!"
