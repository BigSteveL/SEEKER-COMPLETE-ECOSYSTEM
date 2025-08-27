/**
 * SEEKER Consumer Marketplace
 * Revolutionary consumer marketplace with complete price transparency
 */

class SEEKERConsumerMarketplace {
    constructor() {
        this.currentProduct = '';
        this.currentIndustry = '';
        this.currentCategory = '';
        this.isLoading = false;
        
        this.industries = [
            'Electronics', 'Automotive', 'Home & Garden', 'Fashion', 
            'Health & Beauty', 'Sports & Outdoors', 'Toys & Games',
            'Books & Media', 'Food & Beverage', 'Pet Supplies'
        ];
        
        this.categories = [
            'Smartphones', 'Laptops', 'Headphones', 'Cameras',
            'Home Appliances', 'Furniture', 'Clothing', 'Shoes',
            'Cosmetics', 'Supplements', 'Exercise Equipment', 'Board Games'
        ];
        
        this.init();
    }
    
    init() {
        console.log('🛒 SEEKER Consumer Marketplace initialized');
        this.setupEventListeners();
        this.loadInitialData();
    }
    
    setupEventListeners() {
        // Product search
        const productSearch = document.getElementById('productSearch');
        if (productSearch) {
            productSearch.addEventListener('input', (e) => {
                this.currentProduct = e.target.value;
                this.updateSearchButton();
            });
        }
        
        // Industry selection
        const industrySelect = document.getElementById('marketplaceIndustrySelect');
        if (industrySelect) {
            industrySelect.addEventListener('change', (e) => {
                this.currentIndustry = e.target.value;
                this.updateSearchButton();
            });
        }
        
        // Category selection
        const categorySelect = document.getElementById('marketplaceCategorySelect');
        if (categorySelect) {
            categorySelect.addEventListener('change', (e) => {
                this.currentCategory = e.target.value;
                this.updateSearchButton();
            });
        }
        
        // Search button
        const searchBtn = document.getElementById('searchProductBtn');
        if (searchBtn) {
            searchBtn.addEventListener('click', () => this.searchProduct());
        }
        
        // Price alert button
        const alertBtn = document.getElementById('setPriceAlertBtn');
        if (alertBtn) {
            alertBtn.addEventListener('click', () => this.setPriceAlert());
        }
        
        // Sustainability comparison button
        const sustainabilityBtn = document.getElementById('sustainabilityComparisonBtn');
        if (sustainabilityBtn) {
            sustainabilityBtn.addEventListener('click', () => this.getSustainabilityComparison());
        }
        
        // Cost transparency button
        const transparencyBtn = document.getElementById('costTransparencyBtn');
        if (transparencyBtn) {
            transparencyBtn.addEventListener('click', () => this.getCostTransparency());
        }
    }
    
    loadInitialData() {
        this.populateIndustrySelect();
        this.populateCategorySelect();
        this.loadMarketplaceInfo();
    }
    
    populateIndustrySelect() {
        const industrySelect = document.getElementById('marketplaceIndustrySelect');
        if (!industrySelect) return;
        
        industrySelect.innerHTML = '<option value="">Select Industry</option>';
        this.industries.forEach(industry => {
            const option = document.createElement('option');
            option.value = industry;
            option.textContent = industry;
            industrySelect.appendChild(option);
        });
    }
    
