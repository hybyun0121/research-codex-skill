#!/usr/bin/env node
import { Automizer } from 'pptx-automizer';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');
const defaultTemplate = path.join(skillRoot, 'templates', 'pptx', 'template_yonsei.pptx');
const defaultFont = 'Gothic A1';

const C = {
  navy: '004F8B',
  navyDark: '00205B',
  sky: '4A94D0',
  blue: '2563EB',
  pale: 'F5F8FC',
  ice: 'EAF3FF',
  ink: '111827',
  slate: '334155',
  muted: '64748B',
  line: 'D7E0EA',
  white: 'FFFFFF',
  green: '047857',
  amber: 'B45309',
  red: 'B91C1C',
};

const removeShapes = {
  1: [
    'Google Shape;40;p5',
    'Google Shape;41;p5',
    'Google Shape;42;p5',
    'Google Shape;43;p5',
    'Google Shape;44;p5',
  ],
  2: ['Google Shape;50;p6'],
  3: ['Google Shape;57;p7', 'Google Shape;59;p7'],
};

const box = {
  cover: {
    eyebrow: { x: 0.34, y: 0.84, w: 5.35, h: 0.28 },
    title: { x: 0.34, y: 1.58, w: 9.18, h: 1.08 },
    subtitle: { x: 0.34, y: 2.84, w: 8.8, h: 0.54 },
    thesis: { x: 3.6, y: 3.55, w: 5.9, h: 1.24 },
    meta: { x: 0.34, y: 4.98, w: 4.3, h: 0.18 },
  },
  claim: {
    title: { x: 0.52, y: 0.46, w: 8.85, h: 0.44 },
    statement: { x: 0.68, y: 1.18, w: 8.48, h: 0.96 },
    cards: { x: 0.68, y: 2.42, w: 8.48, h: 1.1 },
    footer: { x: 0.52, y: 4.07, w: 8.65, h: 0.44 },
    page: { x: 9.39, y: 5.27, w: 0.27, h: 0.13 },
  },
  content: {
    title: { x: 0.34, y: 0.08, w: 8.86, h: 0.28 },
    subtitle: { x: 0.34, y: 0.48, w: 8.8, h: 0.22 },
    body: { x: 0.36, y: 0.98, w: 9.26, h: 3.82 },
    source: { x: 0.34, y: 5.15, w: 8.65, h: 0.16 },
    page: { x: 9.39, y: 5.27, w: 0.27, h: 0.13 },
  },
};

function parseArgs(argv) {
  const args = {
    state: '.research-agent/state.json',
    output: 'slides/research-presentation.pptx',
    previewDir: 'research/assets/slides',
    template: defaultTemplate,
    font: defaultFont,
  };
  for (let i = 0; i < argv.length; i += 1) {
    if (!argv[i].startsWith('--')) continue;
    const key = argv[i].slice(2).replace(/-([a-z])/g, (_, l) => l.toUpperCase());
    const value = argv[i + 1];
    if (value === undefined || value.startsWith('--')) throw new Error(`missing value for ${argv[i]}`);
    args[key] = value;
    i += 1;
  }
  return args;
}

function inferRepoRoot(statePath) {
  const resolved = path.resolve(statePath);
  if (path.basename(path.dirname(resolved)) === '.research-agent') return path.dirname(path.dirname(resolved));
  return process.cwd();
}

function resolveFrom(root, value) {
  return path.isAbsolute(value) ? value : path.resolve(root, value);
}

function compact(value, max = 130) {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (text.length <= max) return text;
  return `${text.slice(0, max - 1).trim()}...`;
}

function list(value) {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
}

function pick(obj, keys, fallback = '') {
  if (obj === null || obj === undefined) return fallback;
  if (typeof obj !== 'object') return compact(obj);
  for (const key of keys) {
    if (obj[key]) return compact(obj[key]);
  }
  return compact(Object.values(obj).filter(Boolean).slice(0, 3).join(' | '), 120) || fallback;
}

