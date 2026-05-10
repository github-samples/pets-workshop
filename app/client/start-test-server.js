// Cross-platform script to seed the test database and start the Flask server
import { execSync, spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const serverDir = path.resolve(__dirname, '..', 'server');
const testDbPath = path.join(serverDir, 'e2e_test_dogshelter.db');
const python = process.env.PYTHON || (process.platform === 'win32' ? 'py' : 'python3');
const flaskPort = process.env.FLASK_PORT || '5100';

// Seed the test database
execSync(`${python} utils/seed_test_database.py`, {
  cwd: serverDir,
  stdio: 'inherit',
});

// Start Flask with the test database
const server = spawn(python, ['app.py'], {
  cwd: serverDir,
  env: { ...process.env, DATABASE_PATH: testDbPath, FLASK_PORT: flaskPort },
  stdio: 'inherit',
});

server.on('close', (code) => process.exit(code ?? 1));
