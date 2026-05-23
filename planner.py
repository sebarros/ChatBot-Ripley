import re

class Planner:

    def create_plan(self, query: str):

        q = query.lower()

        if re.search(r"clima|tiempo|temperatura|weather", q):
            return {"tool": "weather"}

        if re.search(r"ropa|polera|jean|zapatilla|chaqueta|parka", q):
            return {"tool": "search_product"}

        if re.search(r"catálogo|catalogo|lista|productos", q):
            return {"tool": "list_products"}

        return {"tool": None}