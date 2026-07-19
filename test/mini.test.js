"use strict";

const { describe, it, beforeEach, afterEach, mock } = require("node:test");
const assert = require("node:assert");
const path = require("node:path");

const themeLoader = require("../src/theme-loader");
themeLoader.init(path.join(__dirname, "..", "src"));
const _defaultTheme = themeLoader.loadTheme("clawd");

function cloneTheme(theme) {
  return JSON.parse(JSON.stringify(theme));
}

function loadMiniWithElectron(screenExports) {
  const electronPath = require.resolve("electron");
  const miniPath = require.resolve("../src/mini");
  const previousElectron = Object.prototype.hasOwnProperty.call(require.cache, electronPath)
    ? require.cache[electronPath]
    : null;
  const previousMini = Object.prototype.hasOwnProperty.call(require.cache, miniPath)
    ? require.cache[miniPath]
    : null;

  require.cache[electronPath] = {
    id: electronPath,
    filename: electronPath,
    loaded: true,
    exports: {
      screen: screenExports,
    },
  };
  delete require.cache[miniPath];

  return {
    initMini: require("../src/mini"),
    restore() {
      if (previousElectron) require.cache[electronPath] = previousElectron;
      else delete require.cache[electronPath];
      if (previousMini) require.cache[miniPath] = previousMini;
      else delete require.cache[miniPath];
    },
  };
}

function makeCtx(theme, stateLog, initialX = 160) {
  const bounds = { x: initialX, y: 180, width: 120, height: 120 };
  return {
    theme,
    visualLog: [],
    currentState: "idle",
    win: {
      getBounds() { return { ...bounds }; },
      setBounds(next) {
        bounds.x = next.x;
        bounds.y = next.y;
        bounds.width = next.width;
        bounds.height = next.height;
      },
      setPosition(x, y) {
        bounds.x = x;
        bounds.y = y;
      },
      isDestroyed() { return false; },
    },
    doNotDisturb: false,
    bubbleFollowPet: false,
    pendingPermissions: [],
    currentSize: "m",
    mouseOverPet: false,
    SIZES: { m: { width: 120, height: 120 } },
    getCurrentPixelSize() { return { width: 120, height: 120 }; },
    getPetWindowBounds() { return { ...bounds }; },
    getAnimationAssetCycleMs(file) {
      if (file && file.includes("mini-enter")) return 1000;
      return null;
    },
    getBoundsSnapshot() { return { ...bounds }; },
    setViewportOffsetY() {},
    stopWakePoll() {},
    sendToRenderer() {},
    sendToHitWin() {},
    buildContextMenu() {},
    buildTrayMenu() {},
    syncHitWin() {},
    repositionBubbles() {},
    getNearestWorkArea() { return { x: 0, y: 0, width: 800, height: 600 }; },
    clampToScreenVisual(x, y, width, height) { return { x, y, width, height }; },
    resolveDisplayState() { return "idle"; },
    getSvgOverride() { return null; },
    applyState(state, file) {
      this.currentState = state;
      this.visualLog.push({ state, file: file || null });
      stateLog.push(state);
    },
  };
}

