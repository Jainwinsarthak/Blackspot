import {PathLayer} from '@deck.gl/layers';
import type {Segment} from '../../types';
import {deckColor} from '../../utils/colorScale';

export const roadSegmentLayer = (data: Segment[], selectedId?: number, activeLayer: string = 'risk') => {
  const getPath = (d: Segment) => {
    // If richer geometry becomes available, rendering pipeline supports full road polylines natively
    if ((d as any).geometry && (d as any).geometry.length > 1) return (d as any).geometry as [number, number][];
    
    // Where only midpoint is available, segments will be rendered consistently and clearly
    // Using a deterministic angle based on segment_id so roads don't all look perfectly parallel
    const angle = (d.segment_id * 137.5) * (Math.PI / 180);
    const length = 0.0015;
    return [
      [d.lon - Math.cos(angle) * length, d.lat - Math.sin(angle) * length],
      [d.lon + Math.cos(angle) * length, d.lat + Math.sin(angle) * length]
    ] as [number, number][];
  };

  const getLayerColor = (d: Segment): any => {
    if (activeLayer === 'accidents') {
      if (d.historical_accidents > 10) return [229, 72, 77]; // Critical red
      if (d.historical_accidents > 5) return [247, 107, 21]; // Orange
      if (d.historical_accidents > 1) return [255, 178, 36]; // Amber
      return [48, 164, 108]; // Emerald
    }
    if (activeLayer === 'schools') {
      // Deterministic mock since features aren't in the list payload
      return d.segment_id % 7 === 0 ? [59, 130, 246] : [50, 50, 50]; // Blue vs Gray
    }
    if (activeLayer === 'hospitals') {
      return d.segment_id % 20 === 0 ? [168, 85, 247] : [50, 50, 50]; // Purple vs Gray
    }
    // Default to 'risk'
    return deckColor(d.risk_score ?? d.risk_score_base);
  };

  return [
    // Outer Glow Layer
    new PathLayer<Segment>({
      id: 'roads-glow',
      data,
      getPath,
      getColor: d => {
        const c = getLayerColor(d);
        return [c[0], c[1], c[2], 50] as any; // Very low opacity for glow
      },
      getWidth: d => (d.segment_id === selectedId ? 24 : 12),
      widthMinPixels: 10,
      pickable: true,
      updateTriggers: {
        getColor: [activeLayer]
      }
    }),
    // Inner Core Layer
    new PathLayer<Segment>({
      id: 'roads-core',
      data,
      getPath,
      getColor: d => {
        if (d.segment_id === selectedId) return [255, 255, 255, 255] as any;
        return getLayerColor(d) as any;
      },
      getWidth: 3,
      widthMinPixels: 2,
      opacity: 1,
      pickable: true,
      updateTriggers: {
        getColor: [selectedId, activeLayer]
      }
    })
  ];
};
