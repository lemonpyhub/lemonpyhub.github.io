// ============================================
// LEMONPYHUB - MASTER SCRIPT.JS
// Consolidated & Error-Free Version
// ============================================

// ===== 1. GLOBAL VARIABLES =====
let matrixAnimationId = null;
let isMatrixRunning = false;

// ===== 2. MATRIX RAIN EFFECT (Single Master Function) =====
function initMatrixRain() {

  // Stop existing animation if running
  if (matrixAnimationId) {
    cancelAnimationFrame(matrixAnimationId);
    matrixAnimationId = null;
  }

  try {
    const canvas = document.getElementById('matrixCanvas');
    if (!canvas) {
      console.warn('Matrix canvas not found');
      return;
    }
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.warn('Canvas context not supported');
      return;
    }

    // Set canvas to full window size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$#@%&*';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function drawMatrix() {
      // Semi-transparent black to create trail effect
      ctx.fillStyle = 'rgba(13, 17, 23, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = '#00ffcc';
      ctx.font = `${fontSize}px 'Fira Code', monospace`;
      
      for (let i = 0; i < drops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length));
        const x = i * fontSize;
        const y = drops[i] * fontSize;
        
        ctx.fillText(text, x, y);
        
        // Reset drop to top when it reaches bottom with random condition
        if (y > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }

    // Optimized animation using requestAnimationFrame
    function animateMatrix() {
      drawMatrix();
      matrixAnimationId = requestAnimationFrame(animateMatrix);
    }

    // Start optimized animation
    animateMatrix();
    isMatrixRunning = true;

    // Handle window resize
    function handleResize() {
      const resizeCanvas = document.getElementById('matrixCanvas');
      if (resizeCanvas) {
        resizeCanvas.width = window.innerWidth;
        resizeCanvas.height = window.innerHeight;
      }
    }
    
    window.removeEventListener('resize', handleResize);
    window.addEventListener('resize', handleResize);

    // Pause animation when tab is not visible for performance
    function handleVisibilityChange() {
      if (document.hidden) {
        if (matrixAnimationId) {
          cancelAnimationFrame(matrixAnimationId);
          matrixAnimationId = null;
        }
      } else if (!matrixAnimationId && isMatrixRunning) {
        // Restart animation
        const restartCanvas = document.getElementById('matrixCanvas');
        if (restartCanvas && restartCanvas.getContext) {
          animateMatrix();
        }
      }
    }
    
    document.removeEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('visibilitychange', handleVisibilityChange);

  } catch (error) {
    console.warn('Matrix animation initialization failed:', error);
  }
}

// ===== 3. SIMPLE MATRIX RAIN (Fallback for older pages using setInterval) =====
function initSimpleMatrixRain() {
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
  
  if (window.matrixInterval) clearInterval(window.matrixInterval);
  window.matrixInterval = setInterval(drawMatrix, 50);
  
  window.addEventListener('resize', function() {
    if (canvas) {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
  });
}

// ===== 4. SHARE FUNCTIONS (Single Source of Truth) =====
function getCurrentURL() { 
  return encodeURIComponent(window.location.href); 
}

function getPageTitle() { 
  return encodeURIComponent(document.title); 
}

function shareOnFacebook() { 
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${getCurrentURL()}`, '_blank', 'width=600,height=400'); 
}

function shareOnTikTok() { 
  // Try native share first, fallback to copy link
  if (navigator.share) {
    navigator.share({
      title: document.title,
      text: 'Check out LemonPyHub — free Python tools for Windows!',
      url: window.location.href
    }).catch(() => {
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied! Now paste it on TikTok 🎵');
    });
  } else {
    navigator.clipboard.writeText(window.location.href);
    alert('Link copied! Now paste it on TikTok 🎵');
  }
}

function shareOnInstagram() { 
  if (navigator.share) {
    navigator.share({
      title: document.title,
      text: 'Check out LemonPyHub — free Python tools for Windows!',
      url: window.location.href
    }).catch(() => {
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied! Now paste it on Instagram 📸');
    });
  } else {
    navigator.clipboard.writeText(window.location.href);
    alert('Link copied! Now paste it on Instagram 📸');
  }
}

function shareOnWhatsApp() { 
  window.open(`https://api.whatsapp.com/send?text=${getPageTitle()} - ${getCurrentURL()}`, '_blank'); 
}

function shareOnTelegram() { 
  window.open(`https://t.me/share/url?url=${getCurrentURL()}&text=${getPageTitle()}`, '_blank'); 
}

function shareOnReddit() { 
  window.open(`https://reddit.com/submit?url=${getCurrentURL()}&title=${getPageTitle()}`, '_blank'); 
}

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

// ===== 5. BLOG PAGE SPECIFIC =====
function initBlogFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  if (filterBtns.length === 0) return;
  
  filterBtns.forEach(button => {
    button.addEventListener('click', function() {
      filterBtns.forEach(btn => btn.classList.remove('active'));
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
}

// ===== 6. DOWNLOAD PAGE SPECIFIC =====
function initDownloadPage() {
  const searchInput = document.getElementById('searchInput');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.app-card');
  
  if (cards.length === 0) return;
  
  function filterApps() {
    const activeFilter = document.querySelector('.filter-btn.active')?.dataset.filter || 'all';
    const searchTerm = searchInput?.value.toLowerCase() || '';
    cards.forEach(card => {
      const cats = card.dataset.category;
      const matchesFilter = activeFilter === 'all' || (cats && cats.includes(activeFilter));
      const title = card.querySelector('.app-title')?.textContent.toLowerCase() || '';
      const desc = card.querySelector('.app-description')?.textContent.toLowerCase() || '';
      const matchesSearch = title.includes(searchTerm) || desc.includes(searchTerm);
      card.style.display = (matchesFilter && matchesSearch) ? 'flex' : 'none';
    });
  }
  
  if (filterBtns.length > 0) {
    filterBtns.forEach(btn => btn.addEventListener('click', ()=>{
      filterBtns.forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      filterApps();
    }));
  }
  
  if (searchInput) {
    searchInput.addEventListener('input', filterApps);
  }
  
  // Image modal
  if (!document.getElementById('imgModal')) {
    const newModal = document.createElement('div');
    newModal.id = 'imgModal';
    newModal.className = 'modal';
    newModal.innerHTML = '<span class="modal-close">&times;</span><img class="modal-content" id="modalImage" src="#" alt="Enlarged">';
    document.body.appendChild(newModal);
  }
  
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
  
  const closeModal = document.querySelector('.modal-close');
  if (closeModal) {
    closeModal.addEventListener('click', ()=>{
      const modalElem = document.getElementById('imgModal');
      if (modalElem) modalElem.style.display = 'none';
    });
  }
  
  // Details buttons
  document.querySelectorAll('.details-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const appId = this.getAttribute('data-app');
      const modal = document.getElementById(appId + '-modal');
      if (modal) {
        modal.style.display = 'block';
        modal.scrollTop = 0;
      }
    });
  });
  
  // Close modals
  document.querySelectorAll('.close-detail').forEach(btn => {
    btn.addEventListener('click', function() {
      const modal = this.closest('.app-detail-modal');
      if (modal) modal.style.display = 'none';
    });
  });
  
  // Click outside to close
  window.addEventListener('click', function(e) {
    document.querySelectorAll('.app-detail-modal').forEach(modal => {
      if (e.target === modal) modal.style.display = 'none';
    });
    const imgModalElem = document.getElementById('imgModal');
    if (e.target === imgModalElem && imgModalElem) imgModalElem.style.display = 'none';
  });
  
  // Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.app-detail-modal, .modal').forEach(m => {
        if (m) m.style.display = 'none';
      });
    }
  });
}

