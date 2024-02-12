import aiosqlite

class Database:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path

    async def create_tables(self):
        try:
            async with aiosqlite.connect(self.db_file_path) as db:
                await db.execute("""CREATE TABLE IF NOT EXISTS complexes (
                                name TEXT NULL,
                                url TEXT UNIQUE NOT NULL,
                                PRIMARY KEY(name)
                                )""")
                await db.execute("""CREATE TABLE IF NOT EXISTS layouts (
                                name TEXT NOT NULL,
                                complex_name TEXT NOT NULL,
                                PRIMARY KEY(name, complex_name),
                                FOREIGN KEY(complex_name) REFERENCES complexes(name)
                                )""")
                await db.commit()
                return True
        except Exception as e:
            print(f'Failed to create tables: {e}')
            return False

    async def add_complex(self, complex_name, complex_url):
        try:
            async with aiosqlite.connect(self.db_file_path) as db:
                await db.execute("INSERT INTO complexes (name, url) VALUES (?, ?)", (complex_name, complex_url))
                await db.commit()
            return True
        except Exception as e:
            print(f"Failed to add complex: {e}")
            return False

    async def remove_complex(self, complex_name):
        try:
            async with aiosqlite.connect(self.db_file_path) as db:
                await db.execute("DELETE FROM complexes WHERE name = ?", (complex_name,))
                await db.commit()
            return True
        except Exception as e:
            print(f"Failed to remove complex: {e}")
            return False

    async def add_layout(self, layout_name, complex_name):
        try:
            async with aiosqlite.connect(self.db_file_path) as db:
                await db.execute("INSERT INTO layouts (name, complex_name) VALUES (?, ?)", (layout_name, complex_name))
                await db.commit()
            return True
        except Exception as e:
            print(f"Failed to add layout: {e}")
            return False

    async def remove_layout(self, layout_name, complex_name):
        try:
            async with aiosqlite.connect(self.db_file_path) as db:
                await db.execute("DELETE FROM layouts WHERE name = ? AND complex_name = ?", (layout_name, complex_name))
                await db.commit()
            return True
        except Exception as e:
            print(f"Failed to remove layout: {e}")
            return False

    async def list_all_layouts(self):
        try:
            complex_layouts = {}
            query = '''
                    SELECT name, complex_name
                    FROM layouts
                    '''
            async with aiosqlite.connect(self.db_file_path) as db:
                async with db.execute(query) as cursor:
                    async for row in cursor:
                        layout_name = row[0]
                        complex_name = row[1]
                        if complex_name not in complex_layouts:
                            complex_layouts[complex_name] = []
                        complex_layouts[complex_name].append(layout_name)
            return complex_layouts
        except Exception as e:
            print(f"Failed to list all layouts: {e}")
            return False

    async def list_all_complex(self):
        try:
            complexes = {}
            query = '''
                    SELECT name, url
                    FROM complexes
                    '''
            async with aiosqlite.connect(self.db_file_path) as db:
                async with db.execute(query) as cursor:
                    async for row in cursor:
                        name = row[0]
                        url = row[1]
                        complexes[name] = url
            return complexes
        except Exception as e:
            print(f"Failed to list all complexes: {e}")
            return False
        
    async def get_complex_url(self, complex_name):
        try:
            query = '''
                    SELECT name, url
                    FROM complexes
                    WHERE name = ?
                    '''
            async with aiosqlite.connect(self.db_file_path) as db:
                async with db.execute(query,(complex_name,)) as cursor:
                    async for row in cursor:
                        url = row[1]
                        return str(url)
        except Exception as e:
            print(f"Failed to retrieve complex url: {e}")
            return False
            

