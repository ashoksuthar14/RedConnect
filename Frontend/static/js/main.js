// Initialize AOS animation library
AOS.init({
    duration: 1000,
    once: true
});

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add hover effect to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Form submission handling
    const donorForm = document.getElementById('donorForm');
    if (donorForm) {
        donorForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show success message
            const formData = new FormData(donorForm);
            alert('Thank you for registering as a donor! We will contact you soon.');
            donorForm.reset();
        });
    }
});

// Contact form handling
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show success message
        const formData = new FormData(contactForm);
        alert('Thank you for your message! We will get back to you soon.');
        contactForm.reset();
    });
}

// Registration form donation details toggle
const donorRadios = document.querySelectorAll('input[name="isDonor"]');
const donationDetails = document.getElementById('donationDetails');

if (donorRadios.length > 0) {
    donorRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'yes') {
                donationDetails.style.display = 'grid';
            } else {
                donationDetails.style.display = 'none';
            }
        });
    });
}

// Registration form handling
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show success message and redirect to profile
        alert('Registration successful! Redirecting to your profile...');
        window.location.href = '/profile';
    });
} 