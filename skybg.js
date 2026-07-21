
(function(){
  const c=document.getElementById("sky");if(!c)return;const x=c.getContext("2d");
  const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
  let W,H,st=[];
  function mk(){W=c.width=innerWidth;H=c.height=innerHeight;st=[];
    for(let i=0;i<120;i++)st.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.3+.3,
      tw:Math.random()*6.28,ts:.002+Math.random()*.008,vx:(Math.random()-.5)*.03,vy:(Math.random()-.5)*.03});}
  function tick(){x.clearRect(0,0,W,H);
    for(const s of st){if(!reduce){s.tw+=s.ts;s.x+=s.vx;s.y+=s.vy;
      if(s.x<0||s.x>W)s.vx*=-1;if(s.y<0||s.y>H)s.vy*=-1;}
      x.fillStyle=`rgba(238,242,255,${.18+.14*Math.sin(s.tw)})`;
      x.beginPath();x.arc(s.x,s.y,s.r,0,7);x.fill();}
    requestAnimationFrame(tick);}
  addEventListener("resize",mk);mk();if(!reduce)tick();else{st.forEach(s=>{x.fillStyle="rgba(238,242,255,.25)";x.beginPath();x.arc(s.x,s.y,s.r,0,7);x.fill();});}
})();
