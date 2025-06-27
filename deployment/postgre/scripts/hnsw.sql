\c ragdb ragdb_mgmt_user;

-- Create HNSW index
SET maintenance_work_mem = '12GB';
CREATE INDEX ON rag.text_segments USING hnsw (embedding vector_cosine_ops);


