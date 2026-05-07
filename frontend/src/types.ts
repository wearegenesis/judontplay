export type BracketMatch = [string | null, string | null];
export type WeightState = {weight:string;gender:string;bracket:Record<string,BracketMatch[]>;odds_winner:Record<string,number>;odds_top4:Record<string,number>;athlete_strengths:Record<string,any>};
export type TournamentState = {competition_name:string;weights:WeightState[]};
export type Pick = {weight:string;gender?:string|null;market:string;athlete:string;odds:number;fair_probability:number;implied_probability:number;edge:number};
export type AnalyzeResponse = {winner_ranking:{athlete:string;prob:number}[];top4_ranking:{athlete:string;prob:number}[];value_winner:Pick[];value_top4:Pick[];recommended_picks:Pick[];warnings:string[]};
export type TournamentResponse = {competition_name:string;weights:Record<string,AnalyzeResponse>;global_recommended_picks:Pick[];warnings:string[]};
