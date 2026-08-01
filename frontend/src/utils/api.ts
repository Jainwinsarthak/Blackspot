import fallback from '../data/predictions.json'; import type {Condition,Detail,Segment,Summary} from '../types'; import {riskCategory} from './colorScale';
const API_BASE=import.meta.env.VITE_API_URL||'http://127.0.0.1:8000';
let demo=false; export const isDemo=()=>demo;
const conditionDelta=(c:Condition)=>(c.weather==='rain'?13:c.weather==='fog'?18:0)+(c.time!=='day'?12:0)+(c.festival?11:0);
export async function fetchSegments(conditions:Condition):Promise<Segment[]>{try{const r=await fetch(`${API_BASE}/api/risk/batch`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({conditions})});if(!r.ok)throw Error();demo=false;return r.json()}catch{demo=true;return fallback.segments.map(s=>{const risk_score=Math.min(100,s.risk_score_base+conditionDelta(conditions));return {...s,risk_score,risk_category:riskCategory(risk_score)} as Segment})}}
export async function fetchSummary():Promise<Summary>{try{const r=await fetch(`${API_BASE}/api/summary`);if(!r.ok)throw Error();return r.json()}catch{return fallback.summary as Summary}}
export async function fetchDetail(id:number):Promise<Detail>{const r=await fetch(`${API_BASE}/api/segments/${id}`);if(!r.ok)throw Error();return r.json()}
export async function simulate(id:number,interventions:string[],conditions:Condition){const r=await fetch(`${API_BASE}/api/simulate/whatif`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({segment_id:id,interventions,conditions})});if(!r.ok)throw Error();return r.json()}
