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
            padding-bottom: 0.6rem;
            max-width: 1600px;
        }
        header[data-testid="stHeader"] { height: 0; }
        #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r"""
<div id="parallax-app-v5">
  <style>
    #parallax-app-v5 {
      --border: rgba(255,255,255,.09);
      --text: #eaf2fb;
      --muted: #9cafc4;
      --accent: #78d6ff;
      --target: #ffd86a;
      width: 100%;
      padding-top: 8px;
      color: var(--text);
      font-family: Inter, Pretendard, "Noto Sans KR", system-ui, sans-serif;
      user-select: none;
    }

    #parallax-app-v5 * { box-sizing: border-box; }

    .sim-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 14px;
    }

    .sim-panel {
      position: relative;
      min-width: 0;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 18px;
      background: linear-gradient(180deg, #071525 0%, #050d18 100%);
    }

    .panel-tag {
      position: absolute;
      top: 18px;
      left: 16px;
      z-index: 3;
      padding: 5px 9px;
      border: 1px solid rgba(255,255,255,.09);
      border-radius: 999px;
      background: rgba(5,13,24,.64);
      color: rgba(235,243,251,.72);
      font-size: 12px;
      font-weight: 750;
      backdrop-filter: blur(6px);
    }

    svg { display: block; width: 100%; height: auto; }

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
      color: #fff;
      font-size: 19px;
      cursor: pointer;
    }

    .play-btn:hover { background: #1d385d; }

    .range-group {
      display: grid;
      grid-template-columns: auto 1fr;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }

    .mini-label {
      color: var(--muted);
      font-size: 12px;
      font-weight: 750;
      white-space: nowrap;
    }

    input[type="range"] {
      width: 100%;
      accent-color: #72cfff;
      cursor: pointer;
    }

    .toggle {
      display: flex;
      align-items: center;
      gap: 7px;
      min-height: 42px;
      padding: 7px 8px;
      border-radius: 10px;
      color: #b9c8d8;
      font-size: 12px;
      font-weight: 750;
      white-space: nowrap;
      cursor: pointer;
    }

    .toggle:hover { background: rgba(255,255,255,.035); }
    .toggle input { accent-color: #72cfff; }

    .legend-row {
      min-height: 26px;
      padding: 6px 4px 0;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 15px;
      color: rgba(205,220,235,.55);
      font-size: 10px;
    }

    .ring-key {
      display: inline-block;
      width: 11px;
      height: 11px;
      margin-right: 4px;
      border: 1.5px solid var(--accent);
      border-radius: 50%;
      vertical-align: -2px;
      opacity: .8;
    }

    .ghost-key {
      display: inline-block;
      width: 9px;
      height: 9px;
      margin-right: 4px;
      border-radius: 50%;
      background: rgba(255,255,255,.26);
      vertical-align: -1px;
    }

    .footnote {
      margin-top: 1px;
      text-align: right;
      color: rgba(205,220,235,.38);
      font-size: 9.5px;
      padding-right: 4px;
    }

    @media (max-width: 900px) {
      .sim-grid { grid-template-columns: 1fr; }
      .control-bar { grid-template-columns: auto 1fr; }
      .toggle { white-space: normal; }
    }
  </style>

  <div class="sim-grid">
    <section class="sim-panel">
      <div class="panel-tag">우주 공간</div>

      <svg id="spaceSvg" viewBox="0 0 760 900" role="img" aria-label="지구 공전과 연주시차의 공간 모형">
        <defs>
          <radialGradient id="sunGlow5">
            <stop offset="0%" stop-color="#fff8c9"/>
            <stop offset="40%" stop-color="#ffd46e"/>
            <stop offset="100%" stop-color="#f7963c"/>
          </radialGradient>
          <radialGradient id="earthGlow5">
            <stop offset="0%" stop-color="#c7ebff"/>
            <stop offset="100%" stop-color="#4f9fe9"/>
          </radialGradient>
          <filter id="softGlow5">
            <feGaussianBlur stdDeviation="4.5" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>

        <rect width="760" height="900" fill="#050d18"/>
        <g id="spaceDust"></g>

        <g opacity=".9">
          <rect x="62" y="166" width="636" height="148" rx="16"
                fill="#0b1a2c" opacity=".48"
                stroke="#c6d8e8" stroke-width="1" stroke-opacity=".08"/>
          <line x1="88" y1="240" x2="672" y2="240"
                stroke="#c6d8e8" stroke-width="1.2" opacity=".16"/>
          <g id="backgroundReferenceStars"></g>
        </g>

        <g id="leftInset"></g>

        <ellipse cx="380" cy="760" rx="220" ry="55"
                 fill="none" stroke="rgba(212,228,242,.22)" stroke-width="2"/>

        <g id="sightLines"></g>

        <g>
          <circle cx="380" cy="760" r="30" fill="url(#sunGlow5)" filter="url(#softGlow5)"/>
          <circle cx="380" cy="760" r="6" fill="#fffce2"/>
        </g>

        <g id="earthGhost"></g>
        <g id="earthNow"></g>
        <g id="targetSpaceStar"></g>
      </svg>
    </section>

    <section class="sim-panel">
      <div class="panel-tag">지구에서 본 하늘</div>

      <svg id="skySvg" viewBox="0 0 760 900" role="img" aria-label="지구에서 본 별의 연주시차">
        <defs>
          <filter id="skyGlow5">
            <feGaussianBlur stdDeviation="4" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>

        <rect width="760" height="900" fill="#040b15"/>
        <g id="skyDust"></g>
        <g id="skyReference"></g>
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
      <input id="orbitRange" type="range" min="0" max="360" step="0.2" value="210" aria-label="지구 공전 위치">
    </label>

    <label class="range-group">
      <span class="mini-label">별 거리</span>
      <input id="distanceRange" type="range" min="130" max="220" step="1" value="160" aria-label="주인공 별 거리">
    </label>

    <label class="toggle"><input id="farParallax" type="checkbox">먼 별 시차</label>
    <label class="toggle"><input id="sightToggle" type="checkbox" checked>시선</label>
  </div>

  <div class="legend-row">
    <span><span class="ring-key"></span>배경 기준으로 적합</span>
    <span><span class="ghost-key"></span>6개월 전</span>
  </div>

  <div class="footnote">거리와 각도는 이해를 위해 과장됨</div>

  <script>
    (() => {
      const root = document.getElementById("parallax-app-v5");
      if (!root || root.dataset.ready === "1") return;
      root.dataset.ready = "1";

      const NS = "http://www.w3.org/2000/svg";

      const backgroundReferenceStars = root.querySelector("#backgroundReferenceStars");
      const leftInset = root.querySelector("#leftInset");
      const sightLines = root.querySelector("#sightLines");
      const earthGhost = root.querySelector("#earthGhost");
      const earthNow = root.querySelector("#earthNow");
      const targetSpaceStar = root.querySelector("#targetSpaceStar");
      const skyReference = root.querySelector("#skyReference");
      const skyPaths = root.querySelector("#skyPaths");
      const skyGhosts = root.querySelector("#skyGhosts");
      const skyStars = root.querySelector("#skyStars");

      const orbitRange = root.querySelector("#orbitRange");
      const distanceRange = root.querySelector("#distanceRange");
      const farParallax = root.querySelector("#farParallax");
      const sightToggle = root.querySelector("#sightToggle");
      const playBtn = root.querySelector("#playBtn");

      // 실제 계산 좌표계
      // 태양 (0,0,0), 지구는 x-y 평면에서 반지름 1의 원운동,
      // 주인공 별은 공전면에 수직인 +z 방향에 둔다.
      // 따라서 주인공 별의 연주시차 궤적은 정확히 원이 된다.
      const EARTH_ORBIT_R = 1.0;
      const BACKGROUND_PLANE_Z = 300.0;

      // 왼쪽 공간 모형용 동일 좌표계의 직교 투영
      const SPACE_CX = 380;
      const SPACE_ORBIT_Y = 760;
      const SPACE_X_SCALE = 220;
      const SPACE_Y_SCALE = 55;
      const SPACE_Z_SCALE = (760 - 240) / BACKGROUND_PLANE_Z;

      // 오른쪽 천구 접평면
      const SKY_CX = 380;
      const SKY_CY = 450;
      const SKY_SCALE = 14500;

      // 왼쪽 위의 작은 천구 투영도 똑같은 각좌표를 사용
      const INSET_CX = 610;
      const INSET_CY = 95;
      const INSET_SCALE = 6200;

      // 실제 유한 거리를 가진 먼 별들.
      // a,b는 태양 기준 겉보기 각방향, d는 거리이다.
      const FAR_STARS = [
        { a:-0.0140, b:-0.0110, d:420,  size:4.1 },
        { a: 0.0115, b:-0.0135, d:700,  size:4.8 },
        { a:-0.0190, b: 0.0050, d:950,  size:3.8 },
        { a: 0.0200, b: 0.0100, d:1200, size:4.6 },
        { a:-0.0070, b: 0.0180, d:1500, size:3.7 },
        { a: 0.0050, b: 0.0160, d:1800, size:4.0 },
        { a: 0.0260, b:-0.0020, d:1100, size:3.6 },
        { a:-0.0250, b:-0.0010, d:1350, size:4.3 },
        { a: 0.0155, b: 0.0220, d:900,  size:3.5 },
        { a:-0.0165, b: 0.0240, d:1600, size:3.9 }
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
          el("circle", {cx:x, cy:y, r, fill:"#deedff", opacity:op}, group);
        }
      }

      drawDust(root.querySelector("#spaceDust"), 84, 760, 900, 21, .4, 1.45, .85);
      drawDust(root.querySelector("#skyDust"), 145, 760, 900, 83, .45, 1.75, 1);

      function earth3D(theta) {
        return {
          x: EARTH_ORBIT_R * Math.cos(theta),
          y: EARTH_ORBIT_R * Math.sin(theta),
          z: 0
        };
      }

      function projectSpace(p) {
        return {
          x: SPACE_CX + SPACE_X_SCALE * p.x,
          y: SPACE_ORBIT_Y + SPACE_Y_SCALE * p.y - SPACE_Z_SCALE * p.z
        };
      }

      function target3D(distance) {
        return {x:0, y:0, z:distance};
      }

      // 관측자(지구)에서 본 천구 접평면 좌표.
      // 왼쪽 교점/왼쪽 위/오른쪽 화면이 모두 이 계산에서 출발한다.
      function skyCoords(star, earth) {
        const dz = star.z - earth.z;
        return {
          x: (star.x - earth.x) / dz,
          y: (star.y - earth.y) / dz
        };
      }

      // 지구 -> 별 시선을 같은 직선으로 연장해 가상 먼 배경 평면과 만나는 점
      function linePlaneIntersection(earth, star, planeZ) {
        const dz = star.z - earth.z;
        const t = (planeZ - earth.z) / dz;
        return {
          x: earth.x + t * (star.x - earth.x),
          y: earth.y + t * (star.y - earth.y),
          z: planeZ
        };
      }

      function angularToSkyScreen(a) {
        return {x: SKY_CX + SKY_SCALE*a.x, y: SKY_CY + SKY_SCALE*a.y};
      }

      function angularToInset(a) {
        return {x: INSET_CX + INSET_SCALE*a.x, y: INSET_CY + INSET_SCALE*a.y};
      }

      function drawEarth(group, pos, ghost=false) {
        clear(group);
        const p = projectSpace(pos);

        if (ghost) {
          el("circle", {cx:p.x, cy:p.y, r:10, fill:"#7bc2ff", opacity:.22}, group);
          return;
        }

        el("circle", {cx:p.x, cy:p.y, r:14, fill:"url(#earthGlow5)"}, group);
        el("circle", {cx:p.x-3.5, cy:p.y-2.2, r:2.7, fill:"#e2f5ff", opacity:.9}, group);
      }

      function starShape(parent, x, y, r, fill, opacity=1, glow=false, filterId="softGlow5") {
        const g = el("g", {opacity}, parent);

        if (glow) {
          el("circle", {
            cx:x, cy:y, r:r*2.25,
            fill, opacity:.12,
            filter:`url(#${filterId})`
          }, g);
        }

        const pts = [];
        for (let i=0;i<10;i++) {
          const ang = -Math.PI/2 + i*Math.PI/5;
          const rr = i%2===0 ? r : r*.42;
          pts.push(`${x + rr*Math.cos(ang)},${y + rr*Math.sin(ang)}`);
        }
        el("polygon", {points:pts.join(" "), fill}, g);
        return g;
      }

      function drawCircle(parent, cx, cy, r, stroke, opacity, dash="3 6") {
        el("circle", {
          cx, cy, r,
          fill:"none",
          stroke,
          "stroke-width":1,
          "stroke-dasharray":dash,
          opacity
        }, parent);
      }

      function targetParallaxRadius(distance, scale) {
        return scale / distance;
      }

      function drawLeftReferenceStars() {
        clear(backgroundReferenceStars);
        const xs = [145, 255, 380, 505, 615];
        const rs = [4.4, 5.1, 4.1, 4.8, 4.2];
        xs.forEach((x,i) => starShape(backgroundReferenceStars, x, 240, rs[i], "#edf6ff", .88, false));
      }

      drawLeftReferenceStars();

      function render() {
        const theta = Number(orbitRange.value) * Math.PI / 180;
        const distance = Number(distanceRange.value);

        const earth = earth3D(theta);
        const earthOpp = earth3D(theta + Math.PI);
        const target = target3D(distance);

        // 주인공 별의 겉보기 좌표: 이 값이 모든 화면의 원본
        const targetAngular = skyCoords(target, earth);
        const targetAngularOpp = skyCoords(target, earthOpp);

        // 동일한 시선의 먼 배경 평면 교점
        const hit = linePlaneIntersection(earth, target, BACKGROUND_PLANE_Z);
        const hitOpp = linePlaneIntersection(earthOpp, target, BACKGROUND_PLANE_Z);

        const earthScreen = projectSpace(earth);
        const earthOppScreen = projectSpace(earthOpp);
        const targetScreen = projectSpace(target);
        const hitScreen = projectSpace(hit);
        const hitOppScreen = projectSpace(hitOpp);

        drawEarth(earthNow, earth, false);
        drawEarth(earthGhost, earthOpp, true);

        clear(targetSpaceStar);
        clear(sightLines);
        clear(leftInset);
        clear(skyReference);
        clear(skyPaths);
        clear(skyGhosts);
        clear(skyStars);

        // 왼쪽: 실제 공간 모형
        starShape(targetSpaceStar, targetScreen.x, targetScreen.y, 10, "#ffd86a", 1, true);

        if (sightToggle.checked) {
          // 직교 투영은 직선성을 보존하므로 지구-별-배경 교점이 한 직선에 놓인다.
          el("line", {
            x1:earthScreen.x, y1:earthScreen.y,
            x2:hitScreen.x, y2:hitScreen.y,
            stroke:"#ffd86a", "stroke-width":1.7, opacity:.76
          }, sightLines);

          el("line", {
            x1:earthOppScreen.x, y1:earthOppScreen.y,
            x2:hitOppScreen.x, y2:hitOppScreen.y,
            stroke:"#f5f8fb", "stroke-width":1.1,
            "stroke-dasharray":"4 6", opacity:.23
          }, sightLines);

          el("circle", {cx:hitScreen.x, cy:hitScreen.y, r:4, fill:"#ffd86a", opacity:.88}, sightLines);
          el("circle", {cx:hitOppScreen.x, cy:hitOppScreen.y, r:3.4, fill:"#ffffff", opacity:.25}, sightLines);
        }

        // 왼쪽 위: 오른쪽과 완전히 같은 targetAngular를 사용한 천구 투영
        const insetR = targetParallaxRadius(distance, INSET_SCALE);
        const insetNow = angularToInset(targetAngular);
        const insetOpp = angularToInset(targetAngularOpp);

        el("circle", {
          cx:INSET_CX, cy:INSET_CY,
          r:Math.max(46, insetR+14),
          fill:"#071525", opacity:.72,
          stroke:"#c5d7e8", "stroke-width":1, "stroke-opacity":.09
        }, leftInset);

        drawCircle(leftInset, INSET_CX, INSET_CY, insetR, "#ffd86a", .28);
        el("circle", {cx:insetOpp.x, cy:insetOpp.y, r:3.6, fill:"#ffd86a", opacity:.18}, leftInset);
        starShape(leftInset, insetNow.x, insetNow.y, 6.4, "#ffd86a", 1, true);

        // 오른쪽: 같은 targetAngular를 실제 관측 화면 좌표로 변환
        const targetSky = angularToSkyScreen(targetAngular);
        const targetSkyOpp = angularToSkyScreen(targetAngularOpp);
        const targetSkyR = targetParallaxRadius(distance, SKY_SCALE);

        drawCircle(skyPaths, SKY_CX, SKY_CY, targetSkyR, "#ffd86a", .23);
        el("circle", {cx:targetSkyOpp.x, cy:targetSkyOpp.y, r:5.5, fill:"#ffd86a", opacity:.20}, skyGhosts);

        // 실제 먼 별들: 체크 시 같은 지구 위치/같은 skyCoords 공식을 사용
        FAR_STARS.forEach((s) => {
          const star = {x:s.a*s.d, y:s.b*s.d, z:s.d};
          const fixedAngular = {x:s.a, y:s.b};
          const currentAngular = farParallax.checked ? skyCoords(star, earth) : fixedAngular;
          const oppositeAngular = farParallax.checked ? skyCoords(star, earthOpp) : fixedAngular;

          const current = angularToSkyScreen(currentAngular);
          const opposite = angularToSkyScreen(oppositeAngular);
          const candidate = s.d >= distance * 2.7;

          if (candidate) {
            el("circle", {
              cx:current.x, cy:current.y, r:10.5,
              fill:"none", stroke:"#78d6ff",
              "stroke-width":1.05, opacity:.28
            }, skyReference);
          }

          if (farParallax.checked) {
            const smallR = SKY_SCALE / s.d;
            drawCircle(
              skyPaths,
              SKY_CX + SKY_SCALE*s.a,
              SKY_CY + SKY_SCALE*s.b,
              smallR,
              "#d7e9f8",
              .065,
              "2 5"
            );

            el("circle", {
              cx:opposite.x, cy:opposite.y, r:2.8,
              fill:"#ffffff", opacity:.12
            }, skyGhosts);
          }

          starShape(skyStars, current.x, current.y, s.size, "#eef7ff", .96, false, "skyGlow5");
        });

        starShape(skyStars, targetSky.x, targetSky.y, 9.4, "#ffd86a", 1, true, "skyGlow5");
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
        const dt = Math.min(50, t-lastT);
        lastT = t;

        let deg = Number(orbitRange.value);
        deg = (deg + dt*.0105) % 360;
        orbitRange.value = String(deg);
        render();
        raf = requestAnimationFrame(tick);
      }

      playBtn.addEventListener("click", () => setPlaying(!playing));

      orbitRange.addEventListener("input", () => {
        if (playing) setPlaying(false);
        render();
      });

      distanceRange.addEventListener("input", render);
      farParallax.addEventListener("change", render);
      sightToggle.addEventListener("change", render);

      if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        setPlaying(false);
      }

      render();
    })();
  </script>
</div>
"""

components.html(APP_HTML, height=1190, scrolling=False)
