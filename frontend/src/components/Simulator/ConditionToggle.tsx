import {CloudFog, CloudRain, Moon, Sun, Layers, Play} from 'lucide-react';
import type {Condition} from '../../types';
import './ConditionToggle.css';

export function ConditionToggle({
  conditions, setWeather, toggleNight, additional,
  activeLayer, setActiveLayer, timelineYear, setTimelineYear
}: {
  conditions: Condition; setWeather: (v: Condition['weather']) => void; toggleNight: () => void; toggleFestival: () => void; additional: number;
  activeLayer: string; setActiveLayer: (l: 'risk'|'accidents'|'schools'|'hospitals') => void;
  timelineYear: number; setTimelineYear: (y: number) => void;
}) {
  return (
    <div className="toolbar-container">
      <section className="condition-bar">
        <div className="toolbar-group">
          <div className="dropdown">
            <button className="tool-btn"><Layers size={14}/> {activeLayer === 'risk' ? 'Risk Layers' : activeLayer.charAt(0).toUpperCase() + activeLayer.slice(1)}</button>
            <div className="dropdown-content">
              <button onClick={() => setActiveLayer('risk')} className={activeLayer==='risk'?'active':''}>Predicted Risk</button>
              <button onClick={() => setActiveLayer('accidents')} className={activeLayer==='accidents'?'active':''}>Historical Crashes</button>
              <button onClick={() => setActiveLayer('schools')} className={activeLayer==='schools'?'active':''}>School Zones</button>
              <button onClick={() => setActiveLayer('hospitals')} className={activeLayer==='hospitals'?'active':''}>Hospitals</button>
            </div>
          </div>
          <div className="dropdown">
            <button className="tool-btn"><Play size={14}/> {timelineYear}</button>
            <div className="dropdown-content">
              <button onClick={() => setTimelineYear(2026)} className={timelineYear===2026?'active':''}>2026 (Live)</button>
              <button onClick={() => setTimelineYear(2025)} className={timelineYear===2025?'active':''}>2025</button>
              <button onClick={() => setTimelineYear(2024)} className={timelineYear===2024?'active':''}>2024</button>
              <button onClick={() => setTimelineYear(2023)} className={timelineYear===2023?'active':''}>2023</button>
            </div>
          </div>
        </div>
        
        <div className="toolbar-divider" />

        <div className="toggles">
          <button className={conditions.weather === 'clear' ? 'active' : ''} onClick={() => setWeather('clear')}>
            <Sun size={14}/> Clear
          </button>
          <button className={conditions.weather === 'rain' ? 'active' : ''} onClick={() => setWeather('rain')}>
            <CloudRain size={14}/> Rain
          </button>
          <button className={conditions.weather === 'fog' ? 'active' : ''} onClick={() => setWeather('fog')}>
            <CloudFog size={14}/> Fog
          </button>
          <button className={conditions.time === 'night' ? 'active' : ''} onClick={toggleNight}>
            <Moon size={14}/> Night
          </button>
        </div>
      </section>

      {additional > 0 && (
        <div className="condition-warning">
          <span className="live-dot pulse"/>
          {additional} new critical segments detected in current conditions
        </div>
      )}
    </div>
  );
}
