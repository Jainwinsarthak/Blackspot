import {memo} from 'react';
import {AlertTriangle,Car,HeartPulse,ShieldAlert} from 'lucide-react';
import type {Segment,Summary} from '../../types';
import {StatCard} from '../common/StatCard';
import {number} from '../../utils/formatters';
import './RiskSummaryPanel.css';

export const RiskSummaryPanel = memo(function RiskSummaryPanel({summary, segments}: {summary: Summary | null; segments: Segment[]}) {
  const critical = segments.filter(x => (x.risk_score ?? x.risk_score_base) >= 80).length;
  const high = segments.filter(x => {
    const v = x.risk_score ?? x.risk_score_base;
    return v >= 60 && v < 80;
  }).length;

  return (
    <section className="summary fade-in">
      <div className="summary-header">
        <p className="eyebrow">CITY INTELLIGENCE</p>
        <h1>Delhi Risk Pulse</h1>
      </div>
      <p className="muted">Live predictive analysis of geometry, crash history, and infrastructure combined with environmental telemetry.</p>
      
      <div className="stat-grid">
        <StatCard icon={<AlertTriangle size={15}/>} value={number(critical)} label="Critical Hotspots" color="var(--risk-critical)"/>
        <StatCard icon={<ShieldAlert size={15}/>} value={number(high)} label="High Risk Zones" color="var(--risk-high)"/>
        <StatCard icon={<Car size={15}/>} value={number(summary?.total_accidents || 0)} label="Analyzed Crashes" color="var(--text-primary)"/>
        <StatCard icon={<HeartPulse size={15}/>} value={number(Math.round(critical * 2.4))} label="Lives at Risk" color="var(--risk-critical)"/>
      </div>

      <div className="hint-card">
        <div className="hint-pulse"></div>
        <p>Select any road segment on the map to inspect AI risk factors and simulate infrastructure upgrades.</p>
      </div>
    </section>
  );
});