describe("mini drag detach", () => {
  let loader;

  beforeEach(() => {
    mock.timers.enable({ apis: ["setTimeout", "Date"] });
  });

  afterEach(() => {
    if (loader) loader.restore();
    mock.timers.reset();
    loader = null;
  });

  it("exits mini immediately and clears clipping without a jump animation", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const stateLog = [];
    const rendererEvents = [];
    const hitEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), stateLog, 700);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    ctx.sendToHitWin = (...args) => hitEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.restoreFromPrefs(
      { x: 700, y: 180, preMiniX: 200, preMiniY: 180, miniEdge: "right" },
      { width: 120, height: 120 },
    );

    assert.strictEqual(mini.exitMiniModeForDrag(), true);
    assert.strictEqual(mini.getMiniMode(), false);
    assert.strictEqual(mini.getMiniTransitioning(), false);
    assert.ok(rendererEvents.some((event) => event[0] === "mini-clip" && event[1] === null));
    assert.ok(rendererEvents.some((event) => event[0] === "mini-mode-change" && event[1] === false));
    assert.ok(hitEvents.some((event) => event[0] === "hit-state-sync"
      && event[1].miniMode === false && event[1].miniEdge === "right"));
    assert.deepStrictEqual(stateLog, ["idle"]);
  });

  it("lets a drag cancel an unfinished mini entry transition", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const stateLog = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), stateLog, 600);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    assert.strictEqual(mini.getMiniMode(), true);
    assert.strictEqual(mini.getMiniTransitioning(), true);

    assert.strictEqual(mini.exitMiniModeForDrag(), true);
    assert.strictEqual(mini.getMiniMode(), false);
    assert.strictEqual(mini.getMiniTransitioning(), false);

    mock.timers.tick(5000);
    assert.strictEqual(mini.getMiniMode(), false);
    assert.deepStrictEqual(stateLog, ["idle"]);
  });

  it("cancels an active peek animation before the drag snapshot is taken", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 700);
    const mini = loader.initMini(ctx);
    mini.restoreFromPrefs(
      { x: 700, y: 180, preMiniX: 200, preMiniY: 180, miniEdge: "right" },
      { width: 120, height: 120 },
    );

    mini.miniPeekIn();
    mock.timers.tick(80);
    assert.strictEqual(mini.getIsAnimating(), true);

    assert.strictEqual(mini.prepareForDrag(), true);
    const settledBounds = ctx.getBoundsSnapshot();
    assert.strictEqual(mini.getIsAnimating(), false);
    assert.strictEqual(settledBounds.x, mini.getCurrentMiniX());

    mock.timers.tick(300);
    assert.deepStrictEqual(ctx.getBoundsSnapshot(), settledBounds);
  });

  it("chooses left edge, right edge, or normal mode from the final X position", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const theme = cloneTheme(_defaultTheme);
    const left = loader.initMini(makeCtx(theme, [], 0));
    const center = loader.initMini(makeCtx(theme, [], 300));
    const right = loader.initMini(makeCtx(theme, [], 680));

    left.checkMiniModeSnap();
    center.checkMiniModeSnap();
    right.checkMiniModeSnap();

    assert.strictEqual(left.getMiniMode(), true);
    assert.strictEqual(left.getMiniEdge(), "left");
    assert.strictEqual(center.getMiniMode(), false);
    assert.strictEqual(right.getMiniMode(), true);
    assert.strictEqual(right.getMiniEdge(), "right");
  });
});

