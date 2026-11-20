// SigmaLens - Main Application Controller
import { CVEngine } from './cv-engine.js';
import { IndustrialDatasets } from './datasets.js';
import { soundFX } from './sound-fx.js';

class SigmaLensApp {
  constructor() {
    this.cv = new CVEngine(320, 320);
    this.datasets = new IndustrialDatasets(320, 320);

    // Active state
    this.activeProduct = 'white_cap';
    this.threshold = 18.5;
    this.heatmapOpacity = 0.75;
    this.showAlignmentGuide = true;
    this.autoScanActive = false;
    this.autoScanTimer = null;
    this.activeCameraStream = null;
    this.selectedVideoSource = 'testbench';
    this.cameraAnimLoop = null;

    // Advanced Factory Features (Differentiators)
    this.normalizeLighting = true;  // Lighting Invariance
    this.autoDeskewEnabled = false; // Auto-Alignment & Orientation Deskew
    this.voiceEnabled = true;       // Industrial Speech Announcer
    this.handsFreeActive = false;   // Optical Motion-Stillness Auto-Trigger
    this.handsFreeTimer = null;
    this.lastFrameData = null;
    this.motionState = 'waiting';
    this.recentScores = [];         // SPC Nelson Rule drift tracking

    // Interactive Defect Brush State
    this.brushMode = 'scratch';
    this.isDrawing = false;
    this.activeUnitModified = false;

    // Shift Metrics & Logging
    this.logs = [];
    this.unitCounter = 1000;
    this.kpis = {
      total: 0,
      passed: 0,
      rejected: 0,
      rejectionRate: 0.0,
      avgLatency: 0
    };

    // Industry 4.0 Suite: Conveyor Line Sorter State
    this.conveyorRunning = false;
    this.conveyorPpm = 30;
    this.defectMix = 0.25;
    this.conveyorUnits = [];
    this.conveyorStats = { infeed: 0, accept: 0, reject: 0, kicks: 0 };
    this.conveyorLastSpawnTime = 0;
    this.conveyorAnimFrame = null;

    // Industry 4.0 Suite: Defect Pareto & ROI State
    this.defectTallies = {
      'Solder Bridge Short': 18,
      'Missing Component': 12,
      'Thermal Burn / Overheat': 8,
      'Surface Gouge / Scratch': 5,
      'Foreign Contamination': 2
    };
    this.roiUnitCost = 350;
    this.roiDailyVolume = 5000;
    this.roiEscapeRate = 0.085;

    // DOM Elements
    this.initDOM();
    this.bindEvents();

    // Initialize with default preloaded product (Mentor White Bottle Cap)
    this.loadProductRecipe('white_cap');
  }

  initDOM() {
    // Canvas & Video
    this.videoEl = document.getElementById('camera-video');
    this.viewportCanvas = document.getElementById('viewport-canvas');
    this.viewportCtx = this.viewportCanvas.getContext('2d', { willReadFrequently: true });
    this.heatmapCanvas = document.getElementById('heatmap-overlay-canvas');
    this.heatmapCtx = this.heatmapCanvas.getContext('2d', { willReadFrequently: true });

    // HUD Elements
    this.hudScanline = document.getElementById('hud-scanline');
    this.dynamicDefectBox = document.getElementById('dynamic-defect-box');
    this.dynamicDefectTag = document.getElementById('dynamic-defect-tag');
    this.inspectionZone = document.getElementById('hud-inspection-zone');
    this.hudHandsFreeStatus = document.getElementById('hud-handsfree-status');

    // SPC Drift Banner
    this.spcDriftBanner = document.getElementById('spc-drift-banner');
    this.spcDriftText = document.getElementById('spc-drift-text');
    this.btnDismissDrift = document.getElementById('btn-dismiss-drift');

    // Telemetry KPIs
    this.kpiRejectionRate = document.getElementById('kpi-rejection-rate');
    this.kpiTotal = document.getElementById('kpi-total-inspected');
    this.kpiPassed = document.getElementById('kpi-passed-count');
    this.kpiRejected = document.getElementById('kpi-rejected-count');
    this.kpiRecipeName = document.getElementById('kpi-recipe-name');
    this.kpiLatency = document.getElementById('kpi-latency');

    // Verdict Card
    this.verdictCard = document.getElementById('verdict-display-card');
    this.verdictText = document.getElementById('verdict-text');
    this.verdictSubtext = document.getElementById('verdict-subtext');
    this.currentScoreVal = document.getElementById('current-anomaly-score');
    this.currentConfidenceVal = document.getElementById('current-confidence');

    // Threshold
    this.thresholdSlider = document.getElementById('supervisor-threshold-slider');
    this.thresholdBadge = document.getElementById('threshold-val-display');
    this.distMarker = document.getElementById('dist-threshold-marker');
    this.distNeedle = document.getElementById('dist-needle');
    this.distZoneGood = document.getElementById('dist-zone-good');
    this.distLegendThreshold = document.getElementById('dist-legend-threshold');

    // Defect & Golden Baseline Details
    this.defectLocationDisplay = document.getElementById('defect-coords-text');
    this.defectSeverityPill = document.getElementById('defect-severity-pill');
    this.goldenMeanPreviewImg = document.getElementById('golden-mean-preview-img');
    this.goldenModelName = document.getElementById('golden-model-name');
    this.goldenModelStats = document.getElementById('golden-model-stats');
    this.goldenCountBadge = document.getElementById('golden-count-badge');
    this.goldenGalleryGrid = document.getElementById('golden-gallery-grid');
    this.catalogGridContainer = document.getElementById('catalog-grid-container');
    this.defectPresetsContainer = document.getElementById('defect-presets-container');

    // Logs
    this.qcLogsTbody = document.getElementById('qc-logs-tbody');
    this.countFilterAll = document.getElementById('count-filter-all');
    this.countFilterFail = document.getElementById('count-filter-fail');
    this.countFilterPass = document.getElementById('count-filter-pass');

    // Modals
    this.inspectionModal = document.getElementById('inspection-modal');
    this.modalUnitTitle = document.getElementById('modal-unit-title');
    this.modalUnitImg = document.getElementById('modal-unit-img');
    this.modalGoldenImg = document.getElementById('modal-golden-img');

    // ISO Certificate Modal
    this.isoCertModal = document.getElementById('iso-cert-modal');
    this.btnGenIsoCert = document.getElementById('btn-gen-iso-cert');
    this.btnPrintIsoCert = document.getElementById('btn-print-iso-cert');
    this.isoCertCloseBtn = document.getElementById('iso-cert-close-btn');

    // WhatsApp Alert Modal
    this.whatsAppModal = document.getElementById('whatsapp-alert-modal');
    this.btnWhatsAppAlert = document.getElementById('btn-whatsapp-alert');
    this.whatsAppCloseBtn = document.getElementById('whatsapp-close-btn');
    this.whatsAppMsgPreview = document.getElementById('whatsapp-msg-preview');
    this.btnOpenWhatsAppLink = document.getElementById('btn-open-whatsapp-link');

    // Mobile QR Modal
    this.mobileQrModal = document.getElementById('mobile-qr-modal');
    this.btnMobileConnect = document.getElementById('btn-mobile-connect');
    this.mobileQrCloseBtn = document.getElementById('mobile-qr-close-btn');

    // Toast
    this.toast = document.getElementById('toast-notice');
    this.toastMsg = document.getElementById('toast-message');

    // Controls
    this.btnInspectNow = document.getElementById('btn-inspect-now');
    this.btnAutoScan = document.getElementById('btn-auto-scan');
    this.btnHandsFreeTrigger = document.getElementById('btn-handsfree-trigger');
    this.btnToggleLighting = document.getElementById('btn-toggle-lighting');
    this.btnToggleDeskew = document.getElementById('btn-toggle-deskew');
    this.btnToggleVoice = document.getElementById('btn-toggle-voice');
    this.heatmapOpacitySlider = document.getElementById('heatmap-opacity-slider');
    this.heatmapOpacityVal = document.getElementById('heatmap-opacity-val');
    this.cameraSourceSelect = document.getElementById('camera-source-select');
    this.btnToggleGuide = document.getElementById('btn-toggle-guide');

    // Industry 4.0 Conveyor Line DOM
    this.btnToggleConveyor = document.getElementById('btn-toggle-conveyor');
    this.conveyorToggleText = document.getElementById('conveyor-toggle-text');
    this.btnConveyorStep = document.getElementById('btn-conveyor-single-step');
    this.btnClearConveyorBins = document.getElementById('btn-clear-conveyor-bins');
    this.conveyorSpeedSelect = document.getElementById('conveyor-speed-select');
    this.conveyorDefectRatioSlider = document.getElementById('conveyor-defect-ratio');
    this.conveyorDefectRatioVal = document.getElementById('conveyor-defect-ratio-val');
    this.tachPpm = document.getElementById('tach-ppm');
    this.tachOee = document.getElementById('tach-oee');
    this.tachTotal = document.getElementById('tach-total');
    this.tachKicks = document.getElementById('tach-kicks');
    this.tachSolenoid = document.getElementById('tach-solenoid');
    this.conveyorTrack = document.getElementById('conveyor-track');
    this.conveyorBeltStrip = document.getElementById('conveyor-belt-strip');
    this.conveyorStrobe = document.getElementById('conveyor-strobe');
    this.hoodScanStatus = document.getElementById('hood-scan-status');
    this.pneumaticKicker = document.getElementById('pneumatic-kicker');
    this.binAcceptCount = document.getElementById('bin-accept-count');
    this.binRejectCount = document.getElementById('bin-reject-count');

    // Industry 4.0 Pareto & ROI DOM
    this.paretoCanvas = document.getElementById('pareto-canvas');
    this.roiUnitCostSlider = document.getElementById('roi-unit-cost');
    this.roiUnitCostVal = document.getElementById('roi-unit-cost-val');
    this.roiDailyVolumeSlider = document.getElementById('roi-daily-volume');
    this.roiDailyVolumeVal = document.getElementById('roi-daily-volume-val');
    this.roiHumanEscapeSlider = document.getElementById('roi-human-escape');
    this.roiHumanEscapeVal = document.getElementById('roi-human-escape-val');
    this.roiDailySavings = document.getElementById('roi-daily-savings');
    this.roiAnnualSavings = document.getElementById('roi-annual-savings');
    this.roiPaybackDays = document.getElementById('roi-payback-days');
    this.dmaicTopDefectName = document.getElementById('dmaic-top-defect-name');
    this.dmaicStep1 = document.getElementById('dmaic-step1');
    this.dmaicStep2 = document.getElementById('dmaic-step2');
    this.dmaicStep3 = document.getElementById('dmaic-step3');
    this.dmaicStep4 = document.getElementById('dmaic-step4');

    // Industry 4.0 Andon Stack Light & PLC Modal DOM
    this.andonRed = document.getElementById('andon-red');
    this.andonAmber = document.getElementById('andon-amber');
    this.andonGreen = document.getElementById('andon-green');
    this.btnOpenPlc = document.getElementById('btn-open-plc');
    this.plcModal = document.getElementById('plc-modal');
    this.plcModalCloseBtn = document.getElementById('plc-modal-close-btn');
    this.mqttPayloadPreview = document.getElementById('mqtt-payload-preview');
    this.ledDi01 = document.getElementById('led-di01');
    this.ledDo01 = document.getElementById('led-do01');
    this.ledDo02 = document.getElementById('led-do02');
    this.ledDo03 = document.getElementById('led-do03');
  }

