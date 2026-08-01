import {useMemo,useState} from 'react'; 
import DeckGL from '@deck.gl/react'; 
import Map from 'react-map-gl/maplibre'; 
import 'maplibre-gl/dist/maplibre-gl.css'; 
import type {Segment} from '../../types'; 
import {DELHI_VIEW,MAP_STYLE} from '../../config/constants'; 
import {roadSegmentLayer} from './RoadSegmentLayer'; 
import {accidentMarkers} from './AccidentMarkers'; 
import './MapView.css';

export function MapView({segments, selected, onSelect, activeLayer}: {segments: Segment[]; selected: Segment | null; onSelect: (x: Segment) => void; activeLayer: string}) {
  const [hover, setHover] = useState<Segment | null>(null);

  const layers = useMemo(() => {
    return [
      ...roadSegmentLayer(segments, selected?.segment_id, activeLayer),
      accidentMarkers(segments)
    ];
  }, [segments, selected?.segment_id, activeLayer]);

  return (
    <div className="map-wrap">
      <DeckGL 
        initialViewState={DELHI_VIEW} 
        controller 
        layers={layers} 
        onClick={i => i.object && onSelect(i.object as Segment)} 
        onHover={i => setHover((i.object as Segment) || null)}
      >
        <Map mapStyle={MAP_STYLE}/>
      </DeckGL>

      {hover && (
        <div className="map-tooltip" style={{ left: hover ? '50%' : '-1000px', top: '24px', transform: 'translateX(-50%)' }}>
          <b>{hover.name}</b>
          <span>Risk {Math.round(hover.risk_score ?? hover.risk_score_base)} / 100</span>
        </div>
      )}
    </div>
  );
}