describe("mini mode entry timing", () => {
  let loader;

  beforeEach(() => {
    mock.timers.enable({ apis: ["setTimeout", "Date"] });
  });

  afterEach(() => {
    if (loader) loader.restore();
    mock.timers.reset();
    loader = null;
  });

  it("drag-snap entry slides to mini position first, then plays mini-enter", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const stateLog = [];
    const theme = cloneTheme(_defaultTheme);
    // Start away from the mini position so the 100ms slide is observable.
    const ctx = makeCtx(theme, stateLog, 600);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");

    // After the 100ms window slide: window is at mini position,
    // mini-enter has just been applied, enter animation is playing.
    mock.timers.tick(120);
    assert.deepStrictEqual(stateLog, ["mini-enter"]);
    assert.equal(ctx.getBoundsSnapshot().x, mini.getCurrentMiniX());
    assert.equal(mini.getMiniTransitioning(), true);

    // After the mini-enter animation settles (mocked to 1000ms).
    mock.timers.tick(1020);
    assert.deepStrictEqual(stateLog, ["mini-enter", "mini-idle"]);
    assert.equal(mini.getMiniTransitioning(), false);
    assert.equal(mini.getMiniMode(), true);
  });

  it("via-menu mini handoff preloads mini-enter offscreen before revealing the pet", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const stateLog = [];
    const theme = cloneTheme(_defaultTheme);
    const ctx = makeCtx(theme, stateLog, 710);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, true, "right");
    mock.timers.tick(360);

    assert.deepStrictEqual(stateLog, ["mini-enter"]);
    assert.notEqual(ctx.getBoundsSnapshot().x, mini.getCurrentMiniX());
    assert.equal(mini.getMiniTransitioning(), true);

    mock.timers.tick(300);
    assert.equal(ctx.getBoundsSnapshot().x, mini.getCurrentMiniX());

    mock.timers.tick(1020);

    assert.deepStrictEqual(stateLog, ["mini-enter", "mini-idle"]);
    assert.equal(mini.getMiniTransitioning(), false);
    assert.equal(mini.getMiniMode(), true);
  });

  it("via-menu crabwalk tells renderer to flip edge without entering mini layout early", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const stateLog = [];
    const rendererEvents = [];
    const theme = cloneTheme(_defaultTheme);
    const ctx = makeCtx(theme, stateLog, 710);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.enterMiniViaMenu();

    assert.deepStrictEqual(stateLog, ["mini-crabwalk"]);
    assert.deepStrictEqual(rendererEvents[0], [
      "mini-mode-change",
      true,
      "right",
      { preEntry: true, normalWalk: true },
    ]);
    assert.equal(mini.getMiniMode(), false);
    assert.equal(mini.getMiniTransitioning(), true);
  });

  it("uses a normal-size walk asset and hands off at the final mini X without a second jump", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const stateLog = [];
    const theme = cloneTheme(_defaultTheme);
    theme.miniMode.menuEntry = {
      walkFile: "running-right.webp",
      walkSpeed: 1,
      minDuration: 100,
      maxDuration: 1000,
      twirlThreshold: 9999,
    };
    const ctx = makeCtx(theme, stateLog, 400);
    const mini = loader.initMini(ctx);

    mini.enterMiniViaMenu();
    assert.deepStrictEqual(ctx.visualLog[0], {
      state: "mini-crabwalk",
      file: "running-right.webp",
    });

    mock.timers.tick(360);
    assert.deepStrictEqual(stateLog, ["mini-crabwalk", "mini-enter"]);
    assert.equal(ctx.getBoundsSnapshot().x, mini.getCurrentMiniX());
    assert.equal(mini.getMiniMode(), true);
    assert.equal(mini.getMiniTransitioning(), true);

    mock.timers.tick(1020);
    assert.deepStrictEqual(stateLog, ["mini-crabwalk", "mini-enter", "mini-idle"]);
    assert.equal(mini.getMiniTransitioning(), false);
  });

  it("plays one dedicated upright twirl asset during a long menu walk", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const rendererEvents = [];
    const theme = cloneTheme(_defaultTheme);
    theme.miniMode.menuEntry = {
      walkFile: "running-right.webp",
      twirlFile: "menu-twirl.webp",
      walkSpeed: 1,
      minDuration: 100,
      maxDuration: 1000,
      twirlThreshold: 200,
      twirlDuration: 100,
    };
    const ctx = makeCtx(theme, [], 400);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.enterMiniViaMenu();
    mock.timers.tick(180);
    assert.ok(ctx.visualLog.some((event) => event.state === "mini-crabwalk"
      && event.file === "menu-twirl.webp"));

    mock.timers.tick(220);
    assert.ok(ctx.visualLog.some((event) => event.state === "mini-crabwalk"
      && event.file === "running-right.webp"));
    assert.ok(rendererEvents.every((event) => !event[3] || event[3].twirl === undefined));
    assert.equal(mini.getMiniMode(), true);
  });

  it("drag-snap still plays full mini-enter even when the cursor is over the pet", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const stateLog = [];
    const theme = cloneTheme(_defaultTheme);
    const rightMiniX = 800 - Math.round(120 * (1 - theme.miniMode.offsetRatio));
    const ctx = makeCtx(theme, stateLog, rightMiniX);
    ctx.mouseOverPet = true;
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);
    assert.deepStrictEqual(stateLog, ["mini-enter"]);

    mock.timers.tick(1020);
    assert.deepStrictEqual(stateLog, ["mini-enter", "mini-idle"]);
    assert.equal(mini.getMiniTransitioning(), false);
    assert.equal(mini.getMiniMode(), true);
  });
});

describe("mini mode vertical dragging", () => {
  let loader;

  beforeEach(() => {
    mock.timers.enable({ apis: ["setTimeout", "Date"] });
  });

  afterEach(() => {
    if (loader) loader.restore();
    mock.timers.reset();
    loader = null;
  });

  it("locks X to the edge, updates Y, and clamps inside the attached work area", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);
    mock.timers.tick(1020);

    const start = ctx.getBoundsSnapshot();
    const snapshot = {
      cursor: { x: 700, y: 200 },
      bounds: { x: start.x, y: start.y },
      size: { width: start.width, height: start.height },
    };

    assert.equal(mini.moveWindowForDrag(snapshot, { x: 500, y: 340 }), true);
    assert.equal(ctx.getBoundsSnapshot().x, mini.getCurrentMiniX());
    assert.equal(ctx.getBoundsSnapshot().y, 320);
    assert.equal(mini.getMiniSnap().y, 320);

    assert.equal(mini.moveWindowForDrag(snapshot, { x: 500, y: 2000 }), true);
    assert.equal(ctx.getBoundsSnapshot().x, mini.getCurrentMiniX());
    assert.equal(ctx.getBoundsSnapshot().y, 480);
    assert.equal(mini.getMiniSnap().y, 480);
  });
});

