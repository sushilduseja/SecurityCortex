/**
 * AI Governance Dashboard
 * Main Application JavaScript
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the dashboard
    initDashboard();
    
    // Set up navigation event listeners
    setupNavigation();
    
    // Fetch initial data
    fetchDashboardData();
    
    // Initialize loading animation
    initLoadingAnimation();
    
    // Set up theme toggling
    setupThemeToggle();
});

/**
 * Initialize dashboard components
 */
function initDashboard() {
    console.log('Initializing AI Governance Dashboard...');
    
    // Add a loading animation while initial data loads
    showLoading();
    
    // Simulate loading time (remove in production)
    setTimeout(() => {
        hideLoading();
    }, 1500);
    
    // Add theme toggle button to the DOM
    addThemeToggleButton();
}

/**
 * Set up navigation event listeners for the sidebar
 */
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get the section to show
            const sectionToShow = this.getAttribute('data-section');
            
            // Update navigation state
            updateNavigation(this);
            
            // Show the appropriate content section
            showSection(sectionToShow);
        });
    });
    
    // Set up quick action cards
    const actionCards = document.querySelectorAll('.action-card');
    
    actionCards.forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            
            const section = this.getAttribute('data-section');
            const action = this.getAttribute('data-action');
            
            // Navigate to the section
            const navLink = document.querySelector(`.nav-link[data-section="${section}"]`);
            if (navLink) {
                updateNavigation(navLink);
                showSection(section);
                
                // Handle specific action (if needed)
                handleAction(section, action);
            }
        });
    });
}

/**
 * Update navigation state (active classes)
 */
function updateNavigation(activeLink) {
    // Remove active class from all links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        link.classList.add('text-white');
    });
    
    // Add active class to the clicked link
    activeLink.classList.add('active');
    activeLink.classList.remove('text-white');
}

/**
 * Show the specified content section
 */
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show the requested section
    const sectionToShow = document.getElementById(`${sectionName}-section`);
    if (sectionToShow) {
        // Add loading animation
        showLoading();
        
        // Simulate data loading (remove in production)
        setTimeout(() => {
            sectionToShow.classList.add('active');
            hideLoading();
            
            // Trigger animations for the section
            animateSection(sectionName);
            
            // Fetch data for the section
            fetchSectionData(sectionName);
        }, 800);
    }
}

/**
 * Handle specific actions for sections
 */
function handleAction(section, action) {
    console.log(`Handling action: ${action} in section: ${section}`);
    
    // Show appropriate modal or form based on the action
    switch(action) {
        case 'new-policy':
            showModal('Generate New Policy', 'Policy generation form will appear here.');
            break;
        case 'new-assessment':
            showModal('Risk Assessment', 'Risk assessment form will appear here.');
            break;
        case 'view-compliance':
            // No modal needed, just show the compliance section
            break;
        case 'generate-report':
            showModal('Generate Report', 'Report generation options will appear here.');
            break;
    }
}

/**
 * Fetch data for the dashboard
 */
function fetchDashboardData() {
    // In production, this would be an API call
    console.log('Fetching dashboard data...');
    
    // Simulate API call
    setTimeout(() => {
        updateDashboardMetrics({
            policies: 12,
            riskScore: 76,
            complianceRate: 94,
            monitors: 8
        });
        
        // Update charts after data is received
        updateCharts();
    }, 1000);
}

/**
 * Fetch data for a specific section
 */
function fetchSectionData(section) {
    console.log(`Fetching data for ${section} section...`);
    
    // In production, make an API call to get section data
    // For now, just simulate different actions based on section
    switch(section) {
        case 'governance':
            // Fetch governance policies
            break;
        case 'risk':
            // Fetch risk assessments
            break;
        case 'monitoring':
            // Fetch monitoring data
            break;
        case 'reports':
            // Fetch reports
            break;
    }
}

/**
 * Update dashboard metrics with real data
 */
