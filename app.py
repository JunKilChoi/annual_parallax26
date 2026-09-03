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
            padding-top: 0.45rem;
            padding-bottom: 0.5rem;
            max-width: 1500px;
        }
        header[data-testid="stHeader"] {
            height: 0;
        }
        #MainMenu, footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_HTML = r"""
<div id="parallax-app">
  <style>
    #parallax-app {
      --bg: #07111f;
      --panel: #0b1728;
      --panel2: #0e1d31;
      --line: rgba(255,255,255,.16);
      --muted: #8ea2ba;
      --text: #e9f1fa;
      --accent: #77d7ff;
      --target: #ffd76a;
      --earth: #66b7ff;
      --sun: #ffb24d;
      width: 100%;
      box-sizing: border-box;
      font-family: Inter, Pretendard, "Noto Sans KR", system-ui, sans-serif;
      color: var(--text);
      background: transparent;
      user-select: none;
    }

    #parallax-app * { box-sizing: border-box; }

    .sim-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 12px;
    }

    .sim-panel {
      position: relative;
      min-width: 0;
      background: linear-gradient(180deg, #091526 0%, #07111f 100%);
      border: 1px solid rgba(255,255,255,.10);
      border-radius: 18px;
      overflow: hidden;
    }

    .panel-tag {
      position: absolute;
      top: 12px;
      left: 14px;
      z-index: 3;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: .02em;
      color: rgba(233,241,250,.80);
      padding: 5px 9px;
      border-radius: 999px;
      background: rgba(7,17,31,.62);
      border: 1px solid rgba(255,255,255,.10);
      backdrop-filter: blur(5px);
    }

    svg {
      display: block;
      width: 100%;
      height: auto;
    }

    .control-bar {
      margin-top: 12px;
      display: grid;
      grid-template-columns: auto minmax(170px, 1.1fr) minmax(170px, 1fr) auto auto;
      gap: 12px;
      align-items: center;
      padding: 11px 12px;
      border-radius: 16px;
      background: #0a1627;
      border: 1px solid rgba(255,255,255,.10);
    }

    .play-btn {
      width: 46px;
      height: 46px;
      border: 0;
      border-radius: 14px;
      background: #162943;
      color: #fff;
      font-size: 20px;
      cursor: pointer;
    }

    .play-btn:hover { background: #1b3557; }

    .range-group {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 9px;
      align-items: center;
      min-width: 0;
    }

    .range-group .mini-label {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
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
      font-size: 12px;
      font-weight: 700;
      color: #b9c7d6;
      white-space: nowrap;
      cursor: pointer;
      padding: 8px 8px;
      border-radius: 10px;
    }

    .toggle:hover { background: rgba(255,255,255,.04); }
    .toggle input { accent-color: #72cfff; }

    .legend {
      margin-top: 7px;
      display: flex;
      gap: 14px;
      align-items: center;
      justify-content: flex-end;
      min-height: 18px;
      color: rgba(206,219,233,.66);
      font-size: 10.5px;
      padding-right: 4px;
    }

    .legend-ring {
      display: inline-block;
      width: 11px;
      height: 11px;
      border: 1.5px solid var(--accent);
      border-radius: 50%;
      vertical-align: -2px;
      margin-right: 4px;
    }

    .legend-ghost {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: rgba(255,255,255,.28);
      vertical-align: -1px;
      margin-right: 4px;
    }

    .note {
      margin-top: 3px;
      text-align: right;
      color: rgba(206,219,233,.40);
      font-size: 9.5px;
      padding-right: 3px;
    }

    @media (max-width: 900px) {
      .sim-grid { grid-template-columns: 1fr; }
      .control-bar {
        grid-template-columns: auto 1fr;
      }
      .range-group { grid-column: span 1; }
      .toggle { white-space: normal; }
    }
  </style>

  <div class="sim-grid">
    <section class="sim-panel">
      <div class="panel-tag">우주 공간</div>
      <svg id="spaceSvg" viewBox="0 0 700 520" role="img" aria-label="태양 주위를 공전하는 지구와 거리가 다른 별들">
        <defs>
          <radialGradient id="sunGlow">
            <stop offset="0%" stop-color="#fff2b8"/>
            <stop offset="45%" stop-color="#ffc35b"/>
            <stop offset="100%" stop-color="#ff8f36"/>
          </radialGradient>
          <radialGradient id="earthGlow">
            <stop offset="0%" stop-color="#b6e3ff"/>
            <stop offset="100%" stop-color="#4f9ee8"/>
          </radialGradient>
          <filter id="softGlow">
            <feGaussianBlur stdDeviation="4" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>

        <rect x="0" y="0" width="700" height="520" fill="#07111f"/>
        <g id="spaceDust" opacity=".62"></g>

        <g id="depthGuides" opacity=".18">
          <path d="M350 72 L350 430" stroke="#9fb3c9" stroke-dasharray="3 8"/>
          <path d="M135 430 C200 400 500 400 565 430" fill="none" stroke="#9fb3c9"/>
        </g>

        <ellipse cx="350" cy="390" rx="220" ry="72"
          fill="none" stroke="rgba(200,220,240,.25)" stroke-width="2"/>

        <g id="sightGroup" opacity="1"></g>

        <g id="sunGroup">
          <circle cx="350" cy="390" r="27" fill="url(#sunGlow)" filter="url(#softGlow)"/>
          <circle cx="350" cy="390" r="5" fill="#fff8d8"/>
        </g>

        <g id="earthOpposite"></g>
        <g id="earthCurrent"></g>

        <g id="starLayer"></g>
      </svg>
    </section>

    <section class="sim-panel">
      <div class="panel-tag">지구에서 본 하늘</div>
      <svg id="skySvg" viewBox="0 0 700 520" role="img" aria-label="지구의 위치에 따라 별의 겉보기 위치가 달라지는 밤하늘">
        <defs>
          <filter id="skyGlow">
            <feGaussianBlur stdDeviation="3.5" result="b"/>
            <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <rect x="0" y="0" width="700" height="520" fill="#050d19"/>
        <g id="skyDust"></g>
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
      <input id="distanceRange" type="range" min="35" max="850" step="1" value="95" aria-label="관측 별 거리">
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

  <div class="legend">
    <span><span class="legend-ring"></span>기준 가능</span>
    <span><span class="legend-ghost"></span>6개월 전</span>
  </div>
  <div class="note">거리와 시차는 수업용으로 과장하여 표시</div>

  <script>
    (() => {
      const root = document.getElementById("parallax-app");
      if (!root || root.dataset.ready === "1") return;
      root.dataset.ready = "1";

      const NS = "http://www.w3.org/2000/svg";
      const spaceSvg = root.querySelector("#spaceSvg");
      const skySvg = root.querySelector("#skySvg");
      const starLayer = root.querySelector("#starLayer");
      const sightGroup = root.querySelector("#sightGroup");
      const earthCurrent = root.querySelector("#earthCurrent");
      const earthOpposite = root.querySelector("#earthOpposite");
      const skyStars = root.querySelector("#skyStars");
      const skyGhosts = root.querySelector("#skyGhosts");
      const orbitRange = root.querySelector("#orbitRange");
      const distanceRange = root.querySelector("#distanceRange");
      const farParallax = root.querySelector("#farParallax");
      const sightToggle = root.querySelector("#sightToggle");
      const playBtn = root.querySelector("#playBtn");

      const BG_STARS = [
        { id: "A", distance: 135, baseX: 118, baseY: 152, size: 5.2 },
        { id: "B", distance: 255, baseX: 535, baseY: 112, size: 4.5 },
        { id: "C", distance: 510, baseX: 195, baseY: 352, size: 4.1 },
        { id: "D", distance: 1100, baseX: 560, baseY: 338, size: 3.8 }
      ];

      const targetBase = { id: "★", baseX: 354, baseY: 242, size: 8.4 };

      let playing = false;
      let raf = null;
      let lastT = null;
      let theta = Number(orbitRange.value) * Math.PI / 180;

      function el(name, attrs = {}, parent = null) {
        const node = document.createElementNS(NS, name);
        for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
        if (parent) parent.appendChild(node);
        return node;
      }

      function clear(node) {
        while (node.firstChild) node.removeChild(node.firstChild);
      }

      function seededRandom(seed) {
        let x = Math.sin(seed * 999.91) * 43758.5453;
        return x - Math.floor(x);
      }

      function drawDust(group, count, w, h, seedBase, minR, maxR) {
        clear(group);
        for (let i = 0; i < count; i++) {
          const x = seededRandom(seedBase + i * 3.11) * w;
          const y = seededRandom(seedBase + i * 7.47) * h;
          const r = minR + seededRandom(seedBase + i * 11.93) * (maxR - minR);
          const op = .18 + seededRandom(seedBase + i * 5.17) * .58;
          el("circle", { cx: x, cy: y, r, fill: "#dcecff", opacity: op }, group);
        }
      }

      drawDust(root.querySelector("#spaceDust"), 52, 700, 520, 20, .45, 1.5);
      drawDust(root.querySelector("#skyDust"), 92, 700, 520, 80, .45, 1.8);

      function earthPos(angle) {
        return {
          x: 350 + 220 * Math.cos(angle),
          y: 390 + 72 * Math.sin(angle)
        };
      }

      function distanceToSpaceY(d) {
        const minD = 35, maxD = 1100;
        const t = (Math.log(d) - Math.log(minD)) / (Math.log(maxD) - Math.log(minD));
        return 315 - Math.max(0, Math.min(1, t)) * 225;
      }

      function distanceToSpaceX(d, index) {
        const spread = [265, 440, 230, 485][index] ?? 350;
        return spread;
      }

      function drawEarth(group, pos, ghost=false) {
        clear(group);
        const opacity = ghost ? .26 : 1;
        el("circle", {
          cx: pos.x, cy: pos.y, r: ghost ? 10 : 13,
          fill: "url(#earthGlow)", opacity
        }, group);
        if (!ghost) {
          el("circle", {
            cx: pos.x - 3, cy: pos.y - 2, r: 2.5,
            fill: "#d8f4ff", opacity: .85
          }, group);
        }
      }

      function starSymbol(parent, x, y, r, fill, opacity=1, glow=false) {
        const g = el("g", { opacity }, parent);
        if (glow) {
          el("circle", { cx:x, cy:y, r:r*1.9, fill, opacity:.12, filter:"url(#softGlow)" }, g);
        }
        const pts = [];
        for (let i=0;i<10;i++) {
          const a = -Math.PI/2 + i*Math.PI/5;
          const rr = i%2===0 ? r : r*0.42;
          pts.push(`${x + rr*Math.cos(a)},${y + rr*Math.sin(a)}`);
        }
        el("polygon", { points: pts.join(" "), fill }, g);
        return g;
      }

      function skyPosition(star, angle, useParallax=true) {
        const d = star.distance;
        const amp = 1600 / d;
        const px = useParallax ? amp * Math.cos(angle) : 0;
        const py = useParallax ? amp * .32 * Math.sin(angle) : 0;
        return {
          x: star.baseX - px,
          y: star.baseY - py
        };
      }

      function render() {
        theta = Number(orbitRange.value) * Math.PI / 180;
        const targetDistance = Number(distanceRange.value);

        const eNow = earthPos(theta);
        const eOpp = earthPos(theta + Math.PI);
        drawEarth(earthCurrent, eNow, false);
        drawEarth(earthOpposite, eOpp, true);

        // LEFT: physical space
        clear(starLayer);
        clear(sightGroup);

        const targetSpace = {
          x: 350,
          y: distanceToSpaceY(targetDistance)
        };

        // subtle Sun-target axis
        el("line", {
          x1:350, y1:365, x2:targetSpace.x, y2:targetSpace.y + 10,
          stroke:"#cbd9e8", "stroke-width":1,
          "stroke-dasharray":"2 7", opacity:.13
        }, starLayer);

        // background/reference stars
        BG_STARS.forEach((s, i) => {
          const x = distanceToSpaceX(s.distance, i);
          const y = distanceToSpaceY(s.distance);
          const eligible = s.distance > targetDistance;

          if (eligible) {
            el("circle", {
              cx:x, cy:y, r:11,
              fill:"none", stroke:"#77d7ff",
              "stroke-width":1.5, opacity:.72
            }, starLayer);
          }
          starSymbol(starLayer, x, y, 5.4, "#eaf3ff", .96, false);
          el("text", {
            x:x+10, y:y+4, fill:"#b6c7d8",
            "font-size":"10", "font-weight":"700", opacity:.62
          }, starLayer).textContent = s.id;
        });

        // target star
        starSymbol(starLayer, targetSpace.x, targetSpace.y, 9.2, "#ffd76a", 1, true);

        if (sightToggle.checked) {
          // current and opposite 6-month sight lines to same target star
          el("line", {
            x1:eNow.x, y1:eNow.y, x2:targetSpace.x, y2:targetSpace.y,
            stroke:"#ffd76a", "stroke-width":1.6, opacity:.72
          }, sightGroup);
          el("line", {
            x1:eOpp.x, y1:eOpp.y, x2:targetSpace.x, y2:targetSpace.y,
            stroke:"#ffffff", "stroke-width":1.2,
            "stroke-dasharray":"4 5", opacity:.28
          }, sightGroup);
        }

        // RIGHT: apparent sky
        clear(skyStars);
        clear(skyGhosts);

        const targetStar = {
          ...targetBase,
          distance: targetDistance
        };

        const targetNow = skyPosition(targetStar, theta, true);
        const targetOpp = skyPosition(targetStar, theta + Math.PI, true);

        // target 6-month ghost
        el("circle", {
          cx:targetOpp.x, cy:targetOpp.y, r:5.8,
          fill:"#ffd76a", opacity:.24
        }, skyGhosts);
        el("line", {
          x1:targetOpp.x, y1:targetOpp.y, x2:targetNow.x, y2:targetNow.y,
          stroke:"#ffd76a", "stroke-width":1,
          "stroke-dasharray":"3 5", opacity:.24
        }, skyGhosts);

        BG_STARS.forEach((s) => {
          const useRealParallax = farParallax.checked;
          const now = skyPosition(s, theta, useRealParallax);
          const opp = skyPosition(s, theta + Math.PI, useRealParallax);
          const eligible = s.distance > targetDistance;

          if (farParallax.checked) {
            el("circle", {
              cx:opp.x, cy:opp.y, r:3.3,
              fill:"#ffffff", opacity:.16
            }, skyGhosts);
            el("line", {
              x1:opp.x, y1:opp.y, x2:now.x, y2:now.y,
              stroke:"#dfeeff", "stroke-width":.8,
              "stroke-dasharray":"2 4", opacity:.13
            }, skyGhosts);
          }

          if (eligible) {
            el("circle", {
              cx:now.x, cy:now.y, r:10.5,
              fill:"none", stroke:"#77d7ff",
              "stroke-width":1.3, opacity:.68
            }, skyStars);
          }

          starSymbol(skyStars, now.x, now.y, s.size, "#edf6ff", .96, false);
          el("text", {
            x:now.x+10, y:now.y+3,
            fill:"#b7c8d9", "font-size":"10", "font-weight":"700",
            opacity:.60
          }, skyStars).textContent = s.id;
        });

        starSymbol(skyStars, targetNow.x, targetNow.y, targetBase.size, "#ffd76a", 1, true);
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
        const dt = Math.min(50, t - lastT);
        lastT = t;
        let deg = Number(orbitRange.value);
        deg = (deg + dt * 0.012) % 360; // 약 30초에 한 바퀴
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

      const mq = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
      if (mq && mq.matches) setPlaying(false);

      render();
    })();
  </script>
</div>
"""

components.html(APP_HTML, height=820, scrolling=False)
