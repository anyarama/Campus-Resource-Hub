// =============================================================================
// IMAGE CAROUSEL - Resource Detail Page Image Gallery
// =============================================================================
// AI Contribution: Cline created this module on 2025-11-09
// Features: Keyboard navigation, touch gestures, thumbnail nav, fullscreen, accessibility
// =============================================================================

class ImageCarousel {
  constructor(container) {
    this.container = container;
    this.slides = container.querySelectorAll('.carousel__slide');
    this.thumbnails = container.querySelectorAll('.carousel__thumb');
    this.prevBtn = container.querySelector('[data-carousel-prev]');
    this.nextBtn = container.querySelector('[data-carousel-next]');
    this.counter = container.querySelector('[data-carousel-counter]');
    this.fullscreenBtn = container.querySelector('[data-carousel-fullscreen]');
    
    this.currentIndex = 0;
    this.isAnimating = false;
    this.touchStartX = 0;
    this.touchEndX = 0;
    this.isFullscreen = false;
    
    if (this.slides.length > 0) {
      this.init();
    }
  }

  init() {
    // Set initial state
    this.showSlide(0);
    this.updateCounter();
    this.updateButtons();
    
    // Setup event listeners
    this.setupNavigation();
    this.setupThumbnails();
    this.setupKeyboard();
    this.setupTouch();
    this.setupFullscreen();
    
    // Lazy load images
    this.lazyLoadImages();
  }

  // ========================================================================
  // Navigation Controls
  // ========================================================================
  
