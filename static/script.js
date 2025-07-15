// MindMetric AI - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeQuizProgress();
    initializeFormValidation();
    initializeDateRestrictions();
    initializeAnimations();
});

// Quiz progress tracking
function initializeQuizProgress() {
    const quizForm = document.getElementById('quizForm');
    const progressBar = document.getElementById('progressBar');
    
    if (!quizForm || !progressBar) return;
    
    const totalQuestions = 15;
    const allInputs = quizForm.querySelectorAll('input[type="radio"]');
    
    // Update progress when any radio button changes
    allInputs.forEach(input => {
        input.addEventListener('change', updateProgress);
    });
    
    function updateProgress() {
        const answeredQuestions = new Set();
        
        // Count unique questions that have been answered
        allInputs.forEach(input => {
            if (input.checked) {
                answeredQuestions.add(input.name);
            }
        });
        
        const progress = (answeredQuestions.size / totalQuestions) * 100;
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
        
        // Change color based on progress
        if (progress < 50) {
            progressBar.className = 'progress-bar bg-danger';
        } else if (progress < 80) {
            progressBar.className = 'progress-bar bg-warning';
        } else {
            progressBar.className = 'progress-bar bg-success';
        }
    }
    
    // Form submission handling
    quizForm.addEventListener('submit', function(e) {
        const button = quizForm.querySelector('button[type="submit"]');
        button.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Analyzing...';
        button.disabled = true;
        
        // Show loading state
        document.body.classList.add('loading');
    });
}

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation feedback
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
}

// Date restrictions for booking
function initializeDateRestrictions() {
    const dateInput = document.getElementById('date');
    if (!dateInput) return;
    
    // Set minimum date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    dateInput.min = tomorrow.toISOString().split('T')[0];
    
    // Set maximum date to 60 days from now
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + 60);
    dateInput.max = maxDate.toISOString().split('T')[0];
    
    // Disable weekends (optional)
    dateInput.addEventListener('input', function() {
        const selectedDate = new Date(this.value);
        const dayOfWeek = selectedDate.getDay();
        
        // If weekend is selected, show a warning
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-warning mt-2';
            alert.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Note: Weekend sessions may have limited availability.';
            
            // Remove any existing warnings
            const existingAlert = this.parentNode.querySelector('.alert');
            if (existingAlert) {
                existingAlert.remove();
            }
            
            this.parentNode.appendChild(alert);
        }
    });
}

// Animation and UI enhancements
function initializeAnimations() {
    // Fade in animations for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-info):not(.alert-warning):not(.alert-danger)');
    alerts.forEach(alert => {
        if (alert.querySelector('.btn-close')) {
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.style.transition = 'opacity 0.5s ease';
                    alert.style.opacity = '0';
                    setTimeout(() => {
                        if (alert.parentNode) {
                            alert.remove();
                        }
                    }, 500);
                }
            }, 5000);
        }
    });
}

// Utility functions
function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

// Password strength checker
function checkPasswordStrength(password) {
    const strength = {
        score: 0,
        feedback: []
    };
    
    if (password.length >= 8) strength.score += 1;
    else strength.feedback.push('At least 8 characters');
    
    if (/[A-Z]/.test(password)) strength.score += 1;
    else strength.feedback.push('At least one uppercase letter');
    
    if (/[a-z]/.test(password)) strength.score += 1;
    else strength.feedback.push('At least one lowercase letter');
    
    if (/\d/.test(password)) strength.score += 1;
    else strength.feedback.push('At least one number');
    
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength.score += 1;
    else strength.feedback.push('At least one special character');
    
    return strength;
}

