from src.config import Config
from src.database import database_connection
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.report import generate_report
import os

def run_pipeline():
    """Point d'entrée du pipeline ETL complet."""
    print("="*50)
    print("DEMARRAGE DU PIPELINE GAMETRACKER")
    print("="*50)
    
    # Construction des chemins absolus
    players_file = os.path.join(Config.DATA_DIR, 'Players.csv')
    scores_file = os.path.join(Config.DATA_DIR, 'Scores.csv')

    with database_connection() as conn:
        # --- PHASE 1 : JOUEURS ---
        print("\n--- Traitement des Joueurs ---")
        df_players = extract(players_file)
        df_players_clean = transform_players(df_players)
        load_players(df_players_clean, conn)
        
        # Récupération des IDs valides (Crucial pour l'intégrité référentielle)
        valid_player_ids = df_players_clean['player_id'].tolist()
        
        # --- PHASE 2 : SCORES ---
        print("\n--- Traitement des Scores ---")
        df_scores = extract(scores_file)
        # On passe la liste des IDs valides pour filtrer les orphelins
        df_scores_clean = transform_scores(df_scores, valid_player_ids)
        load_scores(df_scores_clean, conn)
        
    # --- PHASE 3 : RAPPORT ---
    print("\n--- Génération du Rapport ---")
    generate_report()
    
    print("\n" + "="*50)
    print("PIPELINE TERMINE AVEC SUCCES")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()