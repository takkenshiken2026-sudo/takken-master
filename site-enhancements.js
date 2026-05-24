(function(){
'use strict';

// =====================================================================
// ユーティリティ
// =====================================================================
function todayStr(){
  return localDateKey(new Date());
}
function daysSince(dateStr){
  if(!dateStr) return 999;
  const diff=new Date(todayStr()).getTime()-new Date(dateStr).getTime();
  return Math.floor(diff/(1000*60*60*24));
}
function fmtRate(n,d){
  if(!d) return '—';
  return Math.round(n/d*100)+'%';
}

// =====================================================================
// 1. スペースドリペティション (SRS)
// =====================================================================
// SM-2アルゴリズムを簡易実装
// srsData: { [qid]: { level:0-4, due:YYYY-MM-DD, lastSeen:YYYY-MM-DD } }
// level 0: 翌日, 1: 3日後, 2: 7日後, 3: 14日後, 4: 30日後
const SRS_INTERVALS = [1, 3, 7, 14, 30];
const SRS_KEY = 'takken_srs_v1';

function getSrsData(){
  try{ return JSON.parse(localStorage.getItem(SRS_KEY)||'{}'); }catch(e){ return {}; }
}
function saveSrsData(data){
  try{ localStorage.setItem(SRS_KEY, JSON.stringify(data)); }catch(e){}
}

// 問題に正解した後、SRSレベルを更新
function srsOnCorrect(qid){
  const data=getSrsData();
  const item=data[qid]||{level:0,due:todayStr(),lastSeen:todayStr()};
  item.level=Math.min(4, (item.level||0)+1);
  item.lastSeen=todayStr();
  const interval=SRS_INTERVALS[item.level];
  const due=new Date(); due.setDate(due.getDate()+interval);
  item.due=localDateKey(due);
  data[qid]=item;
  saveSrsData(data);
}
// 不正解: レベルをリセット
function srsOnWrong(qid){
  const data=getSrsData();
  const item=data[qid]||{level:0,due:todayStr(),lastSeen:todayStr()};
  item.level=0;
  item.lastSeen=todayStr();
  const tmr=new Date(); tmr.setDate(tmr.getDate()+1);
  item.due=localDateKey(tmr);
  data[qid]=item;
  saveSrsData(data);
}
// 今日の復習キューを取得
function getSrsDueQueue(){
  const data=getSrsData();
  const today=todayStr();
  const u=typeof getUserData==='function'?getUserData():null;
  const answers=u?.answers||{};
  const allQ=typeof allPracticeQuestions==='function'?allPracticeQuestions():[];
  // 1. SRSに登録済みで今日以前のdue
  const srsQids=Object.keys(data).filter(qid=>data[qid].due<=today);
  // 2. さらに一度でも解いたことがある問題に限定
  const dueQids=srsQids.filter(qid=>answers[qid]);
  const dueQs=dueQids.map(qid=>{
    const q=allQ.find(qq=>String(qq.id)===qid);
    return q?{q,srs:data[qid]}:null;
  }).filter(Boolean);
  // levelの低い順（優先度高）でソート
  dueQs.sort((a,b)=>(a.srs.level||0)-(b.srs.level||0));
  return dueQs;
}
window.takkenGetSrsDueQueue=getSrsDueQueue;
// 解答済みのすべての問題をSRSに登録（初回）
function initSrsFromAnswers(){
  const data=getSrsData();
  const u=typeof getUserData==='function'?getUserData():null;
  if(!u) return;
  const answers=u.answers||{};
  let changed=false;
  Object.entries(answers).forEach(([qid,a])=>{
    if(!data[qid]){
      const isCorrect=(a.ans!==undefined);
      data[qid]={level:isCorrect?1:0,due:todayStr(),lastSeen:a.date?localDateKey(new Date(a.date)):todayStr()};
      changed=true;
    }
  });
  if(changed) saveSrsData(data);
}
window.takkenInitSrsFromAnswers=initSrsFromAnswers;

// SRSレベル名
const SRS_LEVEL_LABELS=['要復習','弱い','普通','強い','定着'];

function renderSrsBanner(container){
  if(!container) return;
  initSrsFromAnswers();
  const queue=getSrsDueQueue();
  if(!queue.length){ container.innerHTML=''; return; }
  container.innerHTML=`
  <div class="card srs-review-card" onclick="openSrsModal()">
    <div class="srs-review-kicker">スペースドリペティション</div>
    <h2 class="section-label" style="margin-bottom:6px">復習スケジュール</h2>
    <p class="srs-review-lead">忘却曲線に基づく今日の復習</p>
    <div class="srs-review-card-foot">
      <span class="tag tag-blue">${queue.length}問</span>
      <span class="srs-review-action">一覧を見る ›</span>
    </div>
  </div>`;
}

function openSrsModal(){
  const queue=getSrsDueQueue();
  const el=document.getElementById('srs-queue-list');
  const overlay=document.getElementById('srs-modal-overlay');
  if(!el||!overlay) return;
  const FIELD_NAMES={rights:'権利関係',law:'宅建業法',limit:'法令制限',tax:'税・その他'};
  if(!queue.length){
    el.innerHTML='<div style="text-align:center;padding:20px 0;color:var(--text3);font-size:13px">今日の復習はすべて完了しています。</div>';
    const btn=document.getElementById('srs-start-btn');
    if(btn) btn.style.display='none';
  } else {
    const btn=document.getElementById('srs-start-btn');
    if(btn) btn.style.display='';
    el.innerHTML=queue.slice(0,15).map(({q,srs})=>`
    <div class="srs-queue-card" onclick="closeSrsModal();reviewQ(${q.id})">
      <div class="srs-queue-card-body">
        <div class="srs-queue-q">${q.text.slice(0,60)}${q.text.length>60?'…':''}</div>
        <div class="srs-queue-meta">
          <span class="srs-level-chip srs-level-${srs.level||0}">${SRS_LEVEL_LABELS[srs.level||0]}</span>
          <span class="srs-due-chip">${FIELD_NAMES[q.field]||q.field}</span>
          ${srs.lastSeen?`<span class="srs-due-chip">最終：${srs.lastSeen}</span>`:''}
        </div>
      </div>
      <div class="srs-queue-arrow">›</div>
    </div>`).join('');
    if(queue.length>15) el.innerHTML+=`<div style="text-align:center;font-size:12px;color:var(--text3);padding:8px 0">他 ${queue.length-15}問</div>`;
  }
  overlay.style.display='flex';
}
window.openSrsModal=openSrsModal;

function closeSrsModal(){
  const overlay=document.getElementById('srs-modal-overlay');
  if(overlay) overlay.style.display='none';
}
window.closeSrsModal=closeSrsModal;

function startSrsQuiz(){
  const queue=getSrsDueQueue();
  if(!queue.length) return;
  closeSrsModal();
  // 既存のquizStateを使って問題を開始
  if(typeof quizState==='undefined') return;
  quizState.queue=queue.map(({q})=>q).slice(0,20);
  quizState.idx=0;
  quizState.sessionResults=[]; quizState.scoreReplayMode=false;
  quizState.fromReview=true;
  quizState.mode='srs';
  if(typeof gotoPage==='function') gotoPage('quiz');
  if(typeof renderQ==='function') renderQ();
}
window.startSrsQuiz=startSrsQuiz;

// 既存の recordAnswer にフックしてSRSを更新
// quizの採点完了時に呼ばれる recordResult / showScore の直後に処理を差し込む
const _origShowScore=typeof window.showScore==='function'?window.showScore:null;
// answerQ / recordAnswer をラップ
function patchSrsHook(){
  // quizState.sessionResults に記録された後でSRS更新
  const origAdvance=window.advanceQ;
  if(origAdvance){
    window.advanceQ=function(){
      _flushSrsPatch();
      origAdvance.apply(this,arguments);
    };
  }
  function _flushSrsPatch(){
    if(typeof quizState==='undefined') return;
    const res=quizState.sessionResults;
    if(!res||!res.length) return;
    const last=res[res.length-1];
    if(!last||!last.q) return;
    const qid=String(last.q.id);
    if(last.correct) srsOnCorrect(qid);
    else srsOnWrong(qid);
  }
  // showScore完了時にも最終問題を処理
  const origShowScore=window.showScore;
  if(origShowScore){
    window.showScore=function(){
      if(typeof quizState!=='undefined'&&quizState.sessionResults){
        quizState.sessionResults.forEach(r=>{
          if(!r||!r.q) return;
          const qid=String(r.q.id);
          if(r.correct) srsOnCorrect(qid);
          else srsOnWrong(qid);
        });
      }
      return origShowScore.apply(this,arguments);
    };
  }
}
// DOM読み込み後にパッチ適用
setTimeout(patchSrsHook,200);

// =====================================================================
// 2. 分野別レーダーチャート
// =====================================================================
function computeFieldStats(){
  const u=typeof getUserData==='function'?getUserData():null;
  const answers=u?.answers||{};
  const allQ=typeof allPracticeQuestions==='function'?allPracticeQuestions():[];
  const fields=['rights','law','limit','tax'];
  const FIELD_NAMES={rights:'権利関係',law:'宅建業法',limit:'法令制限',tax:'税・その他'};
  return fields.map(f=>{
    const fqs=allQ.filter(q=>q.field===f&&answers[q.id]);
    const correct=fqs.filter(q=>answers[q.id]?.ans===q.ans).length;
    const rate=fqs.length?Math.round(correct/fqs.length*100):0;
    return{field:f,name:FIELD_NAMES[f],total:fqs.length,correct,rate};
  });
}

function renderRadarChart(containerId){
  const el=document.getElementById(containerId);
  if(!el) return;
  const stats=computeFieldStats();
  const pad=42;
  const size=292;
  const cx=size/2, cy=size/2, r=108;
  const fields=stats;
  const n=fields.length;
  const angles=fields.map((_,i)=>-Math.PI/2+(2*Math.PI/n)*i);
  function pt(angle,radius){
    return[cx+Math.cos(angle)*radius, cy+Math.sin(angle)*radius];
  }
  // グリッド
  let gridSVG='';
  [20,40,60,80,100].forEach(pct=>{
    const pts=angles.map(a=>pt(a,r*pct/100));
    gridSVG+=`<polygon points="${pts.map(p=>p.join(',')).join(' ')}" fill="none" stroke="var(--border2)" stroke-width="${pct===100?1.5:0.8}" stroke-dasharray="${pct<100?'4,3':''}"/>`;
  });
  // 軸線
  let axesSVG=angles.map(a=>{
    const[x,y]=pt(a,r);
    return`<line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="var(--border2)" stroke-width="1"/>`;
  }).join('');
  // データポリゴン
  const dataPts=fields.map((f,i)=>pt(angles[i],r*f.rate/100));
  const dataSVG=`<polygon points="${dataPts.map(p=>p.join(',')).join(' ')}" fill="rgba(51,51,51,.12)" stroke="var(--ink)" stroke-width="2" stroke-linejoin="round"/>
    ${dataPts.map(([x,y])=>`<circle cx="${x}" cy="${y}" r="4" fill="var(--ink)"/>`).join('')}`;
  // ラベル
  const LABEL_OFFSET=22;
  const labelsSVG=fields.map((f,i)=>{
    const[x,y]=pt(angles[i],r+LABEL_OFFSET);
    const anchor=x<cx-4?'end':x>cx+4?'start':'middle';
    return`<text x="${x}" y="${y}" text-anchor="${anchor}" class="radar-axis-label" dominant-baseline="middle">${f.name}<tspan x="${x}" dy="13" font-weight="700" fill="var(--text)">${f.total?f.rate+'%':'未解答'}</tspan></text>`;
  }).join('');
  // 目盛りラベル
  const scaleSVG=[20,40,60,80,100].map(pct=>{
    const[x,y]=pt(-Math.PI/2,r*pct/100);
    return`<text x="${x+4}" y="${y}" font-size="9" fill="var(--text3)" dominant-baseline="middle">${pct}%</text>`;
  }).join('');

  el.innerHTML=`
  <div class="radar-wrap">
    <svg class="radar-svg" width="${size+pad*2}" height="${size+pad*2}" viewBox="-${pad} -${pad} ${size+pad*2} ${size+pad*2}">
      ${gridSVG}${axesSVG}${dataSVG}${labelsSVG}${scaleSVG}
    </svg>
  </div>`;
}
window.renderRadarChart=renderRadarChart;

// =====================================================================
// 3. 弱点自動特定・優先出題
// =====================================================================
function getWeakAnalysis(){
  const u=typeof getUserData==='function'?getUserData():null;
  const answers=u?.answers||{};
  const allQ=typeof allPracticeQuestions==='function'?allPracticeQuestions():[];
  const FIELD_NAMES={rights:'権利関係',law:'宅建業法',limit:'法令制限',tax:'税・その他'};

  // ── 分野別の正答率 ──
  const fieldStats={};
  ['rights','law','limit','tax'].forEach(f=>{
    const fqs=allQ.filter(q=>q.field===f&&answers[q.id]);
    const correct=fqs.filter(q=>answers[q.id]?.ans===q.ans).length;
    fieldStats[f]={total:fqs.length,correct,rate:fqs.length?Math.round(correct/fqs.length*100):null,name:FIELD_NAMES[f]};
  });

  // ── 弱点分野（正答率70%未満・5問以上解答済み） ──
  const weakFields=Object.entries(fieldStats)
    .filter(([,s])=>s.total>=5&&s.rate!==null&&s.rate<70)
    .sort(([,a],[,b])=>a.rate-b.rate)
    .map(([f])=>f);

  // ── 不正解問題・SRS定着不足問題のQIDセット ──
  const wrongQids=new Set(
    allQ.filter(q=>answers[q.id]&&answers[q.id].ans!==q.ans).map(q=>String(q.id))
  );
  const srsData=getSrsData();
  const srsWeakQids=new Set(
    Object.entries(srsData).filter(([,s])=>(s.level||0)<=1).map(([qid])=>qid)
  );

  // ── 不正解問題が属する「単元(unit)・分野(field)」を収集 ──
  // unit は過去問にはなく、実践演習にある。fieldは共通。
  const weakUnits=new Set();
  const weakFieldsFromWrong=new Set();
  allQ.filter(q=>wrongQids.has(String(q.id))).forEach(q=>{
    if(q.unit) weakUnits.add(q.unit);
    weakFieldsFromWrong.add(q.field);
  });
  // SRS定着不足問題の単元・分野も追加
  allQ.filter(q=>srsWeakQids.has(String(q.id))&&answers[q.id]).forEach(q=>{
    if(q.unit) weakUnits.add(q.unit);
    weakFieldsFromWrong.add(q.field);
  });

  // ── スコア計算（解答済み問題） ──
  function getWeakScore(q){
    const qid=String(q.id);
    let score=0;
    if(wrongQids.has(qid)) score+=100;       // 不正解
    if(srsWeakQids.has(qid)) score+=50;      // SRS定着不足
    if(weakFields.includes(q.field)) score+=30; // 弱点分野
    const srsLevel=srsData[qid]?.level||0;
    score+=(4-srsLevel)*10;                  // SRSレベルが低いほど優先
    return score;
  }

  // ── 関連未解答問題のスコア計算 ──
  // 不正解問題と同じ単元 or 同じ弱点分野の未解答問題を補完候補に
  function getRelatedScore(q){
    let score=0;
    if(q.unit&&weakUnits.has(q.unit)) score+=60;       // 同単元（最優先）
    else if(weakFieldsFromWrong.has(q.field)) score+=30; // 同分野
    if(weakFields.includes(q.field)) score+=20;          // 弱点分野
    return score;
  }

  // ── 解答済み弱点問題（優先度1位） ──
  const answeredWeak=allQ
    .filter(q=>answers[q.id])
    .map(q=>({q,score:getWeakScore(q),type:'answered'}))
    .filter(({score})=>score>0)
    .sort((a,b)=>b.score-a.score);

  // ── 関連未解答問題（優先度2位・補完用） ──
  const unansweredRelated=allQ
    .filter(q=>!answers[q.id])
    .map(q=>({q,score:getRelatedScore(q),type:'related'}))
    .filter(({score})=>score>0)
    .sort((a,b)=>b.score-a.score);

  // ── 最大20問を構成：解答済み弱点を先に、足りなければ関連未解答で補完 ──
  const POOL_MAX=20;
  const combined=[...answeredWeak,...unansweredRelated].slice(0,POOL_MAX);
  const weakPool=combined.map(({q})=>q);

  return{
    fieldStats,
    weakFields,
    weakPool,
    answeredWeakCount:answeredWeak.length,
    relatedCount:Math.max(0,combined.length-answeredWeak.length),
    weakUnits
  };
}

function openWeakMode(){
  const overlay=document.getElementById('weak-mode-overlay');
  if(!overlay) return;
  const {fieldStats,weakFields,weakPool,answeredWeakCount,relatedCount}=getWeakAnalysis();
  const el=document.getElementById('weak-mode-analysis');
  if(!el) return;
  const FIELD_NAMES={rights:'権利関係',law:'宅建業法',limit:'法令制限',tax:'税・その他'};
  // 分野別バー
  let barsHTML=Object.entries(fieldStats).map(([f,s])=>{
    const rate=s.rate!==null?s.rate:0;
    const barColor=rate>=80?'var(--green)':rate>=60?'var(--text2)':'var(--red)';
    return`<div class="weak-bar-row">
      <div class="weak-bar-label">${s.name}</div>
      <div class="weak-bar-track"><div class="weak-bar-fill" style="width:${s.total?rate:0}%;background:${barColor}"></div></div>
      <div class="weak-bar-val" style="color:${barColor}">${s.total?(rate+'%'):'—'}</div>
    </div>`;
  }).join('');
  // 弱点チップ
  let weakChipsHTML='';
  if(weakFields.length){
    weakChipsHTML=`<div class="weak-field-row">${weakFields.map(f=>`<span class="weak-field-chip bad">${FIELD_NAMES[f]}</span>`).join('')}${Object.keys(FIELD_NAMES).filter(f=>!weakFields.includes(f)&&fieldStats[f]?.total>=5).map(f=>`<span class="weak-field-chip">${FIELD_NAMES[f]}</span>`).join('')}</div>`;
  }
  // 出題内訳
  const totalCount=weakPool.length;
  const breakdown=totalCount
    ?`<div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
        <span style="font-size:12px;background:#fee2e2;color:#b91c1c;border-radius:4px;padding:2px 8px;font-weight:600">不正解・定着不足 ${Math.min(answeredWeakCount,20)}問</span>
        ${relatedCount>0?`<span style="font-size:12px;background:#e0f2fe;color:#0369a1;border-radius:4px;padding:2px 8px;font-weight:600">関連未解答 ${relatedCount}問</span>`:''}
      </div>`
    :'';
  el.innerHTML=`
  <div style="margin-bottom:14px">${barsHTML}</div>
  ${weakChipsHTML}
  <div style="font-size:13px;color:var(--text2);margin-top:10px;padding:10px;background:var(--bg3);border-radius:var(--r);line-height:1.65">
    出題候補 <strong style="color:var(--text)">${totalCount}問</strong>（最大20問を出題）${breakdown}
    <div style="font-size:11px;color:var(--text3);margin-top:6px;line-height:1.7">不正解・定着が弱い問題を優先し、同じ単元・分野の未解答問題で補完します。</div>
  </div>`;
  overlay.style.display='flex';
}
window.openWeakMode=openWeakMode;

function closeWeakMode(){
  const overlay=document.getElementById('weak-mode-overlay');
  if(overlay) overlay.style.display='none';
}
window.closeWeakMode=closeWeakMode;

function startWeakModeQuiz(){
  const {weakPool}=getWeakAnalysis();
  if(!weakPool.length){
    if(typeof showToast==='function') showToast('弱点問題が見つかりませんでした','default',2000);
    closeWeakMode();
    return;
  }
  closeWeakMode();
  if(typeof quizState==='undefined') return;
  quizState.queue=weakPool.slice(0,20);
  quizState.idx=0;
  quizState.sessionResults=[]; quizState.scoreReplayMode=false;
  quizState.fromReview=false;
  quizState.mode='weak';
  if(typeof gotoPage==='function') gotoPage('quiz');
  if(typeof renderQ==='function') renderQ();
}
window.startWeakModeQuiz=startWeakModeQuiz;

// =====================================================================
// ダッシュボードの拡張（レーダーチャート）
// =====================================================================
function injectDashEnhancements(){
  // 理解度レーダー・学習日記（カレンダー）は #page-dash 内の .dash-radar-cal-row に静的配置
}

// quiz-startページに弱点モード・SRSバナーを追加
const WEAK_UNLOCK_COUNT=100; // 解放条件：100問解答

function getWeakUnlocked(){
  const u=typeof getUserData==='function'?getUserData():null;
  const total=Object.keys(u?.answers||{}).length;
  return total>=WEAK_UNLOCK_COUNT;
}

function injectQuizStartEnhancements(){
  const startEl=document.getElementById('page-quiz-start');
  if(!startEl||startEl.querySelector('#weak-mode-inject')) return;
  const modeList=startEl.querySelector('.mode-list-v2');
  if(!modeList) return;

  const unlocked=getWeakUnlocked();
  const u=typeof getUserData==='function'?getUserData():null;
  const total=Object.keys(u?.answers||{}).length;
  const remaining=Math.max(0,WEAK_UNLOCK_COUNT-total);

  // 弱点モードカード（ロック状態 or 解放状態）
  const weakCard=document.createElement('div');
  weakCard.id='weak-mode-inject';
  if(unlocked){
    weakCard.innerHTML=`
    <div class="mode-card-v2" onclick="openWeakMode()">
      <div class="mode-num-v2">04</div>
      <div class="mode-body-v2">
        <div class="mode-purpose-v2">苦手な問題を集中的に克服したい</div>
        <div class="mode-title-v2">弱点集中対策</div>
      </div>
      <div class="mode-arrow-v2">›</div>
    </div>`;
  } else {
    weakCard.innerHTML=`
    <div class="mode-card-v2" style="opacity:.55;cursor:not-allowed;pointer-events:none;position:relative">
      <div class="mode-num-v2" style="color:var(--text3)">04</div>
      <div class="mode-body-v2">
        <div class="mode-purpose-v2" style="display:flex;align-items:center;gap:5px">
          <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="7" width="10" height="8" rx="2"/><path d="M5 7V5a3 3 0 016 0v2"/></svg>
          あと${remaining}問解くと解放されます
        </div>
        <div class="mode-title-v2">弱点集中対策</div>
      </div>
      <div class="mode-arrow-v2" style="color:var(--text3);display:flex;align-items:center;justify-content:center" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg></div>
    </div>`;
  }
  modeList.appendChild(weakCard);
}

// 復習ページ：旧レイアウトで #review-list の外にあった SRS ノードを除去
function injectReviewEnhancements(){
  const list=document.getElementById('review-list');
  if(!list) return;
  const prev=list.previousElementSibling;
  if(prev && prev.id==='srs-review-wrap') prev.remove();
}

// =====================================================================
// 既存の renderDash / gotoPage にフック
// =====================================================================
const _origRenderDash=window.renderDash;
window.renderDash=function(){
  if(_origRenderDash) _origRenderDash.apply(this,arguments);
  // 少し遅らせてDOM生成後に実行（レーダーは renderDashPeriodStats 内で描画済み）
  setTimeout(()=>{
    injectDashEnhancements();
  },50);
};

const _origRenderDashLevel=window.renderDashLevel;
window.renderDashLevel=function(){
  if(_origRenderDashLevel) _origRenderDashLevel.apply(this,arguments);
};

const _origGotoPage=window.gotoPage;
window.gotoPage=function(id){
  if(_origGotoPage) _origGotoPage.apply(this,arguments);
  setTimeout(()=>{
    if(id==='quiz-start'){
      // 弱点カードが既にある場合は解放状態が変わっていれば再描画
      const existing=document.getElementById('weak-mode-inject');
      if(existing) existing.remove();
      injectQuizStartEnhancements();
    }
    if(id==='review'){
      injectReviewEnhancements();
    }
    if(id==='dash'){
      injectDashEnhancements();
      if(typeof window.renderRadarChart==='function'){
        window.renderRadarChart('radar-chart-container');
      }
    }
  },80);
};

// showScore後にquiz-startへ戻ったとき弱点カードを更新するため
// 既存showScoreにフック（30問達成直後の再描画）
const _origShowScore2=window.showScore;
window.showScore=function(){
  if(_origShowScore2) _origShowScore2.apply(this,arguments);
  // スコア表示後に弱点カードを再評価（次のquiz-start遷移時に反映済みのため不要だが念のため）
};

// =====================================================================
// 初期化
// =====================================================================
function init(){
  injectDashEnhancements();
  injectQuizStartEnhancements();
  injectReviewEnhancements();
  const activePage=document.querySelector('.page.active');
  if(activePage){
    const id=activePage.id.replace('page-','');
    if(id==='dash'){
      setTimeout(()=>{
        injectDashEnhancements();
        if(typeof window.renderRadarChart==='function'){
          window.renderRadarChart('radar-chart-container');
        }
      },120);
    }
  }
}

window.initTakkenEnhancements=init;
})();
