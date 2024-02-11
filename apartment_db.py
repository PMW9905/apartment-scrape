import aiosqlite

class Database:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path

    async def create_tables(self):
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

    async def add_complex(self, complex_name, complex_url):
        async with aiosqlite.connect(self.db_file_path) as db:
            await db.execute("INSERT INTO complexes (name, url) VALUES (?, ?)",(complex_name,complex_url))
            await db.commit()

    async def remove_complex(self, complex_name):
        async with aiosqlite.connect(self.db_file_path) as db:
            await db.execute(f"DELETE FROM complexes WHERE url = ?", (complex_name,))
            await db.commit()

    async def add_layout(self, layout_name, complex_name):
        async with aiosqlite.connect(self.db_file_path) as db:
            await db.execute("INSERT INTO layout (name, complex_name) VALUES (?, ?)",(layout_name, complex_name))
            await db.commit()

    async def remove_layout(self, layout_name, complex_name):
        async with aiosqlite.connect(self.db_file_path) as db:
            await db.execute(f"DELETE FROM layout WHERE name = ? AND complex_name = ?", (layout_name, complex_name))
            await db.commit()

    async def list_all_layouts(self):
        complex_layouts = {}
        query = '''
                SELECT name, complex_name
                FROM layouts
                '''
        async with aiosqlite.connect(self.db_file_path) as db:
            async with db.execute(query) as cursor:
                async for row in cursor:
                    if row['complex_name'] not in complex_layouts:
                        complex_layouts[row['complex_name']] = []
                    # Append the layout name to the list of layouts for this complex
                    complex_layouts[row['complex_name']].append(row['name'])

        return complex_layouts
    
    async def list_all_complex(self):
        complexs = {}
        query = '''
                SELECT name, url
                FROM complexes
                '''
        async with aiosqlite.connect(self.db_file_path) as db:
            async with db.execute(query) as cursor:
                async for row in cursor:
                    complexs[row['name']] = row['url']

        return complexs

            

