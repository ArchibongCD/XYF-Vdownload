// Helper for Toast Notifications
function showNotify(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.innerText = message;
    toast.className = `animate__animated animate__fadeInUp ${type === 'error' ? 'toast-error' : 'toast-success'}`;
    toast.style.display = 'block';
    
    setTimeout(() => {
        toast.className = 'animate__animated animate__fadeOutDown';
        setTimeout(() => { 
            toast.style.display = 'none'; 
        }, 500);
    }, 3000);
}


// 1. Trigger fetch on Enter key
document.getElementById('url-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('fetch-btn').click();
    }
});

// Fetch Video Information
async function fetchVideoInfo() {
    const urlInput = document.getElementById('url-input');
    const resCard = document.getElementById('result-card');
    const fetchBtn = document.getElementById('fetch-btn');
    
    if (!urlInput.value.trim()) {
        showNotify('Please paste a video URL first!', 'error');
        return;
    }

    // Set loading state
    fetchBtn.disabled = true;
    resCard.classList.remove('show');

    try {
        const response = await fetch(`/fetch/?url=${encodeURIComponent(urlInput.value.trim())}`);
        const data = await response.json();

        if (data.status === 'success') {
            // Populate video information
            document.getElementById('res-title').innerText = data.title;
            document.getElementById('res-thumb').src = data.thumbnail;
            
            // Populate quality selector
            const selector = document.getElementById('quality-selector');
            selector.innerHTML = '';
            data.formats.forEach(format => {
                const option = document.createElement('option');
                option.value = format.url;
                option.text = `${format.res} (.${format.ext})`;
                selector.appendChild(option);
            });
            
            // Show result card with animation
            resCard.classList.add('show');
            showNotify('Video found! Select quality and download.');
        } else {
            showNotify(data.message || 'Failed to fetch video. Check the URL and try again.', 'error');
        }
    } catch (error) {
        console.error('Fetch error:', error);
        showNotify('Connection failed. Please check your internet and try again.', 'error');
    } finally {
        // Reset button state
        fetchBtn.disabled = false;
        fetchBtn.innerHTML = 'Fetch Video';
    }
}

// Download Video
function downloadVideo() {
    const streamUrl = document.getElementById('quality-selector').value;
    const title = document.getElementById('res-title').innerText;
    
    if (!streamUrl) {
        showNotify('Please select a quality first!', 'error');
        return;
    }
    
    window.location.href = `/download/?url=${encodeURIComponent(streamUrl)}&title=${encodeURIComponent(title)}`;
    showNotify('Download started! Check your downloads folder.');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const fetchBtn = document.getElementById('fetch-btn');
    const urlInput = document.getElementById('url-input');
    const downloadBtn = document.getElementById('download-btn');
    
    // Fetch button click
    if (fetchBtn) {
        fetchBtn.addEventListener('click', fetchVideoInfo);
    }
    
    // Enter key on input
    if (urlInput) {
        urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                fetchVideoInfo();
            }
        });
    }
    
    // Download button click
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadVideo);
    }
    
    // Contact form submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
});

// Handle Contact Form Submission
function handleContactForm(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    // Validate form data
    if (!data.name || !data.email || !data.subject || !data.message) {
        showNotify('Please fill in all required fields.', 'error');
        return;
    }
    
    // TODO: Send to backend endpoint when ready
    console.log('Contact form data:', data);
    
    // Show success message
    showNotify('Thank you for contacting us! We will get back to you within 24 hours.');
    
    // Reset form
    e.target.reset();
}