function paper(row, index) {
  if (!row || typeof row !== 'object') return compact(row || `Prior work ${index + 1}`, 44);
  const title = compact(row.title || `Prior work ${index + 1}`, 38);
  const venue = row.venue_year || row.venue || '';
  return venue ? `${title}\n${venue}` : title;
}

function experimentRows(experiments) {
  const rows = list(experiments.plan).slice(0, 4).map((row) => ({
    claim: pick(row, ['claim', 'name'], 'Main claim'),
    dataset: pick(row, ['dataset', 'benchmark'], 'Target benchmark'),
    metric: pick(row, ['metric'], 'Primary metric'),
    baseline: pick(row, ['baseline'], 'Closest baseline'),
  }));
  if (rows.length) return rows;
  return [
    { claim: 'Main effect', dataset: 'Target benchmark', metric: 'Primary metric', baseline: 'Closest prior method' },
    { claim: 'Ablation', dataset: 'Same split', metric: 'Delta vs full model', baseline: 'Remove novel component' },
  ];
}

function buildDeck(state) {
  const research = state.research || {};
  const motivation = state.motivation || {};
  const method = state.method || {};
  const experiments = state.experiments || {};
  const project = state.project || {};

  const question = research.question || 'Untitled Research Question';
  const domain = research.domain || project.repo_name || 'Research project';
  const direction = research.selected_direction || 'A selected research direction should be recorded before final slides.';
  const criteria = list(motivation.criteria);
  const gaps = list(motivation.gaps);
  const landscape = list(motivation.landscape);
  const claims = list(experiments.claims);
  const risks = list(experiments.risks);
  const qualitative = list(experiments.qualitative);
  const sweeps = list(experiments.sweeps);

  const gap = compact(gaps[0] || 'The closest methods leave a measurable gap that this project targets.', 126);
  const methodClaim = compact(method.claim || direction, 145);
  const mechanism = compact(method.algorithm || method.formulation || 'Turn the novelty claim into an executable mechanism.', 120);
  const test = compact(claims[0] || 'A falsifiable evaluation must compare against strong baselines and isolate the new component.', 120);

  return [
    {
      slide: 1,
      type: 'cover',
      eyebrow: domain,
      title: question,
      subtitle: 'Motivation, method, and evaluation plan for a paper-quality research direction',
      thesis: direction,
      meta: 'Research Agent final deck',
    },
    {
      slide: 2,
      type: 'claim',
      title: 'One-Sentence Thesis',
      statement: methodClaim,
      cards: [
        { label: 'Problem', text: gap, color: C.red },
        { label: 'Mechanism', text: mechanism, color: C.blue },
        { label: 'Falsification', text: test, color: C.green },
      ],
      footer: 'The presentation should defend a claim that can be rejected by experiments.',
    },
    {
      slide: 3,
      type: 'cards',
      title: 'Why This Problem Matters',
      subtitle: 'A strong paper starts by making the gap unavoidable',
      cards: [
        { label: 'Impact', text: compact(criteria[0] || 'The problem changes capability, cost, safety, or scientific understanding.', 110) },
        { label: 'Gap', text: gap },
        { label: 'Feasibility', text: compact(criteria[1] || 'The project can be tested with available data, compute, and baselines.', 110) },
      ],
      source: 'source: research/motivation.md',
    },
    {
      slide: 3,
      type: 'matrix',
      title: 'Prior Work Leaves a Specific Opening',
      subtitle: 'Novelty must be visible against the closest methods',
      rows: (landscape.length ? landscape : [{}, {}, {}]).slice(0, 4).map((row, i) => ({
        paper: paper(row, i),
        contribution: pick(row, ['main_contribution', 'contribution', 'method'], 'Known contribution'),
        limitation: pick(row, ['limitation', 'gap'], i === 0 ? gap : 'Remaining limitation'),
      })),
      takeaway: gap,
      source: 'source: research/motivation.md',
    },
    {
      slide: 3,
      type: 'pipeline',
      title: 'Method Overview',
      subtitle: 'The audience should see where the novelty enters the computation',
      stages: [
        { label: 'Input', text: 'Task instance / query' },
        { label: 'Signal', text: compact(method.formulation || 'Compute the signal used by the proposed method.', 70) },
        { label: 'Intervention', text: compact(mechanism, 70) },
        { label: 'Output', text: 'Prediction with measurable evidence' },
      ],
      claim: methodClaim,
      source: 'source: research/method.md',
    },
    {
      slide: 3,
      type: 'contrast',
      title: 'What Is Actually New',
      subtitle: 'Separate the proposal from nearby engineering baselines',
      leftTitle: 'Closest Prior Pattern',
      left: [
        pick(landscape[0], ['main_contribution', 'contribution'], 'Strong baseline behavior'),
        pick(landscape[0], ['limitation'], 'Does not close the selected gap directly'),
      ],
      rightTitle: 'This Proposal',
      right: [direction, mechanism],
      source: 'source: research/method.md',
    },
    {
      slide: 3,
      type: 'experiment',
      title: 'Experimental Design',
      subtitle: 'Every claim gets a benchmark, metric, and baseline',
      rows: experimentRows(experiments),
      decision: 'Accept the thesis only if the method improves the target metric and ablations isolate the novel component.',
      source: 'source: research/experiments.md',
    },
    {
      slide: 3,
      type: 'cards',
      title: 'Ablations and Failure Analysis',
      subtitle: 'A paper-quality evaluation explains both gains and boundaries',
      cards: [
        { label: 'Ablation', text: compact(pick(sweeps[0], ['name', 'claim'], 'Vary or remove the novel component.'), 110) },
        { label: 'Qualitative', text: compact(qualitative[0] || 'Inspect representative successes and failures.', 110) },
        { label: 'Risk', text: compact(risks[0] || 'State the main validity threat before claiming success.', 110) },
      ],
      source: 'source: research/experiments.md',
    },
    {
      slide: 2,
      type: 'claim',
      title: 'Expected Contribution',
      statement: direction,
      cards: [
        { label: 'Method', text: methodClaim, color: C.blue },
        { label: 'Evidence', text: test, color: C.green },
        { label: 'Next Step', text: compact(risks[0] || 'Lock benchmarks and run first baseline comparison.', 110), color: C.amber },
      ],
      footer: 'The final deck is a research argument: claim, mechanism, evidence, and risk.',
    },
  ];
}

