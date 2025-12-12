from mcp.server.fastmcp import FastMCP
import urllib.request
import json
import ssl

BASE_URL = "https://openlibrary.org"

# Désactiver la vérification SSL pour éviter les problèmes de certificat (à éviter en production)
ssl._create_default_https_context = ssl._create_unverified_context

# MCP server global
mcp = FastMCP("OpenLibrary Assistant")

def make_request(url):
    """Fait une requête HTTP avec urllib"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MCP-Server/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

@mcp.tool()
def search_books(query: str) -> list:
    """
    Search for books in OpenLibrary using a query string.
    
    Args:
        query: Search term (e.g., "python", "harry potter")
    
    Returns:
        List of books with title and author
    """
    try:
        # Encoder le query pour l'URL
        encoded_query = urllib.parse.quote(query)
        url = f"{BASE_URL}/search.json?q={encoded_query}"
        
        data = make_request(url)
        
        if "error" in data:
            return [data]
        
        books = data.get("docs", [])[:5]  # Limiter à 5 résultats
        
        result = []
        for b in books:
            result.append({
                "title": b.get("title", "Unknown"),
                "author": b.get("author_name", ["Unknown"])[0] if b.get("author_name") else "Unknown",
                "year": b.get("first_publish_year"),
                "work_id": b.get("key", "").replace("/works/", "")
            })
        
        return result if result else [{"message": "No books found"}]
        
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]

@mcp.tool()
def get_book_details(work_id: str) -> dict:
    """
    Get basic book details
    
    Args:
        work_id: Work ID (e.g., "OL2784125W")
    
    Returns:
        Book information
    """
    try:
        url = f"{BASE_URL}/works/{work_id}.json"
        data = make_request(url)
        
        if "error" in data:
            return data
        
        return {
            "title": data.get("title", "Unknown"),
            "description": data.get("description", "No description available"),
            "subjects": data.get("subjects", [])[:5],
            "first_publish_date": data.get("first_publish_date"),
            "work_id": work_id
        }
        
    except Exception as e:
        return {"error": f"Failed to get book details: {str(e)}"}

@mcp.tool()
def get_popular_python_books() -> list:
    """
    Get a list of popular Python programming books
    
    Returns:
        List of popular Python books
    """
    # Livres Python populaires avec leurs IDs OpenLibrary
    python_books = [
        {"title": "Learning Python", "author": "Mark Lutz", "work_id": "OL2784125W"},
        {"title": "Python Cookbook", "author": "Alex Martelli", "work_id": "OL14873289W"},
        {"title": "Fluent Python", "author": "Luciano Ramalho", "work_id": "OL19932156W"},
        {"title": "Think Python", "author": "Allen B. Downey", "work_id": "OL16976951W"},
        {"title": "Automate the Boring Stuff with Python", "author": "Al Sweigart", "work_id": "OL16876139W"}
    ]
    
    return python_books

@mcp.tool()
def get_book_recommendations(topic: str) -> list:
    """
    Get book recommendations by topic
    
    Args:
        topic: Topic of interest (python, ai, fiction, etc.)
    
    Returns:
        List of recommended books
    """
    topics = {
        "python": [
            {"title": "Learning Python", "author": "Mark Lutz", "level": "Beginner"},
            {"title": "Fluent Python", "author": "Luciano Ramalho", "level": "Advanced"},
            {"title": "Python Crash Course", "author": "Eric Matthes", "level": "Beginner"}
        ],
        "ai": [
            {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "level": "Intermediate"},
            {"title": "Hands-On Machine Learning", "author": "Aurélien Géron", "level": "Intermediate"}
        ],
        "fiction": [
            {"title": "1984", "author": "George Orwell", "genre": "Dystopian"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic"}
        ]
    }
    
    topic_lower = topic.lower()
    if topic_lower in topics:
        return topics[topic_lower]
    else:
        return [{"error": f"Topic '{topic}' not found. Available topics: {', '.join(topics.keys())}"}]

if __name__ == "__main__":
    print("📚 Serveur OpenLibrary MCP (version simplifiée)")
    print("📋 Outils disponibles:")
    print("   - search_books: Rechercher des livres")
    print("   - get_book_details: Obtenir les détails d'un livre")
    print("   - get_popular_python_books: Livres Python populaires")
    print("   - get_book_recommendations: Recommandations par sujet")
    print("\n🚀 Serveur démarré...")
    mcp.run(transport="stdio")