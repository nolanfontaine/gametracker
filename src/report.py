from src.database import database_connection
from datetime import datetime

def generate_report():
    """Génère un rapport de synthèse formaté avec sauts de ligne."""
    output_file = "/app/output/rapport.txt"
    
    print(f"[REPORT] Génération du rapport dans {output_file}...")
    
    with database_connection() as conn:
        cursor = conn.cursor()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # --- EN-TÊTE ---
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            f.write("=" * 52 + "\n")
            f.write("GAMETRACKER - Rapport de synthese\n")
            f.write(f"Genere le : {now}\n")
            f.write("=" * 52 + "\n")
            
            # --- 1. STATISTIQUES GENERALES ---
            cursor.execute("SELECT COUNT(*) FROM players")
            nb_players = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM scores")
            nb_scores = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT game) FROM scores")
            nb_games = cursor.fetchone()[0]
            
            f.write("\n")
            f.write("--- Statistiques generales ---\n")
            f.write(f"Nombre de joueurs : {nb_players}\n")
            f.write(f"Nombre de scores : {nb_scores}\n")
            f.write(f"Nombre de jeux : {nb_games}\n")
            
            # --- 2. TOP 5 ---
            f.write("\n") # <--- SAUT DE LIGNE AJOUTÉ
            f.write("--- Top 5 des meilleurs scores ---\n")
            query_top5 = """
                SELECT p.username, s.game, s.score 
                FROM scores s
                JOIN players p ON s.player_id = p.player_id
                ORDER BY s.score DESC 
                LIMIT 5
            """
            cursor.execute(query_top5)
            for i, (user, game, score) in enumerate(cursor.fetchall(), 1):
                f.write(f"{i}. {user} | {game} | {score}\n")
            
            # --- 3. MOYENNES ---
            f.write("\n") # <--- SAUT DE LIGNE AJOUTÉ
            f.write("--- Score moyen par jeu ---\n")
            cursor.execute("SELECT game, AVG(score) FROM scores GROUP BY game")
            for game, avg in cursor.fetchall():
                f.write(f"{game} : {avg:.1f}\n")
            
            # --- 4. PAYS ---
            f.write("\n") # <--- SAUT DE LIGNE AJOUTÉ
            f.write("--- Joueurs par pays ---\n")
            cursor.execute("SELECT country, COUNT(*) FROM players GROUP BY country")
            for country, count in cursor.fetchall():
                f.write(f"{country or 'Inconnu'} : {count}\n")

            # --- 5. PLATEFORMES ---
            f.write("\n") # <--- SAUT DE LIGNE AJOUTÉ
            f.write("--- Sessions par plateforme ---\n")
            cursor.execute("SELECT platform, COUNT(*) FROM scores GROUP BY platform")
            for platform, count in cursor.fetchall():
                f.write(f"{platform or 'Inconnu'} : {count}\n")
                
            f.write("\n" + "=" * 52 + "\n")

    print("[REPORT] Rapport généré avec succès.")