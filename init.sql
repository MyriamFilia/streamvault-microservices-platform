-- Création des databases si elles n'existent pas
SELECT 'CREATE DATABASE userdb' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'userdb')\gexec
SELECT 'CREATE DATABASE reviewdb' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'reviewdb')\gexec
SELECT 'CREATE DATABASE favoritesdb' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'favoritesdb')\gexec