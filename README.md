<div align="center">

# AI Portfolio Assistant

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange.svg)
![Pushover](https://img.shields.io/badge/Notifications-Pushover-blue.svg)

*Ce projet est un mini-projet de démonstration. Son but principal est d'illustrer la maîtrise et la compréhension de la logique interne d'un chatbot, en implémentant une boucle de discussion conversationnelle de zéro, sans faire appel à des frameworks d'orchestration IA (comme LangChain, LlamaIndex, etc.).*

</div>

## Concept & Logique du Projet

L'objectif technique est de démontrer comment orchestrer manuellement l'état d'une conversation, l'injection de contexte en amont (RAG simplifié) et la gestion de l'appel d'outils (Function Calling) à l'aide d'une boucle `while` personnalisée.

L'agent lit votre parcours professionnel et répond aux questions des visiteurs à votre place, tout en capturant des leads et en remontant les questions sans réponse de manière entièrement programmée et transparente.

### Fonctionnalités Clés :
1. **Jeu de rôle / Persona (System Prompting) :** L'agent est instruit via un prompt système pour agir en tant que vous-même, avec un ton professionnel et engageant.
2. **Injection de Contexte Personnel :** Au démarrage, le script lit des documents locaux (`me/Profile.pdf` et `me/summary.txt`). Ces informations sont injectées dans le contexte du modèle pour lui permettre de répondre précisément sur vos compétences et votre expérience.
3. **Appel de Fonctions (Tool Calling) :** Le LLM est doté d'outils (fonctions Python) qu'il peut décider d'utiliser de manière autonome :
   - `record_user_details` : Si un recruteur ou un client souhaite être contacté, l'IA lui demande son email et l'enregistre.
   - `record_unknown_question` : Si on pose une question à l'IA dont la réponse ne se trouve pas dans son contexte, elle enregistre la question pour que vous puissiez l'étudier plus tard (plutôt que d'halluciner une réponse).
4. **Notifications Push :** Dès qu'un outil est utilisé (nouvel email récupéré ou question sans réponse), le script envoie une requête API à **Pushover**, qui déclenche instantanément une notification push sur votre smartphone.
5. **Interface Utilisateur :** Une interface de chat clé-en-main est générée via **Gradio** (`gr.ChatInterface`).

## 🛠 Prérequis

- **Python 3.10+** (Recommandé)
- Une clé API [OpenAI](https://platform.openai.com/)
- Un compte [Pushover](https://pushover.net/) (Clé utilisateur et Token d'application)
- [uv](https://github.com/astral-sh/uv) 

## Installation & Utilisation

Nous utilisons `uv` pour configurer l'environnement Python de manière rapide et fiable.

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/maximeKets/ai-portfolio-assistant.git
   cd ai-portfolio-assistant
   ```

2. **Installer les dépendances et créer l'environnement  :**
   ```bash
   uv sync
   ```

4. **Configurer l'environnement :**
   ```bash
   cp .env.example .env
   ```
   Remplissez les variables dans `.env` :
   - `OPENAI_API_KEY` : Votre clé API OpenAI.
   - `PUSHOVER_USER` : Votre clé utilisateur Pushover.
   - `PUSHOVER_TOKEN` : Votre token d'application Pushover.

5. **Ajouter vos données personnelles :**
   Créez un dossier `me/` à la racine du projet et ajoutez-y :
   - `Profile.pdf` : Votre CV ou export LinkedIn au format PDF.
   - `summary.txt` : Un fichier texte résumant qui vous êtes.

6. **Lancer l'assistant :**
   ```bash
   uv run python main.py
   ```
   Un lien local (ex: `http://127.0.0.1:7860`) s'affichera pour accéder à l'interface de chat.


