// ============================================
// LEMONPYHUB - MASTER SCRIPT.JS
// Consolidated & Error-Free Version
// ============================================

// ===== 1. GLOBAL VARIABLES =====
let matrixAnimationId = null;
let isMatrixRunning = false;

// ===== 2. MATRIX RAIN EFFECT (Optimized for Mobile & Desktop) =====
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

    // Responsive font size: 14px on desktop, 10px on mobile
    const isMobile = window.innerWidth <= 768;
    const fontSize = isMobile ? 10 : 14;
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$#@%&*';
    const columns = Math.floor(canvas.width / fontSize);
    const drops = Array(columns).fill(1);
    
    // Limit columns on mobile for better performance
    const maxColumns = isMobile ? 40 : 200;
    const actualColumns = Math.min(columns, maxColumns);

    function drawMatrix() {
      // Semi-transparent black to create trail effect - lighter on mobile for performance
      ctx.fillStyle = isMobile ? 'rgba(13, 17, 23, 0.15)' : 'rgba(13, 17, 23, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = '#00ffcc';
      ctx.font = `${fontSize}px 'Fira Code', monospace`;
      
      for (let i = 0; i < actualColumns; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length));
        const x = i * fontSize;
        const y = drops[i] * fontSize;
        
        // Only draw if within canvas bounds (performance)
        if (y < canvas.height + fontSize) {
          ctx.fillText(text, x, y);
        }
        
        // Reset drop to top when it reaches bottom
        if (y > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }

    // Optimized animation using requestAnimationFrame
    let lastTimestamp = 0;
    const frameInterval = isMobile ? 60 : 40; // Lower fps on mobile for battery
    
    function animateMatrix(currentTime) {
      if (!isMatrixRunning) return;
      
      // Throttle frame rate on mobile for better battery
      if (isMobile && currentTime - lastTimestamp < frameInterval) {
        matrixAnimationId = requestAnimationFrame(animateMatrix);
        return;
      }
      lastTimestamp = currentTime;
      
      drawMatrix();
      matrixAnimationId = requestAnimationFrame(animateMatrix);
    }

    // Start optimized animation
    isMatrixRunning = true;
    animateMatrix(0);

    // Handle window resize with debounce for mobile
    let resizeTimeout;
    function handleResize() {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        if (canvas) {
          canvas.width = window.innerWidth;
          canvas.height = window.innerHeight;
          
          // Recalculate columns on resize
          const newIsMobile = window.innerWidth <= 768;
          const newFontSize = newIsMobile ? 10 : 14;
          const newColumns = Math.min(Math.floor(canvas.width / newFontSize), newIsMobile ? 40 : 200);
          
          // Reset drops array with new size
          drops.length = newColumns;
          for (let i = 0; i < newColumns; i++) {
            drops[i] = drops[i] || 1;
          }
        }
      }, 150);
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
          isMatrixRunning = true;
          animateMatrix(0);
        }
      }
    }
    
    document.removeEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('visibilitychange', handleVisibilityChange);

  } catch (error) {
    console.warn('Matrix animation initialization failed:', error);
  }
}

// ===== 3. SIMPLE MATRIX RAIN (Optimized for Mobile & Desktop - Fallback) =====
function initSimpleMatrixRain() {
  const canvas = document.getElementById('matrixCanvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  
  canvas.width = window.innerWidth; 
  canvas.height = window.innerHeight;
  
  const isMobile = window.innerWidth <= 768;
  const fontSize = isMobile ? 10 : 14;
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$#@%&*';
  const columns = Math.min(Math.floor(canvas.width / fontSize), isMobile ? 40 : 200);
  const drops = Array(columns).fill(1);
  
  // Slower interval on mobile for battery saving
  const intervalTime = isMobile ? 80 : 50;
  
  function drawMatrix() {
    ctx.fillStyle = isMobile ? 'rgba(13, 17, 23, 0.15)' : 'rgba(13, 17, 23, 0.1)'; 
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#00ffcc'; 
    ctx.font = `${fontSize}px 'Fira Code', monospace`;
    
    for (let i = 0; i < columns; i++) {
      const text = characters.charAt(Math.floor(Math.random() * characters.length));
      const x = i * fontSize; 
      const y = drops[i] * fontSize;
      
      if (y < canvas.height + fontSize) {
        ctx.fillText(text, x, y);
      }
      
      if (y > canvas.height && Math.random() > 0.975) { 
        drops[i] = 0; 
      }
      drops[i]++;
    }
  }
  
  if (window.matrixInterval) clearInterval(window.matrixInterval);
  window.matrixInterval = setInterval(drawMatrix, intervalTime);
  
  let resizeTimeout;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      if (canvas) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
      }
    }, 150);
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
  
  // TAKRIFKAN fileName di sini - LUAR blok if
  const fileName = link.href.split('/').pop();
  
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

  // FALLBACK: teka dari nama file (guna fileName yang dah ditakrifkan)
  if (appName === 'Unknown') {
    if (fileName.includes('Maintenance')) appName = 'WMT';
    else if (fileName.includes('DNS')) appName = 'DNSM';
    else if (fileName.includes('Optimizer')) appName = 'WOPT';
    else if (fileName.includes('Dockers')) appName = 'DOCK';
    else if (fileName.includes('Debloater')) appName = 'WDP';
    else if (fileName.includes('Winget')) appName = 'WGET';
    else if (fileName.includes('Security')) appName = 'WSM';
    else if (fileName.includes('Math')) appName = 'MCPG';
  }
  
  if (typeof gtag === 'function') {
    gtag('event', 'download_completed', {
      'app_name': appName,
      'file_name': fileName,
      'send_to': 'G-Q9HFE57YHB'
    });
  }
  
  console.log('✅ Tracked:', appName, fileName);
  
  if (link.target !== '_blank') {
    event.preventDefault();
    setTimeout(() => {
      window.location.href = link.href;
    }, 200);
  }
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

