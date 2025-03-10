-- Start by connecting to the default 'postgres' database
\c postgres;

-- Create the ragdb database if it doesn't exist
SELECT 'CREATE DATABASE ragdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ragdb')
\gexec

-- Connect to the ragdb database
\c ragdb;

-- Create schema if it doesnt exist
CREATE SCHEMA IF NOT EXISTS rag;
-- Set the search path
SET search_path TO rag;

-- Create or update ragdb_mgmt_user
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ragdb_mgmt_user') THEN
      CREATE USER ragdb_mgmt_user WITH PASSWORD 'd0ck3r' CREATEROLE;
ELSE
      ALTER USER ragdb_mgmt_user WITH PASSWORD 'd0ck3r' CREATEROLE;
END IF;
END
$do$;

-- Create or update chatbot_read_user
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'chatbot_read_user') THEN
      CREATE USER chatbot_read_user WITH PASSWORD 'd0ck3r' CREATEROLE;
ELSE
      ALTER USER chatbot_read_user WITH PASSWORD 'd0ck3r' CREATEROLE;
END IF;
END
$do$;

-- Create or update document_ingestion_write_user
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'document_ingestion_write_user') THEN
      CREATE USER document_ingestion_write_user WITH PASSWORD 'd0ck3r' NOINHERIT;
ELSE
      ALTER USER document_ingestion_write_user WITH PASSWORD 'd0ck3r' NOINHERIT;
END IF;
END
$do$;

GRANT USAGE, CREATE ON SCHEMA rag TO ragdb_mgmt_user;
ALTER ROLE ragdb_mgmt_user SET search_path = rag;

ALTER ROLE ragdb_mgmt_user WITH CREATEDB;
ALTER ROLE ragdb_mgmt_user WITH CREATEROLE;
GRANT pg_read_all_stats TO ragdb_mgmt_user;

ALTER DATABASE ragdb OWNER TO ragdb_mgmt_user;

-- Grant necessary permissions to the user for document importing, document_ingestion_write_user
GRANT USAGE ON SCHEMA rag TO document_ingestion_write_user;
ALTER ROLE document_ingestion_write_user SET search_path = rag;
-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA rag GRANT SELECT ON TABLES TO document_ingestion_write_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA rag GRANT INSERT ON TABLES TO document_ingestion_write_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA rag GRANT UPDATE ON TABLES TO document_ingestion_write_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA rag GRANT DELETE ON TABLES TO document_ingestion_write_user;
GRANT ALL ON SCHEMA rag TO document_ingestion_write_user;

-- Grant necessary permissions to the user for interacting only with the API-side of the DB
GRANT USAGE ON SCHEMA rag TO chatbot_read_user;
ALTER ROLE chatbot_read_user SET search_path = rag;
-- Set default privileges for future tables
GRANT SELECT ON ALL TABLES IN SCHEMA rag TO chatbot_read_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA rag GRANT SELECT ON TABLES TO chatbot_read_user;

-- Create the extension
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA rag;

ALTER DATABASE ragdb SET search_path TO rag;
