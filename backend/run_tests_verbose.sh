#!/bin/bash
# Script pour lancer les tests avec output complet

cd /Users/steph/go/src/opti-campaign/backend
echo "🧪 Lancement des tests avec détails complets..."
echo ""
pytest tests/test_campaigns.py -v --tb=long -s