    populateCategorySelect() {
        const categorySelect = document.getElementById('marketplaceCategorySelect');
        if (!categorySelect) return;
        
        categorySelect.innerHTML = '<option value="">Select Category</option>';
        this.categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categorySelect.appendChild(option);
        });
    }
    
    async loadMarketplaceInfo() {
        try {
            const response = await fetch('/api/v1/consumer-marketplace/health');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayMarketplaceInfo(data.data);
            }
        } catch (error) {
            console.error('Error loading marketplace info:', error);
        }
    }
    
    displayMarketplaceInfo(marketplaceData) {
        const infoContainer = document.getElementById('marketplaceInfo');
        if (!infoContainer) return;
        
        infoContainer.innerHTML = `
            <div class="marketplace-header">
                <h5><i class="fas fa-shopping-cart me-2"></i>Consumer Marketplace</h5>
                <p class="text-muted">Complete price transparency across 7 continents</p>
            </div>
            <div class="features-grid">
                ${marketplaceData.features.map(feature => `
                    <div class="feature-item">
                        <i class="fas fa-check-circle text-success"></i>
                        <span>${feature}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    updateSearchButton() {
        const searchBtn = document.getElementById('searchProductBtn');
        if (!searchBtn) return;
        
        if (this.currentProduct && this.currentIndustry && this.currentCategory) {
            searchBtn.disabled = false;
            searchBtn.textContent = `Search ${this.currentProduct}`;
        } else {
            searchBtn.disabled = true;
            searchBtn.textContent = 'Enter Product, Industry & Category';
        }
    }
    
    async searchProduct() {
        if (!this.currentProduct || !this.currentIndustry || !this.currentCategory) {
            this.showNotification('Please enter product name, industry, and category', 'warning');
            return;
        }
        
        if (this.isLoading) {
            this.showNotification('Search already in progress...', 'info');
            return;
        }
        
        this.isLoading = true;
        this.showSearchProgress();
        
        try {
            const response = await fetch(`/api/v1/consumer-marketplace/product-comparison?product_name=${encodeURIComponent(this.currentProduct)}&industry=${encodeURIComponent(this.currentIndustry)}&category=${encodeURIComponent(this.currentCategory)}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayProductComparison(data.data);
                this.showNotification('Product comparison completed!', 'success');
            } else {
                this.showNotification('Failed to get product comparison', 'error');
            }
        } catch (error) {
            console.error('Error searching product:', error);
            this.showNotification('Error searching product', 'error');
        } finally {
            this.isLoading = false;
            this.hideSearchProgress();
        }
    }
    
    displayProductComparison(comparison) {
        const resultsContainer = document.getElementById('marketplaceResults');
        if (!resultsContainer) return;
        
        resultsContainer.innerHTML = `
            <div class="comparison-header">
                <h4><i class="fas fa-chart-line me-2"></i>Price Comparison: ${comparison.product_name}</h4>
                <p class="text-muted">${comparison.industry} - ${comparison.category}</p>
            </div>
            
            <div class="price-overview">
                <div class="row">
                    <div class="col-md-4">
                        <div class="price-card">
                            <h6>Average Price</h6>
                            <div class="price-value">$${comparison.average_price}</div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="price-card">
                            <h6>Price Range</h6>
                            <div class="price-range">$${comparison.price_range.min} - $${comparison.price_range.max}</div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="price-card">
                            <h6>Best Value</h6>
                            <div class="best-value">${comparison.best_value_supplier.supplier_name}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="top-prices-section">
                <h5><i class="fas fa-trophy me-2"></i>Top 3 Best Prices</h5>
                <div class="top-prices-grid">
                    ${comparison.top_3_prices.map((price, index) => `
                        <div class="price-item ${index === 0 ? 'best-price' : ''}">
                            <div class="rank-badge">#${price.rank}</div>
                            <h6>${price.supplier_name}</h6>
                            <div class="price">$${price.price_usd}</div>
                            <div class="location">${price.continent.replace('_', ' ').toUpperCase()}</div>
                            <div class="metrics">
                                <span class="quality">Quality: ${price.quality_score}</span>
                                <span class="rating">Rating: ${price.consumer_rating}/5</span>
                            </div>
                            <button class="btn btn-sm btn-outline-primary" onclick="consumerMarketplace.showCostBreakdown('${price.supplier_name}', ${JSON.stringify(price.cost_breakdown).replace(/"/g, '&quot;')})">
                                <i class="fas fa-calculator me-1"></i>Cost Breakdown
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="transparency-section">
                <h5><i class="fas fa-eye me-2"></i>Cost Transparency Rankings</h5>
                <div class="transparency-list">
                    ${comparison.cost_transparency_rankings.slice(0, 5).map((ranking, index) => `
                        <div class="transparency-item">
                            <div class="rank">#${ranking.rank}</div>
                            <div class="supplier">${ranking.supplier_name}</div>
                            <div class="transparency-score">${(ranking.transparency_score * 100).toFixed(1)}%</div>
                            <div class="price">$${ranking.price_usd}</div>
                            <div class="profit-margin">${ranking.profit_margin_percentage}% profit</div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="consumer-insights">
                <h5><i class="fas fa-lightbulb me-2"></i>Consumer Insights</h5>
                <div class="insights-list">
                    ${comparison.consumer_insights.map(insight => `
                        <div class="insight-item">
                            <i class="fas fa-info-circle me-2"></i>
                            <span>${insight}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    showCostBreakdown(supplierName, costBreakdown) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'costBreakdownModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-calculator me-2"></i>Cost Breakdown: ${supplierName}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="cost-breakdown-grid">
                            <div class="cost-item">
                                <div class="cost-label">Material Cost</div>
                                <div class="cost-value">$${costBreakdown.material_cost}</div>
                                <div class="cost-percentage">${((costBreakdown.material_cost / costBreakdown.final_price) * 100).toFixed(1)}%</div>
                            </div>
                            <div class="cost-item">
                                <div class="cost-label">Labor Cost</div>
                                <div class="cost-value">$${costBreakdown.labor_cost}</div>
                                <div class="cost-percentage">${((costBreakdown.labor_cost / costBreakdown.final_price) * 100).toFixed(1)}%</div>
                            </div>
                            <div class="cost-item">
                                <div class="cost-label">Transportation</div>
                                <div class="cost-value">$${costBreakdown.transportation_cost}</div>
                                <div class="cost-percentage">${((costBreakdown.transportation_cost / costBreakdown.final_price) * 100).toFixed(1)}%</div>
                            </div>
                            <div class="cost-item">
                                <div class="cost-label">Tariffs</div>
                                <div class="cost-value">$${costBreakdown.tariff_cost}</div>
                                <div class="cost-percentage">${((costBreakdown.tariff_cost / costBreakdown.final_price) * 100).toFixed(1)}%</div>
                            </div>
                            <div class="cost-item">
                                <div class="cost-label">Overhead</div>
                                <div class="cost-value">$${costBreakdown.overhead_cost}</div>
                                <div class="cost-percentage">${((costBreakdown.overhead_cost / costBreakdown.final_price) * 100).toFixed(1)}%</div>
                            </div>
                            <div class="cost-item profit">
                                <div class="cost-label">Profit Margin</div>
                                <div class="cost-value">$${costBreakdown.profit_margin}</div>
                                <div class="cost-percentage">${((costBreakdown.profit_margin / costBreakdown.final_price) * 100).toFixed(1)}%</div>
                            </div>
                            <div class="cost-item markup">
                                <div class="cost-label">Retail Markup</div>
                                <div class="cost-value">$${costBreakdown.retail_markup}</div>
                                <div class="cost-percentage">${((costBreakdown.retail_markup / costBreakdown.final_price) * 100).toFixed(1)}%</div>
                            </div>
                        </div>
                        
                        <div class="cost-summary">
                            <div class="summary-item">
                                <div class="summary-label">Total Cost</div>
                                <div class="summary-value">$${costBreakdown.total_cost}</div>
                            </div>
                            <div class="summary-item">
                                <div class="summary-label">Final Price</div>
                                <div class="summary-value final-price">$${costBreakdown.final_price}</div>
                            </div>
                            <div class="summary-item">
                                <div class="summary-label">Transparency Score</div>
                                <div class="summary-value">${(costBreakdown.cost_transparency_score * 100).toFixed(1)}%</div>
                            </div>
                        </div>
                        
                        <div class="transparency-insight">
                            <h6><i class="fas fa-eye me-2"></i>Transparency Insight</h6>
                            <p>This supplier shows ${(costBreakdown.cost_transparency_score * 100).toFixed(1)}% cost transparency, 
                            ${costBreakdown.cost_transparency_score > 0.8 ? 'excellent' : costBreakdown.cost_transparency_score > 0.6 ? 'good' : 'poor'} 
                            for consumer price transparency.</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }
    
    async setPriceAlert() {
        if (!this.currentProduct) {
            this.showNotification('Please search for a product first', 'warning');
            return;
        }
        
        const targetPrice = prompt(`Set price alert for ${this.currentProduct} (enter target price in USD):`);
        if (!targetPrice || isNaN(targetPrice)) {
            this.showNotification('Please enter a valid price', 'warning');
            return;
        }
        
        try {
            const response = await fetch(`/api/v1/consumer-marketplace/price-alerts?product_name=${encodeURIComponent(this.currentProduct)}&target_price=${targetPrice}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayPriceAlerts(data.data);
                this.showNotification(`Price alert set for $${targetPrice}`, 'success');
            } else {
                this.showNotification('Failed to set price alert', 'error');
            }
        } catch (error) {
            console.error('Error setting price alert:', error);
            this.showNotification('Error setting price alert', 'error');
        }
    }
    
    displayPriceAlerts(alertData) {
        const alertsContainer = document.getElementById('priceAlerts');
        if (!alertsContainer) return;
        
        if (alertData.alerts.length === 0) {
            alertsContainer.innerHTML = `
                <div class="no-alerts">
                    <i class="fas fa-bell-slash"></i>
                    <p>No suppliers currently below your target price of $${alertData.target_price}</p>
                </div>
            `;
            return;
        }
        
        alertsContainer.innerHTML = `
            <div class="alerts-header">
                <h5><i class="fas fa-bell me-2"></i>Price Alerts</h5>
                <p>Target: $${alertData.target_price}</p>
            </div>
            <div class="alerts-list">
                ${alertData.alerts.map(alert => `
                    <div class="alert-item">
                        <div class="alert-badge">SAVE $${alert.savings.toFixed(2)}</div>
                        <div class="alert-supplier">${alert.supplier_name}</div>
                        <div class="alert-price">$${alert.current_price}</div>
                        <div class="alert-location">${alert.continent.replace('_', ' ').toUpperCase()}</div>
                        <div class="alert-metrics">
                            <span class="quality">Quality: ${alert.quality_score}</span>
                            <span class="rating">Rating: ${alert.consumer_rating}/5</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    async getSustainabilityComparison() {
        if (!this.currentProduct) {
            this.showNotification('Please search for a product first', 'warning');
            return;
        }
        
        try {
            const response = await fetch(`/api/v1/consumer-marketplace/sustainability-comparison?product_name=${encodeURIComponent(this.currentProduct)}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displaySustainabilityComparison(data.data);
                this.showNotification('Sustainability comparison completed!', 'success');
            } else {
                this.showNotification('Failed to get sustainability comparison', 'error');
            }
        } catch (error) {
            console.error('Error getting sustainability comparison:', error);
            this.showNotification('Error getting sustainability comparison', 'error');
        }
    }
    
    displaySustainabilityComparison(comparison) {
        const sustainabilityContainer = document.getElementById('sustainabilityComparison');
        if (!sustainabilityContainer) return;
        
        sustainabilityContainer.innerHTML = `
            <div class="sustainability-header">
                <h5><i class="fas fa-leaf me-2"></i>Sustainability Comparison</h5>
                <p>${comparison.product_name}</p>
            </div>
            
            <div class="sustainability-overview">
                <div class="overview-item">
                    <div class="overview-label">Average Sustainability</div>
                    <div class="overview-value">${(comparison.average_sustainability * 100).toFixed(1)}%</div>
                </div>
            </div>
            
            <div class="sustainability-rankings">
                <h6>Top Sustainable Suppliers</h6>
                <div class="rankings-list">
                    ${comparison.sustainability_rankings.map((ranking, index) => `
                        <div class="ranking-item ${index === 0 ? 'top-ranking' : ''}">
                            <div class="rank">#${ranking.rank}</div>
                            <div class="supplier">${ranking.supplier_name}</div>
                            <div class="sustainability-score">${(ranking.sustainability_score * 100).toFixed(1)}%</div>
                            <div class="price">$${ranking.price_usd}</div>
                            <div class="quality">Quality: ${ranking.quality_score}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="sustainability-insights">
                <h6><i class="fas fa-lightbulb me-2"></i>Sustainability Insights</h6>
                <div class="insights-list">
                    ${comparison.sustainability_insights.map(insight => `
                        <div class="insight-item">
                            <i class="fas fa-info-circle me-2"></i>
                            <span>${insight}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    async getCostTransparency() {
        if (!this.currentProduct || !this.currentIndustry || !this.currentCategory) {
            this.showNotification('Please search for a product first', 'warning');
            return;
        }
        
        try {
            const response = await fetch(`/api/v1/consumer-marketplace/cost-transparency?product_name=${encodeURIComponent(this.currentProduct)}&industry=${encodeURIComponent(this.currentIndustry)}&category=${encodeURIComponent(this.currentCategory)}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.displayCostTransparency(data.data);
                this.showNotification('Cost transparency report completed!', 'success');
            } else {
                this.showNotification('Failed to get cost transparency report', 'error');
            }
        } catch (error) {
            console.error('Error getting cost transparency:', error);
            this.showNotification('Error getting cost transparency report', 'error');
        }
    }
    
    displayCostTransparency(transparencyData) {
        const transparencyContainer = document.getElementById('costTransparency');
        if (!transparencyContainer) return;
        
        transparencyContainer.innerHTML = `
            <div class="transparency-header">
                <h5><i class="fas fa-eye me-2"></i>Cost Transparency Report</h5>
                <p>${transparencyData.product_name}</p>
            </div>
            
            <div class="transparency-overview">
                <div class="overview-item">
                    <div class="overview-label">Average Transparency</div>
                    <div class="overview-value">${(transparencyData.average_transparency * 100).toFixed(1)}%</div>
                </div>
            </div>
            
            <div class="transparency-rankings">
                <h6>Transparency Rankings</h6>
                <div class="rankings-list">
                    ${transparencyData.transparency_rankings.map((ranking, index) => `
                        <div class="ranking-item ${index === 0 ? 'top-ranking' : ''}">
                            <div class="rank">#${ranking.rank}</div>
                            <div class="supplier">${ranking.supplier_name}</div>
                            <div class="transparency-score">${(ranking.transparency_score * 100).toFixed(1)}%</div>
                            <div class="price">$${ranking.price_usd}</div>
                            <div class="profit-margin">${ranking.profit_margin_percentage}% profit</div>
                            <div class="retail-markup">${ranking.retail_markup_percentage}% markup</div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="transparency-insights">
                <h6><i class="fas fa-lightbulb me-2"></i>Transparency Insights</h6>
                <div class="insights-list">
                    ${transparencyData.transparency_insights.map(insight => `
                        <div class="insight-item">
                            <i class="fas fa-info-circle me-2"></i>
                            <span>${insight}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    showSearchProgress() {
        const progressContainer = document.getElementById('marketplaceProgress');
        if (!progressContainer) return;
        
        progressContainer.innerHTML = `
            <div class="progress-overlay">
                <div class="progress-content">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h5 class="mt-3">Searching Global Marketplace</h5>
                    <p class="text-muted">Analyzing prices across 7 continents...</p>
                </div>
            </div>
        `;
        progressContainer.style.display = 'block';
    }
    
    hideSearchProgress() {
        const progressContainer = document.getElementById('marketplaceProgress');
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    }
    
    showNotification(message, type = 'info') {
        const container = document.getElementById('marketplaceNotificationContainer');
        if (!container) return;
        
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        container.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
}

// Initialize consumer marketplace
if (typeof window !== 'undefined') {
    window.consumerMarketplace = new SEEKERConsumerMarketplace();
} 