// Copy hash function
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
  
  if (link.getAttribute('data-tracked') === 'true') return;
  link.setAttribute('data-tracked', 'true');
  
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
  
  if (link.target !== '_blank') {
    event.preventDefault();
    setTimeout(() => {
      window.location.href = link.href;
    }, 200);
  }
  
  console.log('✅ Tracked:', appName, fileName);
}, true);

// ===== 7. DYNAMIC FONT LOADER =====
function loadDynamicFonts() {
  // Load Font Awesome if not already loaded
  if (!document.querySelector('link[href*="font-awesome"]')) {
    var fa = document.createElement('link');
    fa.rel = 'stylesheet';
    fa.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
    document.head.appendChild(fa);
  }

  // Load Google Fonts if not already loaded
  if (!document.querySelector('link[href*="fonts.googleapis.com/css2"]')) {
    var gf = document.createElement('link');
    gf.rel = 'stylesheet';
    gf.href = 'https://fonts.googleapis.com/css2?family=Fira+Code&family=Lato:wght@700&display=swap';
    document.head.appendChild(gf);
  }
}

// ===== 8. PAGE INITIALIZATION (Detect which page is loaded) =====
document.addEventListener('DOMContentLoaded', function() {
  // Load fonts
  loadDynamicFonts();
  
  // Detect page type and initialize accordingly
  const path = window.location.pathname;
  
  // Check for download page (has apps-grid)
  if (document.querySelector('.apps-grid') || document.querySelector('.app-card')) {
    initDownloadPage();
    initSimpleMatrixRain(); // Use simple setInterval for download page
  }
  // Check for blog page (has blog-card)
  else if (document.querySelector('.blog-card')) {
    initBlogFilters();
    initMatrixRain(); // Use advanced requestAnimationFrame
  }
  // Check for manual or helpfaq page
  else if (path.includes('/manual/') || path.includes('/helpfaq/')) {
    initMatrixRain();
  }
  // Default for other pages (root, donate)
  else {
    initMatrixRain();
  }
});

// Also initialize on load for pages that might have dynamic content
window.addEventListener('load', function() {
  // Re-initialize download page if needed (for modal images that load late)
  if (document.querySelector('.apps-grid')) {
    // Re-attach image modal handlers for any dynamically loaded images
    document.querySelectorAll('.tool-img').forEach(img => {
      if (!img.hasAttribute('data-modal-attached')) {
        img.setAttribute('data-modal-attached', 'true');
        img.onclick = function() {
          const modalElem = document.getElementById('imgModal');
          const modalImgElem = document.getElementById('modalImage');
          if (modalElem && modalImgElem) {
            modalElem.style.display = 'flex';
            modalImgElem.src = this.src;
          }
        };
      }
    });
  }
});
