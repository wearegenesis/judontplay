import type { TournamentResponse } from '../types';
const API=import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export async function health(){const r=await fetch(`${API}/health`);if(!r.ok)throw new Error('health failed');return r.json();}
export async function analyzeTournament(payload:unknown):Promise<TournamentResponse>{const r=await fetch(`${API}/analyze/tournament`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!r.ok)throw new Error(await r.text());return r.json();}
export async function analyzeQazaqstan():Promise<TournamentResponse>{const r=await fetch(`${API}/analyze/qazaqstan`,{method:'POST'});if(!r.ok)throw new Error(await r.text());return r.json();}