// ============================================
// MANUAL PAGE SPECIFIC CODE
// ============================================

// Manual page initialization
function initManualPage() {
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === "#" || href === "") return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add keyboard shortcut tooltips
    const shortcuts = document.querySelectorAll('.shortcut-key');
    shortcuts.forEach(el => {
        if (!el.hasAttribute('title')) {
            el.setAttribute('title', 'Keyboard shortcut');
        }
    });
    
    console.log('Manual page initialized');
}

// ============================================
// BLOG PAGE SPECIFIC CODE
// ============================================

// Blog page image modal functionality
function initBlogPage() {
    // Add click handlers for all tool images to open modal
    const modal = document.getElementById('imgModal');
    if (!modal) {
        // Create modal if it doesn't exist
        const newModal = document.createElement('div');
        newModal.id = 'imgModal';
        newModal.className = 'modal';
        newModal.innerHTML = `
            <span class="modal-close">&times;</span>
            <img class="modal-content" id="modalImage" src="#" alt="Enlarged">
        `;
        document.body.appendChild(newModal);
        
        // Add close button handler
        const closeBtn = newModal.querySelector('.modal-close');
        closeBtn.addEventListener('click', function() {
            newModal.style.display = 'none';
        });
        
        // Click outside to close
        newModal.addEventListener('click', function(e) {
            if (e.target === newModal) {
                newModal.style.display = 'none';
            }
        });
    }
    
    // Add click handlers to all tool thumbnails
    document.querySelectorAll('.tool-thumbnail img').forEach(img => {
        img.addEventListener('click', function(e) {
            const modalElem = document.getElementById('imgModal');
            const modalImgElem = document.getElementById('modalImage');
            if (modalElem && modalImgElem) {
                modalElem.style.display = 'flex';
                modalImgElem.src = this.src;
            }
        });
    });
    
    // Escape key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modalElem = document.getElementById('imgModal');
            if (modalElem) modalElem.style.display = 'none';
        }
    });
    
    console.log('Blog page initialized');
}

// ===== 8. ANCHOR LINK HANDLER (Blink 3 times) =====
function handleAnchorLink() {
    if (window.location.hash) {
        setTimeout(function() {
            const targetId = window.location.hash.substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                // Scroll to element
                targetElement.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                
                // BLINK 3 TIMES effect
                let blinkCount = 0;
                const originalBorder = targetElement.style.border;
                const originalBoxShadow = targetElement.style.boxShadow;
                const originalTransition = targetElement.style.transition;
                
                targetElement.style.transition = 'all 0.15s ease';
                
                const blinkInterval = setInterval(function() {
                    if (blinkCount >= 14) { // 14 = 7 times blink (on/off)
                        clearInterval(blinkInterval);
                        // Restore original styles
                        targetElement.style.boxShadow = originalBoxShadow;
                        targetElement.style.border = originalBorder;
                        setTimeout(function() {
                            targetElement.style.transition = originalTransition;
                        }, 300);
                        console.log('✅ Blink completed for:', targetId);
                        return;
                    }
                    
                    if (blinkCount % 2 === 0) {
                        // ON - highlight
                        targetElement.style.boxShadow = '0 0 0 4px #00ffcc, 0 0 15px 2px #00ffcc';
                        targetElement.style.border = '1px solid #00ffcc';
                    } else {
                        // OFF - normal
                        targetElement.style.boxShadow = originalBoxShadow;
                        targetElement.style.border = originalBorder;
                    }
                    
                    blinkCount++;
                }, 400); // each blink 400ms
                
            } else {
                console.log('⚠️ Element not found:', targetId);
            }
        }, 500);
    }
}

// ===== 9. PAGE INITIALIZATION (Detect which page is loaded) =====
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
  // Check for blog page (has blog-card OR article-container)
  else if (document.querySelector('.blog-card') || document.querySelector('.article-container')) {
    initBlogFilters();      // For blog listing page
    initBlogPage();         // For single article page (image modal)
    initMatrixRain();       // Use advanced requestAnimationFrame
  }
  // Check for manual page
  else if (path.includes('/manual/')) {
    initManualPage();
    initMatrixRain();
  }
  // Check for helpfaq page
  else if (path.includes('/helpfaq/')) {
    initMatrixRain();
  }
  // Default for other pages (root, donate)
  else {
    initMatrixRain();
  }
  
  // Handle anchor links (scroll to element from URL hash)
  handleAnchorLink();
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