// AI Summary formatting and interaction
function formatAISummary() {
    const rawSummary = document.getElementById('raw-summary');
    const summaryContent = document.getElementById('ai-summary-content');
    
    if (!rawSummary || !summaryContent) return;
    
    let text = rawSummary.textContent.trim();
    
    // Format the summary into sections
    const sections = text.split('\n\n');
    let formattedHTML = '';
    
    sections.forEach(section => {
        section = section.trim();
        if (!section) return;
        
        // Check if it's a heading (starts with capital and has fewer than 100 chars)
        if (section.length < 100 && section.charAt(0) === section.charAt(0).toUpperCase() && !section.includes('.')) {
            formattedHTML += `<h4>${section}</h4>`;
        } else {
            // Check if it contains bullet points
            if (section.includes('•') || section.includes('-')) {
                const lines = section.split('\n');
                let ulContent = '';
                let inList = false;
                
                lines.forEach(line => {
                    line = line.trim();
                    if (line.startsWith('•') || line.startsWith('-')) {
                        if (!inList) {
                            if (ulContent) formattedHTML += `<p>${ulContent}</p>`;
                            ulContent = '';
                            inList = true;
                            formattedHTML += '<ul>';
                        }
                        formattedHTML += `<li>${line.substring(1).trim()}</li>`;
                    } else if (line) {
                        if (inList) {
                            formattedHTML += '</ul>';
                            inList = false;
                        }
                        ulContent += line + ' ';
                    }
                });
                
                if (inList) formattedHTML += '</ul>';
                if (ulContent.trim()) formattedHTML += `<p>${ulContent.trim()}</p>`;
            } else {
                formattedHTML += `<div class="summary-section"><p>${section}</p></div>`;
            }
        }
    });
    
    summaryContent.innerHTML = formattedHTML || text;
}

function toggleSummaryView() {
    const content = document.getElementById('ai-summary-content');
    const icon = document.getElementById('toggle-icon');
    const text = document.getElementById('toggle-text');
    const rawSummary = document.getElementById('raw-summary');
    
    if (!content || !icon || !text || !rawSummary) return;
    
    if (content.classList.contains('detailed-view')) {
        // Switch to formatted view
        formatAISummary();
        content.classList.remove('detailed-view');
        icon.className = 'bi bi-eye';
        text.textContent = 'Show Detailed View';
    } else {
        // Switch to raw view
        content.innerHTML = `<div class="detailed-view"><pre>${rawSummary.textContent}</pre></div>`;
        content.classList.add('detailed-view');
        icon.className = 'bi bi-eye-slash';
        text.textContent = 'Show Formatted View';
    }
}

// Booking page functionality
function selectConsultationType(type) {
    // Remove selected class from all options
    document.querySelectorAll('.consultation-type').forEach(el => {
        el.classList.remove('selected');
    });
    
    // Add selected class to clicked option
    document.getElementById(type + '-option').classList.add('selected');
    
    // Check the corresponding radio button
    document.getElementById(type + '-radio').checked = true;
    
    // Update the hidden input for form submission
    const hiddenInput = document.getElementById('consultation_type_input');
    if (hiddenInput) {
        hiddenInput.value = type;
    }
}

// Initialize password strength checker if password field exists
const passwordInput = document.getElementById('password');
if (passwordInput) {
    const strengthDiv = document.createElement('div');
    strengthDiv.className = 'password-strength mt-1';
    passwordInput.parentNode.appendChild(strengthDiv);
    
    passwordInput.addEventListener('input', function() {
        const strength = checkPasswordStrength(this.value);
        let strengthText = '';
        let strengthClass = '';
        
        switch (strength.score) {
            case 0:
            case 1:
                strengthText = 'Very Weak';
                strengthClass = 'text-danger';
                break;
            case 2:
                strengthText = 'Weak';
                strengthClass = 'text-warning';
                break;
            case 3:
                strengthText = 'Fair';
                strengthClass = 'text-info';
                break;
            case 4:
                strengthText = 'Good';
                strengthClass = 'text-success';
                break;
            case 5:
                strengthText = 'Strong';
                strengthClass = 'text-success fw-bold';
                break;
        }
        
        strengthDiv.innerHTML = `<small class="${strengthClass}">Password strength: ${strengthText}</small>`;
    });
}

// Initialize all functionality when DOM loads
document.addEventListener('DOMContentLoaded', function() {
    initializeQuizProgress();
    initializeFormValidation();
    initializeDateRestrictions();
    initializeAnimations();
    formatAISummary(); // Format AI summary on results page
});
