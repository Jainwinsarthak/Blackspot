import {useState, memo} from 'react';
import {Zap} from 'lucide-react';
import type {Condition, Segment} from '../../types';
import {simulate} from '../../utils/api';
import './WhatIfPanel.css';

const options = [
  {id: 'add_signal', label: 'Traffic Signal', cost: 1500000},
  {id: 'add_median', label: 'Divider / Median', cost: 800000},
  {id: 'add_streetlight', label: 'Street Lighting', cost: 450000},
  {id: 'add_speed_breaker', label: 'Speed Breaker', cost: 75000},
  {id: 'add_crossing', label: 'Zebra Crossing', cost: 40000}
] as const;

export const WhatIfPanel = memo(function WhatIfPanel({segment, conditions, onScore}: {segment: Segment; conditions: Condition; onScore: (x: number) => void}) {
  const [chosen, setChosen] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{new_risk: number; delta_pct: number} | null>(null);

  const toggle = (id: string) => setChosen(a => a.includes(id) ? a.filter(x => x !== id) : [...a, id]);

  const run = async () => {
    setBusy(true);
    try {
      const x = await simulate(segment.segment_id, chosen, conditions);
      setResult(x);
      onScore(x.new_risk);
    } catch {
      const reduction = chosen.reduce((n, id) => n + Math.abs(segment.what_if[id]?.delta || 0), 0);
      const base = segment.risk_score ?? segment.risk_score_base;
      const score = Math.max(0, base - reduction);
      setResult({new_risk: score, delta_pct: ((score - base) / base) * 100});
      onScore(score);
    } finally {
      setBusy(false);
    }
  };

  const totalCost = chosen.reduce((acc, id) => acc + (options.find(o => o.id === id)?.cost || 0), 0);
  const livesSaved = result ? Math.abs(Math.round((result.delta_pct / 100) * segment.historical_accidents * 2.4)) : 0;

  return (
    <section className="whatif">
      <div className="whatif-header">
        <Zap size={14} className="accent-icon"/>
        <h3>Simulation Engine</h3>
      </div>
      
      <div className="intervention-list">
        {options.map((o) => (
          <label key={o.id} className={chosen.includes(o.id) ? 'selected' : ''}>
            <input type="checkbox" checked={chosen.includes(o.id)} onChange={() => toggle(o.id)}/>
            <span>{o.label}</span>
            <small>₹{(o.cost / 100000).toFixed(1)}L</small>
          </label>
        ))}
      </div>
      
      <button disabled={!chosen.length || busy} onClick={run} className={busy ? 'loading' : ''}>
        {busy ? <><span className="spinner"/> Computing tensor...</> : 'Run Simulation'}
      </button>

      {result && (
        <div className="outcome-grid fade-in">
          <div className="outcome-metric">
            <span>New Risk</span>
            <strong className="number">{Math.round(result.new_risk)}</strong>
          </div>
          <div className="outcome-metric">
            <span>Lives Saved</span>
            <strong className="number positive">+{livesSaved}</strong>
          </div>
          <div className="outcome-metric">
            <span>Capital Est.</span>
            <strong className="number">₹{(totalCost / 100000).toFixed(1)}L</strong>
          </div>
        </div>
      )}
    </section>
  );
});
