/* ============================================================
   AzUAC Campus Events — Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Custom Cursor ─────────────────────────────────────── */
  const cursor   = document.querySelector('.cursor');
  const follower = document.querySelector('.cursor-follower');

  let mx = -100, my = -100;
  let fx = -100, fy = -100;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    if (cursor) { cursor.style.left = mx + 'px'; cursor.style.top = my + 'px'; }
  });

  // Smooth follower
  function animateFollower() {
    fx += (mx - fx) * .15;
    fy += (my - fy) * .15;
    if (follower) { follower.style.left = fx + 'px'; follower.style.top = fy + 'px'; }
    requestAnimationFrame(animateFollower);
  }
  animateFollower();

  // Cursor grow on interactive elements
  document.querySelectorAll('a, button, [data-hover]').forEach(el => {
    el.addEventListener('mouseenter', () => {
      if (cursor)   cursor.style.transform   = 'translate(-50%,-50%) scale(2.2)';
      if (follower) { follower.style.width = '60px'; follower.style.height = '60px'; follower.style.opacity = '.3'; }
    });
    el.addEventListener('mouseleave', () => {
      if (cursor)   cursor.style.transform   = 'translate(-50%,-50%) scale(1)';
      if (follower) { follower.style.width = '36px'; follower.style.height = '36px'; follower.style.opacity = '.6'; }
    });
  });

  document.addEventListener('mouseleave', () => { if (cursor) cursor.style.opacity = '0'; });
  document.addEventListener('mouseenter', () => { if (cursor) cursor.style.opacity = '1'; });


  /* ── Particle Canvas ────────────────────────────────────── */
  const canvas = document.getElementById('particle-canvas');
  if (canvas) {
    const ctx  = canvas.getContext('2d');
    let W, H, particles = [];

    function resize() {
      W = canvas.width  = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    class Particle {
      constructor() { this.reset(); }
      reset() {
        this.x    = Math.random() * W;
        this.y    = Math.random() * H;
        this.vx   = (Math.random() - .5) * .35;
        this.vy   = (Math.random() - .5) * .35;
        this.r    = Math.random() * 1.8 + .4;
        this.alpha = Math.random() * .5 + .1;
        this.color = Math.random() > .6
          ? `rgba(201,168,76,${this.alpha})`
          : `rgba(255,255,255,${this.alpha * .5})`;
      }
      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
      }
      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
      }
    }

    // Create particles + connections
    for (let i = 0; i < 120; i++) particles.push(new Particle());

    function drawLines() {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx*dx + dy*dy);
          if (dist < 110) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(201,168,76,${(1 - dist/110) * .12})`;
            ctx.lineWidth = .6;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
    }

    function animateParticles() {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(p => { p.update(); p.draw(); });
      drawLines();
      requestAnimationFrame(animateParticles);
    }
    animateParticles();
  }


  /* ── Navbar Scroll Behavior ─────────────────────────────── */
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    }, { passive: true });
  }


  /* ── Mobile Hamburger ───────────────────────────────────── */
  const hamburger = document.querySelector('.hamburger');
  const navLinks  = document.querySelector('.nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navLinks.classList.toggle('mobile-open');
    });
  }


  /* ── Scroll Reveal ──────────────────────────────────────── */
  const reveals = document.querySelectorAll('[data-reveal]');
  if (reveals.length) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .12 });
    reveals.forEach(el => observer.observe(el));
  }


  /* ── Animated Number Counter ────────────────────────────── */
  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const dur    = 1600;
    const start  = performance.now();

    function step(now) {
      const t   = Math.min((now - start) / dur, 1);
      const val = Math.round(easeOutExpo(t) * target);
      el.textContent = val.toLocaleString() + (el.dataset.suffix || '');
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function easeOutExpo(t) {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }

  const counters = document.querySelectorAll('[data-target]');
  if (counters.length) {
    const cObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          cObserver.unobserve(entry.target);
        }
      });
    }, { threshold: .5 });
    counters.forEach(c => cObserver.observe(c));
  }


  /* ── Tilt Cards (3D on hover) ───────────────────────────── */
  document.querySelectorAll('[data-tilt]').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width  - .5;
      const y = (e.clientY - rect.top)  / rect.height - .5;
      card.style.transform = `perspective(800px) rotateY(${x*12}deg) rotateX(${-y*12}deg) translateY(-6px)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });


  /* ── Magnetic Buttons ───────────────────────────────────── */
  document.querySelectorAll('[data-magnetic]').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const dx = e.clientX - rect.left - rect.width  / 2;
      const dy = e.clientY - rect.top  - rect.height / 2;
      btn.style.transform = `translate(${dx * .25}px, ${dy * .25}px)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
    });
  });


  /* ── Smooth Page Transitions ────────────────────────────── */
  const overlay = document.querySelector('.page-overlay');
  if (overlay) {
    // Animate in on load
    overlay.style.transform = 'scaleY(1)';
    requestAnimationFrame(() => {
      overlay.style.transition = 'transform .7s cubic-bezier(.76,0,.24,1)';
      overlay.style.transformOrigin = 'top';
      overlay.style.transform = 'scaleY(0)';
    });

    // Animate out on navigation
    document.querySelectorAll('a:not([href^="#"]):not([target="_blank"])').forEach(link => {
      link.addEventListener('click', e => {
        const href = link.getAttribute('href');
        if (!href || href.startsWith('http') || href.startsWith('mailto')) return;
        e.preventDefault();
        overlay.style.transformOrigin = 'bottom';
        overlay.style.transition = 'transform .55s cubic-bezier(.76,0,.24,1)';
        overlay.style.transform = 'scaleY(1)';
        setTimeout(() => { window.location.href = href; }, 580);
      });
    });
  }


  /* ── Parallax Hero Text on Scroll ───────────────────────── */
  const heroContent = document.querySelector('.hero-content');
  if (heroContent) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      heroContent.style.transform = `translateY(${y * .3}px)`;
      heroContent.style.opacity   = 1 - y / 600;
    }, { passive: true });
  }


  /* ── Typewriter Effect ──────────────────────────────────── */
  const typeEl = document.querySelector('[data-typewriter]');
  if (typeEl) {
    const words  = JSON.parse(typeEl.dataset.typewriter);
    let wi = 0, ci = 0, deleting = false;

    function type() {
      const word = words[wi];
      if (!deleting) {
        typeEl.textContent = word.slice(0, ++ci);
        if (ci === word.length) { deleting = true; setTimeout(type, 1800); return; }
      } else {
        typeEl.textContent = word.slice(0, --ci);
        if (ci === 0) { deleting = false; wi = (wi + 1) % words.length; }
      }
      setTimeout(type, deleting ? 60 : 110);
    }
    type();
  }


  /* ── Toast Notification ─────────────────────────────────── */
  window.showToast = function(msg, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${msg}</span>`;
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  };


  /* ── Form submit loader ─────────────────────────────────── */
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('[type="submit"]');
      if (btn) {
        btn.innerHTML = '<span class="spinner"></span> Please wait…';
        btn.disabled = true;
      }
    });
  });

});