function removeTemplateText(slide, templateSlide) {
  for (const name of removeShapes[templateSlide] || []) {
    try {
      slide.removeElement(name);
    } catch {
      // Template revisions can rename decorative shapes.
    }
  }
}

function text(s, content, b, opt = {}) {
  s.addText(content || '', {
    x: b.x,
    y: b.y,
    w: b.w,
    h: b.h,
    fontFace: opt.fontFace || defaultFont,
    fontSize: opt.size || 10,
    bold: opt.bold || false,
    color: opt.color || C.ink,
    align: opt.align || 'left',
    valign: opt.valign || 'mid',
    margin: opt.margin ?? 0.04,
    fit: 'shrink',
    breakLine: false,
    fill: opt.fill ? { color: opt.fill, transparency: opt.transparency || 0 } : undefined,
    line: opt.line ? { color: opt.line, transparency: opt.lineTransparency || 0, width: opt.lineWidth || 1 } : undefined,
  });
}

function title(s, spec, fontFace) {
  text(s, spec.title, box.content.title, { fontFace, size: 14, bold: true, color: C.white, margin: 0 });
  text(s, spec.subtitle || '', box.content.subtitle, { fontFace, size: 8.2, color: C.white, margin: 0 });
}

function pageAndSource(s, spec, pageNumber, fontFace) {
  if (spec.source && spec.slide === 3) {
    text(s, spec.source, box.content.source, { fontFace, size: 6.2, color: C.muted, margin: 0 });
  }
  const p = spec.slide === 3 ? box.content.page : box.claim.page;
  text(s, String(pageNumber), p, { fontFace, size: 6.5, color: C.white, align: 'center', margin: 0 });
}

