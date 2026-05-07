import {useEffect, useMemo, useState} from 'react';
import BackendStatus from './components/BackendStatus';
import TournamentDashboard from './components/TournamentDashboard';
import JsonEditor from './components/JsonEditor';
import PicksTable from './components/PicksTable';
import WeightAnalysisCard from './components/WeightAnalysisCard';
import {analyzeQazaqstan, health} from './api/client';
import type {TournamentResponse} from './types';

export default function App(){
  const [online,setOnline]=useState<boolean|null>(null);
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  const [oddsPatch,setOddsPatch]=useState<any>({});
  const [strengthPatch,setStrengthPatch]=useState<any>({});
  const [res,setRes]=useState<TournamentResponse|null>(null);
  const [weightFilter,setWeightFilter]=useState<string|undefined>(undefined);

  useEffect(()=>{health().then(()=>setOnline(true)).catch(()=>setOnline(false));},[]);

  async function onAnalyze(cfg:{weight?:string;onlyPositive:boolean;topN:number}){
    setLoading(true);setError(''); setWeightFilter(cfg.weight);
    try{
      const out=await analyzeQazaqstan();
      if(cfg.onlyPositive){out.global_recommended_picks=out.global_recommended_picks.filter(p=>p.edge>0);}
      out.global_recommended_picks=out.global_recommended_picks.slice(0,cfg.topN);
      setRes(out);
    }catch(e:any){setError(e.message)}
    setLoading(false);
  }

  const weights=useMemo(()=>{
    if(!res) return [] as [string, any][];
    const entries=Object.entries(res.weights);
    if(!weightFilter) return entries;
    return entries.filter(([w])=>w===weightFilter || w===`${weightFilter} kg` || w.replace(' kg','')===weightFilter);
  },[res,weightFilter]);

  const filteredPicks=useMemo(()=>{
    if(!res) return [];
    if(!weightFilter) return res.global_recommended_picks;
    return res.global_recommended_picks.filter(p=>p.weight===weightFilter || p.weight===`${weightFilter} kg` || p.weight.replace(' kg','')===weightFilter);
  },[res,weightFilter]);

  return <main className='max-w-7xl mx-auto p-6 space-y-4'>
    <h1 className='text-3xl font-bold'>Judo Value Analyzer</h1>
    <BackendStatus online={online}/>
    <TournamentDashboard onAnalyze={onAnalyze}/>
    <div className='grid md:grid-cols-2 gap-4'><JsonEditor title='Odds Editor' onApply={setOddsPatch}/><JsonEditor title='Strengths Editor' onApply={setStrengthPatch}/></div>
    <p className='text-xs text-slate-400'>Overrides currently local/experimental; backend endpoint /analyze/qazaqstan uses server files.</p>
    {loading && <div className='p-3 rounded bg-slate-800'>Loading analysis...</div>}
    {error && <div className='p-3 rounded bg-rose-900/40 text-rose-300'>{error}</div>}
    {res && <section className='space-y-4'>
      <div className='p-4 rounded-xl border border-slate-700 bg-slate-900'>
        <div className='font-semibold'>{res.competition_name}</div>
        <div>Weights analyzed: {Object.keys(res.weights).length}</div>
        <div>Total global recommended picks: {res.global_recommended_picks.length}</div>
        <div className='text-amber-300 text-sm'>Warnings total: {res.warnings.length}</div>
      </div>
      <div className='p-4 rounded-xl border border-slate-700 bg-slate-900'><h2 className='font-semibold mb-2'>Global recommended picks</h2>{filteredPicks.length===0?<p className='text-slate-300'>No value picks found. Add odds in qazaqstan_2026_odds.json and rerun the analysis.</p>:<PicksTable picks={filteredPicks}/>}</div>
      <div className='grid md:grid-cols-2 gap-4'>{weights.map(([w,d])=><WeightAnalysisCard key={w} weight={w} data={d}/>)}</div>
    </section>}
  </main>
}
