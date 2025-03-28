/**
 * AI Governance Dashboard
 * Animations and Visual Effects JavaScript
 */

// Initialize GSAP animations when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Register plugins if needed
    // gsap.registerPlugin(ScrollTrigger, TextPlugin);
    
    // Initial animations
    runEntranceAnimations();
    
    // Set up scroll-based animations
    setupScrollAnimations();
    
    // Set up hover effects
    setupHoverEffects();
});

/**
 * Run entrance animations when the page loads
 */
function runEntranceAnimations() {
    // Sidebar animation
    gsap.from('#sidebar', {
        x: -100,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    });
    
    // Header animation
    gsap.from('.h2', {
        y: -20,
        opacity: 0,
        duration: 0.6,
        delay: 0.2,
        ease: 'back.out(1.7)'
    });
    
    // Cards staggered animation
    gsap.from('.metric-cards .card', {
        y: 50,
        opacity: 0,
        duration: 0.7,
        stagger: 0.1,
        delay: 0.3,
        ease: 'power2.out'
    });
    
    // Animate charts
    gsap.from('.chart-container', {
        scale: 0.9,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2,
        delay: 0.7,
        ease: 'elastic.out(1, 0.75)'
    });
    
    // Activity table animation
    gsap.from('#activities-table', {
        y: 30,
        opacity: 0,
        duration: 0.6,
        delay: 1,
        ease: 'power2.out'
    });
    
    // Quick actions animation
    gsap.from('.action-card', {
        scale: 0.8,
        opacity: 0,
        duration: 0.5,
        stagger: 0.1,
        delay: 1.2,
        ease: 'back.out(1.7)'
    });
}

/**
 * Set up animations based on scroll position
 */
function setupScrollAnimations() {
    // Animate elements as they come into view
    const elements = document.querySelectorAll('.card, .chart-container, .table');
    
    // Create observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadein');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe all elements
    elements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Set up hover effects for interactive elements
 */
function setupHoverEffects() {
    // Add hover effects for cards
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            gsap.to(this, {
                y: -5,
                boxShadow: '0 0.5rem 1.5rem 0 rgba(58, 59, 69, 0.2)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', function() {
            gsap.to(this, {
                y: 0,
                boxShadow: '0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });
    
    // Add hover effects for action cards
    const actionCards = document.querySelectorAll('.action-card');
    
    actionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            gsap.to(this, {
                y: -8,
                scale: 1.03,
                boxShadow: '0 0.7rem 2rem 0 rgba(58, 59, 69, 0.25)',
                duration: 0.3,
                ease: 'power3.out'
            });
        });
        
        card.addEventListener('mouseleave', function() {
            gsap.to(this, {
                y: 0,
                scale: 1,
                boxShadow: '0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });
    
    // Add hover effects for navigation
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                gsap.to(this, {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    color: '#fff',
                    duration: 0.2,
                    ease: 'power1.out'
                });
            }
        });
        
        link.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                gsap.to(this, {
                    backgroundColor: 'transparent',
                    color: 'rgba(255, 255, 255, 0.8)',
                    duration: 0.2,
                    ease: 'power1.out'
                });
            }
        });
        
        link.addEventListener('click', function() {
            // Animation on click
            gsap.from(this, {
                backgroundColor: 'rgba(255, 255, 255, 0.4)',
                duration: 0.5,
                ease: 'power2.out'
            });
        });
    });
}

/**
 * Run animations for section content when navigating
 */
function animateSection(sectionName) {
    const section = document.getElementById(`${sectionName}-section`);
    
    if (section) {
        // Animate section header
        gsap.from(`#${sectionName}-section h2`, {
            y: -20,
            opacity: 0,
            duration: 0.5,
            ease: 'back.out(1.7)'
        });
        
        // Animate cards in the section
        gsap.from(`#${sectionName}-section .card`, {
            y: 40,
            opacity: 0,
            duration: 0.6,
            stagger: 0.1,
            delay: 0.1,
            ease: 'power2.out'
        });
        
        // Animate charts in the section
        gsap.from(`#${sectionName}-section .chart-container`, {
            scale: 0.9,
            opacity: 0,
            duration: 0.7,
            stagger: 0.15,
            delay: 0.3,
            ease: 'elastic.out(1, 0.75)',
            onComplete: function() {
                // Initialize charts after animation completes
                initSectionCharts(sectionName);
            }
        });
        
        // Animate tables in the section
        gsap.from(`#${sectionName}-section .table`, {
            y: 30,
            opacity: 0,
            duration: 0.6,
            delay: 0.4,
            ease: 'power2.out'
        });
    }
}

/**
 * Animate notifications or alerts
 */
function animateNotification(element) {
    gsap.from(element, {
        x: 50,
        opacity: 0,
        duration: 0.5,
        ease: 'power2.out',
        onComplete: function() {
            // Auto-remove after delay
            setTimeout(() => {
                gsap.to(element, {
                    x: 100,
                    opacity: 0,
                    duration: 0.5,
                    ease: 'power2.in',
                    onComplete: function() {
                        element.remove();
                    }
                });
            }, 5000);
        }
    });
}

/**
 * Add typewriter effect to an element
 */
function typewriterEffect(element, text, speed = 30) {
    let i = 0;
    element.innerHTML = '';
    
    function typeWriter() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
    }
    
    typeWriter();
}

/**
 * Create a counter animation that counts up to a value
 */
function animateCounter(element, targetValue, duration = 1.5) {
    const startValue = 0;
    const increment = targetValue / (duration * 60); // 60fps
    let currentValue = startValue;
    
    function updateCounter() {
        if (currentValue < targetValue) {
            currentValue += increment;
            if (currentValue > targetValue) {
                currentValue = targetValue;
            }
            
            // Format based on type (percentage, whole number, etc.)
            if (targetValue % 1 === 0) {
                // Integer
                element.textContent = Math.floor(currentValue);
            } else {
                // Float, show one decimal place
                element.textContent = currentValue.toFixed(1);
            }
            
            requestAnimationFrame(updateCounter);
        }
    }
    
    updateCounter();
}

/**
 * Create a pulse animation on an element
 */
function pulseAnimation(element, repeat = 3) {
    gsap.to(element, {
        scale: 1.05,
        boxShadow: '0 0 15px rgba(78, 115, 223, 0.6)',
        duration: 0.5,
        repeat: repeat * 2 - 1,
        yoyo: true,
        ease: 'power1.inOut'
    });
}

/**
 * Create a fade transition between two elements
 */
function fadeTransition(hideElement, showElement, duration = 0.4) {
    gsap.to(hideElement, {
        opacity: 0,
        duration: duration,
        onComplete: function() {
            hideElement.style.display = 'none';
            showElement.style.display = 'block';
            gsap.fromTo(showElement, 
                { opacity: 0 },
                { opacity: 1, duration: duration }
            );
        }
    });
}