CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  email TEXT,
  password TEXT,
  role TEXT,
  login_id TEXT UNIQUE,
  mobile TEXT,
  city TEXT,
  state TEXT,
  status TEXT,
  last_login_time TEXT,
  last_login_location TEXT
);

CREATE TABLE car_search_logs (
  id SERIAL PRIMARY KEY,
  emp_id TEXT NOT NULL,
  emp_name TEXT NOT NULL,
  chasis_no TEXT NOT NULL,
  searched_at TEXT NOT NULL,
  location TEXT NOT NULL,
  device_info TEXT NOT NULL,
  suspicious INTEGER DEFAULT 0
);
