from mcp.server.fastmcp import FastMCP
import os
import json

# Chemin absolu vers le fichier flights.json
FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")

# Création du serveur
mcp = FastMCP(name="Aéroport Info")

def load_flights():
    """Charge les données des vols depuis le fichier JSON"""
    try:
        with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("flights", [])
    except FileNotFoundError:
        print(f"Erreur: Fichier {FLIGHTS_PATH} non trouvé")
        return []
    except json.JSONDecodeError:
        print(f"Erreur: Fichier {FLIGHTS_PATH} n'est pas un JSON valide")
        return []

#
# RESSOURCE MCP (fichier JSON lisible par l'LLM)
#
@mcp.resource("flights://today")
def flights_resource():
    """
    Resource qui expose la liste des vols du jour.
    L'URL 'flights://today' sera visible par Copilot/Claude.
    """
    try:
        with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erreur lors du chargement des données: {str(e)}"

#
# OUTILS (TOOLS) MCP
#

# a. Recherche par numéro de vol
@mcp.tool()
def search_by_flight_number(flight_number: str) -> dict:
    """
    Recherche un vol par son numéro de vol
    
    Args:
        flight_number: Numéro de vol (ex: AF123, BA456)
    
    Returns:
        Dictionnaire avec les informations du vol
    """
    flights = load_flights()
    
    # Recherche insensible à la casse
    flight_number = flight_number.upper().strip()
    
    for flight in flights:
        if flight.get("flight_number", "").upper() == flight_number:
            return {
                "found": True,
                "flight": flight,
                "message": f"Vol {flight_number} trouvé"
            }
    
    return {
        "found": False,
        "message": f"Vol {flight_number} non trouvé",
        "available_flights": [f["flight_number"] for f in flights]
    }

# b. Filtrage par destination
@mcp.tool()
def filter_by_destination(destination: str) -> dict:
    """
    Filtre les vols par destination
    
    Args:
        destination: Ville de destination (ex: Paris, London)
    
    Returns:
        Liste des vols pour cette destination
    """
    flights = load_flights()
    
    destination = destination.title().strip()
    filtered_flights = []
    
    for flight in flights:
        if flight.get("destination", "").title() == destination:
            filtered_flights.append(flight)
    
    return {
        "destination": destination,
        "count": len(filtered_flights),
        "flights": filtered_flights,
        "message": f"{len(filtered_flights)} vol(s) trouvé(s) pour {destination}"
    }

# c. Filtrage par statut (TRAVAIL À FAIRE - complété)
@mcp.tool()
def filter_by_status(status: str) -> dict:
    """
    Filtre les vols par statut
    
    Args:
        status: Statut du vol (on time, delayed, boarding, scheduled, cancelled)
    
    Returns:
        Liste des vols avec ce statut
    """
    flights = load_flights()
    
    status = status.lower().strip()
    valid_statuses = ["on time", "delayed", "boarding", "scheduled", "cancelled"]
    
    if status not in valid_statuses:
        return {
            "error": f"Statut invalide. Statuts valides: {', '.join(valid_statuses)}",
            "valid_statuses": valid_statuses
        }
    
    filtered_flights = []
    
    for flight in flights:
        if flight.get("status", "").lower() == status:
            filtered_flights.append(flight)
    
    return {
        "status": status,
        "count": len(filtered_flights),
        "flights": filtered_flights,
        "message": f"{len(filtered_flights)} vol(s) avec statut '{status}'"
    }

# d. Outil libre basé sur votre propre logique métier (TRAVAIL À FAIRE - complété)
@mcp.tool()
def get_flights_by_time_range(start_time: str, end_time: str) -> dict:
    """
    Recherche les vols dans une plage horaire
    
    Args:
        start_time: Heure de début (format HH:MM, ex: 08:00)
        end_time: Heure de fin (format HH:MM, ex: 18:00)
    
    Returns:
        Liste des vols dans cette plage horaire
    """
    flights = load_flights()
    
    def time_to_minutes(time_str):
        """Convertit une heure HH:MM en minutes depuis minuit"""
        try:
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes
        except:
            return 0
    
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    
    if start_minutes > end_minutes:
        return {
            "error": "L'heure de début doit être avant l'heure de fin",
            "start_time": start_time,
            "end_time": end_time
        }
    
    filtered_flights = []
    
    for flight in flights:
        departure = flight.get("departure", "00:00")
        departure_minutes = time_to_minutes(departure)
        
        if start_minutes <= departure_minutes <= end_minutes:
            filtered_flights.append(flight)
    
    # Trier par heure de départ
    filtered_flights.sort(key=lambda x: time_to_minutes(x.get("departure", "00:00")))
    
    return {
        "time_range": f"{start_time} - {end_time}",
        "count": len(filtered_flights),
        "flights": filtered_flights,
        "message": f"{len(filtered_flights)} vol(s) au départ entre {start_time} et {end_time}"
    }

# e. Outil supplémentaire : statistiques des vols
@mcp.tool()
def get_flight_statistics() -> dict:
    """
    Fournit des statistiques sur les vols
    
    Returns:
        Statistiques des vols (par statut, par destination, etc.)
    """
    flights = load_flights()
    
    if not flights:
        return {"error": "Aucun vol disponible"}
    
    # Statistiques par statut
    status_stats = {}
    for flight in flights:
        status = flight.get("status", "unknown")
        status_stats[status] = status_stats.get(status, 0) + 1
    
    # Statistiques par destination
    destination_stats = {}
    for flight in flights:
        destination = flight.get("destination", "unknown")
        destination_stats[destination] = destination_stats.get(destination, 0) + 1
    
    # Statistiques par terminal
    terminal_stats = {}
    for flight in flights:
        terminal = flight.get("terminal", "unknown")
        terminal_stats[terminal] = terminal_stats.get(terminal, 0) + 1
    
    return {
        "total_flights": len(flights),
        "status_distribution": status_stats,
        "destination_distribution": destination_stats,
        "terminal_distribution": terminal_stats,
        "message": f"Statistiques sur {len(flights)} vol(s)"
    }

# Lancement du serveur
if __name__ == "__main__":
    print("✈️  Serveur d'information aérienne MCP")
    print(f"📁 Données chargées depuis: {FLIGHTS_PATH}")
    print("📋 Outils disponibles:")
    print("   - search_by_flight_number: Recherche par numéro de vol")
    print("   - filter_by_destination: Filtre par destination")
    print("   - filter_by_status: Filtre par statut")
    print("   - get_flights_by_time_range: Recherche par plage horaire")
    print("   - get_flight_statistics: Statistiques des vols")
    print("🔗 Ressource disponible: flights://today")
    print("\n🚀 Serveur démarré...")
    mcp.run(transport="stdio")