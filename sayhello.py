from mcp.server.fastmcp import FastMCP

# Créer une instance du serveur MCP
mcp = FastMCP(name="say_hello_server")

# Définir un outil MCP
@mcp.tool()
def say_hello(name: str) -> str:
    """Retourne un message de bienvenue personnalisé"""
    return f"Hello {name}! 😊"

# Point d'entrée principal
if __name__ == "__main__":
    # Démarrer le serveur avec transport stdio
    mcp.run(transport="stdio")