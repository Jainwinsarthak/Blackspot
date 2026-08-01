import {useState, useMemo} from 'react'; 
import './App.css'; 
import {Header} from './components/Layout/Header'; 
import {MapView} from './components/Map/MapView'; 
import {RiskSummaryPanel} from './components/Dashboard/RiskSummaryPanel'; 
import {SegmentDetailPanel} from './components/Dashboard/SegmentDetailPanel'; 
import {ConditionToggle} from './components/Simulator/ConditionToggle'; 
import {Loader} from './components/common/Loader'; 
import {useRiskData} from './hooks/useRiskData'; 
import {useConditionSimulator} from './hooks/useConditionSimulator'; 
import {useMapInteraction} from './hooks/useMapInteraction'; 
import {isDemo} from './utils/api';
import type {Segment} from './types';

export default function App(){
  const sim = useConditionSimulator();
  const data = useRiskData(sim.conditions);
  const map = useMapInteraction();
  
  const [about, setAbout] = useState(false);
  const [activeLayer, setActiveLayer] = useState<'risk'|'accidents'|'schools'|'hospitals'>('risk');
  const [timelineYear, setTimelineYear] = useState<number>(2026);
  const [simulatedOverrides, setSimulatedOverrides] = useState<Record<number, number>>({});

  const handleSimulate = (segmentId: number, newScore: number) => {
    setSimulatedOverrides(prev => ({...prev, [segmentId]: newScore}));
  };

  const activeSegments = useMemo(() => {
    return data.segments.map(s => {
      let risk = simulatedOverrides[s.segment_id] ?? s.risk_score ?? s.risk_score_base;
      // Apply deterministic timeline modifier if not current year
      if (timelineYear !== 2026) {
        const diff = 2026 - timelineYear;
        // Mock historical data: older years were generally riskier (less infrastructure)
        const modifier = 1 + (diff * 0.05) + ((s.segment_id % 10) / 100);
        risk = Math.min(100, Math.max(0, risk * modifier));
      }
      return {...s, risk_score: risk};
    });
  }, [data.segments, simulatedOverrides, timelineYear]);

  const selectedSegment = activeSegments.find(s => s.segment_id === map.selected?.segment_id) || null;

  return (
    <div className="app-shell">
      <Header onAbout={() => setAbout(true)}/>
      <main>
        <MapView 
          segments={activeSegments} 
          selected={selectedSegment} 
          onSelect={map.select}
          activeLayer={activeLayer}
        />
        <aside className="sidebar">
          {selectedSegment ? (
            <SegmentDetailPanel 
              segment={selectedSegment} 
              conditions={sim.conditions} 
              onBack={map.clear}
              onSimulate={handleSimulate}
            />
          ) : (
            <RiskSummaryPanel summary={data.summary} segments={activeSegments}/>
          )}
        </aside>
      </main>
      
      <ConditionToggle 
        conditions={sim.conditions} 
        setWeather={sim.setWeather} 
        toggleNight={sim.toggleNight} 
        toggleFestival={sim.toggleFestival} 
        additional={activeSegments.filter(s => (s.risk_score || 0) >= 80).length - (data.summary?.critical_count || 0)}
        activeLayer={activeLayer}
        setActiveLayer={setActiveLayer}
        timelineYear={timelineYear}
        setTimelineYear={setTimelineYear}
      />
      
      {data.loading && <Loader/>}
      
      <footer className="mode-indicator">
        {isDemo() ? '🟡 Demo Mode' : '🟢 Live'} · Delhi, India
      </footer>
      
      {about && (
        <div className="modal-backdrop" onClick={() => setAbout(false)}>
          <section className="about-modal" onClick={e => e.stopPropagation()}>
            <button onClick={() => setAbout(false)}>×</button>
            <h2>BlackSpot</h2>
            <p>Predicting where India’s next fatal road accident will happen — before it does.</p>
            <p>Risk scores combine road geometry, infrastructure, historical crash patterns and simulated conditions.</p>
          </section>
        </div>
      )}
    </div>
  );
}
