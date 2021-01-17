CREATE INDEX resource_uri FOR (n:Resource) ON (n.uri);

CREATE INDEX labels_polish FOR (n:Resource) ON (n.labels_polish);
CREATE INDEX labels_english FOR (n:Resource) ON (n.labels_english);
