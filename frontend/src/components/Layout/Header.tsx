import {Github, Settings, MapPin, Layers} from 'lucide-react';
import './Header.css';

export function Header({onAbout}: {onAbout: () => void}) {
  return (
    <header className="header-pill">
      <div className="brand">
        <span className="live-dot pulse"/>
        <b>BlackSpot</b>
      </div>
      
      <div className="header-divider" />
      
      <button className="header-btn city-locked">
        <MapPin size={14}/> Delhi
      </button>

      <div className="header-divider" />

      <nav className="header-nav">
        <button className="header-btn"><Layers size={14}/> Layers</button>
        <button className="header-btn" onClick={onAbout}><Settings size={14}/> Settings</button>
        <a href="https://github.com/blackspot/predictive-twin" target="_blank" rel="noreferrer" className="header-btn">
          <Github size={14}/> GitHub
        </a>
      </nav>
    </header>
  );
}