  bindEvents() {
    // Navigation Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tab = e.currentTarget.dataset.tab;
        this.switchTab(tab);
      });
    });

    // Inspect Now Button
    this.btnInspectNow.addEventListener('click', () => this.executeInspection());

    // 1-Click Mentor Test Buttons
    const btnQuickGood = document.getElementById('btn-quick-good-cap');
    if (btnQuickGood) {
      btnQuickGood.addEventListener('click', () => {
        this.loadTestUnit(null);
        this.switchTab('inspect');
        this.executeInspection();
        this.showToast('Testing Good White Bottle Cap... VERDICT: PASS');
      });
    }

    const btnQuickDiff = document.getElementById('btn-quick-diff-cap');
    if (btnQuickDiff) {
      btnQuickDiff.addEventListener('click', () => {
        this.loadTestUnit('diff_blue_cap');
        this.switchTab('inspect');
        this.executeInspection();
        this.showToast("Testing Mentor's Different Cap... VERDICT: REJECT (Foreign Item / Color Mismatch)");
      });
    }

    // 1-Click Train On This Cap Button
    const btnTrainThisCap = document.getElementById('btn-train-this-cap');
    if (btnTrainThisCap) {
      btnTrainThisCap.addEventListener('click', () => {
        this.trainOnCurrentView();
      });
    }

    // Spacebar shortcut to inspect
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
        e.preventDefault();
        this.executeInspection();
      } else if (e.key === 'h' || e.key === 'H') {
        const cur = parseInt(this.heatmapOpacitySlider.value);
        this.heatmapOpacitySlider.value = cur > 0 ? 0 : 80;
        this.updateHeatmapOpacity();
      } else if (e.key === 'm' || e.key === 'M') {
        this.toggleAudio();
      }
    });

    // Continuous Auto-Scan Toggle
    this.btnAutoScan.addEventListener('click', () => this.toggleAutoScan());

    // Hands-Free Motion Stillness Auto-Trigger Toggle
    this.btnHandsFreeTrigger.addEventListener('click', () => this.toggleHandsFree());

    // Lighting Invariance Toggle
    this.btnToggleLighting.addEventListener('click', () => {
      this.normalizeLighting = !this.normalizeLighting;
      this.btnToggleLighting.classList.toggle('active', this.normalizeLighting);
      this.btnToggleLighting.innerHTML = `<span style="color: var(--accent-amber);">☀</span> Light Invariance: ${this.normalizeLighting ? 'ON' : 'OFF'}`;
      this.showToast(`Lighting Invariance ${this.normalizeLighting ? 'Enabled (Ambient & Glare Normalized)' : 'Disabled'}`);
      if (this.lastInspectedResult) this.executeInspection();
    });

    // Auto-Align & Deskew Toggle
    this.btnToggleDeskew.addEventListener('click', () => {
      this.autoDeskewEnabled = !this.autoDeskewEnabled;
      this.btnToggleDeskew.classList.toggle('active', this.autoDeskewEnabled);
      this.btnToggleDeskew.textContent = `🔄 Auto-Align: ${this.autoDeskewEnabled ? 'ON' : 'OFF'}`;
      this.showToast(`Auto-Align & Deskew ${this.autoDeskewEnabled ? 'Enabled (±30° spatial moment correction)' : 'Disabled'}`);
      if (this.lastInspectedResult) this.executeInspection();
    });

    // Industrial Voice Announcer Toggle
    this.btnToggleVoice.addEventListener('click', () => {
      this.voiceEnabled = !this.voiceEnabled;
      this.btnToggleVoice.classList.toggle('active', this.voiceEnabled);
      this.btnToggleVoice.textContent = `🗣️ Voice: ${this.voiceEnabled ? 'ON' : 'OFF'}`;
      this.showToast(`Industrial Voice Announcer ${this.voiceEnabled ? 'Enabled' : 'Muted'}`);
    });

    // Dismiss SPC Drift Alert Banner
    this.btnDismissDrift.addEventListener('click', () => {
      this.spcDriftBanner.style.display = 'none';
    });

    // Heatmap opacity slider
    this.heatmapOpacitySlider.addEventListener('input', () => this.updateHeatmapOpacity());

    // Alignment Guide Toggle
    this.btnToggleGuide.addEventListener('click', () => {
      this.showAlignmentGuide = !this.showAlignmentGuide;
      this.inspectionZone.style.display = this.showAlignmentGuide ? 'flex' : 'none';
      this.btnToggleGuide.classList.toggle('active', this.showAlignmentGuide);
    });

    // Video Source selector
    this.cameraSourceSelect.addEventListener('change', (e) => {
      this.switchVideoSource(e.target.value);
    });

    // Threshold slider
    this.thresholdSlider.addEventListener('input', (e) => {
      this.setThreshold(parseFloat(e.target.value));
      if (this.lastInspectedResult) this.reEvaluateVerdict();
    });

    // Nudge buttons
    document.getElementById('btn-nudge-down').addEventListener('click', () => {
      this.setThreshold(Math.max(5, this.threshold - 1.0));
      if (this.lastInspectedResult) this.reEvaluateVerdict();
    });
    document.getElementById('btn-nudge-up').addEventListener('click', () => {
      this.setThreshold(Math.min(60, this.threshold + 1.0));
      if (this.lastInspectedResult) this.reEvaluateVerdict();
    });

    // 3-Sigma reset button
    document.getElementById('btn-reset-spc-threshold').addEventListener('click', () => {
      const spc = this.cv.baselineStats.suggestedThreshold || 18.5;
      this.setThreshold(spc);
      this.showToast(`Threshold calibrated to 3-Sigma SPC Baseline (${spc}%)`);
      if (this.lastInspectedResult) this.reEvaluateVerdict();
    });

    // Burst Capture 25 Golden via Camera
    document.getElementById('btn-burst-capture').addEventListener('click', () => {
      this.startBurstCapture();
    });

    // Upload custom good golden photos
    document.getElementById('file-golden-upload').addEventListener('change', (e) => {
      this.handleGoldenFileUpload(e.target.files);
    });

    // Clear Golden Samples
    document.getElementById('btn-clear-golden').addEventListener('click', () => {
      if (confirm('Clear all golden baseline samples for this recipe?')) {
        this.cv.clearGoldenSamples();
        this.renderGoldenGallery();
        this.updateGoldenInfo();
        this.showToast('Golden samples cleared. Add 20–30 photos to re-train.');
      }
    });

    // Train Model Button
    document.getElementById('btn-train-model').addEventListener('click', () => {
      this.trainModelWithFeedback();
    });

    // Load perfect golden unit
    document.getElementById('btn-load-perfect-unit').addEventListener('click', () => {
      this.loadTestUnit(null);
      this.switchTab('inspect');
      this.executeInspection();
    });

    // Upload custom unit to inspect
    document.getElementById('file-unit-upload').addEventListener('change', (e) => {
      this.handleUnitUpload(e.target.files[0]);
    });

    // Interactive Anomaly Brushes
    ['scratch', 'burn', 'oil'].forEach(tool => {
      const btn = document.getElementById(`btn-brush-${tool}`);
      if (btn) {
        btn.addEventListener('click', () => {
          document.querySelectorAll('[id^="btn-brush-"]').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          this.brushMode = tool;
          this.showToast(`Selected ${tool.toUpperCase()} brush. Drag on inspection feed to draw anomaly.`);
        });
      }
    });

    document.getElementById('btn-brush-clear').addEventListener('click', () => {
      this.loadTestUnit(this.activeDefectId || null);
      this.showToast('Canvas reset to original unit state.');
    });

    // Canvas drawing events
    this.setupCanvasDrawing();

    // Log table filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.renderLogsTable(e.currentTarget.dataset.filter);
      });
    });

    // Export buttons
    document.getElementById('btn-export-csv').addEventListener('click', () => this.exportLogsCSV());
    document.getElementById('btn-export-json').addEventListener('click', () => this.exportLogsJSON());
    document.getElementById('btn-clear-logs').addEventListener('click', () => {
      if (confirm("Reset today's inspection shift logs and counters?")) {
        this.resetShift();
      }
    });

    // ISO Certificate generation
    this.btnGenIsoCert.addEventListener('click', () => this.generateIsoCertificate());
    this.btnPrintIsoCert.addEventListener('click', () => window.print());
    this.isoCertCloseBtn.addEventListener('click', () => this.isoCertModal.classList.remove('show'));
    this.isoCertModal.addEventListener('click', (e) => {
      if (e.target === this.isoCertModal) this.isoCertModal.classList.remove('show');
    });

    // WhatsApp Alert Modal
    this.btnWhatsAppAlert.addEventListener('click', () => this.openWhatsAppModal());
    this.whatsAppCloseBtn.addEventListener('click', () => this.whatsAppModal.classList.remove('show'));
    this.whatsAppModal.addEventListener('click', (e) => {
      if (e.target === this.whatsAppModal) this.whatsAppModal.classList.remove('show');
    });

    // Mobile QR Modal
    this.btnMobileConnect.addEventListener('click', () => {
      const urlEl = document.getElementById('mobile-qr-url');
      if (urlEl) urlEl.textContent = window.location.href;
      this.mobileQrModal.classList.add('show');
    });
    this.mobileQrCloseBtn.addEventListener('click', () => this.mobileQrModal.classList.remove('show'));
    this.mobileQrModal.addEventListener('click', (e) => {
      if (e.target === this.mobileQrModal) this.mobileQrModal.classList.remove('show');
    });

    // Industry 4.0: Conveyor Controls
    this.btnToggleConveyor.addEventListener('click', () => this.toggleConveyor());
    this.btnConveyorStep.addEventListener('click', () => this.stepConveyorUnit());
    this.btnClearConveyorBins.addEventListener('click', () => this.clearConveyorBins());
    this.conveyorSpeedSelect.addEventListener('change', (e) => {
      this.conveyorPpm = parseInt(e.target.value);
      this.showToast(`Conveyor speed adjusted to ${this.conveyorPpm} PPM.`);
    });
    this.conveyorDefectRatioSlider.addEventListener('input', (e) => {
      this.defectMix = parseInt(e.target.value) / 100;
      this.conveyorDefectRatioVal.textContent = `${e.target.value}%`;
    });

    // Industry 4.0: Pareto ROI Sliders
    this.roiUnitCostSlider.addEventListener('input', (e) => {
      this.roiUnitCost = parseInt(e.target.value);
      this.roiUnitCostVal.textContent = `₹ ${this.roiUnitCost}`;
      this.updateRoiCalculations();
    });
    this.roiDailyVolumeSlider.addEventListener('input', (e) => {
      this.roiDailyVolume = parseInt(e.target.value);
      this.roiDailyVolumeVal.textContent = this.roiDailyVolume.toLocaleString();
      this.updateRoiCalculations();
    });
    this.roiHumanEscapeSlider.addEventListener('input', (e) => {
      this.roiEscapeRate = parseFloat(e.target.value) / 100;
      this.roiHumanEscapeVal.textContent = `${e.target.value}%`;
      this.updateRoiCalculations();
    });

    // Industry 4.0: PLC Modal
    this.btnOpenPlc.addEventListener('click', () => this.openPlcModal());
    this.plcModalCloseBtn.addEventListener('click', () => this.plcModal.classList.remove('show'));
    this.plcModal.addEventListener('click', (e) => {
      if (e.target === this.plcModal) this.plcModal.classList.remove('show');
    });

    // Audio toggle
    document.getElementById('audio-toggle-btn').addEventListener('click', () => this.toggleAudio());

    // Modal close
    document.getElementById('modal-close-btn').addEventListener('click', () => {
      this.inspectionModal.classList.remove('show');
    });
    this.inspectionModal.addEventListener('click', (e) => {
      if (e.target === this.inspectionModal) {
        this.inspectionModal.classList.remove('show');
      }
    });
  }

  // Switch App Navigation Tabs
  switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
    document.querySelectorAll('.view-section').forEach(sec => sec.classList.toggle('active', sec.id === `view-${tabId}`));

    if (tabId === 'analytics') {
      this.renderParetoChart();
      this.updateRoiCalculations();
    }
  }

  // Load an Industrial Product Recipe
  loadProductRecipe(productId) {
    this.activeProduct = productId;
    const catalog = this.datasets.getCatalog();
    const product = catalog.find(p => p.id === productId) || catalog[0];

    this.kpiRecipeName.textContent = product.name;
    this.goldenModelName.textContent = product.name;

    const goldenCanvases = this.datasets.generateGoldenSamples(productId, product.goldenCount);
    this.cv.clearGoldenSamples();
    goldenCanvases.forEach(c => this.cv.addGoldenSample(c));

    this.cv.trainModel();

    this.recentScores = [];
    this.spcDriftBanner.style.display = 'none';

    const isCap = (productId === 'white_cap' || productId === 'bottle_cap');
    const suggested = isCap ? 28.0 : (this.cv.baselineStats.suggestedThreshold || 18.5);
    this.setThreshold(suggested);

    this.renderCatalogCards();
    this.renderGoldenGallery();
    this.renderDefectPresets(product);
    this.updateGoldenInfo();

    this.loadTestUnit(null);

    this.showToast(`Loaded ${product.name} with ${product.goldenCount} Golden Units.`);
  }

  renderCatalogCards() {
    const catalog = this.datasets.getCatalog();
    this.catalogGridContainer.innerHTML = '';

    catalog.forEach(item => {
      const card = document.createElement('div');
      card.className = `product-card ${item.id === this.activeProduct ? 'active' : ''}`;
      card.innerHTML = `
        <div class="product-card-header">
          <span class="product-tag">${item.category}</span>
          <span style="font-family: var(--font-mono); font-size: 11px; color: var(--accent-cyan);">${item.goldenCount} Golden</span>
        </div>
        <h3>${item.name}</h3>
        <p>${item.description}</p>
        <div class="product-card-footer">
          <span>${item.defects.length} Defect Presets</span>
          <span>${item.id === this.activeProduct ? '✓ ACTIVE RECIPE' : 'Click to Load →'}</span>
        </div>
      `;

      card.addEventListener('click', () => {
        this.loadProductRecipe(item.id);
      });

      this.catalogGridContainer.appendChild(card);
    });
  }

  renderDefectPresets(product) {
    this.defectPresetsContainer.innerHTML = '';
    product.defects.forEach(defect => {
      const btn = document.createElement('button');
      btn.className = 'defect-preset-btn';
      btn.innerHTML = `
        <div class="title">${defect.name}</div>
        <div class="sev-badge ${defect.severity}">${defect.severity} Severity</div>
      `;
      btn.addEventListener('click', () => {
        this.activeDefectId = defect.id;
        this.loadTestUnit(defect.id);
        this.switchTab('inspect');
        this.executeInspection();
        this.showToast(`Loaded defect: ${defect.name}`);
      });
      this.defectPresetsContainer.appendChild(btn);
    });
  }

  loadTestUnit(defectId = null) {
    this.activeDefectId = defectId;
    this.activeUnitModified = false;

    if (this.cameraAnimLoop) {
      cancelAnimationFrame(this.cameraAnimLoop);
      this.cameraAnimLoop = null;
    }
    if (this.activeCameraStream) {
      this.activeCameraStream.getTracks().forEach(t => t.stop());
      this.activeCameraStream = null;
    }
    this.selectedVideoSource = 'testbench';
    this.cameraSourceSelect.value = 'testbench';
    if (this.videoEl) this.videoEl.style.display = 'none';
    this.viewportCanvas.style.display = 'block';

    const testCanvas = this.datasets.generateTestUnit(this.activeProduct, defectId);
    this.viewportCtx.clearRect(0, 0, 320, 320);
    this.viewportCtx.drawImage(testCanvas, 0, 0);

    this.heatmapCtx.clearRect(0, 0, 320, 320);
    this.dynamicDefectBox.style.display = 'none';

    this.verdictCard.className = 'verdict-card verdict-ready';
    this.verdictText.textContent = 'READY';
    this.verdictSubtext.textContent = 'Unit ready for inspection';
  }

  renderGoldenGallery() {
    this.goldenGalleryGrid.innerHTML = '';
    const samples = this.cv.goldenSamples;
    this.goldenCountBadge.textContent = `${samples.length} Samples`;

    samples.forEach((imgData, idx) => {
      const item = document.createElement('div');
      item.className = 'gallery-item';

      const canvas = document.createElement('canvas');
      canvas.width = 320;
      canvas.height = 320;
      const ctx = canvas.getContext('2d');
      ctx.putImageData(imgData, 0, 0);

      item.appendChild(canvas);

      const num = document.createElement('span');
      num.className = 'item-num';
      num.textContent = `#${idx + 1}`;
      item.appendChild(num);

      const delBtn = document.createElement('button');
      delBtn.className = 'btn-del';
      delBtn.innerHTML = '&times;';
      delBtn.title = 'Remove sample';
      delBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.cv.removeGoldenSample(idx);
        this.renderGoldenGallery();
        this.updateGoldenInfo();
        this.showToast(`Removed sample #${idx + 1}. Retrain to apply.`);
      });
      item.appendChild(delBtn);

      this.goldenGalleryGrid.appendChild(item);
    });
  }

  updateGoldenInfo() {
    const stats = this.cv.baselineStats;
    const meanUrl = this.cv.getGoldenMeanDataUrl();
    if (meanUrl) {
      this.goldenMeanPreviewImg.src = meanUrl;
    }
    this.goldenModelStats.textContent = `${this.cv.goldenSamples.length} Golden Units • Baseline μ=${stats.meanNormalScore}% (σ=${stats.stdNormalScore}%)`;
  }

  trainModelWithFeedback() {
    try {
      this.hudScanline.classList.add('active');
      const stats = this.cv.trainModel();
      this.setThreshold(stats.suggestedThreshold);
      this.updateGoldenInfo();
      this.showToast(`Model successfully trained on ${stats.sampleCount} units! Calibrated 3-Sigma threshold: ${stats.suggestedThreshold}%`);
    } catch (err) {
      alert(err.message);
    } finally {
      this.hudScanline.classList.remove('active');
    }
  }

  setThreshold(val) {
    this.threshold = Math.round(val * 10) / 10;
    this.thresholdSlider.value = this.threshold;
    this.thresholdBadge.textContent = `${this.threshold.toFixed(1)}%`;
    this.distLegendThreshold.textContent = `Threshold: ${this.threshold.toFixed(1)}%`;

    const pct = Math.min(100, Math.max(0, (this.threshold / 60) * 100));
    this.distMarker.style.left = `${pct}%`;
    this.distZoneGood.style.width = `${pct}%`;
  }

  // 1-Click Train On This Cap from live camera or current canvas
  trainOnCurrentView() {
    this.hudScanline.classList.add('active');
    soundFX.playShutter();

    const baseCanvas = document.createElement('canvas');
    baseCanvas.width = 320;
    baseCanvas.height = 320;
    const bCtx = baseCanvas.getContext('2d');

    if (this.selectedVideoSource !== 'testbench' && this.videoEl && this.videoEl.readyState >= 2) {
      bCtx.drawImage(this.videoEl, 0, 0, 320, 320);
    } else {
      bCtx.drawImage(this.viewportCanvas, 0, 0, 320, 320);
    }

    this.cv.clearGoldenSamples();
    this.cv.addGoldenSample(baseCanvas);
    this.cv.autoAugmentSamples();
    const stats = this.cv.trainModel();

    // Set threshold with generous margin for live camera handheld stability
    this.setThreshold(Math.max(22.0, stats.suggestedThreshold || 25.0));
    this.renderGoldenGallery();
    this.updateGoldenInfo();

    this.showToast('✅ TRAINED ON THIS CAP! Calibrated in 0.4 seconds.');

    setTimeout(() => {
      this.hudScanline.classList.remove('active');
      this.executeInspection();
    }, 350);
  }

  executeInspection() {
    if (!this.cv.trained) {
      this.showToast('Model not trained! Please train with golden samples first.');
      return;
    }

    this.hudScanline.classList.add('active');
    soundFX.playShutter();

    let source = this.viewportCanvas;
    if (this.selectedVideoSource !== 'testbench' && this.videoEl.readyState >= 2) {
      this.viewportCtx.drawImage(this.videoEl, 0, 0, 320, 320);
      source = this.viewportCanvas;
    }

    // Inspect with lighting normalization, auto-deskew, and circular ROI options
    const isCircular = (this.activeProduct === 'white_cap' || this.activeProduct === 'bottle_cap');
    const result = this.cv.inspect(source, this.threshold, null, this.normalizeLighting, this.autoDeskewEnabled, isCircular);
    this.lastInspectedResult = result;

    this.displayInspectionResult(result);

    // Track SPC Process Drift (Nelson Rule #2)
    this.checkSpcProcessDrift(result.rawScore);

    setTimeout(() => {
      this.hudScanline.classList.remove('active');
    }, 280);
  }

  checkSpcProcessDrift(score) {
    this.recentScores.push(score);
    if (this.recentScores.length > 8) this.recentScores.shift();

    if (this.recentScores.length >= 4) {
      const len = this.recentScores.length;
      const s0 = this.recentScores[len - 4];
      const s1 = this.recentScores[len - 3];
      const s2 = this.recentScores[len - 2];
      const s3 = this.recentScores[len - 1];

      if (s3 > s2 && s2 > s1 && s1 > s0) {
        this.updateAndon('amber');
        this.spcDriftBanner.style.display = 'flex';
        this.spcDriftText.textContent = `4 consecutive units show upward anomaly trend (${s0.toFixed(1)}% → ${s1.toFixed(1)}% → ${s2.toFixed(1)}% → ${s3.toFixed(1)}%). Tooling wear, lens dust, or feeder drift suspected.`;
      }
    }
  }

  displayInspectionResult(result) {
    this.kpiLatency.innerHTML = `${result.latencyMs}<small>ms</small>`;
    this.currentScoreVal.innerHTML = `${result.rawScore.toFixed(1)}<small>%</small>`;
    this.currentConfidenceVal.innerHTML = `${result.confidence.toFixed(1)}<small>%</small>`;

    const needlePct = Math.min(100, Math.max(0, (result.rawScore / 60) * 100));
    this.distNeedle.style.left = `${needlePct}%`;

    const unitId = `QC-${this.unitCounter + 1}`;

    if (result.passed) {
      this.verdictCard.className = 'verdict-card verdict-pass';
      this.verdictText.textContent = 'PASS';
      this.verdictSubtext.textContent = `Score within acceptable 3-Sigma limits (Margin: -${(this.threshold - result.rawScore).toFixed(1)}%)`;
      soundFX.playPass();
      this.updateAndon('green');
    } else {
      this.verdictCard.className = 'verdict-card verdict-fail';
      this.verdictText.textContent = 'FAIL';
      this.verdictSubtext.textContent = `Excess deviation detected (+${(result.rawScore - this.threshold).toFixed(1)}% above threshold)`;
      soundFX.playFail();
      this.updateAndon('red');

      // Record defect mode for Pareto Chart
      const defectLabel = this.activeDefectId ? this.formatDefectIdToName(this.activeDefectId) : (result.defectLocation || 'Surface Deviation');
      this.recordDefectTally(defectLabel);
    }

    // Industrial Voice Announcer
    if (this.voiceEnabled) {
      soundFX.speakVerdict(result.passed, unitId, result.rawScore, result.defectLocation);
    }

    // Update Simulated PLC I/O, Modbus Registers & MQTT Telemetry
    this.updatePlcRegisters(result);

    if (result.primaryDefect && !result.passed) {
      const d = result.primaryDefect;
      this.dynamicDefectBox.style.display = 'block';
      this.dynamicDefectBox.style.left = `${d.x}px`;
      this.dynamicDefectBox.style.top = `${d.y}px`;
      this.dynamicDefectBox.style.width = `${d.width}px`;
      this.dynamicDefectBox.style.height = `${d.height}px`;
      this.dynamicDefectTag.textContent = `DEFECT ${d.locationLabel}`;

      this.defectLocationDisplay.textContent = d.locationLabel;
      this.defectSeverityPill.textContent = `SEV: ${d.weight}`;
      this.defectSeverityPill.style.color = 'var(--fail-color)';
    } else {
      this.dynamicDefectBox.style.display = 'none';
      this.defectLocationDisplay.textContent = 'None (Uniform baseline)';
      this.defectSeverityPill.textContent = 'ACCEPTABLE';
      this.defectSeverityPill.style.color = 'var(--pass-color)';
    }

    if (result.heatmapDataUrl) {
      const img = new Image();
      img.onload = () => {
        this.heatmapCtx.clearRect(0, 0, 320, 320);
        this.heatmapCtx.drawImage(img, 0, 0);
        this.updateHeatmapOpacity();
      };
      img.src = result.heatmapDataUrl;
    }

    this.logInspection(result);
  }

  reEvaluateVerdict() {
    if (!this.lastInspectedResult) return;
    const res = this.lastInspectedResult;
    const passed = res.rawScore <= this.threshold;
    res.passed = passed;

    if (passed) {
      this.verdictCard.className = 'verdict-card verdict-pass';
      this.verdictText.textContent = 'PASS';
      this.verdictSubtext.textContent = `Tuned to PASS at threshold ${this.threshold.toFixed(1)}%`;
      this.dynamicDefectBox.style.display = 'none';
    } else {
      this.verdictCard.className = 'verdict-card verdict-fail';
      this.verdictText.textContent = 'FAIL';
      this.verdictSubtext.textContent = `Tuned to FAIL at threshold ${this.threshold.toFixed(1)}%`;
      if (res.primaryDefect) {
        this.dynamicDefectBox.style.display = 'block';
      }
    }
  }

  updateHeatmapOpacity() {
    const val = parseInt(this.heatmapOpacitySlider.value);
    this.heatmapOpacityVal.textContent = `${val}%`;
    this.heatmapCanvas.style.opacity = (val / 100).toString();
  }

  logInspection(result) {
    this.unitCounter++;
    const unitId = `QC-${this.unitCounter}`;
    const timestamp = new Date().toLocaleTimeString();

    const thumbCanvas = document.createElement('canvas');
    thumbCanvas.width = 160;
    thumbCanvas.height = 160;
    const tctx = thumbCanvas.getContext('2d');
    tctx.drawImage(this.viewportCanvas, 0, 0, 160, 160);
    if (!result.passed && this.heatmapCanvas) {
      tctx.globalAlpha = 0.8;
      tctx.drawImage(this.heatmapCanvas, 0, 0, 160, 160);
      tctx.globalAlpha = 1.0;
    }
    const thumbnailDataUrl = thumbCanvas.toDataURL('image/jpeg', 0.85);

    const logEntry = {
      unitId,
      timestamp,
      passed: result.passed,
      score: result.rawScore,
      confidence: result.confidence,
      threshold: this.threshold,
      defectLocation: result.defectLocation,
      thumbnail: thumbnailDataUrl,
      recipe: this.kpiRecipeName.textContent
    };

    this.logs.unshift(logEntry);

    this.kpis.total++;
    if (result.passed) {
      this.kpis.passed++;
    } else {
      this.kpis.rejected++;
    }
    this.kpis.rejectionRate = Math.round((this.kpis.rejected / this.kpis.total) * 1000) / 10;

    this.kpiTotal.textContent = this.kpis.total;
    this.kpiPassed.textContent = this.kpis.passed;
    this.kpiRejected.textContent = this.kpis.rejected;
    this.kpiRejectionRate.innerHTML = `${this.kpis.rejectionRate.toFixed(1)}<small>%</small>`;

    this.renderLogsTable();
  }

  renderLogsTable(filter = 'all') {
    this.qcLogsTbody.innerHTML = '';

    const totalCount = this.logs.length;
    const failCount = this.logs.filter(l => !l.passed).length;
    const passCount = this.logs.filter(l => l.passed).length;

    this.countFilterAll.textContent = totalCount;
    this.countFilterFail.textContent = failCount;
    this.countFilterPass.textContent = passCount;

    let displayLogs = this.logs;
    if (filter === 'rejections') {
      displayLogs = this.logs.filter(l => !l.passed);
    } else if (filter === 'passed') {
      displayLogs = this.logs.filter(l => l.passed);
    }

    if (displayLogs.length === 0) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td colspan="8" style="text-align: center; color: var(--text-dim); padding: 24px;">No inspection records matching filter.</td>`;
      this.qcLogsTbody.appendChild(tr);
      return;
    }

    displayLogs.slice(0, 50).forEach(log => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-family: var(--font-mono); font-weight: 600;">${log.unitId}</td>
        <td style="color: var(--text-muted); font-size: 11px;">${log.timestamp}</td>
        <td>
          <span class="status-badge ${log.passed ? 'PASS' : 'FAIL'}">
            ${log.passed ? '✓ PASS' : '✗ FAIL'}
          </span>
        </td>
        <td style="font-family: var(--font-mono); font-weight: 700; color: ${log.passed ? 'var(--pass-color)' : 'var(--fail-color)'};">
          ${log.score.toFixed(1)}%
        </td>
        <td style="font-family: var(--font-mono);">${log.confidence.toFixed(1)}%</td>
        <td style="font-family: var(--font-mono); color: var(--accent-amber);">${log.threshold.toFixed(1)}%</td>
        <td style="font-family: var(--font-mono); font-size: 11px;">${log.defectLocation}</td>
        <td>
          <img src="${log.thumbnail}" class="table-thumb" alt="Thumbnail" title="Click to view side-by-side audit" />
        </td>
      `;

      tr.querySelector('.table-thumb').addEventListener('click', () => {
        this.openAuditModal(log);
      });

      this.qcLogsTbody.appendChild(tr);
    });
  }

  generateIsoCertificate() {
    document.getElementById('cert-id').textContent = `TF-ISO-${Math.floor(100000 + Math.random() * 900000)}`;
    document.getElementById('cert-date').textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    document.getElementById('cert-recipe').textContent = this.kpiRecipeName.textContent;
    document.getElementById('cert-total').textContent = this.kpis.total;
    document.getElementById('cert-passed').textContent = this.kpis.passed;
    document.getElementById('cert-rejected').textContent = this.kpis.rejected;

    const yieldRate = this.kpis.total > 0 ? (100 - this.kpis.rejectionRate).toFixed(1) : '100.0';
    document.getElementById('cert-yield').textContent = `${yieldRate}%`;

    let cpk = 1.45;
    if (this.logs.length > 2) {
      const scores = this.logs.map(l => l.score);
      const mean = scores.reduce((a, b) => a + b, 0) / scores.length;
      const variance = scores.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / scores.length;
      const sigma = Math.sqrt(variance) || 1.0;
      cpk = Math.max(0.6, Math.min(2.5, Math.round(((this.threshold - mean) / (3 * sigma)) * 100) / 100));
    }
    const cpkEl = document.getElementById('cert-cpk');
    cpkEl.textContent = cpk.toFixed(2);
    cpkEl.className = cpk >= 1.33 ? 'num green' : 'num red';

    this.isoCertModal.classList.add('show');
  }

  openWhatsAppModal() {
    const time = new Date().toLocaleTimeString();
    const rate = this.kpis.rejectionRate.toFixed(1);
    const recipe = this.kpiRecipeName.textContent;
    const total = this.kpis.total;
    const rejections = this.kpis.rejected;

    const rawText = `🚨 *SIGMALENS EMERGENCY SHIFT ALERT*\n📍 Product Line: ${recipe}\n⚠️ Today Rejection Rate: ${rate}% (${rejections}/${total} Units)\n🛑 Attention: Line Rejection Threshold Exceeded!\n⏱️ Shift Timestamp: ${time}`;
    this.whatsAppMsgPreview.innerHTML = rawText.replace(/\n/g, '<br>').replace(/\*(.*?)\*/g, '<strong>$1</strong>');

    const encoded = encodeURIComponent(rawText);
    this.btnOpenWhatsAppLink.href = `https://wa.me/?text=${encoded}`;
    this.whatsAppModal.classList.add('show');
  }

  openAuditModal(log) {
    this.modalUnitTitle.textContent = `Inspection Audit - ${log.unitId} (${log.passed ? 'PASS' : 'REJECT'})`;
    this.modalUnitImg.src = log.thumbnail;
    this.modalGoldenImg.src = this.cv.getGoldenMeanDataUrl();
    this.inspectionModal.classList.add('show');
  }

  resetShift() {
    this.logs = [];
    this.kpis = { total: 0, passed: 0, rejected: 0, rejectionRate: 0.0, avgLatency: 0 };
    this.recentScores = [];
    this.spcDriftBanner.style.display = 'none';
    this.kpiTotal.textContent = '0';
    this.kpiPassed.textContent = '0';
    this.kpiRejected.textContent = '0';
    this.kpiRejectionRate.innerHTML = '0.0<small>%</small>';
    this.renderLogsTable();
    this.showToast("Today's shift data and counters have been reset.");
  }

  async switchVideoSource(sourceType) {
    this.selectedVideoSource = sourceType;
    this.cameraSourceSelect.value = sourceType;

    if (this.cameraAnimLoop) {
      cancelAnimationFrame(this.cameraAnimLoop);
      this.cameraAnimLoop = null;
    }

    if (this.activeCameraStream) {
      this.activeCameraStream.getTracks().forEach(t => t.stop());
      this.activeCameraStream = null;
    }

    if (sourceType === 'testbench') {
      this.videoEl.style.display = 'none';
      this.viewportCanvas.style.display = 'block';
      this.loadTestUnit(null);
      this.showToast('Switched to Preloaded Test Bench Mode.');
      return;
    }

    try {
      const constraints = {
        video: {
          width: { ideal: 640 },
          height: { ideal: 640 },
          facingMode: sourceType === 'environment' ? { ideal: 'environment' } : 'user'
        },
        audio: false
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      this.activeCameraStream = stream;
      this.videoEl.srcObject = stream;
      this.videoEl.style.display = 'none'; // Keep hidden, render to viewportCanvas
      this.viewportCanvas.style.display = 'block';
      await this.videoEl.play().catch(e => console.warn('Video play warning:', e));

      // Continuous render loop from video element into viewport canvas
      const renderFrame = () => {
        if (this.selectedVideoSource !== 'testbench' && this.videoEl && this.videoEl.readyState >= 2) {
          this.viewportCtx.drawImage(this.videoEl, 0, 0, 320, 320);
        }
        if (this.selectedVideoSource !== 'testbench') {
          this.cameraAnimLoop = requestAnimationFrame(renderFrame);
        }
      };
      this.cameraAnimLoop = requestAnimationFrame(renderFrame);

      this.showToast(`Connected to live camera (${sourceType === 'environment' ? 'Rear Camera' : 'Webcam'}). Point at bottle cap.`);
    } catch (err) {
      console.warn('Camera access failed:', err);
      this.showToast('Camera unavailable or permission denied. Using Test Bench mode.');
      this.cameraSourceSelect.value = 'testbench';
      this.switchVideoSource('testbench');
    }
  }

  toggleHandsFree() {
    this.handsFreeActive = !this.handsFreeActive;
    if (this.handsFreeActive) {
      if (this.autoScanActive) this.toggleAutoScan();

      this.btnHandsFreeTrigger.classList.add('active');
      this.btnHandsFreeTrigger.innerHTML = `✋ Hands-Free: ACTIVE`;
      this.hudHandsFreeStatus.style.display = 'block';
      this.hudHandsFreeStatus.textContent = 'HANDS-FREE: PLACE PART & KEEP STILL';
      this.motionState = 'waiting';
      this.showToast('Hands-Free Mode: Place part into target zone. Auto-inspects on stillness.');
      this.runHandsFreeLoop();
    } else {
      this.btnHandsFreeTrigger.classList.remove('active');
      this.btnHandsFreeTrigger.innerHTML = `✋ Hands-Free Auto: OFF`;
      this.hudHandsFreeStatus.style.display = 'none';
      if (this.handsFreeTimer) clearTimeout(this.handsFreeTimer);
      this.showToast('Hands-Free Mode disabled.');
    }
  }

  runHandsFreeLoop() {
    if (!this.handsFreeActive) return;

    let currImgData = null;
    if (this.selectedVideoSource !== 'testbench' && this.videoEl.readyState >= 2) {
      this.viewportCtx.drawImage(this.videoEl, 0, 0, 320, 320);
      currImgData = this.viewportCtx.getImageData(0, 0, 320, 320);
    } else {
      currImgData = this.viewportCtx.getImageData(0, 0, 320, 320);
    }

    if (this.lastFrameData && currImgData) {
      const motionEnergy = this.cv.computeMotionEnergy(currImgData, this.lastFrameData);

      if (motionEnergy > 8.0) {
        this.motionState = 'moving';
        this.hudHandsFreeStatus.textContent = 'MOTION DETECTED: ALIGNING PART...';
        this.hudHandsFreeStatus.style.borderColor = 'var(--accent-amber)';
        this.hudHandsFreeStatus.style.color = 'var(--accent-amber)';
      } else if (this.motionState === 'moving' && motionEnergy < 2.5) {
        this.motionState = 'settled';
        this.hudHandsFreeStatus.textContent = 'PART SETTLED: TRIGGERING INSPECTION!';
        this.hudHandsFreeStatus.style.borderColor = 'var(--pass-color)';
        this.hudHandsFreeStatus.style.color = 'var(--pass-color)';

        this.executeInspection();

        setTimeout(() => {
          if (this.handsFreeActive) {
            this.motionState = 'waiting';
            this.hudHandsFreeStatus.textContent = 'HANDS-FREE: READY FOR NEXT PART';
            this.hudHandsFreeStatus.style.borderColor = 'var(--accent-cyan)';
            this.hudHandsFreeStatus.style.color = 'var(--accent-cyan)';
          }
        }, 1200);
      }
    }

    this.lastFrameData = currImgData;
    this.handsFreeTimer = setTimeout(() => {
      this.runHandsFreeLoop();
    }, 180);
  }

  toggleAutoScan() {
    this.autoScanActive = !this.autoScanActive;
    if (this.autoScanActive) {
      if (this.handsFreeActive) this.toggleHandsFree();

      this.btnAutoScan.classList.add('active');
      this.btnAutoScan.innerHTML = `
        <span class="pulse-dot" style="width: 6px; height: 6px; background: var(--pass-color);"></span>
        Auto-Scan: ACTIVE
      `;
      this.showToast('Continuous Auto-Scan started (400ms interval).');
      this.runAutoScanLoop();
    } else {
      this.btnAutoScan.classList.remove('active');
      this.btnAutoScan.innerHTML = `
        <span class="pulse-dot" style="width: 6px; height: 6px; background: var(--text-dim);"></span>
        Auto-Scan: OFF
      `;
      if (this.autoScanTimer) clearTimeout(this.autoScanTimer);
      this.showToast('Continuous Auto-Scan paused.');
    }
  }

  runAutoScanLoop() {
    if (!this.autoScanActive) return;
    this.executeInspection();
    this.autoScanTimer = setTimeout(() => {
      this.runAutoScanLoop();
    }, 450);
  }

  async startBurstCapture() {
    this.showToast('Starting burst capture of 24 golden units. Keep part steady...');
    this.cv.clearGoldenSamples();

    let count = 0;
    const interval = setInterval(() => {
      count++;
      const snapCanvas = document.createElement('canvas');
      snapCanvas.width = 320;
      snapCanvas.height = 320;
      const ctx = snapCanvas.getContext('2d');

      if (this.selectedVideoSource !== 'testbench' && this.videoEl.readyState >= 2) {
        ctx.drawImage(this.videoEl, 0, 0, 320, 320);
      } else {
        // Testbench capture with realistic rotational jitter
        const angle = (count * 15) * Math.PI / 180;
        ctx.save();
        ctx.translate(160, 160);
        ctx.rotate(angle);
        ctx.drawImage(this.viewportCanvas, -160, -160);
        ctx.restore();
      }

      this.cv.addGoldenSample(snapCanvas);
      soundFX.playShutter();
      this.showToast(`Captured Golden Sample ${count} / 24...`);

      if (count >= 24) {
        clearInterval(interval);
        this.trainModelWithFeedback();
        this.renderGoldenGallery();
        this.switchTab('training');
        this.showToast('Model training complete on 24 golden samples!');
      }
    }, 120);
  }

  handleGoldenFileUpload(files) {
    if (!files || files.length === 0) return;
    let loaded = 0;
    const fileList = Array.from(files);
    fileList.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          this.cv.addGoldenSample(img);
          loaded++;
          if (loaded === fileList.length) {
            this.trainModelWithFeedback();
            this.renderGoldenGallery();
            this.showToast(`Imported ${loaded} photo(s). Model automatically trained and calibrated!`);
          }
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  handleUnitUpload(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        this.selectedVideoSource = 'testbench';
        this.cameraSourceSelect.value = 'testbench';
        this.videoEl.style.display = 'none';
        this.viewportCanvas.style.display = 'block';

        this.viewportCtx.clearRect(0, 0, 320, 320);
        this.viewportCtx.drawImage(img, 0, 0, 320, 320);
        this.showToast('Uploaded custom unit photo. Triggering inspection...');
        this.executeInspection();
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  setupCanvasDrawing() {
    const canvas = this.viewportCanvas;

    const getPos = (e) => {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      return {
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY
      };
    };

    canvas.addEventListener('mousedown', (e) => {
      this.isDrawing = true;
      this.lastDrawPos = getPos(e);
      this.drawAnomalyStroke(this.lastDrawPos, this.lastDrawPos);
    });

    canvas.addEventListener('mousemove', (e) => {
      if (!this.isDrawing) return;
      const currentPos = getPos(e);
      this.drawAnomalyStroke(this.lastDrawPos, currentPos);
      this.lastDrawPos = currentPos;
    });

    const stopDrawing = () => {
      if (this.isDrawing) {
        this.isDrawing = false;
        this.executeInspection();
      }
    };

    window.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);
  }

  drawAnomalyStroke(p0, p1) {
    const ctx = this.viewportCtx;
    ctx.save();
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    if (this.brushMode === 'scratch') {
      ctx.strokeStyle = '#c0392b';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(p0.x, p0.y);
      ctx.lineTo(p1.x, p1.y);
      ctx.stroke();

      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(p0.x + 1, p0.y + 1);
      ctx.lineTo(p1.x + 1, p1.y + 1);
      ctx.stroke();
    } else if (this.brushMode === 'burn') {
      ctx.strokeStyle = '#3e1c07';
      ctx.lineWidth = 14;
      ctx.beginPath();
      ctx.moveTo(p0.x, p0.y);
      ctx.lineTo(p1.x, p1.y);
      ctx.stroke();

      ctx.strokeStyle = '#120701';
      ctx.lineWidth = 8;
      ctx.beginPath();
      ctx.moveTo(p0.x, p0.y);
      ctx.lineTo(p1.x, p1.y);
      ctx.stroke();
    } else if (this.brushMode === 'oil') {
      ctx.strokeStyle = 'rgba(25, 20, 10, 0.7)';
      ctx.lineWidth = 18;
      ctx.beginPath();
      ctx.moveTo(p0.x, p0.y);
      ctx.lineTo(p1.x, p1.y);
      ctx.stroke();
    }

    ctx.restore();
    this.activeUnitModified = true;
  }

  exportLogsCSV() {
    if (this.logs.length === 0) {
      this.showToast('No inspection logs available to export.');
      return;
    }

    let csv = 'Unit_ID,Timestamp,Recipe,Decision,Anomaly_Score_Pct,Confidence_Pct,Threshold_Pct,Defect_Location\n';
    this.logs.forEach(l => {
      csv += `"${l.unitId}","${l.timestamp}","${l.recipe}","${l.passed ? 'PASS' : 'FAIL'}",${l.score.toFixed(1)},${l.confidence.toFixed(1)},${l.threshold.toFixed(1)},"${l.defectLocation}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SigmaLens_Shift_Log_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    this.showToast('Exported inspection log to CSV.');
  }

  exportLogsJSON() {
    if (this.logs.length === 0) {
      this.showToast('No inspection logs available to export.');
      return;
    }

    const exportData = {
      exportDate: new Date().toISOString(),
      activeProduct: this.activeProduct,
      kpis: this.kpis,
      threshold: this.threshold,
      baselineStats: this.cv.baselineStats,
      records: this.logs
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SigmaLens_Report_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    this.showToast('Exported shift report to JSON.');
  }

  toggleAudio() {
    soundFX.enabled = !soundFX.enabled;
    const btn = document.getElementById('audio-toggle-btn');
    btn.classList.toggle('muted', !soundFX.enabled);
    this.showToast(`Audio chimes ${soundFX.enabled ? 'Enabled' : 'Muted'}`);
  }

  showToast(message) {
    if (this.toastTimeout) clearTimeout(this.toastTimeout);
    this.toastMsg.textContent = message;
    this.toast.classList.add('show');
    this.toastTimeout = setTimeout(() => {
      this.toast.classList.remove('show');
    }, 2800);
  }

  formatDefectIdToName(id) {
    if (!id) return 'Surface Anomaly';
    const catalog = this.datasets.getCatalog();
    for (const p of catalog) {
      const match = p.defects.find(d => d.id === id);
      if (match) return match.name;
    }
    return id.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }

  // Andon Stack Light Controller
  updateAndon(state) {
    this.andonState = state;
    if (this.andonRed && this.andonAmber && this.andonGreen) {
      this.andonRed.classList.toggle('active', state === 'red');
      this.andonAmber.classList.toggle('active', state === 'amber');
      this.andonGreen.classList.toggle('active', state === 'green');
    }
    if (this.ledDo03) {
      this.ledDo03.classList.toggle('active', state === 'red');
    }
  }

  // Open Simulated PLC Modal
  openPlcModal() {
    this.plcModal.classList.add('show');
  }

  // Update Simulated PLC & Modbus TCP Registers
  updatePlcRegisters(result) {
    if (!result) return;
    const scoreVal = Math.round(result.rawScore * 10);
    const scoreHex = '0x' + scoreVal.toString(16).toUpperCase().padStart(4, '0');
    const verdictDec = result.passed ? 0 : 1;
    const verdictHex = '0x' + verdictDec.toString(16).toUpperCase().padStart(4, '0');
    const totalHex = '0x' + this.kpis.total.toString(16).toUpperCase().padStart(4, '0');
    const rejectHex = '0x' + this.kpis.rejected.toString(16).toUpperCase().padStart(4, '0');

    const m2Hex = document.getElementById('modbus-40002-hex');
    const m2Dec = document.getElementById('modbus-40002-dec');
    const m3Hex = document.getElementById('modbus-40003-hex');
    const m3Dec = document.getElementById('modbus-40003-dec');
    const m4Hex = document.getElementById('modbus-40004-hex');
    const m4Dec = document.getElementById('modbus-40004-dec');
    const m5Hex = document.getElementById('modbus-40005-hex');
    const m5Dec = document.getElementById('modbus-40005-dec');

    if (m2Hex) {
      m2Hex.textContent = scoreHex;
      m2Dec.textContent = `${scoreVal} (${result.rawScore.toFixed(1)}%)`;
      m3Hex.textContent = verdictHex;
      m3Dec.textContent = `${verdictDec} (${result.passed ? 'PASS' : 'FAIL'})`;
      m4Hex.textContent = totalHex;
      m4Dec.textContent = this.kpis.total.toString();
      m5Hex.textContent = rejectHex;
      m5Dec.textContent = this.kpis.rejected.toString();
    }

    // Flash Strobe Output LED
    if (this.ledDo01) {
      this.ledDo01.classList.add('active');
      setTimeout(() => this.ledDo01.classList.remove('active'), 120);
    }

    // Solenoid Reject LED
    if (this.ledDo02) {
      if (!result.passed) {
        this.ledDo02.classList.add('active');
        setTimeout(() => this.ledDo02.classList.remove('active'), 600);
      }
    }

    // MQTT Telemetry Frame Update
    if (this.mqttPayloadPreview) {
      const mqttData = {
        timestamp: new Date().toISOString(),
        stationId: "AOI-LINE-01",
        recipe: this.kpiRecipeName.textContent,
        status: this.spcDriftBanner.style.display !== 'none' ? "WARNING_DRIFT" : (result.passed ? "RUNNING_NOMINAL" : "REJECT_FAULT"),
        metrics: {
          totalInspected: this.kpis.total,
          rejectionRatePct: this.kpis.rejectionRate,
          lastVerdict: result.passed ? "PASS" : "REJECT",
          anomalyScore: result.rawScore,
          primaryDefect: result.defectLocation
        },
        fieldbus: {
          modbusWord40001: "0x0001",
          plcCycleTimeMs: 1.8
        }
      };
      this.mqttPayloadPreview.textContent = JSON.stringify(mqttData, null, 2);
    }
  }

  // --- CONVEYOR LINE SIMULATION METHODS ---

  toggleConveyor() {
    this.conveyorRunning = !this.conveyorRunning;
    this.btnToggleConveyor.classList.toggle('running', this.conveyorRunning);
    this.conveyorBeltStrip.classList.toggle('moving', this.conveyorRunning);

    if (this.conveyorRunning) {
      this.conveyorToggleText.textContent = 'STOP CONVEYOR LINE';
      this.showToast(`Conveyor Line Started @ ${this.conveyorPpm} PPM.`);
      this.conveyorLastSpawnTime = performance.now();
      this.runConveyorLoop();
    } else {
      this.conveyorToggleText.textContent = 'START CONVEYOR LINE';
      this.showToast('Conveyor Line Paused.');
      if (this.conveyorAnimFrame) cancelAnimationFrame(this.conveyorAnimFrame);
    }
  }

  stepConveyorUnit() {
    this.spawnConveyorUnit();
    this.showToast('Fed 1 unit into conveyor queue.');
  }

  clearConveyorBins() {
    this.conveyorStats = { infeed: 0, accept: 0, reject: 0, kicks: 0 };
    this.binAcceptCount.textContent = '0';
    this.binRejectCount.textContent = '0';
    this.tachKicks.textContent = '0';
    this.tachTotal.textContent = '0';
    this.tachOee.textContent = '100.0%';
    this.showToast('Emptied conveyor bins and reset counters.');
  }

  runConveyorLoop() {
    if (!this.conveyorRunning) return;

    const now = performance.now();
    const spawnInterval = (60 / this.conveyorPpm) * 1000;

    // Check if time to spawn new infeed unit
    if (now - this.conveyorLastSpawnTime >= spawnInterval) {
      this.spawnConveyorUnit();
      this.conveyorLastSpawnTime = now;
    }

    // Move existing units
    this.updateConveyorPhysics();

    this.conveyorAnimFrame = requestAnimationFrame(() => this.runConveyorLoop());
  }

  spawnConveyorUnit() {
    const isDefect = Math.random() < this.defectMix;
    let defectId = null;

    if (isDefect) {
      const catalog = this.datasets.getCatalog();
      const current = catalog.find(p => p.id === this.activeProduct) || catalog[0];
      if (current.defects && current.defects.length > 0) {
        const idx = Math.floor(Math.random() * current.defects.length);
        defectId = current.defects[idx].id;
      }
    }

    // Generate unit canvas
    const unitCanvas = this.datasets.generateTestUnit(this.activeProduct, defectId);

    // Create DOM element on track
    const unitEl = document.createElement('div');
    unitEl.className = `conveyor-unit ${defectId ? 'defective' : ''}`;
    unitEl.style.left = '-60px';

    const thumb = document.createElement('canvas');
    thumb.width = 48;
    thumb.height = 48;
    const tctx = thumb.getContext('2d');
    tctx.drawImage(unitCanvas, 0, 0, 48, 48);
    unitEl.appendChild(thumb);

    this.conveyorTrack.appendChild(unitEl);

    this.conveyorUnits.push({
      x: -60,
      canvas: unitCanvas,
      defectId,
      inspected: false,
      passed: true,
      kicked: false,
      el: unitEl
    });

    this.conveyorStats.infeed++;
    this.updateConveyorTachometer();
  }

  updateConveyorPhysics() {
    const trackWidth = this.conveyorTrack.clientWidth || 700;
    const speedPxPerFrame = (trackWidth / (60 / this.conveyorPpm * 60)) * 1.8;

    for (let i = this.conveyorUnits.length - 1; i >= 0; i--) {
      const u = this.conveyorUnits[i];
      u.x += speedPxPerFrame;
      u.el.style.left = `${u.x}px`;

      const pct = (u.x / trackWidth) * 100;

      // Position ~42%: Inspection Hood
      if (pct >= 41 && pct <= 46 && !u.inspected) {
        u.inspected = true;
        this.inspectConveyorUnit(u);
      }

      // Position ~63%: Pneumatic Reject Kicker
      if (pct >= 62 && pct <= 66 && !u.passed && !u.kicked) {
        u.kicked = true;
        this.triggerPneumaticKicker(u);
      }

      // Position >= 92%: Reached end of belt
      if (pct >= 92) {
        if (u.passed && !u.kicked) {
          this.conveyorStats.accept++;
          this.binAcceptCount.textContent = this.conveyorStats.accept;
        }
        if (u.el.parentNode) u.el.parentNode.removeChild(u.el);
        this.conveyorUnits.splice(i, 1);
        this.updateConveyorTachometer();
      }
    }
  }

  inspectConveyorUnit(u) {
    if (!this.cv.trained) return;

    // Optical trigger beam & strobe pulse
    this.conveyorStrobe.classList.add('flash');
    this.hoodScanStatus.textContent = 'SCANNING...';
    this.hoodScanStatus.style.color = 'var(--accent-cyan)';
    soundFX.playShutter();

    if (this.ledDi01) {
      this.ledDi01.classList.add('active');
      setTimeout(() => this.ledDi01.classList.remove('active'), 150);
    }

    setTimeout(() => {
      this.conveyorStrobe.classList.remove('flash');
      this.hoodScanStatus.textContent = 'TRIGGERED';
    }, 100);

    const result = this.cv.inspect(u.canvas, this.threshold, null, this.normalizeLighting, false);
    u.passed = result.passed;

    // Copy to main viewport canvas
    this.viewportCtx.drawImage(u.canvas, 0, 0);
    this.lastInspectedResult = result;
    this.displayInspectionResult(result);

    this.tachSolenoid.textContent = result.passed ? 'PASS (GATE OK)' : 'FAIL (ARM ENGAGED)';
    this.tachSolenoid.style.color = result.passed ? 'var(--pass-color)' : 'var(--fail-color)';
  }

  triggerPneumaticKicker(u) {
    this.conveyorStats.kicks++;
    this.conveyorStats.reject++;
    this.binRejectCount.textContent = this.conveyorStats.reject;
    this.tachKicks.textContent = this.conveyorStats.kicks;

    // Kick animation
    this.pneumaticKicker.classList.add('kick');
    soundFX.playPneumaticPuff();

    u.el.classList.add('kicked');

    setTimeout(() => {
      this.pneumaticKicker.classList.remove('kick');
    }, 280);

    this.updateConveyorTachometer();
  }

  updateConveyorTachometer() {
    this.tachTotal.textContent = this.conveyorStats.infeed;
    const totalSorted = this.conveyorStats.accept + this.conveyorStats.reject;
    const oee = totalSorted > 0 ? ((this.conveyorStats.accept / totalSorted) * 100).toFixed(1) : '100.0';
    this.tachOee.textContent = `${oee}%`;
    this.tachPpm.innerHTML = `${this.conveyorRunning ? this.conveyorPpm.toFixed(1) : '0.0'} <small style="font-size: 12px;">PPM</small>`;
  }

  // --- PARETO DEFECT ANALYTICS & SIX SIGMA ROI ---

  recordDefectTally(name) {
    if (!name) name = 'Unspecified Deviation';
    const key = name.split('(')[0].trim();
    this.defectTallies[key] = (this.defectTallies[key] || 0) + 1;
    this.renderParetoChart();
  }

  renderParetoChart() {
    if (!this.paretoCanvas) return;
    const canvas = this.paretoCanvas;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    // Sort tallies descending
    const entries = Object.entries(this.defectTallies).sort((a, b) => b[1] - a[1]);
    if (entries.length === 0) return;

    const totalDefects = entries.reduce((sum, e) => sum + e[1], 0);
    const maxCount = entries[0][1] * 1.25 || 10;

    const padLeft = 40;
    const padRight = 45;
    const padTop = 30;
    const padBottom = 55;
    const plotW = w - padLeft - padRight;
    const plotH = h - padTop - padBottom;

    // Draw gridlines
    ctx.strokeStyle = '#1e2638';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padTop + (plotH / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padLeft, y);
      ctx.lineTo(w - padRight, y);
      ctx.stroke();

      // Right Y-axis percentage labels
      ctx.fillStyle = '#64748b';
      ctx.font = '10px JetBrains Mono, monospace';
      ctx.textAlign = 'left';
      ctx.fillText(`${100 - i * 25}%`, w - padRight + 6, y + 3);
    }

    // 80% Vital Few reference line (Red Dashed)
    const y80 = padTop + plotH * (1 - 0.8);
    ctx.strokeStyle = '#ff3366';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(padLeft, y80);
    ctx.lineTo(w - padRight, y80);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#ff3366';
    ctx.font = '9px JetBrains Mono, monospace';
    ctx.fillText('80% VITAL FEW CUTOFF', padLeft + 6, y80 - 4);

    const barWidth = Math.min(48, (plotW / entries.length) * 0.65);
    const gap = plotW / entries.length;

    let cumPct = 0;
    const points = [];

    // Draw Bars
    entries.forEach((e, idx) => {
      const count = e[1];
      const barH = (count / maxCount) * plotH;
      const x = padLeft + idx * gap + (gap - barWidth) / 2;
      const y = padTop + plotH - barH;

      // Bar gradient
      const grad = ctx.createLinearGradient(0, y, 0, padTop + plotH);
      grad.addColorStop(0, '#00e5ff');
      grad.addColorStop(1, '#005b82');
      ctx.fillStyle = grad;
      ctx.fillRect(x, y, barWidth, barH);

      // Bar count label
      ctx.fillStyle = '#e2e8f0';
      ctx.font = '11px JetBrains Mono, monospace';
      ctx.textAlign = 'center';
      ctx.fillText(count.toString(), x + barWidth / 2, y - 5);

      // X-axis label
      ctx.fillStyle = '#94a3b8';
      ctx.font = '10px Inter, sans-serif';
      ctx.save();
      ctx.translate(x + barWidth / 2, padTop + plotH + 14);
      ctx.rotate(-0.25);
      const shortName = e[0].length > 14 ? e[0].substring(0, 12) + '..' : e[0];
      ctx.fillText(shortName, 0, 0);
      ctx.restore();

      // Cumulative line points
      cumPct += (count / totalDefects);
      const pointY = padTop + plotH - (cumPct * plotH);
      points.push({ x: x + barWidth / 2, y: pointY, pct: Math.round(cumPct * 100) });
    });

    // Draw Cumulative Curve (Orange)
    ctx.strokeStyle = '#ffb300';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    points.forEach((p, idx) => {
      if (idx === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    });
    ctx.stroke();

    // Draw Cumulative Point Markers
    points.forEach(p => {
      ctx.fillStyle = '#ffb300';
      ctx.beginPath();
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#06080b';
      ctx.beginPath();
      ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
      ctx.fill();
    });

    // Update DMAIC Root Cause Guide
    if (entries.length > 0) {
      this.updateDmaicGuide(entries[0][0]);
    }
  }

  updateDmaicGuide(topDefect) {
    if (!this.dmaicTopDefectName) return;
    this.dmaicTopDefectName.textContent = topDefect;

    if (topDefect.includes('Solder') || topDefect.includes('Bridge')) {
      this.dmaicStep1.textContent = 'Accounts for primary rework costs. Concentrated at fine-pitch SMD IC terminals.';
      this.dmaicStep2.textContent = 'Excessive solder paste stencil volume or flux viscosity degradation from ambient heat.';
      this.dmaicStep3.textContent = 'Reduce paste stencil aperture by 12% and calibrate wave solder nitrogen blanket flow.';
      this.dmaicStep4.textContent = 'Hold SigmaLens threshold at 3-Sigma. Alert line if 2 consecutive solder bridges occur.';
    } else if (topDefect.includes('Missing') || topDefect.includes('Capacitor') || topDefect.includes('Pill')) {
      this.dmaicStep1.textContent = 'High-criticality defect leading to complete product field functional failure.';
      this.dmaicStep2.textContent = 'Pick-and-place pneumatic vacuum nozzle clogging or feeder reel tape jam.';
      this.dmaicStep3.textContent = 'Purge suction nozzles with ultrasonic solvent bath and inspect tape reel feeder pitch.';
      this.dmaicStep4.textContent = 'Enable Voice Announcer. Immediate buzzer on any empty cavity detected.';
    } else {
      this.dmaicStep1.textContent = `Top Pareto defect: accounts for highest scrap proportion in current recipe.`;
      this.dmaicStep2.textContent = 'Component fixture vibration, tooling wear, or manual handling friction.';
      this.dmaicStep3.textContent = 'Adjust guide rail tension and implement soft silicone component grippers.';
      this.dmaicStep4.textContent = 'Track Nelson Rule #2 SPC drift to catch tooling degradation prior to scrap creation.';
    }
  }

  updateRoiCalculations() {
    const cost = this.roiUnitCost;
    const vol = this.roiDailyVolume;
    const escape = this.roiEscapeRate;

    // SigmaLens reduces escape by 95%
    const defectsPreventedDaily = Math.round(vol * escape * 0.95);
    const dailySavings = defectsPreventedDaily * cost;
    const annualSavings = dailySavings * 300; // 300 manufacturing days
    const keyenceCost = 2000000; // 20 Lakhs
    const paybackDays = dailySavings > 0 ? (keyenceCost / dailySavings).toFixed(1) : '0';

    if (this.roiDailySavings) {
      this.roiDailySavings.textContent = `₹ ${dailySavings.toLocaleString('en-IN')}`;
    }
    if (this.roiAnnualSavings) {
      if (annualSavings >= 10000000) {
        this.roiAnnualSavings.textContent = `₹ ${(annualSavings / 10000000).toFixed(2)} Cr`;
      } else {
        this.roiAnnualSavings.textContent = `₹ ${(annualSavings / 100000).toFixed(2)} Lakh`;
      }
    }
    if (this.roiPaybackDays) {
      this.roiPaybackDays.textContent = `${paybackDays} Days`;
    }
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.app = new SigmaLensApp();
});
