// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Example text functionality for the analyze page
    if (document.querySelector('.example-texts')) {
        setupExampleTexts();
    }
    
    // Setup alerts to auto-dismiss
    setupAutoDismissAlerts();
    
    // Add animation to the sentiment result
    if (document.querySelector('.sentiment-icon')) {
        animateSentimentIcon();
    }
});

/**
 * Set up the example text functionality
 */
function setupExampleTexts() {
    const exampleBtns = document.querySelectorAll('.example-btn');
    const textArea = document.getElementById('text');
    
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const exampleContent = this.nextElementSibling.textContent;
            textArea.value = exampleContent;
            textArea.focus();
            
            // Scroll to the submit button
            const submitBtn = document.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

/**
 * Set up auto-dismissing alerts
 */
function setupAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Animate the sentiment icon on the results page
 */
function animateSentimentIcon() {
    const icon = document.querySelector('.sentiment-icon span');
    
    // Simple animation
    icon.style.transform = 'scale(0)';
    icon.style.transition = 'transform 0.5s ease';
    
    setTimeout(() => {
        icon.style.transform = 'scale(1.2)';
        
        setTimeout(() => {
            icon.style.transform = 'scale(1)';
        }, 200);
    }, 100);
}

/**
 * Form validation
 */
function validateForm() {
    const textInput = document.getElementById('text');
    
    if (!textInput.value.trim()) {
        alert('Please enter some text to analyze.');
        return false;
    }
    
    return true;
}