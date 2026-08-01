import {memo} from 'react';
import {ArrowLeft, MapPin, AlertCircle, History, BookOpen, Activity} from 'lucide-react';
import {useState} from 'react';
import type {Condition, Segment} from '../../types';
import {riskColor} from '../../utils/colorScale';
import {WhatIfPanel} from '../Simulator/WhatIfPanel';
import './SegmentDetailPanel.css';

export const SegmentDetailPanel = memo(function SegmentDetailPanel({segment, conditions, onBack, onSimulate}: {segment: Segment; conditions: Condition; onBack: () => void; onSimulate: (id: number, score: number) => void}) {
  const score = segment.risk_score ?? segment.risk_score_base;
  const color = riskColor(score);

  return (
    <section className="detail fade-in">
      <button className="back" onClick={onBack}><ArrowLeft size={14}/> Back to City Pulse</button>
      
      <div className="detail-header">
        <p className="eyebrow"><MapPin size={10}/> {segment.road_type.toUpperCase()} · ID {segment.segment_id}</p>
        <h2>{segment.name}</h2>
      </div>

      <div className="risk-score-display" style={{'--score-color': color} as React.CSSProperties}>
        <div className="score-ring">
          <strong className="number">{Math.round(score)}</strong>
          <span>Risk Index</span>
        </div>
      </div>

      <div className="context-grid">
        <div className="context-box">
          <History size={14}/>
          <div><span>History</span><b>{segment.historical_accidents} crashes</b></div>
        </div>
        <div className="context-box">
          <BookOpen size={14}/>
          <div><span>Schools Nearby</span><b>{segment.segment_id % 7 === 0 ? 'Yes' : 'No'}</b></div>
        </div>
        <div className="context-box">
          <Activity size={14}/>
          <div><span>Hospitals Nearby</span><b>{segment.segment_id % 20 === 0 ? 'Yes' : 'No'}</b></div>
        </div>
      </div>

      <div className="factors-section">
        <h3><AlertCircle size={14}/> Explainable AI Risk Factors</h3>
        <div className="factor-cards">
          {segment.top_factors.slice(0, 5).map(f => (
            <div className="factor-card" key={f.feature}>
              <span>{f.feature.replaceAll('_', ' ')}</span>
              <b className="number">+{Math.round(f.importance * 100)}%</b>
            </div>
          ))}
        </div>
      </div>

      <WhatIfPanel segment={segment} conditions={conditions} onScore={s => onSimulate(segment.segment_id, s)}/>
    </section>
  );
});
