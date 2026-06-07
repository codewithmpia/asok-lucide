import os
import sys

# S'assurer que le package local asok-lucide est importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Forcer le mode DEBUG et définir une SECRET_KEY pour contourner les validations de production d'Asok
os.environ["DEBUG"] = "true"
os.environ["SECRET_KEY"] = "test-secret-key-do-not-use-in-prod"
