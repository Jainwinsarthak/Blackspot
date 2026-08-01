export type Weather='clear'|'rain'|'fog'; export type DayTime='day'|'night'|'dawn'|'dusk';
export interface Condition { weather:Weather; time:DayTime; festival:boolean }
export interface Factor { feature:string; importance:number; value?:number }
export interface WhatIf { new_score:number; delta:number }
export interface Segment { segment_id:number; lat:number; lon:number; name:string; risk_score_base:number; risk_score?:number; risk_category:string; top_factors:Factor[]; what_if:Record<string,WhatIf>; historical_accidents:number; road_type:string; lane_count:number; risk_scores?:Record<string,number> }
export interface Summary {total_segments:number;critical_count:number;high_count:number;medium_count:number;low_count:number;total_accidents:number;top_city_factors:Factor[]}
export interface Detail {segment_id:number;name:string;road_type:string;risk_score:number;risk_category:string;features:Record<string,unknown>;shap_values:Factor[];historical_accidents:number;accidents:Array<Record<string,unknown>>;what_if_results:Record<string,WhatIf>}