function drawCover(s, spec, fontFace) {
  text(s, spec.eyebrow, box.cover.eyebrow, { fontFace, size: 10, bold: true, color: C.navy, margin: 0 });
  text(s, spec.title, box.cover.title, { fontFace, size: 24, bold: true, color: C.ink, margin: 0 });
  text(s, spec.subtitle, box.cover.subtitle, { fontFace, size: 11, color: C.slate, margin: 0 });
  text(s, spec.thesis, box.cover.thesis, {
    fontFace,
    size: 13.5,
    bold: true,
    color: C.white,
    fill: C.navy,
    line: C.navy,
    margin: 0.1,
  });
  text(s, spec.meta, box.cover.meta, { fontFace, size: 7.2, color: C.muted, margin: 0 });
}

function drawClaim(s, spec, fontFace) {
  text(s, spec.title, box.claim.title, { fontFace, size: 18.5, bold: true, color: C.ink, margin: 0 });
  text(s, spec.statement, box.claim.statement, {
    fontFace,
    size: 19,
    bold: true,
    color: C.white,
    fill: C.navy,
    line: C.navy,
    margin: 0.12,
  });
  const gap = 0.12;
  const w = (box.claim.cards.w - gap * 2) / 3;
  spec.cards.forEach((card, i) => {
    const x = box.claim.cards.x + i * (w + gap);
    text(s, card.label, { x, y: box.claim.cards.y, w, h: 0.28 }, {
      fontFace,
      size: 8.3,
      bold: true,
      color: card.color || C.blue,
      fill: C.pale,
      line: C.line,
      margin: 0.06,
    });
    text(s, card.text, { x, y: box.claim.cards.y + 0.28, w, h: 0.76 }, {
      fontFace,
      size: 8.6,
      color: C.slate,
      fill: C.white,
      line: C.line,
      valign: 'top',
      margin: 0.08,
    });
  });
  text(s, spec.footer, box.claim.footer, { fontFace, size: 9.8, bold: true, color: C.white, margin: 0.08 });
}

function drawCards(s, spec, fontFace) {
  title(s, spec, fontFace);
  const body = box.content.body;
  const gap = 0.18;
  const w = (body.w - gap * 2) / 3;
  spec.cards.forEach((card, i) => {
    const x = body.x + i * (w + gap);
    text(s, card.label, { x, y: body.y + 0.08, w, h: 0.38 }, {
      fontFace,
      size: 12,
      bold: true,
      color: C.white,
      fill: i === 1 ? C.navy : C.blue,
      line: i === 1 ? C.navy : C.blue,
      align: 'center',
      margin: 0.06,
    });
    text(s, card.text, { x, y: body.y + 0.56, w, h: 2.44 }, {
      fontFace,
      size: 12.3,
      bold: i === 1,
      color: C.ink,
      fill: C.white,
      line: C.line,
      align: 'center',
      margin: 0.12,
    });
  });
}

function drawMatrix(s, spec, fontFace) {
  title(s, spec, fontFace);
  const body = box.content.body;
  const widths = [2.5, 3.15, 3.18];
  const xs = [body.x, body.x + widths[0], body.x + widths[0] + widths[1]];
  ['Paper', 'Contribution', 'Limitation'].forEach((h, i) => {
    text(s, h, { x: xs[i], y: body.y + 0.05, w: widths[i] - 0.04, h: 0.28 }, {
      fontFace,
      size: 8.1,
      bold: true,
      color: C.white,
      fill: C.navy,
      line: C.navy,
      margin: 0.05,
    });
  });
  spec.rows.slice(0, 4).forEach((row, r) => {
    const y = body.y + 0.38 + r * 0.55;
    [row.paper, row.contribution, row.limitation].forEach((value, i) => {
      text(s, value, { x: xs[i], y, w: widths[i] - 0.04, h: 0.51 }, {
        fontFace,
        size: 7.2,
        color: i === 2 ? C.red : C.slate,
        fill: r % 2 ? C.pale : C.white,
        line: C.line,
        margin: 0.05,
      });
    });
  });
  text(s, `Opening: ${spec.takeaway}`, { x: body.x, y: body.y + 3.02, w: body.w, h: 0.48 }, {
    fontFace,
    size: 10.8,
    bold: true,
    color: C.white,
    fill: C.navy,
    line: C.navy,
    margin: 0.08,
  });
}

