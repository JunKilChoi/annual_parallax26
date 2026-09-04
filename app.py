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
            padding-top: 1.15rem;
            padding-bottom: 0.5rem;
            max-width: 1580px;
        }
        header[data-testid="stHeader"] { height: 0; }
        #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r"""
<div id="parallax-app-v4">
  <style>
    #parallax-app-v4 {
      --border: rgba(255,255,255,.09);
      --text: #eaf2fb;
      --muted: #9cafc4;
      --accent: #78d6ff;
      --target: #ffd86a;
      width: 100%;
      color: var(--text);
      font-family: Inter, Pretendard, "Noto Sans KR", system-ui, sans-serif;
      user-select: none;
      padding-top: 6px;
    }
    #parallax-app-v4 * { box-sizing: border-box; }

    .sim-grid {
      display: grid;
      grid-template-columns: minmax(0,1fr) minmax(0,1fr);
      gap: 14px;
    }

    .sim-panel {
      position: relative;
      min-width: 0;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 18px;
      background: linear-gradient(180deg,#071525 0%,#050d18 100%);
    }

    .panel-tag {
      position: absolute;
      top: 18px;
      left: 16px;
      z-index: 2;
      padding: 5px 9px;
      border: 1px solid rgba(255,255,255,.09);
      border-radius: 999px;
      background: rgba(5,13,24,.62);
      color: rgba(235,243,251,.72);
      font-size: 12px;
      font-weight: 750;
      backdrop-filter: blur(6px);
    }

    svg { display:block; width:100%; height:auto; }

    .control-bar {
      margin-top: 12px;
      display: grid;
      grid-template-columns: auto minmax(220px,1.2fr) minmax(220px,1fr) auto auto;
      gap: 12px;
      align-items: center;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: 15px;
      background: #081525;
    }

    .play-btn {
      width: 46px;
      height: 46px;
      border: 0;
      border-radius: 13px;
      background: #172b46;
      color: white;
      font-size: 19px;
      cursor: pointer;
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

    @media (max-width:900px) {
      .sim-grid { grid-template-columns:1fr; }
      .control-bar { grid-template-columns:auto 1fr; }
      .toggle { white-space:normal; }
    }
  </style>

  <div class="sim-grid">
    <section class="sim-panel">
      <div class="panel-tag">우주 공간</div>

      <svg id="spaceSvg" viewBox="0 0 760 820" role="img"
           aria-label="태양 주위를 공전하는 지구와 연주시차의 기하학적 구조">
        <defs>
          <radialGradient id="sunGlow4">
            <stop offset="0%" stop-color="#fff8c9"/>
            <stop offset="40%" stop-color="#ffd46e"/>
            <stop offset="100%" stop-color="#f7963c"/>
          </radialGradient>
          <radialGradient id="earthGlow4">
            <stop offset="0%" stop-color="#c7ebff"/>
            <stop offset="100%" stop-color="#4f9fe9"/>
          </radialGradient>
          <filter id="softGlow4">
            <feGaussianBlur stdDeviation="4.5" result="b"/>
            <feMerge>
              <feMergeNode in="b"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        <rect width="760" height="820" fill="#050d18"/>
        <g id="spaceDust"></g>

        <!-- 왼쪽 상단: 같은 겉보기 위치를 원형 궤적으로 재표현 -->
        <g id="leftSkyInset"></g>

        <!-- 먼 배경별들이 놓인 기준선 -->
        <line id="backgroundLineSpace"
              x1="82" y1="190" x2="678" y2="190"
              stroke="#bdd0e1" stroke-width="1.2" opacity=".15"/>

        <ellipse cx="380" cy="680" rx="250" ry="82"
                 fill="none" stroke="rgba(212,228,242,.22)" stroke-width="2"/>

        <g id="sightGroup"></g>

        <g>
          <circle cx="380" cy="680" r="30"
                  fill="url(#sunGlow4)" filter="url(#softGlow4)"/>
          <circle cx="380" cy="680" r="6" fill="#fffce2"/>
        </g>

        <g id="earthOpposite"></g>
        <g id="earthCurrent"></g>
        <g id="starLayer"></g>
      </svg>
    </section>

    <section class="sim-panel">
      <div class="panel-tag">지구에서 본 하늘</div>

      <svg id="skySvg" viewBox="0 0 760 820" role="img"
           aria-label="지구의 위치에 따라 달라지는 별의 겉보기 위치">
        <defs>
          <filter id="skyGlow4">
            <feGaussianBlur stdDeviation="4" result="b"/>
            <feMerge>
              <feMergeNode in="b"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        <rect width="760" height="820" fill="#040b15"/>
        <g id="skyDust"></g>

        <line x1="92" y1="420" x2="668" y2="420"
              stroke="#c6d7e8" stroke-width="1" opacity=".10"/>

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
      <input id="orbitRange" type="range" min="0" max="360" step="0.2" value="205"
             aria-label="지구 공전 위치">
    </label>

    <label class="range-group">
      <span class="mini-label">별 거리</span>
      <input id="distanceRange" type="range" min="140" max="1600" step="1" value="320"
             aria-label="관측 별 거리">
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
      const root = document.getElementById("parallax-app-v4");
      if (!root || root.dataset.ready === "1") return;
      root.dataset.ready = "1";

      const NS = "http://www.w3.org/2000/svg";

      const starLayer = root.querySelector("#starLayer");
      const sightGroup = root.querySelector("#sightGroup");
      const earthCurrent = root.querySelector("#earthCurrent");
      const earthOpposite = root.querySelector("#earthOpposite");
      const leftSkyInset = root.querySelector("#leftSkyInset");

      const skyStars = root.querySelector("#skyStars");
      const skyGhosts = root.querySelector("#skyGhosts");
      const skyPaths = root.querySelector("#skyPaths");

      const orbitRange = root.querySelector("#orbitRange");
      const distanceRange = root.querySelector("#distanceRange");
      const farParallax = root.querySelector("#farParallax");
      const sightToggle = root.querySelector("#sightToggle");
      const playBtn = root.querySelector("#playBtn");

      const CX = 380;
      const ORBIT_CY = 680;
      const ORBIT_RX = 250;
      const ORBIT_RY = 82;

      const BG_Y_SPACE = 190;
      const BG_Y_SKY = 420;

      const SKY_SCALE = 0.42;
      const INSET_SCALE = 0.23;

      const BG_STARS = [
        { baseX:150, size:4.6 },
        { baseX:270, size:5.2 },
        { baseX:490, size:4.8 },
        { baseX:610, size:4.2 }
      ];

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

      drawDust(root.querySelector("#spaceDust"), 78, 760, 820, 21, .4, 1.45, .9);
      drawDust(root.querySelector("#skyDust"), 135, 760, 820, 83, .45, 1.75, 1);

      function earthPos(angle) {
        return {
          x: CX + ORBIT_RX*Math.cos(angle),
          y: ORBIT_CY + ORBIT_RY*Math.sin(angle)
        };
      }

      function targetSpaceY(distance) {
        const minD = 140;
        const maxD = 1600;
        const t = Math.max(0, Math.min(1, (distance-minD)/(maxD-minD)));
        return 455 - t*185;
      }

      function drawEarth(group, p, ghost=false) {
        clear(group);
        if (ghost) {
          el("circle", {
            cx:p.x, cy:p.y, r:10.5,
            fill:"#7bc2ff", opacity:.22
          }, group);
          return;
        }

        el("circle", {
          cx:p.x, cy:p.y, r:14,
          fill:"url(#earthGlow4)"
        }, group);

        el("circle", {
          cx:p.x-3.5, cy:p.y-2.2, r:2.7,
          fill:"#e2f5ff", opacity:.9
        }, group);
      }

      function starShape(parent,x,y,r,fill,opacity=1,glow=false,filterId="softGlow4") {
        const g = el("g",{opacity},parent);

        if (glow) {
          el("circle", {
            cx:x, cy:y, r:r*2.25,
            fill, opacity:.12,
            filter:`url(#${filterId})`
          }, g);
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

      // 왼쪽 주 시선의 실제 기하:
      // 지구 -> 주인공 별 직선을 먼 배경 기준선까지 정확히 연장한다.
      function sightIntersection(earth, target) {
        const dy = target.y - earth.y;
        if (Math.abs(dy) < 0.0001) {
          return { x: target.x, y: BG_Y_SPACE };
        }

        const t = (BG_Y_SPACE - earth.y) / dy;

        return {
          x: earth.x + t*(target.x-earth.x),
          y: BG_Y_SPACE
        };
      }

      // 특정 거리에서 시선 교점이 움직일 수 있는 최대 좌우 폭을 실제 왼쪽 기하로 계산
      function intersectionRadius(target) {
        let maxAbs = 1;

        for (let i=0;i<720;i++) {
          const a = i/720*Math.PI*2;
          const e = earthPos(a);
          const p = sightIntersection(e,target);
          maxAbs = Math.max(maxAbs, Math.abs(p.x-CX));
        }

        return maxAbs;
      }

      // 핵심:
      // 오른쪽 별 위치의 x는 왼쪽 시선-배경선 교점에서 직접 가져온다.
      // y는 같은 반지름 위에서 계산해 정확한 원을 만든다.
      function circularApparentVector(theta, intersectionX, radius) {
        const rawX = intersectionX-CX;
        const x = Math.max(-radius, Math.min(radius, rawX));
        const yMag = Math.sqrt(Math.max(0, radius*radius-x*x));

        let sign = -Math.sign(Math.sin(theta));
        if (sign === 0) sign = -1;

        return { x, y: sign*yMag };
      }

      function drawCirclePath(parent,cx,cy,r,stroke,opacity,dash="3 6") {
        el("circle", {
          cx, cy, r,
          fill:"none",
          stroke,
          "stroke-width":1,
          "stroke-dasharray":dash,
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
        clear(leftSkyInset);
        clear(skyStars);
        clear(skyGhosts);
        clear(skyPaths);

        const targetSpace = {
          x: CX,
          y: targetSpaceY(targetDistance)
        };

        // 배경별: 실제 우주 화면에서는 한 직선상
        BG_STARS.forEach((s) => {
          el("circle", {
            cx:s.baseX, cy:BG_Y_SPACE, r:11.2,
            fill:"none",
            stroke:"#78d6ff",
            "stroke-width":1.15,
            opacity:.32
          }, starLayer);

          starShape(
            starLayer,
            s.baseX,
            BG_Y_SPACE,
            5.2,
            "#edf6ff",
            .95,
            false
          );
        });

        starShape(
          starLayer,
          targetSpace.x,
          targetSpace.y,
          10.2,
          "#ffd86a",
          1,
          true
        );

        const sightNow = sightIntersection(nowEarth,targetSpace);
        const sightOpp = sightIntersection(oppositeEarth,targetSpace);
        const rawRadius = intersectionRadius(targetSpace);

        // 현재/6개월 후 시선은 별에서 멈추지 않고 배경선까지 계속 연결
        if (sightToggle.checked) {
          el("line", {
            x1:nowEarth.x, y1:nowEarth.y,
            x2:sightNow.x, y2:sightNow.y,
            stroke:"#ffd86a",
            "stroke-width":1.65,
            opacity:.74
          }, sightGroup);

          el("line", {
            x1:oppositeEarth.x, y1:oppositeEarth.y,
            x2:sightOpp.x, y2:sightOpp.y,
            stroke:"#f4f8fb",
            "stroke-width":1.1,
            "stroke-dasharray":"4 6",
            opacity:.24
          }, sightGroup);

          el("circle", {
            cx:sightNow.x, cy:sightNow.y, r:3.8,
            fill:"#ffd86a", opacity:.9
          }, sightGroup);

          el("circle", {
            cx:sightOpp.x, cy:sightOpp.y, r:3.2,
            fill:"#ffffff", opacity:.25
          }, sightGroup);
        }

        // 동일한 왼쪽 교점 계산으로 원형 겉보기 위치 벡터 생성
        const apparent = circularApparentVector(
          theta,
          sightNow.x,
          rawRadius
        );

        const apparentOpp = circularApparentVector(
          theta+Math.PI,
          sightOpp.x,
          rawRadius
        );

        // -------------------------------------------------
        // 왼쪽 상단: 같은 겉보기 위치를 작은 원 궤적으로 표시
        // -------------------------------------------------
        const insetCX = 380;
        const insetCY = 92;
        const insetR = Math.max(13, Math.min(64, rawRadius*INSET_SCALE));

        drawCirclePath(
          leftSkyInset,
          insetCX,
          insetCY,
          insetR,
          "#ffd86a",
          .28,
          "3 6"
        );

        el("circle", {
          cx: insetCX + apparentOpp.x*INSET_SCALE,
          cy: insetCY + apparentOpp.y*INSET_SCALE,
          r: 3.8,
          fill:"#ffd86a",
          opacity:.18
        }, leftSkyInset);

        starShape(
          leftSkyInset,
          insetCX + apparent.x*INSET_SCALE,
          insetCY + apparent.y*INSET_SCALE,
          6.7,
          "#ffd86a",
          1,
          true
        );

        // -------------------------------------------------
        // 오른쪽: 왼쪽 시선 교점과 동일한 값을 사용
        // -------------------------------------------------
        const skyCX = 380;
        const skyCY = BG_Y_SKY;
        const skyR = Math.max(20, Math.min(128, rawRadius*SKY_SCALE));

        drawCirclePath(
          skyPaths,
          skyCX,
          skyCY,
          skyR,
          "#ffd86a",
          .22,
          "3 6"
        );

        const skyNow = {
          x: skyCX + apparent.x*SKY_SCALE,
          y: skyCY + apparent.y*SKY_SCALE
        };

        const skyOpp = {
          x: skyCX + apparentOpp.x*SKY_SCALE,
          y: skyCY + apparentOpp.y*SKY_SCALE
        };

        el("circle", {
          cx:skyOpp.x,
          cy:skyOpp.y,
          r:5.6,
          fill:"#ffd86a",
          opacity:.20
        }, skyGhosts);

        // 배경 별은 기본적으로 같은 직선상.
        // 체크 시에만 아주 작은 실제 시차 원을 보여준다.
        BG_STARS.forEach((s, i) => {
          let bx = s.baseX;
          let by = BG_Y_SKY;

          if (farParallax.checked) {
            const smallR = 5.5;
            bx += -smallR*Math.cos(theta);
            by += -smallR*Math.sin(theta);

            drawCirclePath(
              skyPaths,
              s.baseX,
              BG_Y_SKY,
              smallR,
              "#d7e9f8",
              .07,
              "2 5"
            );

            el("circle", {
              cx:s.baseX + smallR*Math.cos(theta),
              cy:BG_Y_SKY + smallR*Math.sin(theta),
              r:2.7,
              fill:"#ffffff",
              opacity:.12
            }, skyGhosts);
          }

          el("circle", {
            cx:bx, cy:by, r:10.5,
            fill:"none",
            stroke:"#78d6ff",
            "stroke-width":1.05,
            opacity:.28
          }, skyStars);

          starShape(
            skyStars,
            bx,
            by,
            s.size,
            "#eef7ff",
            .96,
            false,
            "skyGlow4"
          );
        });

        starShape(
          skyStars,
          skyNow.x,
          skyNow.y,
          9.3,
          "#ffd86a",
          1,
          true,
          "skyGlow4"
        );
      }

      function setPlaying(next) {
        playing = next;
        playBtn.textContent = playing ? "Ⅱ" : "▶";
        playBtn.setAttribute(
          "aria-label",
          playing ? "공전 일시정지" : "공전 재생"
        );

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
        lastT = t;

        let deg = Number(orbitRange.value);
        deg = (deg + dt*.0105) % 360;
        orbitRange.value = String(deg);

        render();
        raf = requestAnimationFrame(tick);
      }

      playBtn.addEventListener("click",()=>setPlaying(!playing));

      orbitRange.addEventListener("input",()=>{
        if (playing) setPlaying(false);
        render();
      });

      distanceRange.addEventListener("input",render);
      farParallax.addEventListener("change",render);
      sightToggle.addEventListener("change",render);

      if (
        window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches
      ) {
        setPlaying(false);
      }

      render();
    })();
  </script>
</div>
"""

components.html(APP_HTML, height=1120, scrolling=False)
