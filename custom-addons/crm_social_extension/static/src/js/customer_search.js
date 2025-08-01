document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    /**
     * Live Search Functionality
     */
    class CustomerSearch {
        constructor() {
            this.searchInput = document.querySelector('input[name="search"]');
            this.searchResults = document.getElementById('live_search_results');
            this.searchTimeout = null;
            this.isSearching = false;
            
            if (this.searchInput) {
                this.initializeSearch();
            }
            
            this.initializeSocialLinks();
            this.initializeStats();
        }

        initializeSearch() {
            // Add event listeners
            this.searchInput.addEventListener('input', this.handleSearchInput.bind(this));
            this.searchInput.addEventListener('focus', this.handleSearchFocus.bind(this));
            document.addEventListener('click', this.handleDocumentClick.bind(this));
            
            // Add search icon animation
            this.searchInput.addEventListener('input', function() {
                const button = document.querySelector('.search_form .btn');
                if (this.value.length > 0) {
                    button.classList.add('searching');
                } else {
                    button.classList.remove('searching');
                }
            });
        }

        handleSearchInput(event) {
            const query = event.target.value.trim();
            
            // Clear previous timeout
            if (this.searchTimeout) {
                clearTimeout(this.searchTimeout);
            }
            
            // Hide results if query is too short
            if (query.length < 2) {
                this.hideSearchResults();
                return;
            }
            
            // Debounce search
            this.searchTimeout = setTimeout(() => {
                this.performSearch(query);
            }, 300);
        }

        handleSearchFocus(event) {
            const query = event.target.value.trim();
            if (query.length >= 2) {
                this.performSearch(query);
            }
        }

        handleDocumentClick(event) {
            if (!event.target.closest('.search_section')) {
                this.hideSearchResults();
            }
        }

        async performSearch(query) {
            if (this.isSearching) return;
            
            this.isSearching = true;
            this.showSearchLoading();
            
            try {
                const response = await fetch('/customers/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: {
                            search: query,
                            limit: 6
                        }
                    })
                });
                
                const data = await response.json();
                
                if (data.result) {
                    this.displaySearchResults(data.result.customers);
                } else {
                    this.displaySearchError();
                }
            } catch (error) {
                console.error('Search error:', error);
                this.displaySearchError();
            } finally {
                this.isSearching = false;
            }
        }

        showSearchLoading() {
            this.searchResults.innerHTML = `
                <div class="search_result_item">
                    <div class="d-flex align-items-center">
                        <div class="spinner-border spinner-border-sm me-2" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                        <span>Searching customers...</span>
                    </div>
                </div>
            `;
            this.searchResults.style.display = 'block';
        }

        displaySearchResults(customers) {
            if (!customers || customers.length === 0) {
                this.searchResults.innerHTML = `
                    <div class="search_result_item text-center">
                        <i class="fa fa-search text-muted"></i>
                        <span class="ms-2">No customers found</span>
                    </div>
                `;
            } else {
                const resultsHtml = customers.map(customer => this.createSearchResultItem(customer)).join('');
                this.searchResults.innerHTML = resultsHtml;
            }
            
            this.searchResults.style.display = 'block';
        }

        createSearchResultItem(customer) {
            const socialIcons = customer.social_media.map(social => 
                `<i class="fa ${social.icon} me-1" style="color: ${social.color}"></i>`
            ).join('');
            
            const completionBadge = customer.social_complete 
                ? '<span class="badge badge-success badge-sm">Complete</span>'
                : `<span class="badge badge-warning badge-sm">${Math.round(customer.completion_rate)}%</span>`;
            
            return `
                <div class="search_result_item" onclick="window.location.href='/customers/${customer.id}'">
                    <div class="d-flex align-items-center">
                        <div class="customer_image_small me-3">
                            ${customer.image_url 
                                ? `<img src="${customer.image_url}" class="rounded-circle" width="40" height="40" alt="${customer.name}">`
                                : '<div class="bg-light rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;"><i class="fa fa-building text-muted"></i></div>'
                            }
                        </div>
                        <div class="flex-grow-1">
                            <div class="fw-bold">${customer.name}</div>
                            <div class="text-muted small">
                                ${socialIcons}
                                ${completionBadge}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        displaySearchError() {
            this.searchResults.innerHTML = `
                <div class="search_result_item text-center">
                    <i class="fa fa-exclamation-triangle text-warning"></i>
                    <span class="ms-2">Search temporarily unavailable</span>
                </div>
            `;
            this.searchResults.style.display = 'block';
        }

        hideSearchResults() {
            this.searchResults.style.display = 'none';
        }
    }

    /**
     * Social Media Links Enhancement
     */
    function initializeSocialLinks() {
        document.querySelectorAll('.social_link').forEach(link => {
            link.addEventListener('click', function(e) {
                // Add click animation
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
                
                // Track social media clicks (if analytics available)
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'social_media_click', {
                        'platform': this.dataset.platform,
                        'customer_id': window.location.pathname.split('/').pop()
                    });
                }
            });
        });
    }

    /**
     * Stats Dashboard Enhancement
     */
    async function initializeStats() {
        const statsCards = document.querySelectorAll('.stat_number');
        
        // Animate numbers on page load
        statsCards.forEach(card => {
            const finalValue = parseInt(card.textContent);
            if (!isNaN(finalValue)) {
                animateValue(card, 0, finalValue, 1500);
            }
        });
    }

    /**
     * Animate numerical values
     */
    function animateValue(element, start, end, duration) {
        const range = end - start;
        const stepTime = Math.abs(Math.floor(duration / range));
        const timer = setInterval(() => {
            start += 1;
            element.textContent = start;
            if (start >= end) {
                clearInterval(timer);
                element.textContent = end;
            }
        }, stepTime);
    }

    /**
     * Intersection Observer for animations
     */
    function initializeAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe customer cards
        document.querySelectorAll('.customer_card').forEach(card => {
            observer.observe(card);
        });
    }

    /**
     * Smooth scroll for internal links
     */
    function initializeSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Initialize all functionality
     */
    function init() {
        new CustomerSearch();
        initializeSocialLinks();
        initializeStats();
        initializeAnimations();
        initializeSmoothScroll();
        
        // Add CSS animation classes
        const style = document.createElement('style');
        style.textContent = `
            .customer_card {
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.6s ease;
            }
            
            .customer_card.animate-in {
                opacity: 1;
                transform: translateY(0);
            }
            
            .searching .fa-search {
                animation: pulse 1s infinite;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
    }

    // Initialize when DOM is ready
    init();
});
