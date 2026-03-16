/*
 * Spam Email Detector - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            if (alert.querySelector('.btn-close')) {
                // Only auto-hide if user hasn't clicked close
            } else {
                bsAlert.close();
            }
        });
    }, 5000);
    
    // Character count for textarea
    var emailTextarea = document.getElementById('email_text');
    if (emailTextarea) {
        emailTextarea.addEventListener('input', function() {
            var length = this.value.length;
            var charCount = document.getElementById('charCount');
            if (charCount) {
                charCount.textContent = length + ' characters';
            }
        });
    }
    
    // Form validation
    var predictForm = document.querySelector('form[action*="predict"]');
    if (predictForm) {
        predictForm.addEventListener('submit', function(e) {
            var emailText = document.getElementById('email_text').value.trim();
            
            if (emailText.length < 10) {
                e.preventDefault();
                alert('Please enter at least 10 characters for accurate analysis.');
                return false;
            }
            
            // Show loading state
            var submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="custom-spinner" style="width:20px;height:20px;border-width:2px;"></span> Analyzing...';
            }
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add loading animation to result page
    var resultSection = document.querySelector('.result-section');
    if (resultSection) {
        resultSection.classList.add('fade-in');
    }
    
    // Confidence bar animation
    var confidenceBar = document.querySelector('.confidence-bar');
    if (confidenceBar) {
        var targetWidth = confidenceBar.style.width;
        confidenceBar.style.width = '0%';
        
        setTimeout(function() {
            confidenceBar.style.transition = 'width 1s ease-out';
            confidenceBar.style.width = targetWidth;
        }, 100);
    }
    
    // Print result functionality
    var printBtn = document.getElementById('printResult');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Copy to clipboard functionality
    var copyBtn = document.getElementById('copyResult');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            var resultText = document.querySelector('.result-title').textContent;
            var confidenceText = document.querySelector('.text-center.fw-bold').textContent;
            var textToCopy = 'Spam Detection Result: ' + resultText + '\n' + confidenceText;
            
            navigator.clipboard.writeText(textToCopy).then(function() {
                alert('Result copied to clipboard!');
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        });
    }
});

// Function to validate email input
function validateEmailInput() {
    var emailText = document.getElementById('email_text').value.trim();
    
    if (emailText.length === 0) {
        alert('Please enter email content to analyze.');
        return false;
    }
    
    if (emailText.length < 10) {
        alert('Please enter at least 10 characters for accurate analysis.');
        return false;
    }
    
    return true;
}

// Function to reset form
function resetForm() {
    document.getElementById('email_text').value = '';
    var charCount = document.getElementById('charCount');
    if (charCount) {
        charCount.textContent = '0 characters';
    }
}

// Function to show loading spinner
function showLoading() {
    var loadingDiv = document.createElement('div');
    loadingDiv.className = 'spinner-container';
    loadingDiv.id = 'loadingSpinner';
    loadingDiv.innerHTML = '<div class="custom-spinner"></div>';
    
    var mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.innerHTML = '';
        mainContent.appendChild(loadingDiv);
    }
}
// Function to handle sample email buttons
function loadSample(type) {
    var samples = {
        spam: "CONGRATULATIONS! You've won $1,000,000 in our lottery! Click here immediately to claim your prize! Act now or lose this amazing offer! Your bank account details needed!",
        ham: "Hi John, I hope you're doing well. I wanted to follow up on our meeting scheduled for tomorrow at 3pm. Please let me know if that time still works for you. Thanks!"
    };
    
    var textarea = document.getElementById('email_text');
    if (textarea) {
        textarea.value = samples[type];
        
        // Trigger input event to update character count
        var event = new Event('input', {
            bubbles: true,
            cancelable: true
        });
        textarea.dispatchEvent(event);
    }
}

// Function to share result on social media
function shareResult(platform) {
    var result = document.querySelector('.result-title').textContent;
    var confidence = document.querySelector('.text-center.fw-bold').textContent;
    var text = 'Spam Detection Result: ' + result + ' - ' + confidence;
    
    var shareUrls = {
        twitter: 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text),
        facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(window.location.href),
        linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(window.location.href)
    };
    
    if (shareUrls[platform]) {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
    }
}

// Function to add animation on scroll
function animateOnScroll() {
    var elements = document.querySelectorAll('.feature-card, .stat-item, .tech-item');
    
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-up');
                entry.target.style.opacity = '1';
            }
        });
    }, {
        threshold: 0.1
    });
    
    elements.forEach(function(element) {
        element.style.opacity = '0';
        observer.observe(element);
    });
}

// Initialize scroll animations
if (window.IntersectionObserver) {
    animateOnScroll();
}

// Mobile menu toggle
var navbarToggler = document.querySelector('.navbar-toggler');
var navbarCollapse = document.querySelector('.navbar-collapse');

if (navbarToggler && navbarCollapse) {
    navbarToggler.addEventListener('click', function() {
        navbarCollapse.classList.toggle('show');
    });
    
    // Close mobile menu when clicking a link
    var navLinks = navbarCollapse.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            navbarCollapse.classList.remove('show');
        });
    });
}

// Lazy load images
function lazyLoadImages() {
    var images = document.querySelectorAll('img[data-src]');
    
    var imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(function(img) {
        imageObserver.observe(img);
    });
}

// Initialize lazy loading
if ('IntersectionObserver' in window) {
    lazyLoadImages();
}

// Add to home screen prompt (for mobile)
var deferredPrompt;
var installBtn = document.getElementById('installBtn');

if (deferredPrompt) {
    installBtn.style.display = 'block';
    
    installBtn.addEventListener('click', function() {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function(choiceResult) {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the A2HS prompt');
            }
            deferredPrompt = null;
            installBtn.style.display = 'none';
        });
    });
}

// Service worker registration (for PWA support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('ServiceWorker registration successful');
        }, function(err) {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}

// Console log for debugging
console.log('Spam Email Detector loaded successfully!');