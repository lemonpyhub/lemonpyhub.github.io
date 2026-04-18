// Matrix Digital Rain Effect
const canvas = document.getElementById('matrixCanvas');
if (canvas) {
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; 
  canvas.height = window.innerHeight;
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$#@%&*';
  const fontSize = 14; 
  const columns = canvas.width / fontSize; 
  const drops = Array(Math.floor(columns)).fill(1);
  
  function drawMatrix() {
    ctx.fillStyle = 'rgba(13, 17, 23, 0.1)'; 
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#00ffcc'; 
    ctx.font = `${fontSize}px 'Fira Code', monospace`;
    for (let i = 0; i < drops.length; i++) {
      const text = characters.charAt(Math.floor(Math.random() * characters.length));
      const x = i * fontSize; 
      const y = drops[i] * fontSize;
      ctx.fillText(text, x, y);
      if (y > canvas.height && Math.random() > 0.975) { 
        drops[i] = 0; 
      }
      drops[i]++;
    }
  }
  setInterval(drawMatrix, 50);
}

// Share functions
function getCurrentURL() { return encodeURIComponent(window.location.href); }
function getPageTitle() { return encodeURIComponent(document.title); }
function shareOnFacebook() { window.open(`https://www.facebook.com/sharer/sharer.php?u=${getCurrentURL()}`,'_blank','width=600,height=400'); }
function shareOnTikTok() { window.open('https://www.tiktok.com/upload?lang=en','_blank'); }
function shareOnInstagram() { window.open('https://www.instagram.com/','_blank'); }
function shareOnWhatsApp() { window.open(`https://api.whatsapp.com/send?text=${getPageTitle()} - ${getCurrentURL()}`,'_blank'); }
function shareOnTelegram() { window.open(`https://t.me/share/url?url=${getCurrentURL()}&text=${getPageTitle()}`,'_blank'); }
function shareOnReddit() { window.open(`https://reddit.com/submit?url=${getCurrentURL()}&title=${getPageTitle()}`,'_blank'); }
function nativeShare() { 
  if (navigator.share) { 
    navigator.share({ 
      title: document.title, 
      text: 'Check out LemonPyHub — free Python tools for Windows!', 
      url: window.location.href 
    }); 
  } else { 
    alert('Web Share not supported in your browser. Please use the specific share buttons above.'); 
  } 
}

// Handle window resize
window.addEventListener('resize', function() {
  if (canvas) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
});

// ===== BLOG PAGE SPECIFIC JAVASCRIPT =====

// Category Filter Functionality
document.querySelectorAll('.filter-btn').forEach(button => {
  button.addEventListener('click', function() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.classList.remove('active');
    });
    this.classList.add('active');
    
    const filter = this.getAttribute('data-filter');
    const articles = document.querySelectorAll('.blog-card');
    
    articles.forEach(article => {
      const categories = article.getAttribute('data-category');
      if (filter === 'all' || (categories && categories.includes(filter))) {
        article.style.display = 'flex';
      } else {
        article.style.display = 'none';
      }
    });
  });
});

// ===== DONATE PAGE SPECIFIC JAVASCRIPT =====
// Tambahkan kod ini ke dalam js/script.js yang sedia ada

// Matrix Rain Effect for Donate Page
let animationId;

function initMatrix() {
  // Skip matrix on mobile untuk performance
  if (window.innerWidth < 768) {
    return;
  }

  try {
    const canvas = document.getElementById('matrixCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$#@%&*';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function drawMatrix() {
      ctx.fillStyle = 'rgba(13, 17, 23, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = '#00ffcc';
      ctx.font = `${fontSize}px 'Fira Code', monospace`;
      
      for (let i = 0; i < drops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length));
        const x = i * fontSize;
        const y = drops[i] * fontSize;
        
        ctx.fillText(text, x, y);
        
        if (y > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }

    function animateMatrix() {
      drawMatrix();
      animationId = requestAnimationFrame(animateMatrix);
    }

    setTimeout(animateMatrix, 1000);

    window.addEventListener('resize', function() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });

    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        cancelAnimationFrame(animationId);
      } else {
        animateMatrix();
      }
    });

  } catch (error) {
    console.warn('Matrix animation initialization failed:', error);
  }
}

// Share functions for Donate Page (overriding or adding TikTok/Instagram copy behavior)
function shareOnTikTok() { 
  navigator.clipboard.writeText(window.location.href);
  alert('Link copied! Now paste it on TikTok 🎵');
}

function shareOnInstagram() { 
  navigator.clipboard.writeText(window.location.href);
  alert('Link copied! Now paste it on Instagram 📸');
}

// Initialize donate page specific features
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(() => {
    initMatrix();
  }, 100);
});

