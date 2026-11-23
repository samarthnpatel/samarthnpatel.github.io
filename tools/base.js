
(function(){
var calm=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var still=calm||!('IntersectionObserver' in window);
function clamp(v){return Math.max(0,Math.min(1,v));}
if(!still){
/* numbers count up when they scroll into view */
var io=new IntersectionObserver(function(es){es.forEach(function(e){
 if(!e.isIntersecting)return; io.unobserve(e.target);
 var el=e.target,to=parseFloat(el.dataset.count),dec=(el.dataset.count.split('.')[1]||'').length,t0=null;
 function step(t){if(t0===null)t0=t;var k=clamp((t-t0)/900);k=1-Math.pow(1-k,3);
  el.textContent=(to*k).toFixed(dec); if(k<1)requestAnimationFrame(step); else el.textContent=el.dataset.count;}
 el.textContent=(0).toFixed(dec); requestAnimationFrame(step);
});},{threshold:0.6});
document.querySelectorAll('[data-count]').forEach(function(el){io.observe(el);});
/* robot clip plays only while it is on screen */
var v=document.querySelector('.sec video');
if(v){new IntersectionObserver(function(es){es.forEach(function(e){
 if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){});}else v.pause();});},{threshold:0.5}).observe(v);}
/* carrier board: screen holds while nine boards merge into one */
var sc=document.querySelector('.scene'),ticking=false;
var fit=function(){var on=window.innerWidth>=900&&window.innerHeight>=640;sc.classList.toggle('pin',on);update();};
var update=function(){ticking=false;if(!sc.classList.contains('pin'))return;
 var r=sc.getBoundingClientRect(),p=clamp(-r.top/(r.height-window.innerHeight));
 sc.style.setProperty('--s',(1-clamp(p/0.5)).toFixed(3));
 sc.style.setProperty('--f',clamp((p-0.55)/0.3).toFixed(3));};
if(sc){window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(update);}},{passive:true});
 window.addEventListener('resize',fit);fit();}
}
/* detail sheets */
function openSheet(id){var d=document.getElementById('d-'+id);if(d&&!d.open){d.showModal();d.scrollTop=0;try{history.replaceState(null,'','#'+id);}catch(e){}}}
document.querySelectorAll('[data-open]').forEach(function(b){b.addEventListener('click',function(){openSheet(b.dataset.open);});});
document.querySelectorAll('dialog.sheet').forEach(function(d){
 d.addEventListener('click',function(e){if(e.target===d||e.target.hasAttribute('data-close'))d.close();});
 d.addEventListener('close',function(){try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}});});
if(location.hash.length>1)openSheet(location.hash.slice(1));
})();
