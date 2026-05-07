import {useEffect, useMemo, useRef, useState} from 'react';
import BackendStatus from './components/BackendStatus';
import PicksTable from './components/PicksTable';
import {analyzeCustomTournament, analyzeQazaqstan, getQazaqstanState, health} from './api/client';
import type {TournamentResponse, TournamentState, WeightState} from './types';

const weightLabel=(w:WeightState)=>`${w.weight} ${w.gender}`;

export default function App(){
  const [online,setOnline]=useState<boolean|null>(null);
  const [state,setState]=useState<TournamentState|null>(null);
  const [result,setResult]=useState<TournamentResponse|null>(null);
  const [selectedWeight,setSelectedWeight]=useState<string>('');
  const [loading,setLoading]=useState(false);
  const [error,setError]=useState('');
  const [market,setMarket]=useState('all'); const [sex,setSex]=useState('all'); const [weightFilter,setWeightFilter]=useState('all'); const [minEdge,setMinEdge]=useState(0);
  const editorRef=useRef<HTMLDivElement>(null);

  useEffect(()=>{health().then(()=>setOnline(true)).catch(()=>setOnline(false)); getQazaqstanState().then(s=>{setState(s);setSelectedWeight(s.weights[0]?.weight||'');}).catch(e=>setError(String(e)));},[]);

  const current = state?.weights.find(w=>w.weight===selectedWeight);
  const athletes=useMemo(()=>{if(!current)return []; const set=new Set<string>(); Object.values(current.bracket).forEach(m=>m.forEach(([a,b])=>{if(a)set.add(a);if(b)set.add(b);})); return Array.from(set);},[current]);

  function updateCurrent(mut:(w:WeightState)=>void){if(!state||!current)return;const copy=structuredClone(state);const w=copy.weights.find(x=>x.weight===selectedWeight)!;mut(w);setState(copy)}

  async function analyzeOriginal(){setLoading(true);setError(''); try{setResult(await analyzeQazaqstan())}catch(e:any){setError(e.message)} setLoading(false)}
  async function analyzeEdited(){if(!state)return;setLoading(true);setError(''); try{setResult(await analyzeCustomTournament(state))}catch(e:any){setError(e.message)} setLoading(false)}

  const filteredPicks=useMemo(()=>{if(!result)return [];return result.global_recommended_picks.filter(p=>(market==='all'||p.market===market)&&(sex==='all'||p.gender===sex)&&(weightFilter==='all'||p.weight===weightFilter)&&p.edge>=minEdge)},[result,market,sex,weightFilter,minEdge]);

  return <main className='max-w-7xl mx-auto p-6 space-y-4'>
    <h1 className='text-3xl font-bold'>Judo Value Analyzer</h1><BackendStatus online={online}/>
    <div className='flex gap-2'><button className='px-4 py-2 bg-indigo-700 rounded' onClick={analyzeOriginal}>Analyze Qazaqstan original</button><button className='px-4 py-2 bg-emerald-700 rounded' onClick={analyzeEdited}>Analyze edited tournament</button></div>
    <div ref={editorRef} className='p-4 rounded-xl border border-slate-700 bg-slate-900 space-y-3'>
      <h2 className='text-xl font-semibold'>Tournament Editor</h2>
      <div className='flex flex-wrap gap-2'>{state?.weights.map(w=><button key={w.weight} className={`px-2 py-1 rounded ${selectedWeight===w.weight?'bg-indigo-700':'bg-slate-800'}`} onClick={()=>setSelectedWeight(w.weight)}>{weightLabel(w)}</button>)}</div>
      {current && <>
        <h3 className='font-semibold'>Bracket Editor - {current.weight} {current.gender}</h3>
        {(['A','B','C','D'] as const).map(pool=><div key={pool} className='border border-slate-700 rounded p-2'><div className='font-medium mb-2'>Pool {pool}</div>{current.bracket[pool].map((m,idx)=><div key={idx} className='flex gap-2 mb-1'><input className='bg-slate-950 p-1 rounded flex-1' value={m[0]??''} onChange={e=>updateCurrent(w=>w.bracket[pool][idx][0]=e.target.value||null)}/><input className='bg-slate-950 p-1 rounded flex-1' value={m[1]??''} placeholder='bye/null' onChange={e=>updateCurrent(w=>w.bracket[pool][idx][1]=e.target.value||null)}/><button className='px-2 bg-rose-800 rounded' onClick={()=>updateCurrent(w=>w.bracket[pool].splice(idx,1))}>x</button></div>)}<button className='px-2 py-1 bg-slate-700 rounded' onClick={()=>updateCurrent(w=>w.bracket[pool].push([null,null]))}>+ Add row</button></div>)}
        <h3 className='font-semibold mt-2'>Odds Winner Editor</h3>{athletes.length===0?<p>No athletes</p>:<table className='w-full text-sm'>{athletes.map(a=><tr key={a}><td>{a}</td><td><input className='bg-slate-950 p-1 rounded w-32' value={current.odds_winner[a]??''} onChange={e=>updateCurrent(w=>{const v=e.target.value.trim(); if(!v) delete w.odds_winner[a]; else w.odds_winner[a]=Number(v);})}/></td></tr>)}</table>}
        <h3 className='font-semibold mt-2'>Odds Top4 Editor</h3>{athletes.length===0?<p>No athletes</p>:<table className='w-full text-sm'>{athletes.map(a=><tr key={a}><td>{a}</td><td><input className='bg-slate-950 p-1 rounded w-32' value={current.odds_top4[a]??''} onChange={e=>updateCurrent(w=>{const v=e.target.value.trim(); if(!v) delete w.odds_top4[a]; else w.odds_top4[a]=Number(v);})}/></td></tr>)}</table>}
      </>}
    </div>

    {loading&&<div>Loading...</div>}{error&&<div className='text-rose-300'>{error}</div>}
    {result&&<section className='space-y-3'><div className='p-3 rounded bg-slate-900 border border-slate-700'>Weights analyzed: {Object.keys(result.weights).length}<br/>Total global recommended picks: {result.global_recommended_picks.length}<br/>Warnings total: {result.warnings.length}</div>
    <div className='p-3 rounded bg-slate-900 border border-slate-700'><div className='flex gap-2 mb-2'><select value={market} onChange={e=>setMarket(e.target.value)} className='bg-slate-950 p-1 rounded'><option value='all'>all</option><option value='winner'>winner</option><option value='top4'>top4</option></select><select value={sex} onChange={e=>setSex(e.target.value)} className='bg-slate-950 p-1 rounded'><option value='all'>all</option><option value='M'>M</option><option value='F'>F</option></select><input className='bg-slate-950 p-1 rounded' placeholder='weight' value={weightFilter==='all'?'':weightFilter} onChange={e=>setWeightFilter(e.target.value||'all')}/><input type='number' className='bg-slate-950 p-1 rounded w-24' value={minEdge} onChange={e=>setMinEdge(Number(e.target.value))}/></div>{filteredPicks.length===0?<p>No value picks found. Add odds in qazaqstan_2026_odds.json and rerun the analysis.</p>:<PicksTable picks={filteredPicks}/>}</div>
    {Object.entries(result.weights).map(([w,d])=><details key={w} className='p-3 rounded bg-slate-900 border border-slate-700'><summary className='cursor-pointer font-semibold'>{w} {d.warnings.length===0?'':'- warnings'}</summary><button className='my-2 px-2 py-1 bg-slate-700 rounded' onClick={()=>{setSelectedWeight(w);editorRef.current?.scrollIntoView({behavior:'smooth'});}}>Edit this weight</button>{Object.keys((state?.weights.find(x=>x.weight===w)?.odds_winner)||{}).length===0 && <p>No odds loaded for this weight.</p>}{Object.keys((state?.weights.find(x=>x.weight===w)?.athlete_strengths)||{}).length===0 && <p className='text-amber-300'>Using default strength score for athletes without data.</p>}<div>Winner ranking completo: {d.winner_ranking.map(x=>`${x.athlete}(${x.prob.toFixed(2)})`).join(', ')}</div><div>Top4 ranking completo: {d.top4_ranking.map(x=>`${x.athlete}(${x.prob.toFixed(2)})`).join(', ')}</div><div>Value winner picks: {d.value_winner.map(p=>`${p.athlete}(${p.edge.toFixed(2)})`).join(', ')||'none'}</div><div>Value top4 picks: {d.value_top4.map(p=>`${p.athlete}(${p.edge.toFixed(2)})`).join(', ')||'none'}</div><details><summary>Show warnings ({d.warnings.length})</summary><ul>{d.warnings.slice(0,300).map((w2,i)=><li key={i}>{w2}</li>)}</ul></details></details>)}
    <details className='p-3 rounded bg-slate-900 border border-slate-700'><summary>Advanced JSON Overrides</summary><p className='text-slate-400 text-sm'>Experimental: paste JSON overrides and click Use in analysis.</p></details>
    </section>}
  </main>
}
