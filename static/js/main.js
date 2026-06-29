// ===== NAVBAR SCROLL =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ===== HAMBURGER =====
const hamburger = document.getElementById('hamburger');
const navLinks  = document.querySelector('.nav-links');
hamburger.addEventListener('click', () => navLinks.classList.toggle('open'));
navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));

// ===== FADE IN ON SCROLL =====
const fadeObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });

document.querySelectorAll(
  '.skill-icon-card, .project-card, .timeline-item, .cert-card, .more-card, .contact-card, .section-header, .skill-category-block, .focus-card'
).forEach(el => {
  el.classList.add('fade-in');
  fadeObserver.observe(el);
});

// ===== ACTIVE NAV LINK =====
const sections   = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(sec => { if (window.scrollY >= sec.offsetTop - 120) current = sec.id; });
  navAnchors.forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${current}`));
});

// ===== CHATBOX =====
let chatOpen = false;

function toggleChat() {
  chatOpen = !chatOpen;
  const win = document.getElementById('chat-window');
  win.classList.toggle('chat-hidden', !chatOpen);
  if (chatOpen) setTimeout(() => win.classList.add('chat-visible'), 10);
  else win.classList.remove('chat-visible');
}

function showForm() {
  document.getElementById('chat-intro').style.display   = 'none';
  document.getElementById('chat-success').style.display = 'none';
  document.getElementById('chat-error').style.display   = 'none';
  document.getElementById('chat-form').style.display    = 'flex';
  document.getElementById('msg-name').focus();
}

function resetForm() {
  ['msg-name','msg-email','msg-subject','msg-body'].forEach(id => {
    document.getElementById(id).value = '';
  });
  document.getElementById('chat-form').style.display    = 'none';
  document.getElementById('chat-success').style.display = 'none';
  document.getElementById('chat-intro').style.display   = 'flex';
}

async function submitForm() {
  const name    = document.getElementById('msg-name').value.trim();
  const email   = document.getElementById('msg-email').value.trim();
  const subject = document.getElementById('msg-subject').value.trim();
  const body    = document.getElementById('msg-body').value.trim();
  const btn     = document.getElementById('send-btn');

  // Validate
  const inputs = ['msg-name','msg-email','msg-subject','msg-body'];
  let valid = true;
  inputs.forEach(id => {
    const el = document.getElementById(id);
    if (!el.value.trim()) {
      el.classList.add('input-error');
      valid = false;
    } else {
      el.classList.remove('input-error');
    }
  });
  if (!valid) { shakeBtn(btn); return; }

  // Email format check
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    document.getElementById('msg-email').classList.add('input-error');
    shakeBtn(btn);
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="sending-dots"><span></span><span></span><span></span></span> Sending...';

  try {
    await emailjs.send("service_nnitrqa", "template_xe12r3e", {
      from_name:  name,
      from_email: email,
      subject:    subject,
      message:    body,
      to_name:    'Bijon',
    });
    document.getElementById('chat-form').style.display    = 'none';
    document.getElementById('chat-success').style.display = 'flex';
  } catch (err) {
    console.error('EmailJS error:', err);
    document.getElementById('chat-form').style.display  = 'none';
    document.getElementById('chat-error').style.display = 'flex';
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Send Message</span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>';
  }
}

function shakeBtn(btn) {
  btn.classList.add('shake');
  setTimeout(() => btn.classList.remove('shake'), 500);
}

// Clear error state on input
document.addEventListener('DOMContentLoaded', () => {
  ['msg-name','msg-email','msg-subject','msg-body'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', () => el.classList.remove('input-error'));
  });
});
