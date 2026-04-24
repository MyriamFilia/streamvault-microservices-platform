import requests
import random
import time

# L'URL de ton API Gateway Istio
BASE_URL = "http://127.0.0.1"

# Des vrais IDs de séries populaires sur TVMaze
SERIES_IDS = [
    169,  # Breaking Bad
    82,   # Game of Thrones
    2993, # Stranger Things
    526,  # The Office
    17861,# Dark
    108,  # Peaky Blinders
    431,  # Friends
    426,  # Black Mirror
    143,  # Silicon Valley
    73,   # The Walking Dead
]

# Nos 5 utilisateurs de simulation
USERS = [
    {"username": "Alice_Cinephile", "email": "alice@streamvault.com", "password": "password123"},
    {"username": "Bob_BingeWatcher", "email": "bob@streamvault.com", "password": "password123"},
    {"username": "Charlie_Critic", "email": "charlie@streamvault.com", "password": "password123"},
    {"username": "Diana_SciFi", "email": "diana@streamvault.com", "password": "password123"},
    {"username": "Ethan_Casual", "email": "ethan@streamvault.com", "password": "password123"},
]

# Banques de commentaires pour plus de réalisme
COMMENTS_POS = ["Masterpiece! A must watch.", "Absolutely loved it.", "Best show ever.", "Great acting and incredible plot.", "Highly recommended! 10/10."]
COMMENTS_MIX = ["It was okay.", "A bit slow in the middle seasons.", "Good, but clearly overrated.", "Started great, bad ending."]
COMMENTS_NEG = ["Not my cup of tea at all.", "Boring.", "I couldn't finish the first season, too slow."]

def run_seeder():
    print("🚀 Début du Seeding de StreamVault...")
    
    for user in USERS:
        print(f"\n👤 Traitement de l'utilisateur : {user['username']}")
        
        # 1. Inscription (Register)
        # On ignore l'erreur si l'utilisateur existe déjà
        requests.post(f"{BASE_URL}/users/register", json=user)
        
        # 2. Connexion (Login)
        res_login = requests.post(f"{BASE_URL}/users/login", json={"username": user["username"], "password": user["password"]})
        
        if res_login.status_code != 200:
            print(f"  ❌ Échec de la connexion pour {user['username']}. On passe au suivant.")
            continue
            
        token = res_login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("  ✅ Connecté avec succès.")

        # Chaque utilisateur aura un nombre différent de favoris et de reviews
        num_favorites = random.randint(2, 6)
        num_reviews = random.randint(2, 5)
        
        # On sélectionne des séries au hasard pour cet utilisateur
        user_series = random.sample(SERIES_IDS, max(num_favorites, num_reviews))

        # 3. Ajout des Favoris
        print(f"  ❤️ Ajout de {num_favorites} favoris...")
        for series_id in user_series[:num_favorites]:
            requests.post(f"{BASE_URL}/favorites/", headers=headers, json={"series_id": series_id})
            time.sleep(0.1) # Petite pause pour soulager le routeur Istio
        
        # 4. Ajout des Avis (Reviews)
        print(f"  ⭐ Ajout de {num_reviews} avis...")
        for series_id in user_series[:num_reviews]:
            rating = random.randint(1, 5)
            
            # Attribuer un commentaire logique selon la note
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
            
            requests.post(f"{BASE_URL}/reviews/", headers=headers, json=review_payload)
            time.sleep(0.1)

    print("\n🎉 Seeding terminé avec succès ! StreamVault est prêt pour la démo.")

if __name__ == "__main__":
    run_seeder()