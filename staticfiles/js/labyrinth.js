let c = document.getElementById("canv");
let $ = c.getContext("2d");
c.width = window.innerWidth;
c.height = window.innerHeight;

let max = 100;
let num = 1;
let darr = [];
let dst;
let gsz = 50;
let msX = 0;
let msY = 0;
let grav = 150;
let _psz = 1;
dst = Dist(gsz);

for (let i = 0; i < num; i++) {
  dst.add(Node(c));
}

function nPart() {
  let p;
  if (dst.parr.length < max) {
    if (darr.length > 0) {
      p = darr.pop();
      p.res_(msX, msY);
      dst.add(p);
    } else {
      p = Node(c, msX, msY)
      dst.add(p);
    }
  }
  return p;
}

let pull = .03;

function txt(){
  let t = "EULER GAMES".split("").join(String.fromCharCode(0x2004));
  $.font = "5.5em Philosopher";
  $.fillStyle = 'hsla(0,0%,30%,1)';
  $.fillText(t, (c.width - $.measureText(t).width) * 0.5, c.height * 0.5);
}

function draw() {
 $.fillStyle = 'hsla(0,0%,95%,.45)';
 $.fillRect(0, 0, c.width, c.height);
  txt();
  dst.ref();
  let pos = dst.pos;
  let i = dst.parr.length;
  while (i--) {
    let p = dst.parr[i];
    let n = dst.next(p);
    if (n) {
      let l = n.length;
      while (l--) {
        let pnxt = n[l];
        if (pnxt === p) {
          continue;
        }
        conn(p, pnxt);
        _px = (p.x - pnxt.x) / _dist(pnxt, p);
        _py = (p.y - pnxt.y) / _dist(pnxt, p);
        p.velX -= _px * pull;
        p.velY -= _py * pull;
      }
    }
  }
  upd();
}

function addP(px, py) {
  let p = Node(c, px, py);
  dst.add(p);
}

function conn(p1, p2) {
  $.strokeStyle = 'hsla(0,0%,15%,1)';
  let dist = _dist(p1, p2);
  $.globalAlpha = 1 - dist / 100;
  $.beginPath();
  $.moveTo(p1.x, p1.y);
  $.lineTo(p2.x, p2.y);
  $.stroke();
}

function _dist(p1, p2) {
  let _px = 0;
  let _py = 0;
  _px = p2.x - p1.x;
  _px = _px * _px;
  _py = p2.y - p1.y;
  _py = _py * _py;
  return Math.sqrt(_px + _py);
}

function upd() {
  for (let i = 0; i < dst.parr.length; i++) {
    dst.parr[i].upos();
  }
}

function pRem(p) {
  let i = dst.rem(p)
  darr.push(i[0]);
}

let frict = .9;

function Node(c, px, py) {
  let _p = {};
     _p.res_ = function(px, py) {
     _p.mass = rnd(1, 10);
     _p.gx = rnd(-5, 5);
     _p.gy = rnd(-5, 5);
     _p.x = px || rnd(10, c.width - 10);
     _p.y = py || rnd(10, c.height - 10);
     _p.gx2 = rnd(-2, 2) * .5;
     _p.gy2 = rnd(-2, 2) * .5;

 let vel = 25;
     _p.velX = rnd(-vel, vel);
     _p.velY = rnd(-vel, vel);
}
  _p.upos = function() {
    if (Math.abs(_p.velX) < 1 && Math.abs(_p.velY) < 1) pRem(_p);
    if (rnd(0, 100) > 98) {
      let np = nPart();
      if (np) {
        np.res_(_p.x, _p.y);
        np.velX += rnd(-5, 5);
        np.velY += rnd(-5, 5);
      }
    }
    _p.velX *= frict;
    _p.velY *= frict;

    if (_p.x + _p.velX > c.width) _p.velX *= -1;
    else if (_p.x + _p.velX < 0)  _p.velX *= -1;
    if (_p.y + _p.velY > c.height) _p.velY *= -1;
    else if (_p.y + _p.velY < 0) _p.velY *= -1;

    conn(_p, {
      x: _p.x + _p.velX,
      y: _p.y + _p.velY
    })
    _p.x += _p.velX;
    _p.y += _p.velY;
  }
  _p.res_(px, py);
  return _p;
}

function Dist(gsz) {
  let ret = {};
      ret.gsz = gsz;
      ret.parr = [];
      ret.pos = [];

  ret.next = function(a) {
    let x = Math.ceil(a.x / gsz);
    let y = Math.ceil(a.y / gsz);
    let p = ret.pos;
    let r = p[x][y];

    try {
      if (p[x - 1][y - 1]) {
        r = r.concat(p[x - 1][y - 1]);
      }
    } catch (e) {}
    try {
      if (p[x][y - 1]) {
        r = r.concat(p[x][y - 1]);
      }
    } catch (e) {}
    try {
      if (p[x + 1][y - 1]) {
        r = r.concat(p[x + 1][y - 1]);
      }
    } catch (e) {}
    try {
      if (p[x - 1][y]) {
        r = r.concat(p[x - 1][y]);
      }
    } catch (e) {}
    try {
      if (p[x + 1][y]) {
        r = r.concat(p[x + 1][y]);
      }
    } catch (e) {}
    try {
      if (p[x - 1][y + 1]) {
        r = r.concat(p[x - 1][y + 1]);
      }
    } catch (e) {}
    try {
      if (p[x][y + 1]) {
        r = r.concat(p[x][y + 1]);
      }
    } catch (e) {}
    try {
      if (p[x + 1][y + 1]) {
        r = r.concat(p[x + 1][y + 1]);
      }
    } catch (e) {}
    return r;
  }

  ret.ref = function() {
    ret.pos = [];
    let i = ret.parr.length;
    while (i--) {
      let a = ret.parr[i];
      let x = Math.ceil(a.x / gsz);
      let y = Math.ceil(a.y / gsz);
      if (!ret.pos[x]) ret.pos[x] = [];
      if (!ret.pos[x][y]) ret.pos[x][y] = [a];
      continue;
      ret.pos[x][y].push(a);
    }
  }
  ret.add = function(a) {
    ret.parr.push(a);
  }

  ret.rem = function(a) {
    let i = ret.parr.length;
    while (i--) {
      if (ret.parr[i] === a) return ret.parr.splice(i, 1);
    }
  }
  return ret;
}

function rnd(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

window.addEventListener('mousemove', function(e) {
  let np = nPart();
  if (np) np.res_(e.clientX, e.clientY);
}, false);

window.addEventListener('touchmove', function(e) {
  e.preventDefault();
  let np = nPart();
  if (np)  np.res_(e.touches[0].clientX, e.touches[0].clientY);
}, false);

function run() {
  window.requestAnimationFrame(run);
  draw();
}
run();

window.addEventListener('resize',function(){
  c.width = window.innerWidth;
  c.height = window.innerHeight;
}, false);