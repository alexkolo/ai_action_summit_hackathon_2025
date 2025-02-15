CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    num_social_sec TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    gender TEXT CHECK (gender IN ('M', 'F', 'NB'))
);

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);
