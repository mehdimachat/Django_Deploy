from fastmcp import FastMCP

# Créer une instance du serveur MCP
mcp = FastMCP(name="Calculator")

# 1. Addition
@mcp.tool()
def add(a: float, b: float) -> dict:
    """Additionne deux nombres"""
    result = a + b
    return {
        "operation": "addition",
        "expression": f"{a} + {b}",
        "result": result,
        "formatted": f"{a} + {b} = {result}"
    }

# 2. Soustraction
@mcp.tool()
def subtract(a: float, b: float) -> dict:
    """Soustrait deux nombres"""
    result = a - b
    return {
        "operation": "soustraction",
        "expression": f"{a} - {b}",
        "result": result,
        "formatted": f"{a} - {b} = {result}"
    }

# 3. Multiplication
@mcp.tool()
def multiply(a: float, b: float) -> dict:
    """Multiplie deux nombres"""
    result = a * b
    return {
        "operation": "multiplication",
        "expression": f"{a} × {b}",
        "result": result,
        "formatted": f"{a} × {b} = {result}"
    }

# 4. Division
@mcp.tool()
def divide(a: float, b: float) -> dict:
    """Divise deux nombres"""
    if b == 0:
        return {
            "operation": "division",
            "expression": f"{a} ÷ {b}",
            "result": "error",
            "error": "Division par zéro impossible",
            "formatted": f"{a} ÷ {b} = Erreur (division par zéro)"
        }
    
    result = a / b
    return {
        "operation": "division",
        "expression": f"{a} ÷ {b}",
        "result": result,
        "formatted": f"{a} ÷ {b} = {result:.4f}"
    }

# 5. Puissance
@mcp.tool()
def power(base: float, exponent: float) -> dict:
    """Calcule la puissance d'un nombre"""
    result = base ** exponent
    return {
        "operation": "puissance",
        "expression": f"{base}^{exponent}",
        "result": result,
        "formatted": f"{base}^{exponent} = {result}"
    }

# 6. Racine carrée
@mcp.tool()
def square_root(number: float) -> dict:
    """Calcule la racine carrée d'un nombre"""
    if number < 0:
        return {
            "operation": "racine carrée",
            "expression": f"√{number}",
            "result": "error",
            "error": "Nombre négatif, racine carrée non définie",
            "formatted": f"√{number} = Erreur (nombre négatif)"
        }
    
    result = number ** 0.5
    return {
        "operation": "racine carrée",
        "expression": f"√{number}",
        "result": result,
        "formatted": f"√{number} = {result:.4f}"
    }

# 7. Modulo (reste de division)
@mcp.tool()
def modulo(a: float, b: float) -> dict:
    """Calcule le reste de la division"""
    if b == 0:
        return {
            "operation": "modulo",
            "expression": f"{a} % {b}",
            "result": "error",
            "error": "Division par zéro impossible",
            "formatted": f"{a} % {b} = Erreur (division par zéro)"
        }
    
    result = a % b
    return {
        "operation": "modulo",
        "expression": f"{a} % {b}",
        "result": result,
        "formatted": f"{a} % {b} = {result}"
    }

# 8. Pourcentage
@mcp.tool()
def percentage(value: float, total: float) -> dict:
    """Calcule le pourcentage d'une valeur par rapport à un total"""
    if total == 0:
        return {
            "operation": "pourcentage",
            "expression": f"({value}/{total})×100",
            "result": "error",
            "error": "Total ne peut pas être zéro",
            "formatted": f"({value}/{total})×100 = Erreur (total zéro)"
        }
    
    result = (value / total) * 100
    return {
        "operation": "pourcentage",
        "expression": f"({value}/{total})×100",
        "result": result,
        "formatted": f"({value}/{total})×100 = {result:.2f}%"
    }