function drawPipeline(s, spec, fontFace) {
  title(s, spec, fontFace);
  const body = box.content.body;
  const stepW = 1.86;
  const gap = 0.36;
  const y = body.y + 0.72;
  spec.stages.forEach((stage, i) => {
    const x = body.x + i * (stepW + gap);
    text(s, stage.label, { x, y, w: stepW, h: 0.36 }, {
      fontFace,
      size: 10.2,
      bold: true,
      color: C.white,
      fill: i === 1 ? C.navy : C.blue,
      line: i === 1 ? C.navy : C.blue,
      align: 'center',
      margin: 0.05,
    });
    text(s, stage.text, { x, y: y + 0.42, w: stepW, h: 0.82 }, {
      fontFace,
      size: 8.2,
      color: C.slate,
      fill: C.white,
      line: C.line,
      align: 'center',
      margin: 0.07,
    });
    if (i < spec.stages.length - 1) {
      text(s, '>', { x: x + stepW + 0.05, y: y + 0.55, w: 0.2, h: 0.22 }, {
        fontFace,
        size: 11,
        bold: true,
        color: C.muted,
        align: 'center',
        margin: 0,
      });
    }
  });
  text(s, `Method claim: ${spec.claim}`, { x: body.x + 0.46, y: body.y + 2.72, w: body.w - 0.92, h: 0.62 }, {
    fontFace,
    size: 11.7,
    bold: true,
    color: C.ink,
    fill: C.ice,
    line: C.line,
    align: 'center',
    margin: 0.1,
  });
}

function drawContrast(s, spec, fontFace) {
  title(s, spec, fontFace);
  const body = box.content.body;
  const gap = 0.3;
  const w = (body.w - gap) / 2;
  [
    { title: spec.leftTitle, items: spec.left, x: body.x, color: C.muted },
    { title: spec.rightTitle, items: spec.right, x: body.x + w + gap, color: C.navy },
  ].forEach((col) => {
    text(s, col.title, { x: col.x, y: body.y + 0.16, w, h: 0.38 }, {
      fontFace,
      size: 11.4,
      bold: true,
      color: C.white,
      fill: col.color,
      line: col.color,
      align: 'center',
      margin: 0.06,
    });
    col.items.slice(0, 2).forEach((item, i) => {
      text(s, item, { x: col.x, y: body.y + 0.72 + i * 1.1, w, h: 0.86 }, {
        fontFace,
        size: 10.7,
        bold: col.color === C.navy,
        color: C.ink,
        fill: C.white,
        line: C.line,
        align: 'center',
        margin: 0.1,
      });
    });
  });
}

function drawExperiment(s, spec, fontFace) {
  title(s, spec, fontFace);
  const body = box.content.body;
  const widths = [2.18, 2.22, 2.0, 2.38];
  const xs = [body.x, body.x + widths[0], body.x + widths[0] + widths[1], body.x + widths[0] + widths[1] + widths[2]];
  ['Claim', 'Dataset', 'Metric', 'Baseline'].forEach((h, i) => {
    text(s, h, { x: xs[i], y: body.y + 0.08, w: widths[i] - 0.04, h: 0.32 }, {
      fontFace,
      size: 8,
      bold: true,
      color: C.white,
      fill: C.navy,
      line: C.navy,
      margin: 0.05,
    });
  });
  spec.rows.slice(0, 4).forEach((row, r) => {
    const y = body.y + 0.48 + r * 0.63;
    [row.claim, row.dataset, row.metric, row.baseline].forEach((value, i) => {
      text(s, value, { x: xs[i], y, w: widths[i] - 0.04, h: 0.58 }, {
        fontFace,
        size: 7.3,
        color: C.slate,
        fill: r % 2 ? C.pale : C.white,
        line: C.line,
        margin: 0.05,
      });
    });
  });
  text(s, spec.decision, { x: body.x, y: body.y + 3.22, w: body.w, h: 0.46 }, {
    fontFace,
    size: 9.3,
    bold: true,
    color: C.white,
    fill: C.navy,
    line: C.navy,
    margin: 0.08,
  });
}

