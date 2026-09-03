import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="연주시차 시뮬레이션",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0.25rem;
            padding-bottom: 0.4rem;
            max-width: 1580px;
        }
        header[data-testid="stHeader"] { height: 0; }
        #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r"""
<div id="parallax-app-v2">
  <style>
    #parallax-app-v2 {
      --bg:#050d18;
      --panel:#071321;
      --panel2:#09182a;
      --border:rgba(255,255,255,.09);
      --text:#eaf2fb;
      --muted:#9cafc4;
      --accent:#78d6ff;
      --target:#ffd86a;
      width:100%;
      color:var(--text);
      font-family:Inter, Pretendard, "Noto Sans KR", system-ui, sans-serif;
      user-select:none;
    }
    #parallax-app-v2 * { box-sizing:border-box; }

    .sim-grid {
      display:grid;
      grid-template-columns:minmax(0,1fr) minmax(0,1fr);
      gap:14px;
    }

    .sim-panel {
      position:relative;
      min-width:0;
      overflow:hidden;
      border:1px solid var(--border);
      border-radius:18px;
      background:linear-gradient(180deg,#071525 0%,#050d18 100%);
    }

    .panel-tag {
      position:absolute;
      top:14px;
      left:16px;
      z-index:2;
      padding:5px 9px;
      border:1px solid rgba(255,255,255,.09);
      border-radius:999px;
      background:rgba(5,13,24,.62);
      color:rgba(235,243,251,.72);
      font-size:12px;
      font-weight:750;
      letter-spacing:.02em;
      backdrop-filter:blur(6px);
    }

    svg {
      display:block;
      width:100%;
      height:auto;
    }

    .control-bar {
      margin-top:12px;
      display:grid;
      grid-template-columns:auto minmax(220px,1.2fr) minmax(220px,1fr) auto auto;
      gap:12px;
      align-items:center;
      padding:10px 12px;
      border:1px solid var(--border);
      border-radius:15px;
      background:#081525;
    }

    .play-btn {
      width:46px;
      height:46px;
      border:0;
      border-radius:13px;
      background:#172b46;
      color:white;
      font-size:19px;
      cursor:pointer;
    }
    .play-btn:hover { background:#1d385d; }

    .range-group {
      display:grid;
      grid-template-columns:auto 1fr;
      align-items:center;
      gap:10px;
      min-width:0;
    }

    .mini-label {
      color:var(--muted);
      font-size:12px;
      font-weight:750;
      white-space:nowrap;
    }

    input[type="range"] {
      width:100%;
      accent-color:#72cfff;
      cursor:pointer;
    }

    .toggle {
      display:flex;
      align-items:center;
      gap:7px;
      min-height:42px;
      padding:7px 8px;
      border-radius:10px;
      color:#b9c8d8;
      font-size:12px;
      font-weight:750;
      white-space:nowrap;
      cursor:pointer;
    }
    .toggle:hover { background:rgba(255,255,255,.035); }
    .toggle input { accent-color:#72cfff; }

    .legend-row {
      min-height:26px;
      padding:6px 4px 0;
      display:flex;
      justify-content:flex-end;
      align-items:center;
      gap:15px;
      color:rgba(205,220,235,.52);
      font-size:10px;
    }

    .ring-key {
      display:inline-block;
      width:11px;
      height:11px;
      margin-right:4px;
      border:1.5px solid var(--accent);
      border-radius:50%;
      vertical-align:-2px;
      opacity:.8;
    }

    .ghost-key {
      display:inline-block;
      width:9px;
      height:9px;
      margin-right:4px;
      border-radius:50%;
      background:rgba(255,255,255,.24);
      vertical-align:-1px;
    }

    @media (max-width: 900px) {
      .sim-grid { grid-template-columns:1fr; }
      .control-bar { grid-template-columns:auto 1fr; }
      .range-group { grid-column:span 1; }
      .toggle { white-space:normal; }
    }
  </style>

  <div class="sim-grid">
    <section class="sim-panel">
      <div class="panel-tag">우주 공간</div>
      <svg id="spaceSvg" viewBox="0 0 760 760" role="img" aria-label="태양 주위를 공전하는 지구와 거리가 다른 별들">
        <defs>
          <radialGradient id="sunGlow2">
            <stop offset="0%" stop-color="#fff8c9"/>
            <stop offset="40%" stop-color="#ffd46e"/>
            <stop offset="100%" stop-color="#f7963c"/>
          </radialGradient>
          <radialGradient id="earthGlow2">
            <stop offset="0%" stop-color="#c7ebff"/>
            <stop offset="100%" stop-color="#4f9fe9"/>
          </radialGradient>
          <filter id="softGlow2">
            <feGaussianBlur stdDeviation="4.5" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
          <linearGradient id="depthFade" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#9fb7cf" stop-opacity=".10"/>
            <stop offset="100%" stop-color="#9fb7cf" stop-opacity="0"/>
          </linearGradient>
        </defs>

        <rect width="760" height="760" fill="#050d18"/>
        <g id="spaceDust"></g>

        <g opacity=".18">
          <path d="M380 95 L380 555" stroke="#b6c8dc" stroke-width="1" stroke-dasharray="2 9"/>
          <path d="M110 522 C205 492 555 492 650 522" fill="none" stroke="#9fb4c8" stroke-width="1"/>
        </g>

        <ellipse cx="380" cy="610" rx="250" ry="82"
          fill="none" stroke="rgba(212,228,242,.22)" stroke-width="2"/>

        <g id="sightGroup"></g>

        <g>
          <circle cx="380" cy="610" r="30" fill="url(#sunGlow2)" filter="url(#softGlow2)"/>
          <circle cx="380" cy="610" r="6" fill="#fffce2"/>
        </g>

        <g id="earthOpposite"></g>
        <g id="earthCurrent"></g>
        <g id="starLayer"></g>
      </svg>
    </section>

    <section class="sim-panel">
      <div class="panel-tag">지구에서 본 하늘</div>
      <svg id="skySvg" viewBox="0 0 760 760" role="img" aria-label="지구의 위치에 따라 달라지는 별의 겉보기 위치">
        <defs>
          <filter id="skyGlow2">
            <feGaussianBlur stdDeviation="4" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <rect width="760" height="760" fill="#040b15"/>
        <g id="skyDust"></g>
        <g id="skyPaths"></g>
        <g id="skyGhosts"></g>
        <g id="skyStars"></g>
      </svg>
    </section>
  </div>

  <div class="control-bar">
    <button id="playBtn" class="play-btn" type="button" aria-label="공전 재생">▶</button>

    <label class="range-group">
      <span class="mini-label">공전</span>
      <input id="orbitRange" type="range" min="0" max="360" step="0.2" value="205" aria-label="지구 공전 위치">
    </label>

    <label class="range-group">
      <span class="mini-label">별 거리</span>
      <input id="distanceRange" type="range" min="120" max="1600" step="1" value="280" aria-label="관측 별 거리">
    </label>

    <label class="toggle">
      <input id="farParallax" type="checkbox">
      먼 별 시차
    </label>

    <label class="toggle">
      <input id="sightToggle" type="checkbox" checked>
      시선
    </label>
  </div>

  <div class="legend-row">
    <span><span class="ring-key"></span>배경 기준 가능</span>
    <span><span class="ghost-key"></span>6개월 전 위치</span>
  </div>

  <script>
    (() => {
      const root = document.getElementById("parallax-app-v2");
      if (!root || root.dataset.ready === "1") return;
      root.dataset.ready = "1";

      const NS = "http://www.w3.org/2000/svg";
      const starLayer = root.querySelector("#starLayer");
      const sightGroup = root.querySelector("#sightGroup");
      const earthCurrent = root.querySelector("#earthCurrent");
      const earthOpposite = root.querySelector("#earthOpposite");
      const skyStars = root.querySelector("#skyStars");
      const skyGhosts = root.querySelector("#skyGhosts");
      const skyPaths = root.querySelector("#skyPaths");
      const orbitRange = root.querySelector("#orbitRange");
      const distanceRange = root.querySelector("#distanceRange");
      const farParallax = root.querySelector("#farParallax");
      const sightToggle = root.querySelector("#sightToggle");
      const playBtn = root.querySelector("#playBtn");

      const BG_STARS = [
        { distance: 650,  baseX: 150, baseY: 190, size: 5.0, spaceX: 185 },
        { distance: 1100, baseX: 590, baseY: 145, size: 4.6, spaceX: 590 },
        { distance: 2200, baseX: 245, baseY: 420, size: 4.1, spaceX: 260 },
        { distance: 4500, baseX: 575, baseY: 390, size: 3.8, spaceX: 525 },
      ];

      const TARGET_BASE = { baseX: 382, baseY: 305, size: 9.3 };

      let playing = false;
      let raf = null;
      let lastT = null;

      function el(name, attrs={}, parent=null) {
        const n = document.createElementNS(NS, name);
        for (const [k,v] of Object.entries(attrs)) n.setAttribute(k, String(v));
        if (parent) parent.appendChild(n);
        return n;
      }

      function clear(node) {
        while (node.firstChild) node.removeChild(node.firstChild);
      }

      function seeded(seed) {
        const x = Math.sin(seed * 912.73) * 43758.5453;
        return x - Math.floor(x);
      }

      function drawDust(group, count, width, height, seedBase, rMin, rMax, opacityScale=1) {
        clear(group);
        for (let i=0;i<count;i++) {
          const x = seeded(seedBase + i*2.71) * width;
          const y = seeded(seedBase + i*7.19) * height;
          const r = rMin + seeded(seedBase + i*11.31) * (rMax-rMin);
          const op = (.13 + seeded(seedBase + i*5.83)*.48) * opacityScale;
          el("circle", {cx:x,cy:y,r,fill:"#deedff",opacity:op}, group);
        }
      }

      drawDust(root.querySelector("#spaceDust"), 72, 760, 760, 21, .4, 1.45, .9);
      drawDust(root.querySelector("#skyDust"), 125, 760, 760, 83, .45, 1.75, 1);

      function earthPos(angle) {
        return {
          x: 380 + 250*Math.cos(angle),
          y: 610 + 82*Math.sin(angle)
        };
      }

      function distanceToSpaceY(d) {
        const minD = 120;
        const maxD = 4500;
        const t = Math.max(0, Math.min(1,
          (Math.log(d)-Math.log(minD)) / (Math.log(maxD)-Math.log(minD))
        ));
        return 405 - t*315;
      }

      function drawEarth(group, p, ghost=false) {
        clear(group);
        if (ghost) {
          el("circle", {cx:p.x,cy:p.y,r:10.5,fill:"#7bc2ff",opacity:.22}, group);
          return;
        }
        el("circle", {cx:p.x,cy:p.y,r:14,fill:"url(#earthGlow2)"}, group);
        el("circle", {cx:p.x-3.5,cy:p.y-2.2,r:2.7,fill:"#e2f5ff",opacity:.9}, group);
      }

      function starShape(parent,x,y,r,fill,opacity=1,glow=false,filterId="softGlow2") {
        const g = el("g",{opacity},parent);
        if (glow) {
          el("circle",{cx:x,cy:y,r:r*2.25,fill,opacity:.12,filter:`url(#${filterId})`},g);
        }
        const pts=[];
        for(let i=0;i<10;i++){
          const a=-Math.PI/2+i*Math.PI/5;
          const rr=i%2===0?r:r*.42;
          pts.push(`${x+rr*Math.cos(a)},${y+rr*Math.sin(a)}`);
        }
        el("polygon",{points:pts.join(" "),fill},g);
        return g;
      }

      function skyPos(star, angle, apply=true) {
        if (!apply) return {x:star.baseX,y:star.baseY};
        const amp = 15000 / star.distance;
        return {
          x: star.baseX - amp*Math.cos(angle),
          y: star.baseY - amp*.27*Math.sin(angle)
        };
      }

      function parallaxPath(star, parent, opacity, stroke) {
        const rx = 15000/star.distance;
        const ry = rx*.27;
        el("ellipse", {
          cx:star.baseX, cy:star.baseY,
          rx, ry,
          fill:"none",
          stroke,
          "stroke-width":1,
          "stroke-dasharray":"3 6",
          opacity
        }, parent);
      }

      function render() {
        const theta = Number(orbitRange.value)*Math.PI/180;
        const targetDistance = Number(distanceRange.value);
        const nowEarth = earthPos(theta);
        const oppositeEarth = earthPos(theta+Math.PI);

        drawEarth(earthCurrent, nowEarth, false);
        drawEarth(earthOpposite, oppositeEarth, true);

        clear(starLayer);
        clear(sightGroup);
        clear(skyStars);
        clear(skyGhosts);
        clear(skyPaths);

        const targetSpace = {
          x:380,
          y:distanceToSpaceY(targetDistance)
        };

        // depth layers: stars are all physically separate points
        BG_STARS.forEach((s) => {
          const y = distanceToSpaceY(s.distance);
          const eligible = s.distance >= targetDistance*1.8;

          if (eligible) {
            el("circle", {
              cx:s.spaceX, cy:y, r:12.5,
              fill:"none",
              stroke:"#78d6ff",
              "stroke-width":1.3,
              opacity:.46
            }, starLayer);
          }

          starShape(starLayer,s.spaceX,y,5.5,"#edf6ff",.95,false);
        });

        starShape(starLayer,targetSpace.x,targetSpace.y,10.2,"#ffd86a",1,true);

        if (sightToggle.checked) {
          el("line", {
            x1:nowEarth.x,y1:nowEarth.y,
            x2:targetSpace.x,y2:targetSpace.y,
            stroke:"#ffd86a",
            "stroke-width":1.6,
            opacity:.68
          }, sightGroup);

          el("line", {
            x1:oppositeEarth.x,y1:oppositeEarth.y,
            x2:targetSpace.x,y2:targetSpace.y,
            stroke:"#f4f8fb",
            "stroke-width":1.1,
            "stroke-dasharray":"4 6",
            opacity:.22
          }, sightGroup);
        }

        // apparent sky
        const targetStar = {
          distance:targetDistance,
          baseX:TARGET_BASE.baseX,
          baseY:TARGET_BASE.baseY,
          size:TARGET_BASE.size
        };

        parallaxPath(targetStar, skyPaths, .17, "#ffd86a");

        const targetNow = skyPos(targetStar,theta,true);
        const targetOpp = skyPos(targetStar,theta+Math.PI,true);

        el("circle", {
          cx:targetOpp.x,cy:targetOpp.y,r:5.8,
          fill:"#ffd86a",opacity:.22
        }, skyGhosts);

        BG_STARS.forEach((s) => {
          const apply = farParallax.checked;
          const now = skyPos(s,theta,apply);
          const opp = skyPos(s,theta+Math.PI,apply);
          const eligible = s.distance >= targetDistance*1.8;

          if (farParallax.checked) {
            parallaxPath(s, skyPaths, .08, "#d7e9f8");
            el("circle", {
              cx:opp.x,cy:opp.y,r:3,
              fill:"#ffffff",opacity:.13
            }, skyGhosts);
          }

          if (eligible) {
            el("circle", {
              cx:now.x,cy:now.y,r:11.3,
              fill:"none",
              stroke:"#78d6ff",
              "stroke-width":1.2,
              opacity:.42
            }, skyStars);
          }

          starShape(skyStars,now.x,now.y,s.size,"#eef7ff",.96,false,"skyGlow2");
        });

        starShape(skyStars,targetNow.x,targetNow.y,TARGET_BASE.size,"#ffd86a",1,true,"skyGlow2");
      }

      function setPlaying(next) {
        playing = next;
        playBtn.textContent = playing ? "Ⅱ" : "▶";
        playBtn.setAttribute("aria-label", playing ? "공전 일시정지" : "공전 재생");
        if (playing) {
          lastT = performance.now();
          raf = requestAnimationFrame(tick);
        } else if (raf) {
          cancelAnimationFrame(raf);
          raf = null;
        }
      }

      function tick(t) {
        if (!playing) return;
        const dt = Math.min(50,t-lastT);
        lastT=t;
        let deg=Number(orbitRange.value);
        deg=(deg+dt*.0105)%360;
        orbitRange.value=String(deg);
        render();
        raf=requestAnimationFrame(tick);
      }

      playBtn.addEventListener("click",()=>setPlaying(!playing));
      orbitRange.addEventListener("input",()=>{
        if(playing) setPlaying(false);
        render();
      });
      distanceRange.addEventListener("input",render);
      farParallax.addEventListener("change",render);
      sightToggle.addEventListener("change",render);

      if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        setPlaying(false);
      }

      render();
    })();
  </script>
</div>
"""

components.html(APP_HTML, height=1040, scrolling=False)
