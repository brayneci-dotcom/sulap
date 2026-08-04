# /frontend Plan — Rebrand BSS PDF → SULAP
## Surgical changes (branding only, no UX redesign)
- [ ] `frontend/src/app/layout.tsx`: title → "SULAP — Solusi Unggul, Lengkap, Aman untuk PDF", description update
- [ ] `frontend/src/app/page.tsx`: subtitle → "SULAP — Solusi Unggul, Lengkap, Aman untuk PDF", img alt update
- [ ] `frontend/src/app/dashboard/page.tsx`: sidebar "BSS PDF" → "SULAP", "Toolkit v1.0" → "SULAP v1.0"
- [ ] `backend/config.py`: app_name update
- [ ] `backend/auth/oauth.py`: dev@cloudpdf.local → dev@sulap.local
- [ ] Rebuild + sync static
