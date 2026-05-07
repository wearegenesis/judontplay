import {useEffect, useMemo, useState} from 'react';
import BackendStatus from './components/BackendStatus';
import TournamentDashboard from './components/TournamentDashboard';
import JsonEditor from './components/JsonEditor';
import PicksTable from './components/PicksTable';
import WeightAnalysisCard from './components/WeightAnalysisCard';
import {analyzeTournament, health} from './api/client';
import sample from './data/qazaqstanSample';
import type {TournamentResponse} from './types';

export default function App(){
  const [online,setOnline]=useState<boolean|null>(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  const [oddsPatch,setOddsPatch]=useState<any>({});
  const [strengthPatch,setStrengthPatch]=useState<any>({});
  const [res,setRes]=useState<TournamentResponse|null>(null);

  useEffect(()=>{health().then(()=>setOnline(true)).catch(()=>setOnline(false));},[]);

  async function onAnalyze(cfg:{weight?:string;onlyPositive:boolean;topN:number}){
    setLoading(true);setError('');
    try{
      const payload=JSON.parse(JSON.stringify(sample));
      payload.weights=payload.weights.filter((w:any)=>!cfg.weight || w.weight===cfg.weight);
      payload.weights=payload.weights.map((w:any)=>({
        ...w,
        odds_winner: oddsPatch[w.weight]?.odds_winner ?? w.odds_winner,
        odds_top4: oddsPatch[w.weight]?.odds_top4 ?? w.odds_top4,
        athlete_strengths: strengthPatch[w.weight] ?? w.athlete_strengths,
      }));
      const out=await analyzeTournament(payload);
      if(cfg.onlyPositive){out.global_recommended_picks=out.global_recommended_picks.filter(p=>p.edge>0);}
      out.global_recommended_picks=out.global_recommended_picks.slice(0,cfg.topN);
      setRes(out);
    }catch(e:any){setError(e.message)}
    setLoading(false);
  }

  const weights=useMemo(()=>res?Object.entries(res.weights):[],[res]);

  return <main className='max-w-7xl mx-auto p-6 space-y-4'>
    <h1 className='text-3xl font-bold'>Judo Value Analyzer</h1>
    <BackendStatus online={online}/>
    <TournamentDashboard onAnalyze={onAnalyze}/>
    <div className='grid md:grid-cols-2 gap-4'><JsonEditor title='Odds Editor' onApply={setOddsPatch}/><JsonEditor title='Strengths Editor' onApply={setStrengthPatch}/></div>
    {loading && <div className='p-3 rounded bg-slate-800'>Loading analysis...</div>}
    {error && <div className='p-3 rounded bg-rose-900/40 text-rose-300'>{error}</div>}
    {res && <section className='space-y-4'>
      <div className='p-4 rounded-xl border border-slate-700 bg-slate-900'>
        <div className='font-semibold'>{res.competition_name}</div>
        <div>Weights analyzed: {Object.keys(res.weights).length}</div>
        <div className='text-amber-300 text-sm'>Warnings: {res.warnings.length}</div>
      </div>
      <div className='p-4 rounded-xl border border-slate-700 bg-slate-900'><h2 className='font-semibold mb-2'>Global recommended picks</h2><PicksTable picks={res.global_recommended_picks}/></div>
      <div className='grid md:grid-cols-2 gap-4'>{weights.map(([w,d])=><WeightAnalysisCard key={w} weight={w} data={d}/>)}</div>
    </section>}
  </main>
}