function drawSlide(slide, spec, pageNumber, fontFace) {
  removeTemplateText(slide, spec.slide);
  slide.generate((s) => {
    if (spec.type === 'cover') drawCover(s, spec, fontFace);
    if (spec.type === 'claim') drawClaim(s, spec, fontFace);
    if (spec.type === 'cards') drawCards(s, spec, fontFace);
    if (spec.type === 'matrix') drawMatrix(s, spec, fontFace);
    if (spec.type === 'pipeline') drawPipeline(s, spec, fontFace);
    if (spec.type === 'contrast') drawContrast(s, spec, fontFace);
    if (spec.type === 'experiment') drawExperiment(s, spec, fontFace);
    pageAndSource(s, spec, pageNumber, fontFace);
  }, `research-agent-content-${pageNumber}`);
}

function escapeXml(value) {
  return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function wrap(text, maxChars) {
  const words = compact(text, 180).split(/\s+/).filter(Boolean);
  const lines = [];
  let line = '';
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > maxChars && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) lines.push(line);
  return lines;
}

function svgText(lines, x, y, opt = {}) {
  const size = opt.size || 20;
  const color = opt.color || C.ink;
  const weight = opt.weight || 400;
  const lineHeight = opt.lineHeight || Math.round(size * 1.3);
  const spans = lines.map((line, i) => `<tspan x="${x}" dy="${i === 0 ? 0 : lineHeight}">${escapeXml(line)}</tspan>`).join('');
  return `<text x="${x}" y="${y}" font-family="${escapeXml(opt.font || defaultFont)}, Arial, sans-serif" font-size="${size}" font-weight="${weight}" fill="#${color}">${spans}</text>`;
}

