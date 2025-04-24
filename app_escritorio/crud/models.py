from .database import Database

class OfertaEmpleo:
    def __init__(self):
        self.db = Database()

    def crear(self, titulo, empresa, ubicacion, tipo_trabajo, salario, habilidades, url):
        query = """
        INSERT INTO ofertas_empleo (titulo, empresa, ubicacion, tipo_trabajo, salario, url)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        params = (titulo, empresa, ubicacion, tipo_trabajo, salario, url)
        if self.db.execute_query(query, params):
            oferta_id = self.db.fetch_one("SELECT id FROM ofertas_empleo WHERE titulo = %s", (titulo,))[0]
            # Insertar habilidades
            for habilidad in habilidades:
                self.db.execute_query(
                    "INSERT INTO oferta_habilidades (oferta_id, habilidad_id) VALUES (%s, %s)",
                    (oferta_id, habilidad)
                )
            return oferta_id
        return None

    def obtener_todas(self):
        query = """
        SELECT o.id, o.titulo, o.empresa, o.ubicacion, o.tipo_trabajo, o.salario, o.url,
               array_agg(h.nombre) as habilidades
        FROM ofertas_empleo o
        LEFT JOIN oferta_habilidades oh ON o.id = oh.oferta_id
        LEFT JOIN habilidades h ON oh.habilidad_id = h.id
        GROUP BY o.id
        """
        return self.db.fetch_all(query)

    def actualizar(self, id, titulo, empresa, ubicacion, tipo_trabajo, salario, habilidades, url):
        query = """
        UPDATE ofertas_empleo
        SET titulo = %s, empresa = %s, ubicacion = %s, tipo_trabajo = %s, salario = %s, url = %s
        WHERE id = %s
        """
        params = (titulo, empresa, ubicacion, tipo_trabajo, salario, url, id)
        if self.db.execute_query(query, params):
            # Actualizar habilidades
            self.db.execute_query("DELETE FROM oferta_habilidades WHERE oferta_id = %s", (id,))
            for habilidad in habilidades:
                self.db.execute_query(
                    "INSERT INTO oferta_habilidades (oferta_id, habilidad_id) VALUES (%s, %s)",
                    (id, habilidad)
                )
            return True
        return False

    def eliminar(self, id):
        query = "DELETE FROM ofertas_empleo WHERE id = %s"
        return self.db.execute_query(query, (id,))

class Habilidad:
    def __init__(self):
        self.db = Database()

    def crear(self, nombre, descripcion):
        query = "INSERT INTO habilidades (nombre, descripcion) VALUES (%s, %s) RETURNING id"
        params = (nombre, descripcion)
        if self.db.execute_query(query, params):
            return self.db.fetch_one("SELECT id FROM habilidades WHERE nombre = %s", (nombre,))[0]
        return None

    def obtener_todas(self):
        query = "SELECT id, nombre, descripcion FROM habilidades"
        return self.db.fetch_all(query)

    def actualizar(self, id, nombre, descripcion):
        query = "UPDATE habilidades SET nombre = %s, descripcion = %s WHERE id = %s"
        params = (nombre, descripcion, id)
        return self.db.execute_query(query, params)

    def eliminar(self, id):
        query = "DELETE FROM habilidades WHERE id = %s"
        return self.db.execute_query(query, (id,))

class Usuario:
    def __init__(self):
        self.db = Database()

    def crear(self, username, email, password, rol):
        query = """
        INSERT INTO usuarios (username, email, password, rol)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        params = (username, email, password, rol)
        if self.db.execute_query(query, params):
            return self.db.fetch_one("SELECT id FROM usuarios WHERE username = %s", (username,))[0]
        return None

    def obtener_todos(self):
        query = "SELECT id, username, email, rol FROM usuarios"
        return self.db.fetch_all(query)

    def actualizar(self, id, username, email, password, rol):
        query = """
        UPDATE usuarios
        SET username = %s, email = %s, password = %s, rol = %s
        WHERE id = %s
        """
        params = (username, email, password, rol, id)
        return self.db.execute_query(query, params)

    def eliminar(self, id):
        query = "DELETE FROM usuarios WHERE id = %s"
        return self.db.execute_query(query, (id,)) 