  setupNavigation() {
    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => this.prev());
    }
    
    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => this.next());
    }
  }

  next() {
    if (this.isAnimating || this.slides.length <= 1) return;
    
    const nextIndex = (this.currentIndex + 1) % this.slides.length;
    this.goToSlide(nextIndex);
  }

  prev() {
    if (this.isAnimating || this.slides.length <= 1) return;
    
    const prevIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
    this.goToSlide(prevIndex);
  }

  goToSlide(index) {
    if (index === this.currentIndex || this.isAnimating) return;
    
    this.isAnimating = true;
    
    // Hide current slide
    this.slides[this.currentIndex].classList.remove('is-active');
    this.slides[this.currentIndex].setAttribute('aria-hidden', 'true');
    
    // Show new slide
    this.currentIndex = index;
    this.slides[this.currentIndex].classList.add('is-active');
    this.slides[this.currentIndex].setAttribute('aria-hidden', 'false');
    
    // Update UI
    this.updateThumbnails();
    this.updateCounter();
    this.updateButtons();
    
    // Lazy load next/prev images
    this.lazyLoadAdjacentImages();
    
    // Reset animation flag
    setTimeout(() => {
      this.isAnimating = false;
    }, 300);
  }

  showSlide(index) {
    this.slides.forEach((slide, i) => {
      if (i === index) {
        slide.classList.add('is-active');
        slide.setAttribute('aria-hidden', 'false');
      } else {
        slide.classList.remove('is-active');
        slide.setAttribute('aria-hidden', 'true');
      }
    });
    
    this.currentIndex = index;
    this.updateThumbnails();
    this.updateCounter();
  }

  // ========================================================================
  // Thumbnails
  // ========================================================================
  
  setupThumbnails() {
    this.thumbnails.forEach((thumb, index) => {
      thumb.addEventListener('click', () => {
        this.goToSlide(index);
      });
      
      // Keyboard support for thumbnails
      thumb.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this.goToSlide(index);
        }
      });
      
      // Set initial ARIA
      thumb.setAttribute('role', 'button');
      thumb.setAttribute('tabindex', '0');
      thumb.setAttribute('aria-label', `View image ${index + 1}`);
    });
  }

  updateThumbnails() {
    this.thumbnails.forEach((thumb, index) => {
      if (index === this.currentIndex) {
        thumb.classList.add('is-active');
        thumb.setAttribute('aria-current', 'true');
      } else {
        thumb.classList.remove('is-active');
        thumb.removeAttribute('aria-current');
      }
    });
  }

  // ========================================================================
  // Keyboard Navigation
  // ========================================================================
  
  setupKeyboard() {
    document.addEventListener('keydown', (e) => {
      // Only handle keyboard if carousel is visible and focused
      if (!this.container.contains(document.activeElement)) return;
      
      switch(e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          this.prev();
          break;
        case 'ArrowRight':
          e.preventDefault();
          this.next();
          break;
        case 'Home':
          e.preventDefault();
          this.goToSlide(0);
          break;
        case 'End':
          e.preventDefault();
          this.goToSlide(this.slides.length - 1);
          break;
        case 'Escape':
          if (this.isFullscreen) {
            e.preventDefault();
            this.exitFullscreen();
          }
          break;
      }
    });
  }

  // ========================================================================
  // Touch Gestures (Mobile)
  // ========================================================================
  
  setupTouch() {
    const track = this.container.querySelector('.carousel__track');
    if (!track) return;
    
    track.addEventListener('touchstart', (e) => {
      this.touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    track.addEventListener('touchend', (e) => {
      this.touchEndX = e.changedTouches[0].screenX;
      this.handleSwipe();
    }, { passive: true });
  }

  handleSwipe() {
    const swipeThreshold = 50;
    const diff = this.touchStartX - this.touchEndX;
    
    if (Math.abs(diff) > swipeThreshold) {
      if (diff > 0) {
        // Swipe left - next
        this.next();
      } else {
        // Swipe right - prev
        this.prev();
      }
    }
  }

  // ========================================================================
  // Counter & Button Updates
  // ========================================================================
  
  updateCounter() {
    if (this.counter) {
      this.counter.textContent = `${this.currentIndex + 1} / ${this.slides.length}`;
    }
  }

  updateButtons() {
    if (this.slides.length <= 1) {
      // Hide nav buttons if only one slide
      if (this.prevBtn) this.prevBtn.style.display = 'none';
      if (this.nextBtn) this.nextBtn.style.display = 'none';
    } else {
      if (this.prevBtn) this.prevBtn.style.display = '';
      if (this.nextBtn) this.nextBtn.style.display = '';
    }
  }

  // ========================================================================
  // Lazy Loading Images
  // ========================================================================
  
  lazyLoadImages() {
    // Load first image immediately
    if (this.slides[0]) {
      this.loadSlideImage(0);
    }
    
    // Load adjacent images
    this.lazyLoadAdjacentImages();
  }

  lazyLoadAdjacentImages() {
    // Load next and previous images
    const nextIndex = (this.currentIndex + 1) % this.slides.length;
    const prevIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
    
    this.loadSlideImage(nextIndex);
    this.loadSlideImage(prevIndex);
  }

  loadSlideImage(index) {
    const slide = this.slides[index];
    if (!slide) return;
    
    const img = slide.querySelector('img[data-src]');
    if (img) {
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      img.addEventListener('load', () => {
        img.classList.add('is-loaded');
      });
    }
  }

  // ========================================================================
  // Fullscreen Mode
  // ========================================================================
  
  setupFullscreen() {
    if (!this.fullscreenBtn) return;
    
    this.fullscreenBtn.addEventListener('click', () => {
      if (this.isFullscreen) {
        this.exitFullscreen();
      } else {
        this.enterFullscreen();
      }
    });
    
    // Listen for fullscreen change events
    document.addEventListener('fullscreenchange', () => {
      if (!document.fullscreenElement) {
        this.isFullscreen = false;
        this.container.classList.remove('is-fullscreen');
      }
    });
  }

  enterFullscreen() {
    if (this.container.requestFullscreen) {
      this.container.requestFullscreen();
      this.isFullscreen = true;
      this.container.classList.add('is-fullscreen');
    } else if (this.container.webkitRequestFullscreen) {
      this.container.webkitRequestFullscreen();
      this.isFullscreen = true;
      this.container.classList.add('is-fullscreen');
    }
  }

  exitFullscreen() {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
    this.isFullscreen = false;
    this.container.classList.remove('is-fullscreen');
  }

  // ========================================================================
  // Public API
  // ========================================================================
  
  destroy() {
    // Clean up event listeners if needed
    this.prevBtn?.removeEventListener('click', this.prev);
    this.nextBtn?.removeEventListener('click', this.next);
  }
}

// =============================================================================
// Auto-Initialize Carousels
// =============================================================================

function initCarousels() {
  const carousels = document.querySelectorAll('[data-carousel]');
  const instances = [];
  
  carousels.forEach(carousel => {
    instances.push(new ImageCarousel(carousel));
  });
  
  return instances;
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCarousels);
} else {
  initCarousels();
}

// Export for module usage
export { ImageCarousel, initCarousels };
export default ImageCarousel;