# 9. Factorielle
@mcp.tool()
def factorial(n: int) -> dict:
    """Calcule la factorielle d'un nombre entier"""
    if n < 0:
        return {
            "operation": "factorielle",
            "expression": f"{n}!",
            "result": "error",
            "error": "Factorielle non définie pour les nombres négatifs",
            "formatted": f"{n}! = Erreur (nombre négatif)"
        }
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return {
        "operation": "factorielle",
        "expression": f"{n}!",
        "result": result,
        "formatted": f"{n}! = {result}"
    }

# 10. Valeur absolue
@mcp.tool()
def absolute(number: float) -> dict:
    """Calcule la valeur absolue d'un nombre"""
    result = abs(number)
    return {
        "operation": "valeur absolue",
        "expression": f"|{number}|",
        "result": result,
        "formatted": f"|{number}| = {result}"
    }

# 11. Opération multiple (addition de plusieurs nombres)
@mcp.tool()
def sum_all(numbers: list[float]) -> dict:
    """Additionne plusieurs nombres"""
    if not numbers:
        return {
            "operation": "somme multiple",
            "expression": "somme([])",
            "result": 0,
            "formatted": "somme([]) = 0"
        }
    
    result = sum(numbers)
    expression = " + ".join(str(n) for n in numbers)
    return {
        "operation": "somme multiple",
        "expression": expression,
        "result": result,
        "count": len(numbers),
        "formatted": f"{expression} = {result}"
    }

# 12. Moyenne
@mcp.tool()
def average(numbers: list[float]) -> dict:
    """Calcule la moyenne de plusieurs nombres"""
    if not numbers:
        return {
            "operation": "moyenne",
            "expression": "moyenne([])",
            "result": 0,
            "formatted": "moyenne([]) = 0"
        }
    
    result = sum(numbers) / len(numbers)
    return {
        "operation": "moyenne",
        "expression": f"moyenne de {len(numbers)} nombres",
        "result": result,
        "count": len(numbers),
        "formatted": f"Moyenne = {result:.4f}"
    }

# 13. Maximum et minimum
@mcp.tool()
def max_min(numbers: list[float]) -> dict:
    """Trouve le maximum et le minimum d'une liste de nombres"""
    if not numbers:
        return {
            "operation": "max_min",
            "expression": "max_min([])",
            "result": "error",
            "error": "Liste vide",
            "formatted": "Erreur: liste vide"
        }
    
    max_val = max(numbers)
    min_val = min(numbers)
    
    return {
        "operation": "max_min",
        "expression": f"max_min({numbers})",
        "maximum": max_val,
        "minimum": min_val,
        "range": max_val - min_val,
        "formatted": f"Maximum = {max_val}, Minimum = {min_val}, Étendue = {max_val - min_val}"
    }

# 14. Arrondi
@mcp.tool()
def round_number(number: float, decimals: int = 0) -> dict:
    """Arrondit un nombre avec un nombre spécifique de décimales"""
    result = round(number, decimals)
    return {
        "operation": "arrondi",
        "expression": f"round({number}, {decimals})",
        "result": result,
        "formatted": f"round({number}, {decimals}) = {result}"
    }

# Point d'entrée principal
if __name__ == "__main__":
    print(f"🧮 Calculatrice MCP: {mcp.name}")
    print("📋 Opérations disponibles:")
    print("   1. add(a, b) - Addition")
    print("   2. subtract(a, b) - Soustraction")
    print("   3. multiply(a, b) - Multiplication")
    print("   4. divide(a, b) - Division")
    print("   5. power(base, exponent) - Puissance")
    print("   6. square_root(number) - Racine carrée")
    print("   7. modulo(a, b) - Modulo (reste)")
    print("   8. percentage(value, total) - Pourcentage")
    print("   9. factorial(n) - Factorielle")
    print("   10. absolute(number) - Valeur absolue")
    print("   11. sum_all(numbers) - Somme de plusieurs nombres")
    print("   12. average(numbers) - Moyenne")
    print("   13. max_min(numbers) - Maximum et minimum")
    print("   14. round_number(number, decimals) - Arrondi")
    print("\n🚀 Serveur prêt...")
    mcp.run(transport="stdio")