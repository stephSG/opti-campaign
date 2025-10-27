# Frontend (opti-campaign)

Quick notes to run the frontend locally and in CI.

Prerequisites
- Node.js 18+ (or compatible LTS)
- npm

Install dependencies
```bash
cd frontend
npm install
```

Run dev server
```bash
npm run dev
# open the URL printed by Vite (default http://localhost:5173)
```

Run tests (Vitest)
```bash
npm run test
```

Build
```bash
npm run build
```

Notes
- Icons are provided by `@heroicons/vue` and a small reusable `IconButton.vue` component.
- A reusable `ConfirmModal.vue` replaces native `confirm()` calls for better mobile UX.
- Tests mock the Pinia store where necessary. If you run tests and see failures related to environment, ensure Node/npm versions are compatible and `npm install` was run.