// Two displays tiled side by side: D1 [0,800) and D2 [800,1600), same height.
const SIDE_BY_SIDE = [
  { bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } },
  { bounds: { x: 800, y: 0, width: 800, height: 600 }, workArea: { x: 800, y: 0, width: 800, height: 600 } },
];

function miniClips(rendererEvents) {
  return rendererEvents.filter((e) => e[0] === "mini-clip").map((e) => e[1]);
}

describe("mini mode multi-monitor seam clip", () => {
  let loader;

  beforeEach(() => {
    mock.timers.enable({ apis: ["setTimeout", "Date"] });
  });

  afterEach(() => {
    if (loader) loader.restore();
    mock.timers.reset();
    loader = null;
  });

  it("does not clip on a single display", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [{ bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } }];
      },
    });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);

    const clips = miniClips(rendererEvents);
    assert.ok(clips.length > 0, "expected mini-clip events");
    assert.ok(clips.every((c) => c === null), "single display must never clip");
  });

  it("clips the seam-crossing half at an internal monitor seam (right edge)", () => {
    loader = loadMiniWithElectron({ getAllDisplays() { return SIDE_BY_SIDE; } });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    // Pet lives on D1, snaps to D1's right edge — an internal seam with D2.
    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);

    const last = miniClips(rendererEvents).at(-1);
    assert.ok(last, "expected a non-null clip at the seam");
    assert.equal(last.edge, "right");
    // The window straddles the seam (original peek X) and the clip cuts at
    // D1's bounds edge (x=800): fraction is the visible part on D1.
    const expected = (800 - mini.getCurrentMiniX()) / 120;
    assert.ok(Math.abs(last.fraction - expected) < 1e-9, `fraction ${last.fraction} ≈ ${expected}`);
    assert.ok(last.fraction > 0 && last.fraction < 1, "clip keeps a partial window");
  });

  it("does not clip at the outer edge of the virtual desktop", () => {
    loader = loadMiniWithElectron({ getAllDisplays() { return SIDE_BY_SIDE; } });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 1400);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    // Pet on D2, snaps to D2's right edge — the outer edge, no neighbour.
    mini.enterMiniMode({ x: 800, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);

    const clips = miniClips(rendererEvents);
    assert.ok(clips.every((c) => c === null), "outer edge must not clip");
  });

  it("clips the left half at a left-side seam", () => {
    loader = loadMiniWithElectron({ getAllDisplays() { return SIDE_BY_SIDE; } });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 1000);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    // Pet on D2, snaps to D2's left edge — an internal seam with D1.
    mini.enterMiniMode({ x: 800, y: 0, width: 800, height: 600 }, false, "left");
    mock.timers.tick(120);

    const last = miniClips(rendererEvents).at(-1);
    assert.ok(last, "expected a non-null clip at the left seam");
    assert.equal(last.edge, "left");
    assert.ok(last.fraction > 0 && last.fraction < 1, "clip keeps a partial window");
  });

  it("does not clip when the neighbour does not overlap the pet's vertical band", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [
          { bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } },
          // Neighbour starts below the pet (pet's yMid ≈ 240, this display starts at y=400).
          { bounds: { x: 800, y: 400, width: 800, height: 600 }, workArea: { x: 800, y: 400, width: 800, height: 600 } },
        ];
      },
    });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);

    const clips = miniClips(rendererEvents);
    assert.ok(clips.every((c) => c === null), "no vertical overlap → no clip");
  });

  it("clears the clip when leaving mini mode", () => {
    loader = loadMiniWithElectron({ getAllDisplays() { return SIDE_BY_SIDE; } });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(1140);
    assert.ok(miniClips(rendererEvents).at(-1), "clip active while in contained mini");

    mini.exitMiniMode();
    mock.timers.tick(400);
    assert.equal(miniClips(rendererEvents).at(-1), null, "clip cleared on exit");
    assert.equal(mini.getMiniMode(), false);
  });

  it("clips at a seam on a secondary display with negative coordinates", () => {
    // D1 sits to the left of the origin: [-800,0). D2 is the primary [0,800).
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [
          { bounds: { x: -800, y: 0, width: 800, height: 600 }, workArea: { x: -800, y: 0, width: 800, height: 600 } },
          { bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } },
        ];
      },
    });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 60);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    // Pet on D2, snapping to D2's left edge — an internal seam with D1 at x=0.
    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "left");
    mock.timers.tick(120);

    const last = miniClips(rendererEvents).at(-1);
    assert.ok(last, "expected a non-null clip at the negative-coord seam");
    assert.equal(last.edge, "left");
    const expected = (0 - mini.getCurrentMiniX()) / 120;
    assert.ok(Math.abs(last.fraction - expected) < 1e-9, `fraction ${last.fraction} ≈ ${expected}`);
    assert.ok(last.fraction > 0 && last.fraction < 1, "clip keeps a partial window");
  });

  it("cuts the clip at the physical bounds edge, not the inset workArea", () => {
    // D1's workArea is narrower/shorter than its bounds (docks/panels). The
    // seam is the *physical* monitor boundary, so the clip must use bounds.
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [
          { bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 770, height: 560 } },
          { bounds: { x: 800, y: 0, width: 800, height: 600 }, workArea: { x: 830, y: 0, width: 770, height: 560 } },
        ];
      },
    });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 200);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    // Pet on D1, snapping to D1's right edge — seam with D2.
    mini.enterMiniMode({ x: 0, y: 0, width: 770, height: 560 }, false, "right");
    mock.timers.tick(120);

    const last = miniClips(rendererEvents).at(-1);
    assert.ok(last, "expected a non-null clip at the seam");
    assert.equal(last.edge, "right");
    // Seam is D1's bounds edge (x=800), not its workArea edge (x=770).
    const atBounds = (800 - mini.getCurrentMiniX()) / 120;
    const atWorkArea = (770 - mini.getCurrentMiniX()) / 120;
    assert.ok(Math.abs(last.fraction - atBounds) < 1e-9, `fraction ${last.fraction} ≈ ${atBounds}`);
    assert.ok(Math.abs(last.fraction - atWorkArea) > 1e-3, "must not cut at the workArea edge");
  });

  it("clips when a vertically offset neighbour still overlaps the pet's band", () => {
    loader = loadMiniWithElectron({
      getAllDisplays() {
        return [
          { bounds: { x: 0, y: 0, width: 800, height: 600 }, workArea: { x: 0, y: 0, width: 800, height: 600 } },
          // D2 shifted down 150px — still overlaps D1's vertical band at yMid≈240.
          { bounds: { x: 800, y: 150, width: 800, height: 600 }, workArea: { x: 800, y: 150, width: 800, height: 600 } },
        ];
      },
    });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);

    const last = miniClips(rendererEvents).at(-1);
    assert.ok(last, "vertically overlapping neighbour → clip");
    assert.equal(last.edge, "right");
    assert.ok(last.fraction > 0 && last.fraction < 1, "clip keeps a partial window");
  });

  it("restoreFromPrefs computes the seam without sending renderer IPC", () => {
    loader = loadMiniWithElectron({ getAllDisplays() { return SIDE_BY_SIDE; } });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    // Startup recovery of a contained mini on D1's right edge.
    const restored = mini.restoreFromPrefs(
      { x: 700, y: 180, preMiniX: 200, preMiniY: 180, miniEdge: "right" },
      { width: 120, height: 120 },
    );
    assert.equal(mini.getMiniMode(), true);
    // restore must not touch the renderer — the render window may not exist yet.
    assert.equal(miniClips(rendererEvents).length, 0, "restore sent no mini-clip IPC");
    const seam = mini.getContainedSeam();
    assert.ok(seam && seam.edge === "right", "seam state computed during restore");

    // Once the renderer is up, syncContainedClip re-sends the current clip.
    ctx.win.setBounds(restored);
    mini.syncContainedClip();
    const last = miniClips(rendererEvents).at(-1);
    assert.ok(last && last.edge === "right", "syncContainedClip re-sends the clip");
    assert.ok(last.fraction > 0 && last.fraction < 1, "re-sent clip keeps a partial window");
  });

  it("syncContainedClip is a no-op when the render window is absent", () => {
    loader = loadMiniWithElectron({ getAllDisplays() { return SIDE_BY_SIDE; } });
    const rendererEvents = [];
    const ctx = makeCtx(cloneTheme(_defaultTheme), [], 600);
    ctx.sendToRenderer = (...args) => rendererEvents.push(args);
    const mini = loader.initMini(ctx);

    mini.enterMiniMode({ x: 0, y: 0, width: 800, height: 600 }, false, "right");
    mock.timers.tick(120);
    rendererEvents.length = 0;

    ctx.win = null;
    assert.doesNotThrow(() => mini.syncContainedClip());
    assert.equal(rendererEvents.length, 0, "no IPC sent without a render window");
  });
});