// ===== DOWNLOAD PAGE SPECIFIC JAVASCRIPT =====
// Add this code to your existing js/script.js file

// Filter & Search functionality for download page
const searchInputDownload = document.getElementById('searchInput');
const filterBtnsDownload = document.querySelectorAll('.filter-btn');
const cardsDownload = document.querySelectorAll('.app-card');

function filterAppsDownload() {
  const activeFilter = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
  const searchTerm = searchInputDownload?.value.toLowerCase() || '';
  cardsDownload.forEach(card => {
    const cats = card.dataset.category;
    const matchesFilter = activeFilter === 'all' || (cats && cats.includes(activeFilter));
    const title = card.querySelector('.app-title')?.textContent.toLowerCase() || '';
    const desc = card.querySelector('.app-description')?.textContent.toLowerCase() || '';
    const matchesSearch = title.includes(searchTerm) || desc.includes(searchTerm);
    card.style.display = (matchesFilter && matchesSearch) ? 'flex' : 'none';
  });
}

if (filterBtnsDownload.length > 0) {
  filterBtnsDownload.forEach(btn => btn.addEventListener('click', ()=>{
    filterBtnsDownload.forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    filterAppsDownload();
  }));
}

if (searchInputDownload) {
  searchInputDownload.addEventListener('input', filterAppsDownload);
}

// Image modal for download page (click to enlarge)
const imgModal = document.getElementById("imgModal");
if (!imgModal) {
  const newModal = document.createElement('div');
  newModal.id = 'imgModal';
  newModal.className = 'modal';
  newModal.innerHTML = '<span class="modal-close">&times;</span><img class="modal-content" id="modalImage" src="#" alt="Enlarged">';
  document.body.appendChild(newModal);
}

const modalImgDownload = document.getElementById("modalImage");
document.querySelectorAll('.tool-img').forEach(img => {
  img.onclick = function() {
    const modalElem = document.getElementById('imgModal');
    const modalImgElem = document.getElementById('modalImage');
    if (modalElem && modalImgElem) {
      modalElem.style.display = 'flex';
      modalImgElem.src = this.src;
    }
  };
});

document.querySelector('.modal-close')?.addEventListener('click', ()=>{
  const modalElem = document.getElementById('imgModal');
  if (modalElem) modalElem.style.display = 'none';
});

window.onclick = e => {
  const modalElem = document.getElementById('imgModal');
  if (e.target === modalElem && modalElem) modalElem.style.display = 'none';
};

// Details buttons for download page
document.querySelectorAll('.details-btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    const appId = this.getAttribute('data-app');
    const modal = document.getElementById(appId + '-modal');
    if (modal) {
      modal.style.display = 'block';
      modal.scrollTop = 0;
    } else {
      console.warn('Modal not found:', appId + '-modal');
    }
  });
});

// Close buttons for modals
document.querySelectorAll('.close-detail').forEach(btn => {
  btn.addEventListener('click', function() {
    const modal = this.closest('.app-detail-modal');
    if (modal) modal.style.display = 'none';
  });
});

// Click outside modal to close
window.addEventListener('click', function(e) {
  document.querySelectorAll('.app-detail-modal').forEach(modal => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
});

// Escape key to close modals
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.app-detail-modal, .modal').forEach(m => {
      if (m) m.style.display = 'none';
    });
  }
});

// Copy hash function for download page
window.copyHash = function(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const text = el.innerText || el.textContent;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => alert('SHA256 copied!'));
  } else {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    alert('SHA256 copied!');
  }
};

// Download tracking for GA4
document.addEventListener('click', function(event) {
  const link = event.target.closest('a[download]');
  if (!link) return;
  
  // Check - don't track twice
  if (link.getAttribute('data-tracked') === 'true') return;
  link.setAttribute('data-tracked', 'true');
  
  // Get APP NAME
  let appName = 'Unknown';
  const modal = link.closest('.app-detail-modal');
  if (modal && modal.getAttribute('data-shortname')) {
    appName = modal.getAttribute('data-shortname');
  } else {
    const card = link.closest('.app-card');
    if (card && card.getAttribute('data-shortname')) {
      appName = card.getAttribute('data-shortname');
    }
  }
  
  const fileName = link.href.split('/').pop();
  
  if (typeof gtag === 'function') {
    gtag('event', 'download_completed', {
      'app_name': appName,
      'file_name': fileName,
      'send_to': 'G-Q9HFE57YHB'
    });
  }
  
  // Ensure tracking succeeds before redirect
  if (link.target !== '_blank') {
    event.preventDefault();
    setTimeout(() => {
      window.location.href = link.href;
    }, 200);
  }
  
  console.log('✅ Tracked:', appName, fileName);
}, true);