import {memo} from 'react';
import type {ReactNode} from 'react';
import './StatCard.css';

export const StatCard = memo(function StatCard({label, value, color, icon}: {label: string; value: string|number; color: string; icon: ReactNode}) {
  return (
    <article className="stat-card" style={{'--card-color': color} as React.CSSProperties}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <strong className="number">{value}</strong>
        <span>{label}</span>
      </div>
    </article>
  );
});
