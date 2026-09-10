DROP TABLE IF EXISTS occupancy_metrics;

CREATE TABLE IF NOT EXISTS occupancy_metrics (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    camera_id VARCHAR(255) NOT NULL,
    total_people INTEGER NOT NULL CHECK (total_people >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS occupancy_metrics_camera_timestamp_idx
    ON occupancy_metrics (camera_id, timestamp DESC);
