// SigmaLens - Realistic Procedural Industrial Product Datasets
// Provides 20-25 Golden Samples + Verified Defect Units for instant training & testing

export class IndustrialDatasets {
  constructor(width = 320, height = 320) {
    this.width = width;
    this.height = height;
    this.canvas = document.createElement('canvas');
    this.canvas.width = width;
    this.canvas.height = height;
    this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });

    // Preload Mentor Cap reference images
    this.capImgCache = {};
    const imgList = [
      'white_cap_base', 'defect_blue_cap', 'defect_red_cap',
      'defect_crack', 'defect_stain', 'defect_chipped'
    ];
    for (let i = 0; i < 24; i++) imgList.push(`golden_${i}`);
    imgList.forEach(name => {
      const img = new Image();
      img.src = `/caps/${name}.png`;
      this.capImgCache[name] = img;
    });
  }

  // Get catalog of preloaded industrial products
  getCatalog() {
    return [
      {
        id: 'white_cap',
        name: 'Physical White Bottle Cap (Mentor Test Unit)',
        category: 'Live Mentor Proof Test',
        goldenCount: 24,
        description: 'Physical white plastic fluted bottle cap trained on 24 golden samples. Ready to test against different caps and defect modes.',
        defects: [
          { id: 'diff_blue_cap', name: 'Mentor Different Cap: Blue Beverage Cap', severity: 'Critical' },
          { id: 'diff_red_cap', name: 'Mentor Different Cap: Red Threaded Cap', severity: 'Critical' },
          { id: 'diff_crack', name: 'Hairline Surface Crack', severity: 'High' },
          { id: 'diff_stain', name: 'Oil & Grease Contamination', severity: 'Medium' },
          { id: 'diff_chipped', name: 'Chipped Outer Flute Rim', severity: 'High' }
        ]
      },
      {
        id: 'pcb',
        name: 'SMT Circuit Board (Rev-D)',
        category: 'Electronics Assembly',
        goldenCount: 24,
        description: 'Microcontroller board with IC chips, capacitors, SMD passives, and gold contacts.',
        defects: [
          { id: 'pcb_missing_cap', name: 'Missing Capacitor (C12)', severity: 'High' },
          { id: 'pcb_solder_bridge', name: 'Solder Bridge Short (U1 Pin 4-5)', severity: 'Critical' },
          { id: 'pcb_burnt_resistor', name: 'Thermal Burn / Blown Resistor', severity: 'Critical' },
          { id: 'pcb_trace_scratch', name: 'Deep Copper Trace Scratch', severity: 'Medium' },
          { id: 'pcb_oil_flux', name: 'Excess Flux Contamination', severity: 'Low' }
        ]
      },
      {
        id: 'bearing',
        name: 'Machined Steel Gear Flange',
        category: 'Precision Automotive',
        goldenCount: 22,
        description: 'CNC turned carbon steel bearing with 12 teeth, center bore, and keyway.',
        defects: [
          { id: 'gear_broken_tooth', name: 'Chipped / Fractured Tooth', severity: 'Critical' },
          { id: 'gear_deep_scratch', name: 'Axial Bore Gouge / Scratch', severity: 'High' },
          { id: 'gear_pitting_corrosion', name: 'Surface Pitting Rust Dent', severity: 'High' },
          { id: 'gear_oil_stain', name: 'Heavy Industrial Grease Stain', severity: 'Low' },
          { id: 'gear_machining_burr', name: 'Excess Metal Edge Burr', severity: 'Medium' }
        ]
      },
      {
        id: 'blister',
        name: 'Pharma 10-Capsule Blister Pack',
        category: 'Medical & Packaging',
        goldenCount: 25,
        description: 'Aluminum foil heat-sealed blister tray with 10 bicolored capsules.',
        defects: [
          { id: 'blister_missing_pill', name: 'Missing Capsule (Cavity #7 Empty)', severity: 'Critical' },
          { id: 'blister_crushed_pill', name: 'Crushed Capsule & Powder Leak', severity: 'Critical' },
          { id: 'blister_punctured_foil', name: 'Torn / Punctured Foil Seal', severity: 'High' },
          { id: 'blister_discolored_pill', name: 'Discolored / Degraded Tablet', severity: 'High' }
        ]
      },
      {
        id: 'bottle_cap',
        name: 'Beverage Bottle Cap & Tamper Seal',
        category: 'Food & Beverage',
        goldenCount: 20,
        description: 'Injection-molded threaded cap with tamper-evident security ring.',
        defects: [
          { id: 'cap_broken_seal', name: 'Severed Tamper-Evident Ring', severity: 'Critical' },
          { id: 'cap_skewed_thread', name: 'Cocked / Skewed Cross-Thread', severity: 'High' },
          { id: 'cap_crown_dent', name: 'Punctured Crown Impact Dent', severity: 'High' },
          { id: 'cap_plastic_flash', name: 'Injection Molding Flashing', severity: 'Medium' }
        ]
      }
    ];
  }

  // Generate golden samples for product
  generateGoldenSamples(productId, count = 24) {
    const samples = [];
    for (let i = 0; i < count; i++) {
      const seed = 1000 + i * 47;
      const canvas = document.createElement('canvas');
      canvas.width = this.width;
      canvas.height = this.height;
      const ctx = canvas.getContext('2d');

      if (productId === 'white_cap') {
        const cachedImg = this.capImgCache[`golden_${i % 24}`];
        if (cachedImg && cachedImg.complete && cachedImg.naturalWidth > 0) {
          ctx.drawImage(cachedImg, 0, 0, this.width, this.height);
        } else {
          this.renderWhiteBottleCap(ctx, () => (seed % 1000) / 1000, null);
        }
      } else {
        this.renderProduct(ctx, productId, seed, null);
      }
      samples.push(canvas);
    }
    return samples;
  }

  // Generate a test unit (either golden or defective)
  generateTestUnit(productId, defectId = null, seed = 8888) {
    const canvas = document.createElement('canvas');
    canvas.width = this.width;
    canvas.height = this.height;
    const ctx = canvas.getContext('2d');

    if (productId === 'white_cap') {
      let imgKey = 'white_cap_base';
      if (defectId === 'diff_blue_cap') imgKey = 'defect_blue_cap';
      else if (defectId === 'diff_red_cap') imgKey = 'defect_red_cap';
      else if (defectId === 'diff_crack') imgKey = 'defect_crack';
      else if (defectId === 'diff_stain') imgKey = 'defect_stain';
      else if (defectId === 'diff_chipped') imgKey = 'defect_chipped';

      const cached = this.capImgCache[imgKey];
      if (cached && cached.complete && cached.naturalWidth > 0) {
        ctx.drawImage(cached, 0, 0, this.width, this.height);
      } else {
        this.renderWhiteBottleCap(ctx, () => 0.5, defectId);
      }
      return canvas;
    }

    this.renderProduct(ctx, productId, seed, defectId);
    return canvas;
  }

  // Master product renderer
  renderProduct(ctx, productId, seed, defectId) {
    let s = seed;
    const rng = () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };

    switch (productId) {
      case 'white_cap':
        this.renderWhiteBottleCap(ctx, rng, defectId);
        break;
      case 'pcb':
        this.renderPCB(ctx, rng, defectId);
        break;
      case 'bearing':
        this.renderBearing(ctx, rng, defectId);
        break;
      case 'blister':
        this.renderBlisterPack(ctx, rng, defectId);
        break;
      case 'bottle_cap':
        this.renderBottleCap(ctx, rng, defectId);
        break;
      default:
        this.renderPCB(ctx, rng, defectId);
    }
  }

  // Mentor White Bottle Cap Procedural Fallback Renderer
  renderWhiteBottleCap(ctx, rng, defectId) {
    const w = this.width;
    const h = this.height;
    const cx = w / 2;
    const cy = h / 2;

    // Dark industrial mat background
    ctx.fillStyle = '#181b22';
    ctx.fillRect(0, 0, w, h);

    if (defectId === 'diff_blue_cap') {
      // Mentor's Different Cap: Bright Blue Plastic Cap
      ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
      ctx.beginPath();
      ctx.arc(cx + 4, cy + 4, 102, 0, Math.PI * 2);
      ctx.fill();

      const bgGrad = ctx.createRadialGradient(cx - 20, cy - 20, 10, cx, cy, 100);
      bgGrad.addColorStop(0, '#38bdf8');
      bgGrad.addColorStop(0.6, '#0284c7');
      bgGrad.addColorStop(1, '#0369a1');
      ctx.fillStyle = bgGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, 98, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = '#075985';
      ctx.lineWidth = 3;
      ctx.stroke();

      // Ridges
      for (let r = 0; r < 40; r++) {
        const a = (r / 40) * Math.PI * 2;
        ctx.strokeStyle = (r % 2 === 0) ? '#7dd3fc' : '#0369a1';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx + Math.cos(a) * 88, cy + Math.sin(a) * 88);
        ctx.lineTo(cx + Math.cos(a) * 98, cy + Math.sin(a) * 98);
        ctx.stroke();
      }
      return;
    }

    if (defectId === 'diff_red_cap') {
      // Mentor's Different Cap: Red Cap
      ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
      ctx.beginPath();
      ctx.arc(cx + 4, cy + 4, 105, 0, Math.PI * 2);
      ctx.fill();

      const rGrad = ctx.createRadialGradient(cx - 20, cy - 20, 10, cx, cy, 100);
      rGrad.addColorStop(0, '#f87171');
      rGrad.addColorStop(0.6, '#dc2626');
      rGrad.addColorStop(1, '#991b1b');
      ctx.fillStyle = rGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, 100, 0, Math.PI * 2);
      ctx.fill();
      return;
    }

    // Normal Physical White Bottle Cap
    const capR = 100;

    // Drop shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.beginPath();
    ctx.arc(cx + 4, cy + 5, capR + 2, 0, Math.PI * 2);
    ctx.fill();

    // Outer flutes / ribbed skirt
    const skirtGrad = ctx.createRadialGradient(cx - 25, cy - 25, 20, cx, cy, capR);
    skirtGrad.addColorStop(0, '#f8fafc');
    skirtGrad.addColorStop(0.6, '#e2e8f0');
    skirtGrad.addColorStop(1, '#94a3b8');
    ctx.fillStyle = skirtGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, capR, 0, Math.PI * 2);
    ctx.fill();

    // Outer ribs
    for (let i = 0; i < 48; i++) {
      const a = (i / 48) * Math.PI * 2;
      ctx.strokeStyle = (i % 2 === 0) ? '#ffffff' : '#cbd5e1';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a) * (capR - 8), cy + Math.sin(a) * (capR - 8));
      ctx.lineTo(cx + Math.cos(a) * capR, cy + Math.sin(a) * capR);
      ctx.stroke();
    }

    // Inner bevel circle
    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, 75, 0, Math.PI * 2);
    ctx.stroke();

    // Center gate pip & ring
    ctx.fillStyle = '#f1f5f9';
    ctx.beginPath();
    ctx.arc(cx, cy, 40, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#94a3b8';
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, Math.PI * 2);
    ctx.fill();

    // Crack Defect
    if (defectId === 'diff_crack') {
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(cx - 50, cy - 30);
      ctx.lineTo(cx - 10, cy + 5);
      ctx.lineTo(cx + 25, cy + 40);
      ctx.stroke();
    }

    // Stain Defect
    if (defectId === 'diff_stain') {
      ctx.fillStyle = 'rgba(55, 35, 10, 0.75)';
      ctx.beginPath();
      ctx.ellipse(cx + 30, cy - 25, 20, 12, 0.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Chipped Rim
    if (defectId === 'diff_chipped') {
      ctx.fillStyle = '#181b22';
      ctx.beginPath();
      ctx.arc(cx + capR - 4, cy, 14, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // 1. SMT ELECTRONICS PCB RENDERER
  renderPCB(ctx, rng, defectId) {
    const w = this.width;
    const h = this.height;

    // Background ESD mat / conveyor
    ctx.fillStyle = '#181b20';
    ctx.fillRect(0, 0, w, h);

    // Minor illumination gradient
    const lightShift = (rng() - 0.5) * 12;
    const grad = ctx.createLinearGradient(0, 0, w, h);
    grad.addColorStop(0, `rgb(${24 + lightShift}, ${26 + lightShift}, ${30 + lightShift})`);
    grad.addColorStop(1, '#111317');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // PCB Board Dimensions (with subtle sub-pixel placement jitter)
    const jx = (rng() - 0.5) * 2;
    const jy = (rng() - 0.5) * 2;
    const bx = 28 + jx;
    const by = 28 + jy;
    const bw = w - 56;
    const bh = h - 56;

    // Green FR-4 Solder Mask
    const pcbGrad = ctx.createLinearGradient(bx, by, bx + bw, by + bh);
    pcbGrad.addColorStop(0, '#0d5c34');
    pcbGrad.addColorStop(0.5, '#0a4b2a');
    pcbGrad.addColorStop(1, '#07361e');
    ctx.fillStyle = pcbGrad;
    ctx.beginPath();
    ctx.roundRect(bx, by, bw, bh, 8);
    ctx.fill();

    // Board Bevel & Edge
    ctx.strokeStyle = '#052414';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Mounting Holes in 4 corners
    ctx.fillStyle = '#d4af37'; // Gold annular ring
    const holes = [
      [bx + 14, by + 14],
      [bx + bw - 14, by + 14],
      [bx + 14, by + bh - 14],
      [bx + bw - 14, by + bh - 14]
    ];
    holes.forEach(([hx, hy]) => {
      ctx.beginPath();
      ctx.arc(hx, hy, 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#111317';
      ctx.beginPath();
      ctx.arc(hx, hy, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#d4af37';
    });

    // Copper Traces
    ctx.strokeStyle = '#127341';
    ctx.lineWidth = 2;
    ctx.beginPath();
    // Trace network
    ctx.moveTo(bx + 40, by + 40); ctx.lineTo(bx + 110, by + 40); ctx.lineTo(bx + 130, by + 70);
    ctx.moveTo(bx + 50, by + bh - 40); ctx.lineTo(bx + 100, by + bh - 40); ctx.lineTo(bx + 120, by + bh - 80);
    ctx.moveTo(bx + bw - 50, by + 50); ctx.lineTo(bx + bw - 90, by + 50); ctx.lineTo(bx + bw - 120, by + 90);
    ctx.moveTo(bx + 60, by + 120); ctx.lineTo(bx + 110, by + 120);
    ctx.moveTo(bx + bw - 70, by + bh - 60); ctx.lineTo(bx + bw - 110, by + bh - 60);
    ctx.stroke();

    // Gold Edge Connector Fingers (Right side)
    const fingerW = 6;
    const fingerH = 14;
    for (let f = 0; f < 8; f++) {
      ctx.fillStyle = '#dfb738';
      ctx.fillRect(bx + bw - 16, by + 60 + f * 18, fingerW, fingerH);
      ctx.fillStyle = '#b89422';
      ctx.fillRect(bx + bw - 16, by + 60 + f * 18 + fingerH - 2, fingerW, 2);
    }

    // Silkscreen Markings (White text & outlines)
    ctx.fillStyle = '#e8efe9';
    ctx.font = 'bold 9px monospace';
    ctx.fillText('REV-D4 2026', bx + 28, by + 30);
    ctx.fillText('QC-PASS: V-108', bx + 28, by + bh - 24);
    ctx.strokeStyle = 'rgba(232, 239, 233, 0.4)';
    ctx.lineWidth = 1;
    ctx.strokeRect(bx + 35, by + 55, 60, 45); // U2 IC outline

    // Center QFN / BGA Microcontroller Chip (U1)
    const chipX = w / 2 - 32;
    const chipY = h / 2 - 32;
    const chipSize = 64;

    // Chip Pins (Silver pads)
    ctx.fillStyle = '#dcdde1';
    for (let p = 0; p < 8; p++) {
      // Top pins
      ctx.fillRect(chipX + 8 + p * 6, chipY - 6, 4, 6);
      // Bottom pins
      ctx.fillRect(chipX + 8 + p * 6, chipY + chipSize, 4, 6);
      // Left pins
      ctx.fillRect(chipX - 6, chipY + 8 + p * 6, 6, 4);
      // Right pins
      ctx.fillRect(chipX + chipSize, chipY + 8 + p * 6, 6, 4);
    }

    // DEFECT: Solder Bridge on top pins
    if (defectId === 'pcb_solder_bridge') {
      ctx.fillStyle = '#e0e6ed';
      ctx.beginPath();
      ctx.arc(chipX + 22, chipY - 3, 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#a4b0be';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Chip Body (Matte black epoxy)
    ctx.fillStyle = '#22252a';
    ctx.fillRect(chipX, chipY, chipSize, chipSize);
    // Pin 1 dot
    ctx.fillStyle = '#444';
    ctx.beginPath();
    ctx.arc(chipX + 8, chipY + 8, 3, 0, Math.PI * 2);
    ctx.fill();
    // Laser Etched Markings
    ctx.fillStyle = '#6b7280';
    ctx.font = '8px monospace';
    ctx.fillText('ARM CORTEX', chipX + 8, chipY + 28);
    ctx.fillText('M4-840QC', chipX + 8, chipY + 40);

    // Passive SMD Components (Capacitors C1-C6, Resistors R1-R8)
    const passives = [
      { x: bx + 45, y: by + 160, type: 'resistor', val: '10k', id: 'R1' },
      { x: bx + 45, y: by + 185, type: 'resistor', val: '4k7', id: 'R2' },
      { x: bx + 70, y: by + 172, type: 'cap', val: '10uF', id: 'C12' },
      { x: bx + bw - 85, y: by + 75, type: 'cap', val: '100nF', id: 'C5' },
      { x: bx + bw - 65, y: by + 180, type: 'resistor', val: '220R', id: 'R7' },
      { x: bx + bw - 65, y: by + 205, type: 'cap', val: '22uF', id: 'C9' },
    ];

    passives.forEach(comp => {
      // DEFECT: Missing Capacitor C12
      if (defectId === 'pcb_missing_cap' && comp.id === 'C12') {
        // Just empty silver solder pads with flux residue!
        ctx.fillStyle = '#95a5a6';
        ctx.fillRect(comp.x - 2, comp.y, 4, 8);
        ctx.fillRect(comp.x + 14, comp.y, 4, 8);
        return;
      }

      // DEFECT: Burnt Resistor R1
      if (defectId === 'pcb_burnt_resistor' && comp.id === 'R1') {
        // Charred black/brown burn mark
        ctx.fillStyle = '#4a2511';
        ctx.beginPath();
        ctx.arc(comp.x + 8, comp.y + 4, 16, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#1c0d02';
        ctx.beginPath();
        ctx.arc(comp.x + 8, comp.y + 4, 8, 0, Math.PI * 2);
        ctx.fill();
        return;
      }

      // Normal component
      const cw = 16;
      const ch = 8;
      // Silver terminal pads
      ctx.fillStyle = '#dcdde1';
      ctx.fillRect(comp.x, comp.y, 4, ch);
      ctx.fillRect(comp.x + cw - 4, comp.y, 4, ch);

      // Body (Brown ceramic for capacitor, Black for resistor)
      ctx.fillStyle = comp.type === 'cap' ? '#b9770e' : '#1e272e';
      ctx.fillRect(comp.x + 4, comp.y, cw - 8, ch);
    });

    // Status Green LED
    const ledX = bx + 42;
    const ledY = by + 70;
    ctx.fillStyle = '#2ed573';
    ctx.beginPath();
    ctx.arc(ledX, ledY, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = 'rgba(46, 213, 115, 0.3)';
    ctx.beginPath();
    ctx.arc(ledX, ledY, 9, 0, Math.PI * 2);
    ctx.fill();

    // DEFECT: Deep copper trace scratch
    if (defectId === 'pcb_trace_scratch') {
      ctx.strokeStyle = '#c0392b';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(bx + 80, by + 35);
      ctx.lineTo(bx + 145, by + 85);
      ctx.stroke();

      ctx.strokeStyle = '#f1c40f'; // exposed copper sheen
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(bx + 82, by + 36);
      ctx.lineTo(bx + 143, by + 84);
      ctx.stroke();
    }

    // DEFECT: Solder flux / oil contamination splatter
    if (defectId === 'pcb_oil_flux') {
      ctx.fillStyle = 'rgba(180, 115, 30, 0.65)';
      ctx.beginPath();
      ctx.ellipse(w / 2 + 55, h / 2 + 45, 20, 14, Math.PI / 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(w / 2 + 75, h / 2 + 35, 5, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // 2. MACHINED STEEL BEARING & GEAR FLANGE RENDERER
  renderBearing(ctx, rng, defectId) {
    const w = this.width;
    const h = this.height;
    const cx = w / 2;
    const cy = h / 2;

    // Inspection background
    ctx.fillStyle = '#14161a';
    ctx.fillRect(0, 0, w, h);

    // Gear base parameters
    const outerR = 125;
    const rootR = 105;
    const teethCount = 12;
    const jitterAngle = (rng() - 0.5) * 0.08;

    // Shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.45)';
    ctx.beginPath();
    ctx.arc(cx + 6, cy + 6, outerR + 2, 0, Math.PI * 2);
    ctx.fill();

    // Draw Gear Outer Teeth
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(jitterAngle);

    ctx.beginPath();
    for (let i = 0; i < teethCount; i++) {
      const a0 = (i / teethCount) * Math.PI * 2;
      const a1 = a0 + (Math.PI / teethCount) * 0.45;
      const a2 = a0 + (Math.PI / teethCount) * 0.85;
      const a3 = ((i + 1) / teethCount) * Math.PI * 2;

      // DEFECT: Broken Tooth on tooth #3
      let rTip = outerR;
      if (defectId === 'gear_broken_tooth' && i === 3) {
        rTip = rootR + 4; // broken off!
      }

      const x0 = Math.cos(a0) * rootR;
      const y0 = Math.sin(a0) * rootR;
      const x1 = Math.cos(a1) * rTip;
      const y1 = Math.sin(a1) * rTip;
      const x2 = Math.cos(a2) * rTip;
      const y2 = Math.sin(a2) * rTip;
      const x3 = Math.cos(a3) * rootR;
      const y3 = Math.sin(a3) * rootR;

      if (i === 0) ctx.moveTo(x0, y0);
      else ctx.lineTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.lineTo(x3, y3);
    }
    ctx.closePath();

    // Machined Steel Radial Gradient
    const metalGrad = ctx.createRadialGradient(-20, -20, 20, 0, 0, outerR);
    metalGrad.addColorStop(0, '#e4e7eb');
    metalGrad.addColorStop(0.4, '#b0b6be');
    metalGrad.addColorStop(0.7, '#cfd4db');
    metalGrad.addColorStop(1, '#868e96');
    ctx.fillStyle = metalGrad;
    ctx.fill();

    ctx.strokeStyle = '#495057';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Precision Machining Concentric Grooves
    for (let r = 85; r >= 50; r -= 10) {
      ctx.strokeStyle = (r % 20 === 0) ? 'rgba(255, 255, 255, 0.25)' : 'rgba(0, 0, 0, 0.2)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Center Bore Hole
    const boreR = 38;
    ctx.fillStyle = '#0f1115';
    ctx.beginPath();
    ctx.arc(0, 0, boreR, 0, Math.PI * 2);
    ctx.fill();

    // Keyway Slot in Bore
    ctx.fillRect(-6, -boreR - 8, 12, 12);

    // Bore Inner Chamfer
    ctx.strokeStyle = '#ced4da';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(0, 0, boreR, 0, Math.PI * 2);
    ctx.stroke();

    // DEFECT: Surface Pitting / Corrosion Dent
    if (defectId === 'gear_pitting_corrosion') {
      ctx.fillStyle = '#8b4513';
      ctx.beginPath();
      ctx.arc(48, -35, 9, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#4a2505';
      ctx.beginPath();
      ctx.arc(48, -35, 5, 0, Math.PI * 2);
      ctx.fill();
      // Satellite rust pits
      ctx.fillStyle = '#a0522d';
      ctx.beginPath();
      ctx.arc(58, -30, 3, 0, Math.PI * 2);
      ctx.arc(42, -45, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // DEFECT: Axial Bore Gouge / Deep Scratch
    if (defectId === 'gear_deep_scratch') {
      ctx.strokeStyle = '#2b2d42';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(-60, 20);
      ctx.lineTo(-20, 65);
      ctx.stroke();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(-59, 21);
      ctx.lineTo(-21, 64);
      ctx.stroke();
    }

    // DEFECT: Heavy Industrial Grease Stain
    if (defectId === 'gear_oil_stain') {
      ctx.fillStyle = 'rgba(25, 20, 10, 0.75)';
      ctx.beginPath();
      ctx.ellipse(-30, -50, 22, 12, 0.4, 0, Math.PI * 2);
      ctx.fill();
    }

    // DEFECT: Machining Edge Burr
    if (defectId === 'gear_machining_burr') {
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(outerR - 2, 0, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#222';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    ctx.restore();
  }

  // 3. PHARMACEUTICAL 10-CAPSULE BLISTER PACK RENDERER
  renderBlisterPack(ctx, rng, defectId) {
    const w = this.width;
    const h = this.height;

    ctx.fillStyle = '#16191f';
    ctx.fillRect(0, 0, w, h);

    const bx = 36;
    const by = 25;
    const bw = w - 72;
    const bh = h - 50;

    // Aluminum Foil Blister Card
    const foilGrad = ctx.createLinearGradient(bx, by, bx + bw, by + bh);
    foilGrad.addColorStop(0, '#f1f3f5');
    foilGrad.addColorStop(0.3, '#d8dcde');
    foilGrad.addColorStop(0.7, '#e9ecef');
    foilGrad.addColorStop(1, '#c5cbce');
    ctx.fillStyle = foilGrad;
    ctx.beginPath();
    ctx.roundRect(bx, by, bw, bh, 10);
    ctx.fill();

    // Waffle heat-seal pattern along border
    ctx.fillStyle = 'rgba(0, 0, 0, 0.08)';
    for (let x = bx + 6; x < bx + bw - 6; x += 5) {
      ctx.fillRect(x, by + 4, 2, 4);
      ctx.fillRect(x, by + bh - 8, 2, 4);
    }
    for (let y = by + 6; y < by + bh - 6; y += 5) {
      ctx.fillRect(bx + 4, y, 4, 2);
      ctx.fillRect(bx + bw - 8, y, 4, 2);
    }

    // Silkscreen Batch & Expiry
    ctx.fillStyle = '#495057';
    ctx.font = 'bold 8px sans-serif';
    ctx.fillText('AMOX-500mg | EXP: 11/2028 | LOT: #9204A', bx + 16, by + bh - 14);

    // 2 rows x 5 columns of capsules
    const cols = 5;
    const rows = 2;
    const startX = bx + 24;
    const startY = by + 42;
    const stepX = (bw - 48) / (cols - 1);
    const stepY = (bh - 95) / (rows - 1);

    let pillIdx = 0;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        pillIdx++;
        const cx = startX + c * stepX;
        const cy = startY + r * stepY;

        // Clear Blister Cavity Dome
        ctx.fillStyle = 'rgba(0, 0, 0, 0.12)';
        ctx.beginPath();
        ctx.roundRect(cx - 14, cy - 26, 28, 52, 14);
        ctx.fill();

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(cx - 14, cy - 26, 28, 52, 14);
        ctx.stroke();

        // DEFECT: Missing Capsule (Cavity #7 empty)
        if (defectId === 'blister_missing_pill' && pillIdx === 7) {
          // Just empty plastic pocket!
          ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
          ctx.fillRect(cx - 8, cy - 18, 16, 36);
          continue;
        }

        // DEFECT: Crushed Capsule (#3)
        if (defectId === 'blister_crushed_pill' && pillIdx === 3) {
          ctx.fillStyle = '#d9534f';
          ctx.beginPath();
          ctx.ellipse(cx, cy, 14, 8, 0.4, 0, Math.PI * 2);
          ctx.fill();
          // White powder spill
          ctx.fillStyle = '#f8f9fa';
          ctx.beginPath();
          ctx.arc(cx - 6, cy + 8, 5, 0, Math.PI * 2);
          ctx.arc(cx + 4, cy - 7, 4, 0, Math.PI * 2);
          ctx.fill();
          continue;
        }

        // Normal Bicolor Capsule (Top: Royal Blue, Bottom: Clean White)
        const capW = 18;
        const capH = 40;

        // DEFECT: Discolored pill (#8)
        let topColor = '#1971c2';
        let botColor = '#f8f9fa';
        if (defectId === 'blister_discolored_pill' && pillIdx === 8) {
          topColor = '#8a5a00';
          botColor = '#bf9b30'; // oxidized/yellowed
        }

        // Top half (Blue)
        ctx.fillStyle = topColor;
        ctx.beginPath();
        ctx.roundRect(cx - capW / 2, cy - capH / 2, capW, capH / 2, [9, 9, 0, 0]);
        ctx.fill();

        // Bottom half (White)
        ctx.fillStyle = botColor;
        ctx.beginPath();
        ctx.roundRect(cx - capW / 2, cy, capW, capH / 2, [0, 0, 9, 9]);
        ctx.fill();

        // Capsule Gloss Sheen
        ctx.fillStyle = 'rgba(255, 255, 255, 0.35)';
        ctx.fillRect(cx - 5, cy - capH / 2 + 4, 3, capH - 8);
      }
    }

    // DEFECT: Torn / Punctured Foil Seal (over Cavity #2)
    if (defectId === 'blister_punctured_foil') {
      const fx = startX + stepX;
      const fy = startY;
      ctx.strokeStyle = '#c92a2a';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(fx - 15, fy - 10);
      ctx.lineTo(fx + 12, fy + 8);
      ctx.moveTo(fx + 10, fy - 12);
      ctx.lineTo(fx - 8, fy + 14);
      ctx.stroke();

      ctx.fillStyle = '#111';
      ctx.beginPath();
      ctx.arc(fx, fy, 4, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // 4. BEVERAGE BOTTLE CAP & TAMPER SEAL RENDERER
  renderBottleCap(ctx, rng, defectId) {
    const w = this.width;
    const h = this.height;
    const cx = w / 2;
    const cy = h / 2;

    ctx.fillStyle = '#14171d';
    ctx.fillRect(0, 0, w, h);

    const outerR = 110;
    const capR = 92;
    const ribs = 36;

    // Drop Shadow
    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.beginPath();
    ctx.arc(cx + 4, cy + 4, outerR, 0, Math.PI * 2);
    ctx.fill();

    // DEFECT: Broken Tamper-Evident Ring
    const isRingBroken = defectId === 'cap_broken_seal';

    // Outer Tamper Ring Flutes / Bridges
    for (let i = 0; i < ribs; i++) {
      const angle = (i / ribs) * Math.PI * 2;
      const x0 = cx + Math.cos(angle) * (outerR - 10);
      const y0 = cy + Math.sin(angle) * (outerR - 10);
      const x1 = cx + Math.cos(angle) * outerR;
      const y1 = cy + Math.sin(angle) * outerR;

      // If broken, skip bridge at 45 degrees
      if (isRingBroken && i >= 4 && i <= 8) {
        ctx.strokeStyle = '#1e232a'; // gap!
      } else {
        ctx.strokeStyle = '#c92a2a'; // red bottle cap plastic
      }
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
    }

    if (isRingBroken) {
      // White torn plastic stress mark
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(cx + 80, cy - 60, 5, 0, Math.PI * 2);
      ctx.fill();
    }

    // DEFECT: Skewed Cross-Thread Cap Offset
    let capOffX = 0;
    let capOffY = 0;
    if (defectId === 'cap_skewed_thread') {
      capOffX = 14;
      capOffY = -10;
    }

    // Main Cap Body (Deep Crimson Red with subtle radial highlights)
    const capGrad = ctx.createRadialGradient(cx + capOffX - 25, cy + capOffY - 25, 20, cx + capOffX, cy + capOffY, capR);
    capGrad.addColorStop(0, '#ff6b6b');
    capGrad.addColorStop(0.5, '#e03131');
    capGrad.addColorStop(1, '#9b111e');

    ctx.fillStyle = capGrad;
    ctx.beginPath();
    ctx.arc(cx + capOffX, cy + capOffY, capR, 0, Math.PI * 2);
    ctx.fill();

    // Cap Grip Ribs (Knurling on outer perimeter)
    for (let r = 0; r < 48; r++) {
      const a = (r / 48) * Math.PI * 2;
      const rx0 = cx + capOffX + Math.cos(a) * (capR - 8);
      const ry0 = cy + capOffY + Math.sin(a) * (capR - 8);
      const rx1 = cx + capOffX + Math.cos(a) * capR;
      const ry1 = cy + capOffY + Math.sin(a) * capR;

      ctx.strokeStyle = (r % 2 === 0) ? '#ff8787' : '#720b15';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(rx0, ry0);
      ctx.lineTo(rx1, ry1);
      ctx.stroke();
    }

    // Center Embossed Seal Circle
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx + capOffX, cy + capOffY, 48, 0, Math.PI * 2);
    ctx.stroke();

    // Center Logo Mark
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('PURE•QC', cx + capOffX, cy + capOffY - 6);
    ctx.font = '8px sans-serif';
    ctx.fillText('SEALED', cx + capOffX, cy + capOffY + 8);

    // DEFECT: Impact Dent / Puncture on crown
    if (defectId === 'cap_crown_dent') {
      ctx.fillStyle = '#491013';
      ctx.beginPath();
      ctx.ellipse(cx + capOffX + 24, cy + capOffY + 18, 14, 8, -0.3, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#2b0608';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // DEFECT: Plastic Flash / Excess molding protrusion
    if (defectId === 'cap_plastic_flash') {
      ctx.fillStyle = '#ff6b6b';
      ctx.beginPath();
      ctx.moveTo(cx + capR - 2, cy);
      ctx.lineTo(cx + capR + 18, cy - 10);
      ctx.lineTo(cx + capR + 14, cy + 12);
      ctx.closePath();
      ctx.fill();
    }
  }
}
