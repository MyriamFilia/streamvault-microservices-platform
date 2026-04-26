import requests
import random
import time

# URLs spécifiques pour l'environnement Docker Compose (sans Gateway)
USER_URL = "http://127.0.0.1:8002"
FAVORITES_URL = "http://127.0.0.1:8003"
REVIEWS_URL = "http://127.0.0.1:8004"

# Des vrais IDs de séries populaires sur TVMaze
SERIES_IDS = [169, 82, 2993, 526, 17861, 108, 431, 426, 143, 73]

# Nos 5 utilisateurs de simulation
USERS = [
    {"username": "Alice_Cinephile", "email": "alice@streamvault.com", "password": "password123"},
    {"username": "Bob_BingeWatcher", "email": "bob@streamvault.com", "password": "password123"},
    {"username": "Charlie_Critic", "email": "charlie@streamvault.com", "password": "password123"},
    {"username": "Diana_SciFi", "email": "diana@streamvault.com", "password": "password123"},
    {"username": "Ethan_Casual", "email": "ethan@streamvault.com", "password": "password123"},
]

COMMENTS_POS = ["Masterpiece! A must watch.", "Absolutely loved it.", "Best show ever.", "Great acting and incredible plot.", "Highly recommended! 10/10."]
COMMENTS_MIX = ["It was okay.", "A bit slow in the middle seasons.", "Good, but clearly overrated.", "Started great, bad ending."]
COMMENTS_NEG = ["Not my cup of tea at all.", "Boring.", "I couldn't finish the first season, too slow."]

def run_seeder():
    print("🚀 Début du Seeding de StreamVault (Local/Docker Compose)...")
    
    for user in USERS:
        print(f"\n👤 Traitement de l'utilisateur : {user['username']}")
        
        # 1. Inscription (Register) - Utilise USER_URL
        requests.post(f"{USER_URL}/users/register", json=user)
        
        # 2. Connexion (Login) - Utilise USER_URL
        res_login = requests.post(f"{USER_URL}/users/login", json={"username": user["username"], "password": user["password"]})
        
        if res_login.status_code != 200:
            print(f"  ❌ Échec de la connexion pour {user['username']}. On passe au suivant.")
            continue
            
        token = res_login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("  ✅ Connecté avec succès.")

        num_favorites = random.randint(2, 6)
        num_reviews = random.randint(2, 5)
        user_series = random.sample(SERIES_IDS, max(num_favorites, num_reviews))

        # 3. Ajout des Favoris - Utilise FAVORITES_URL
        print(f"  ❤️ Ajout de {num_favorites} favoris...")
        for series_id in user_series[:num_favorites]:
            requests.post(f"{FAVORITES_URL}/favorites/", headers=headers, json={"series_id": series_id})
            time.sleep(0.1)
        
        # 4. Ajout des Avis (Reviews) - Utilise REVIEWS_URL
        print(f"  ⭐ Ajout de {num_reviews} avis...")
        for series_id in user_series[:num_reviews]:
            rating = random.randint(1, 5)
            
            if rating >= 4:
                comment = random.choice(COMMENTS_POS)
            elif rating == 3:
                comment = random.choice(COMMENTS_MIX)
            else:
                comment = random.choice(COMMENTS_NEG)

            review_payload = {
                "series_id": series_id,
                "rating": rating,
                "comment": comment
            }
            
            requests.post(f"{REVIEWS_URL}/reviews/", headers=headers, json=review_payload)
            time.sleep(0.1)

    print("\n🎉 Seeding terminé avec succès ! StreamVault local est prêt pour la démo.")

if __name__ == "__main__":
    run_seeder()