function svgCard(x, y, w, h, fill = C.white, stroke = C.line) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="#${fill}" stroke="#${stroke}" stroke-width="2"/>`;
}

function slideSvg(spec, page, font) {
  const p = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">', '<rect width="1600" height="900" fill="#FFFFFF"/>'];
  if (spec.slide === 3) {
    p.push(`<rect width="1600" height="68" fill="#${C.navy}"/>`, `<rect y="74" width="1600" height="52" fill="#${C.sky}"/>`);
    p.push(svgText(wrap(spec.title, 62), 56, 43, { size: 26, weight: 700, color: C.white, font }));
    p.push(svgText(wrap(spec.subtitle || '', 82), 56, 106, { size: 17, color: C.white, font }));
  } else if (spec.slide === 2) {
    p.push(`<rect y="635" width="1600" height="150" fill="#${C.navy}"/>`);
  }
  if (spec.type === 'cover') {
    p.push(svgText([spec.eyebrow], 56, 160, { size: 26, weight: 700, color: C.navy, font }));
    p.push(svgText(wrap(spec.title, 45), 56, 285, { size: 52, weight: 700, color: C.ink, lineHeight: 66, font }));
    p.push(svgText(wrap(spec.subtitle, 78), 56, 510, { size: 24, color: C.slate, font }));
    p.push(svgCard(575, 565, 950, 205, C.navy, C.navy));
    p.push(svgText(wrap(spec.thesis, 72), 620, 645, { size: 28, weight: 700, color: C.white, lineHeight: 38, font }));
  } else if (spec.type === 'claim') {
    p.push(svgText([spec.title], 84, 150, { size: 42, weight: 700, color: C.ink, font }));
    p.push(svgCard(106, 204, 1368, 150, C.navy, C.navy));
    p.push(svgText(wrap(spec.statement, 78), 150, 273, { size: 31, weight: 700, color: C.white, lineHeight: 40, font }));
    spec.cards.forEach((card, i) => {
      const x = 106 + i * 458;
      p.push(svgCard(x, 390, 420, 168));
      p.push(svgText([card.label], x + 26, 430, { size: 21, weight: 700, color: card.color || C.blue, font }));
      p.push(svgText(wrap(card.text, 38), x + 26, 480, { size: 18, color: C.slate, lineHeight: 25, font }));
    });
    p.push(svgText(wrap(spec.footer, 92), 86, 710, { size: 24, weight: 700, color: C.white, font }));
  } else if (spec.type === 'cards') {
    spec.cards.forEach((card, i) => {
      const x = 58 + i * 492;
      p.push(svgCard(x, 175, 445, 500));
      p.push(`<rect x="${x}" y="175" width="445" height="68" rx="8" fill="#${i === 1 ? C.navy : C.blue}"/>`);
      p.push(svgText([card.label], x + 26, 220, { size: 26, weight: 700, color: C.white, font }));
      p.push(svgText(wrap(card.text, 32), x + 28, 365, { size: 29, weight: i === 1 ? 700 : 500, color: C.ink, lineHeight: 40, font }));
    });
  } else if (spec.type === 'pipeline') {
    spec.stages.forEach((stage, i) => {
      const x = 70 + i * 360;
      p.push(svgCard(x, 245, 300, 210));
      p.push(`<rect x="${x}" y="245" width="300" height="62" rx="8" fill="#${i === 1 ? C.navy : C.blue}"/>`);
      p.push(svgText([stage.label], x + 24, 286, { size: 22, weight: 700, color: C.white, font }));
      p.push(svgText(wrap(stage.text, 26), x + 24, 354, { size: 18, color: C.slate, lineHeight: 26, font }));
      if (i < spec.stages.length - 1) p.push(svgText(['>'], x + 318, 365, { size: 34, weight: 700, color: C.muted, font }));
    });
    p.push(svgCard(245, 615, 1110, 96, C.ice, C.line));
    p.push(svgText(wrap(`Method claim: ${spec.claim}`, 82), 285, 672, { size: 23, weight: 700, color: C.ink, font }));
  } else if (spec.type === 'matrix') {
    const xs = [58, 458, 960];
    const ws = [390, 492, 492];
    ['Paper', 'Contribution', 'Limitation'].forEach((h, i) => {
      p.push(`<rect x="${xs[i]}" y="160" width="${ws[i]}" height="54" fill="#${C.navy}"/>`);
      p.push(svgText([h], xs[i] + 18, 196, { size: 20, weight: 700, color: C.white, font }));
    });
    spec.rows.slice(0, 4).forEach((row, r) => {
      const y = 224 + r * 88;
      [row.paper, row.contribution, row.limitation].forEach((value, i) => {
        p.push(`<rect x="${xs[i]}" y="${y}" width="${ws[i]}" height="78" fill="#${r % 2 ? C.pale : C.white}" stroke="#${C.line}" stroke-width="2"/>`);
        p.push(svgText(wrap(value, i === 0 ? 30 : 42), xs[i] + 16, y + 30, {
          size: 16,
          weight: i === 2 ? 700 : 500,
          color: i === 2 ? C.red : C.slate,
          lineHeight: 21,
          font,
        }));
      });
    });
    p.push(svgCard(58, 600, 1394, 86, C.navy, C.navy));
    p.push(svgText(wrap(`Opening: ${spec.takeaway}`, 96), 92, 652, { size: 22, weight: 700, color: C.white, font }));
  } else if (spec.type === 'contrast') {
    const cols = [
      { x: 88, title: spec.leftTitle, items: spec.left, color: C.muted },
      { x: 835, title: spec.rightTitle, items: spec.right, color: C.navy },
    ];
    cols.forEach((col) => {
      p.push(svgCard(col.x, 180, 650, 410));
      p.push(`<rect x="${col.x}" y="180" width="650" height="70" rx="8" fill="#${col.color}"/>`);
      p.push(svgText([col.title], col.x + 28, 226, { size: 24, weight: 700, color: C.white, font }));
      col.items.slice(0, 2).forEach((item, i) => {
        const y = 290 + i * 132;
        p.push(svgCard(col.x + 32, y, 586, 104, C.pale, C.line));
        p.push(svgText(wrap(item, 48), col.x + 58, y + 42, {
          size: 21,
          weight: col.color === C.navy ? 700 : 500,
          color: C.ink,
          lineHeight: 28,
          font,
        }));
      });
    });
  } else if (spec.type === 'experiment') {
    const xs = [58, 405, 744, 1046];
    const ws = [337, 329, 292, 406];
    ['Claim', 'Dataset', 'Metric', 'Baseline'].forEach((h, i) => {
      p.push(`<rect x="${xs[i]}" y="164" width="${ws[i]}" height="54" fill="#${C.navy}"/>`);
      p.push(svgText([h], xs[i] + 18, 199, { size: 19, weight: 700, color: C.white, font }));
    });
    spec.rows.slice(0, 4).forEach((row, r) => {
      const y = 228 + r * 84;
      [row.claim, row.dataset, row.metric, row.baseline].forEach((value, i) => {
        p.push(`<rect x="${xs[i]}" y="${y}" width="${ws[i]}" height="74" fill="#${r % 2 ? C.pale : C.white}" stroke="#${C.line}" stroke-width="2"/>`);
        p.push(svgText(wrap(value, i === 3 ? 34 : 28), xs[i] + 14, y + 31, {
          size: 15,
          color: C.slate,
          lineHeight: 20,
          font,
        }));
      });
    });
    p.push(svgCard(58, 600, 1394, 76, C.navy, C.navy));
    p.push(svgText(wrap(spec.decision, 104), 92, 647, { size: 20, weight: 700, color: C.white, font }));
  } else {
    p.push(svgCard(90, 190, 1420, 485));
    p.push(svgText(wrap(spec.title, 60), 130, 330, { size: 34, weight: 700, color: C.ink, font }));
  }
  p.push(svgText([String(page)], 1498, 846, { size: 18, color: C.white, font }), '</svg>');
  return `${p.join('\n')}\n`;
}

function writeSvgPreviews(slides, previewDir, fontFace) {
  fs.mkdirSync(previewDir, { recursive: true });
  for (const entry of fs.readdirSync(previewDir)) {
    if (/^slide-\d+\.(svg|png)$/.test(entry)) fs.unlinkSync(path.join(previewDir, entry));
  }
  slides.forEach((spec, i) => fs.writeFileSync(path.join(previewDir, `slide-${String(i + 1).padStart(2, '0')}.svg`), slideSvg(spec, i + 1, fontFace), 'utf8'));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const repoRoot = args.repo ? path.resolve(args.repo) : inferRepoRoot(args.state);
  const statePath = resolveFrom(repoRoot, args.state);
  const outputPath = resolveFrom(repoRoot, args.output);
  const previewDir = resolveFrom(repoRoot, args.previewDir);
  const templatePath = path.resolve(args.template);
  const templateDir = path.dirname(templatePath);
  const templateFile = path.basename(templatePath);
  if (!fs.existsSync(templatePath)) throw new Error(`template not found: ${templatePath}`);
  if (!fs.existsSync(statePath)) throw new Error(`state not found: ${statePath}`);

  const slides = buildDeck(JSON.parse(fs.readFileSync(statePath, 'utf8')));
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  const automizer = new Automizer({
    templateDir,
    outputDir: path.dirname(outputPath),
    autoImportSlideMasters: true,
    removeExistingSlides: true,
    cleanup: true,
    cleanupPlaceholders: false,
    compression: 0,
    verbosity: 0,
  });
  const pres = automizer.loadRoot(templateFile).load(templateFile, 'research-template');
  slides.forEach((spec, i) => pres.addSlide('research-template', spec.slide, (slide) => drawSlide(slide, spec, i + 1, args.font)));
  await pres.write(path.basename(outputPath));
  writeSvgPreviews(slides, previewDir, args.font);
  console.log(outputPath);
}

await main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