function updateDashboardMetrics(data) {
    // This would update the actual metrics with data from the API
    console.log('Updating dashboard metrics:', data);
}

/**
 * Show loading animation
 */
function showLoading() {
    // Check if loading element already exists
    let loader = document.querySelector('.loading-animation');
    
    if (!loader) {
        // Create and add the loading animation to the DOM
        loader = document.createElement('div');
        loader.className = 'loading-animation';
        loader.innerHTML = '<div class="loader"></div>';
        document.body.appendChild(loader);
    } else {
        loader.style.display = 'flex';
    }
}

/**
 * Hide loading animation
 */
function hideLoading() {
    const loader = document.querySelector('.loading-animation');
    if (loader) {
        loader.style.display = 'none';
    }
}

/**
 * Initialize loading animation
 */
function initLoadingAnimation() {
    // Create loading animation element
    const loadingElement = document.createElement('div');
    loadingElement.className = 'loading-animation';
    loadingElement.style.display = 'none';
    loadingElement.innerHTML = '<div class="loader"></div>';
    
    // Add to the DOM
    document.body.appendChild(loadingElement);
}

/**
 * Add theme toggle button to the DOM
 */
function addThemeToggleButton() {
    const toggleBtn = document.createElement('div');
    toggleBtn.className = 'theme-toggle';
    toggleBtn.innerHTML = '<i class="bx bx-moon fs-4"></i>';
    toggleBtn.setAttribute('title', 'Toggle Dark Mode');
    
    document.body.appendChild(toggleBtn);
}

/**
 * Set up theme toggling
 */
function setupThemeToggle() {
    const toggleBtn = document.querySelector('.theme-toggle');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            
            const icon = toggleBtn.querySelector('i');
            if (document.body.classList.contains('dark-mode')) {
                icon.classList.remove('bx-moon');
                icon.classList.add('bx-sun');
            } else {
                icon.classList.remove('bx-sun');
                icon.classList.add('bx-moon');
            }
        });
    }
}

/**
 * Animate specific section elements
 */
function animateSection(section) {
    // Create staggered animations for elements in the section
    const sectionElement = document.getElementById(`${section}-section`);
    
    if (sectionElement) {
        // Find all cards in the section and animate them
        const cards = sectionElement.querySelectorAll('.card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('animate-fadein');
            }, index * 100);
        });
        
        // Animate charts if present
        const charts = sectionElement.querySelectorAll('.chart-container');
        charts.forEach((chart, index) => {
            setTimeout(() => {
                chart.classList.add('chart-animate');
                chart.classList.add('active');
            }, 300 + (index * 150));
        });
    }
}

/**
 * Show a modal with content
 */
function showModal(title, content) {
    // Remove any existing modal
    const existingModal = document.querySelector('.modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal structure
    const modalHTML = `
        <div class="modal fade" id="actionModal" tabindex="-1" aria-labelledby="actionModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="actionModalLabel">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary">Save changes</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to the DOM
    const modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHTML;
    document.body.appendChild(modalContainer.firstElementChild);
    
    // Initialize and show the modal
    const modalElement = document.getElementById('actionModal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// Add error handling for API requests
function handleApiError(error) {
    console.error('API Error:', error);
    
    // Show error notification to user
    const errorMessage = error.message || 'An unexpected error occurred';
    showNotification('Error', errorMessage, 'error');
}

// Show notification to user
function showNotification(title, message, type = 'info') {
    // This function would create a toast or notification
    // For now, log to console
    console.log(`[${type.toUpperCase()}] ${title}: ${message}`);
    
    // Example toast creation (would require a notification library or custom implementation)
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} animate-fadein`;
    toast.innerHTML = `
        <div class="toast-header">
            <strong>${title}</strong>
            <button type="button" class="btn-close"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    
    // In a real implementation, you would add this to a toast container
    // and initialize it with your toast/notification library
}