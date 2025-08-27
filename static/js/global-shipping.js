/**
 * SEEKER Global Shipping Marketplace
 * Revolutionary shipping transparency with daily volume bidding system
 * Consumer-first global logistics optimization across all 7 continents
 */

class SEEKERGlobalShipping {
    constructor() {
        this.apiBase = '/api/v1/global-shipping';
        this.currentQuote = null;
        this.currentBidding = null;
        this.charts = {};
        
        this.initializeEventListeners();
        this.loadAvailableCarriers();
        this.loadGlobalInsights();
    }

    initializeEventListeners() {
        // Shipping quote form
        const quoteForm = document.getElementById('shipping-quote-form');
        if (quoteForm) {
            quoteForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.getShippingQuote();
            });
        }

        // Daily volume bidding
        const biddingBtn = document.getElementById('daily-volume-bidding-btn');
        if (biddingBtn) {
            biddingBtn.addEventListener('click', () => this.getDailyVolumeBidding());
        }

        // Carrier comparison
        const comparisonBtn = document.getElementById('carrier-comparison-btn');
        if (comparisonBtn) {
            comparisonBtn.addEventListener('click', () => this.getCarrierComparison());
        }

        // Shipping transparency
        const transparencyBtn = document.getElementById('shipping-transparency-btn');
        if (transparencyBtn) {
            transparencyBtn.addEventListener('click', () => this.getShippingTransparency());
        }

        // Sustainability comparison
        const sustainabilityBtn = document.getElementById('sustainability-comparison-btn');
        if (sustainabilityBtn) {
            sustainabilityBtn.addEventListener('click', () => this.getSustainabilityComparison());
        }

        // Export functionality
        const exportBtn = document.getElementById('export-shipping-data');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportShippingData());
        }

        // Refresh data
        const refreshBtn = document.getElementById('refresh-shipping-data');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshShippingData());
        }
    }

    async getShippingQuote() {
        const origin = document.getElementById('shipping-origin').value;
        const destination = document.getElementById('shipping-destination').value;
        const weight = parseFloat(document.getElementById('shipping-weight').value);
        const volume = parseFloat(document.getElementById('shipping-volume').value);
        const serviceType = document.getElementById('shipping-service').value;

        if (!origin || !destination || !weight || !volume || !serviceType) {
            this.showNotification('Please fill in all shipping details', 'warning');
            return;
        }

        this.showLoading('Getting revolutionary shipping quote...');

        try {
            const response = await fetch(`${this.apiBase}/shipping-quote?origin=${origin}&destination=${destination}&weight_kg=${weight}&volume_cm3=${volume}&service_type=${serviceType}`);
            const data = await response.json();

            if (data.status === 'success') {
                this.currentQuote = data.data;
                this.displayShippingQuote(data.data);
                this.showNotification('Shipping quote generated with volume bidding advantages!', 'success');
            } else {
                throw new Error(data.message || 'Failed to get shipping quote');
            }
        } catch (error) {
            console.error('Error getting shipping quote:', error);
            this.showNotification('Error generating shipping quote: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayShippingQuote(quote) {
        const resultsContainer = document.getElementById('shipping-quote-results');
        if (!resultsContainer) return;

        const html = `
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">🚢 Revolutionary Shipping Quote</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>📦 Shipment Details</h6>
                            <p><strong>Route:</strong> ${quote.origin} → ${quote.destination}</p>
                            <p><strong>Weight:</strong> ${quote.weight_kg} kg</p>
                            <p><strong>Volume:</strong> ${quote.volume_cm3} cm³</p>
                            <p><strong>Service:</strong> ${quote.service_type.toUpperCase()}</p>
                            <p><strong>Volume Savings:</strong> <span class="text-success">$${quote.volume_advantage_savings}</span></p>
                        </div>
                        <div class="col-md-6">
                            <h6>💰 Transparency Breakdown</h6>
                            <p><strong>Total Savings:</strong> ${quote.transparency_breakdown.total_consumer_savings}</p>
                            <p><strong>Average Rate (No Volume):</strong> $${quote.transparency_breakdown.average_rate_without_volume}</p>
                            <p><strong>Average Rate (With Volume):</strong> $${quote.transparency_breakdown.average_rate_with_volume}</p>
                            <p><strong>Savings Percentage:</strong> <span class="text-success">${quote.transparency_breakdown.savings_percentage}%</span></p>
                        </div>
                    </div>

                    <h6 class="mt-4">🏆 Top 3 Carriers (Volume Bidding Results)</h6>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Carrier</th>
                                    <th>Rate</th>
                                    <th>Delivery</th>
                                    <th>Reliability</th>
                                    <th>Sustainability</th>
                                    <th>Volume Discount</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${quote.top_3_carriers.map(carrier => `
                                    <tr>
                                        <td><span class="badge bg-primary">${carrier.rank}</span></td>
                                        <td><strong>${carrier.carrier_name}</strong></td>
                                        <td>$${carrier.final_rate_usd}</td>
                                        <td>${carrier.delivery_days} days</td>
                                        <td>${(carrier.reliability_score * 100).toFixed(1)}%</td>
                                        <td>${(carrier.sustainability_score * 100).toFixed(1)}%</td>
                                        <td><span class="text-success">${carrier.volume_discount_percentage}%</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>

                    <div class="row mt-4">
                        <div class="col-md-6">
                            <h6>🌱 Sustainability Ranking</h6>
                            <div class="list-group">
                                ${quote.sustainability_ranking.slice(0, 5).map((carrier, index) => `
                                    <div class="list-group-item">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <strong>${index + 1}. ${carrier.carrier}</strong>
                                                <br><small>${carrier.service_type}</small>
                                            </div>
                                            <div class="text-end">
                                                <span class="badge bg-success">${(carrier.sustainability_score * 100).toFixed(1)}%</span>
                                                <br><small>${carrier.carbon_footprint_kg} kg CO₂</small>
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6>📋 Delivery Options</h6>
                            <div class="list-group">
                                ${quote.delivery_options.slice(0, 5).map(option => `
                                    <div class="list-group-item">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <strong>${option.service_type.toUpperCase()}</strong>
                                                <br><small>${option.carrier}</small>
                                            </div>
                                            <div class="text-end">
                                                <strong>$${option.rate_usd}</strong>
                                                <br><small>${option.delivery_days} days</small>
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <div class="mt-4">
                        <h6>💡 Transparency Insights</h6>
                        <div class="alert alert-info">
                            <ul class="mb-0">
                                ${quote.transparency_breakdown.transparency_insights.map(insight => `
                                    <li>${insight}</li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsContainer.innerHTML = html;
        this.createShippingCharts(quote);
    }

    async getDailyVolumeBidding() {
        const origin = document.getElementById('bidding-origin').value;
        const destination = document.getElementById('bidding-destination').value;

        if (!origin || !destination) {
            this.showNotification('Please select origin and destination continents', 'warning');
            return;
        }

        this.showLoading('Aggregating daily volume for competitive bidding...');

        try {
            const response = await fetch(`${this.apiBase}/daily-volume-bidding?origin_continent=${origin}&destination_continent=${destination}`);
            const data = await response.json();

            if (data.status === 'success') {
                this.currentBidding = data.data;
                this.displayDailyVolumeBidding(data.data);
                this.showNotification('Daily volume bidding results generated!', 'success');
            } else {
                throw new Error(data.message || 'Failed to get volume bidding');
            }
        } catch (error) {
            console.error('Error getting volume bidding:', error);
            this.showNotification('Error getting volume bidding: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayDailyVolumeBidding(bidding) {
        const resultsContainer = document.getElementById('daily-volume-bidding-results');
        if (!resultsContainer) return;

        const html = `
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">📦 Daily Volume Bidding Results</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>📊 Volume Aggregation</h6>
                            <p><strong>Route:</strong> ${bidding.origin_continent} → ${bidding.destination_continent}</p>
                            <p><strong>Total Weight:</strong> ${bidding.total_weight_kg.toLocaleString()} kg</p>
                            <p><strong>Total Volume:</strong> ${bidding.total_volume_cm3.toLocaleString()} cm³</p>
                            <p><strong>Total Packages:</strong> ${bidding.total_packages.toLocaleString()}</p>
                            <p><strong>Average Package Weight:</strong> ${bidding.average_package_weight.toFixed(2)} kg</p>
                        </div>
                        <div class="col-md-6">
                            <h6>🏆 Competitive Bidding</h6>
                            <p><strong>Carrier Bids:</strong> ${bidding.carrier_bids_count}</p>
                            <p><strong>Best Bids Selected:</strong> ${bidding.best_bids.length}</p>
                            <p><strong>Date:</strong> ${new Date(bidding.date).toLocaleDateString()}</p>
                            <p><strong>Bidding Status:</strong> <span class="badge bg-success">Active</span></p>
                        </div>
                    </div>

                    <h6 class="mt-4">🏆 Best Carrier Bids (Consumer Value)</h6>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Carrier</th>
                                    <th>Service</th>
                                    <th>Base Rate</th>
                                    <th>Volume Discount</th>
                                    <th>Final Rate</th>
                                    <th>Delivery</th>
                                    <th>Reliability</th>
                                    <th>Sustainability</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${bidding.best_bids.slice(0, 10).map(bid => `
                                    <tr>
                                        <td><strong>${bid.carrier}</strong></td>
                                        <td>${bid.service_type}</td>
                                        <td>$${bid.base_rate_usd}</td>
                                        <td><span class="text-success">${bid.volume_discount_percentage}%</span></td>
                                        <td><strong>$${bid.final_rate_usd}</strong></td>
                                        <td>${bid.delivery_days} days</td>
                                        <td>${(bid.reliability_score * 100).toFixed(1)}%</td>
                                        <td>${(bid.sustainability_score * 100).toFixed(1)}%</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>

                    <div class="mt-4">
                        <h6>💡 Bidding Insights</h6>
                        <div class="alert alert-success">
                            <ul class="mb-0">
                                ${bidding.bidding_insights.map(insight => `
                                    <li>${insight}</li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>

                    <div class="row mt-4">
                        <div class="col-md-6">
                            <h6>📋 Shipping Requirements</h6>
                            <div class="list-group">
                                ${Object.entries(bidding.shipping_requirements).map(([service, count]) => `
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <span>${service.replace('_', ' ').toUpperCase()}</span>
                                        <span class="badge bg-primary rounded-pill">${count}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <canvas id="volumeBiddingChart" width="400" height="200"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsContainer.innerHTML = html;
        this.createVolumeBiddingChart(bidding);
    }

    async getCarrierComparison() {
        const origin = document.getElementById('comparison-origin').value;
        const destination = document.getElementById('comparison-destination').value;
        const weight = parseFloat(document.getElementById('comparison-weight').value);
        const volume = parseFloat(document.getElementById('comparison-volume').value);

        if (!origin || !destination || !weight || !volume) {
            this.showNotification('Please fill in all comparison details', 'warning');
            return;
        }

        this.showLoading('Comparing all carriers for best value...');

        try {
            const response = await fetch(`${this.apiBase}/carrier-comparison?origin=${origin}&destination=${destination}&weight_kg=${weight}&volume_cm3=${volume}`);
            const data = await response.json();

            if (data.status === 'success') {
                this.displayCarrierComparison(data.data);
                this.showNotification('Carrier comparison completed!', 'success');
            } else {
                throw new Error(data.message || 'Failed to compare carriers');
            }
        } catch (error) {
            console.error('Error comparing carriers:', error);
            this.showNotification('Error comparing carriers: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayCarrierComparison(comparison) {
        const resultsContainer = document.getElementById('carrier-comparison-results');
        if (!resultsContainer) return;

        const html = `
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">🏆 Carrier Comparison Results</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>📦 Comparison Details</h6>
                            <p><strong>Route:</strong> ${comparison.origin} → ${comparison.destination}</p>
                            <p><strong>Weight:</strong> ${comparison.weight_kg} kg</p>
                            <p><strong>Volume:</strong> ${comparison.volume_cm3} cm³</p>
                            <p><strong>Carriers Compared:</strong> ${comparison.total_carriers_compared}</p>
                            <p><strong>Total Quotes:</strong> ${comparison.total_quotes_generated}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>📊 Summary Metrics</h6>
                            <p><strong>Best Value Carrier:</strong> ${comparison.carrier_summary[0]?.carrier_name || 'N/A'}</p>
                            <p><strong>Average Rate:</strong> $${comparison.carrier_summary[0]?.average_rate_usd || 'N/A'}</p>
                            <p><strong>Best Reliability:</strong> ${(comparison.carrier_summary[0]?.average_reliability * 100 || 0).toFixed(1)}%</p>
                            <p><strong>Best Sustainability:</strong> ${(comparison.carrier_summary[0]?.average_sustainability * 100 || 0).toFixed(1)}%</p>
                        </div>
                    </div>

                    <h6 class="mt-4">🏆 Carrier Summary (Ranked by Value)</h6>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Carrier</th>
                                    <th>Services</th>
                                    <th>Avg Rate</th>
                                    <th>Avg Delivery</th>
                                    <th>Reliability</th>
                                    <th>Sustainability</th>
                                    <th>Volume Discount</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${comparison.carrier_summary.map((carrier, index) => `
                                    <tr>
                                        <td><span class="badge bg-primary">${index + 1}</span></td>
                                        <td><strong>${carrier.carrier_name}</strong></td>
                                        <td>${carrier.services_offered}</td>
                                        <td>$${carrier.average_rate_usd}</td>
                                        <td>${carrier.average_delivery_days} days</td>
                                        <td>${(carrier.average_reliability * 100).toFixed(1)}%</td>
                                        <td>${(carrier.average_sustainability * 100).toFixed(1)}%</td>
                                        <td><span class="text-success">${carrier.total_volume_discount}%</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>

                    <div class="mt-4">
                        <h6>💡 Comparison Insights</h6>
                        <div class="alert alert-info">
                            <ul class="mb-0">
                                ${comparison.comparison_insights.map(insight => `
                                    <li>${insight}</li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsContainer.innerHTML = html;
        this.createCarrierComparisonChart(comparison);
    }

    async getShippingTransparency() {
        const origin = document.getElementById('transparency-origin').value;
        const destination = document.getElementById('transparency-destination').value;
        const weight = parseFloat(document.getElementById('transparency-weight').value);
        const volume = parseFloat(document.getElementById('transparency-volume').value);

        if (!origin || !destination || !weight || !volume) {
            this.showNotification('Please fill in all transparency details', 'warning');
            return;
        }

        this.showLoading('Generating complete shipping transparency report...');

        try {
            const response = await fetch(`${this.apiBase}/shipping-transparency?origin=${origin}&destination=${destination}&weight_kg=${weight}&volume_cm3=${volume}`);
            const data = await response.json();

            if (data.status === 'success') {
                this.displayShippingTransparency(data.data);
                this.showNotification('Shipping transparency report generated!', 'success');
            } else {
                throw new Error(data.message || 'Failed to generate transparency report');
            }
        } catch (error) {
            console.error('Error generating transparency report:', error);
            this.showNotification('Error generating transparency report: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayShippingTransparency(transparency) {
        const resultsContainer = document.getElementById('shipping-transparency-results');
        if (!resultsContainer) return;

        const html = `
            <div class="card">
                <div class="card-header bg-warning text-dark">
                    <h5 class="mb-0">🔍 Complete Shipping Transparency Report</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>📦 Transparency Metrics</h6>
                            <p><strong>Route:</strong> ${transparency.origin} → ${transparency.destination}</p>
                            <p><strong>Total Volume Savings:</strong> <span class="text-success">$${transparency.total_volume_savings}</span></p>
                            <p><strong>Average Transparency Score:</strong> ${(transparency.average_transparency_score * 100).toFixed(1)}%</p>
                            <p><strong>Transparency Level:</strong> <span class="badge bg-success">Excellent</span></p>
                        </div>
                        <div class="col-md-6">
                            <h6>💰 Cost Breakdown Analysis</h6>
                            <div class="list-group">
                                ${Object.entries(transparency.cost_breakdown_analysis).map(([cost, description]) => `
                                    <div class="list-group-item">
                                        <strong>${cost.replace('_', ' ').toUpperCase()}:</strong> ${description}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <h6 class="mt-4">📊 Transparency Rankings</h6>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Service</th>
                                    <th>Carrier</th>
                                    <th>Final Rate</th>
                                    <th>Volume Discount</th>
                                    <th>Reliability</th>
                                    <th>Sustainability</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${transparency.transparency_rankings.slice(0, 10).map(ranking => `
                                    <tr>
                                        <td>${ranking.service_type.toUpperCase()}</td>
                                        <td><strong>${ranking.carrier_name}</strong></td>
                                        <td>$${ranking.final_rate_usd}</td>
                                        <td><span class="text-success">${ranking.volume_discount_percentage}%</span></td>
                                        <td>${(ranking.reliability_score * 100).toFixed(1)}%</td>
                                        <td>${(ranking.sustainability_score * 100).toFixed(1)}%</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>

                    <div class="row mt-4">
                        <div class="col-md-6">
                            <h6>💡 Transparency Insights</h6>
                            <div class="alert alert-warning">
                                <ul class="mb-0">
                                    ${transparency.transparency_insights.map(insight => `
                                        <li>${insight}</li>
                                    `).join('')}
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6>🎯 Consumer Empowerment</h6>
                            <div class="alert alert-success">
                                <ul class="mb-0">
                                    ${transparency.consumer_empowerment.map(empowerment => `
                                        <li>${empowerment}</li>
                                    `).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsContainer.innerHTML = html;
    }

    async getSustainabilityComparison() {
        const origin = document.getElementById('sustainability-origin').value;
        const destination = document.getElementById('sustainability-destination').value;
        const weight = parseFloat(document.getElementById('sustainability-weight').value);
        const volume = parseFloat(document.getElementById('sustainability-volume').value);

        if (!origin || !destination || !weight || !volume) {
            this.showNotification('Please fill in all sustainability details', 'warning');
            return;
        }

        this.showLoading('Comparing carriers for sustainability...');

        try {
            const response = await fetch(`${this.apiBase}/sustainability-comparison?origin=${origin}&destination=${destination}&weight_kg=${weight}&volume_cm3=${volume}`);
            const data = await response.json();

            if (data.status === 'success') {
                this.displaySustainabilityComparison(data.data);
                this.showNotification('Sustainability comparison completed!', 'success');
            } else {
                throw new Error(data.message || 'Failed to compare sustainability');
            }
        } catch (error) {
            console.error('Error comparing sustainability:', error);
            this.showNotification('Error comparing sustainability: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displaySustainabilityComparison(sustainability) {
        const resultsContainer = document.getElementById('sustainability-comparison-results');
        if (!resultsContainer) return;

        const html = `
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">🌱 Sustainability Comparison Results</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>📊 Overall Sustainability Metrics</h6>
                            <p><strong>Route:</strong> ${sustainability.origin} → ${sustainability.destination}</p>
                            <p><strong>Average Sustainability Score:</strong> ${(sustainability.overall_sustainability_metrics.average_sustainability_score * 100).toFixed(1)}%</p>
                            <p><strong>Average Carbon Footprint:</strong> ${sustainability.overall_sustainability_metrics.average_carbon_footprint_kg} kg CO₂</p>
                            <p><strong>Average Renewable Energy:</strong> ${sustainability.overall_sustainability_metrics.average_renewable_energy_usage}%</p>
                            <p><strong>Carriers Analyzed:</strong> ${sustainability.overall_sustainability_metrics.total_carriers_analyzed}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>🏆 Top Sustainable Carriers</h6>
                            <div class="list-group">
                                ${sustainability.carrier_sustainability_ranking.slice(0, 5).map((carrier, index) => `
                                    <div class="list-group-item">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <strong>${index + 1}. ${carrier.carrier_name}</strong>
                                                <br><small>${carrier.services_analyzed} services analyzed</small>
                                            </div>
                                            <div class="text-end">
                                                <span class="badge bg-success">${(carrier.average_sustainability_score * 100).toFixed(1)}%</span>
                                                <br><small>${carrier.average_carbon_footprint} kg CO₂</small>
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>

                    <h6 class="mt-4">🌍 Environmental Impact Analysis</h6>
                    <div class="row">
                        <div class="col-md-6">
                            <h6>📊 Carbon Footprint Ranges</h6>
                            <div class="list-group">
                                ${Object.entries(sustainability.environmental_impact_analysis.carbon_footprint_ranges).map(([service, range]) => `
                                    <div class="list-group-item d-flex justify-content-between align-items-center">
                                        <span>${service.toUpperCase()}</span>
                                        <span class="badge bg-info">${range}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <h6>💡 Sustainability Recommendations</h6>
                            <div class="alert alert-success">
                                <ul class="mb-0">
                                    ${sustainability.environmental_impact_analysis.sustainability_recommendations.map(rec => `
                                        <li>${rec}</li>
                                    `).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>

                    <div class="mt-4">
                        <h6>💡 Sustainability Insights</h6>
                        <div class="alert alert-success">
                            <ul class="mb-0">
                                ${sustainability.sustainability_insights.map(insight => `
                                    <li>${insight}</li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;

        resultsContainer.innerHTML = html;
        this.createSustainabilityChart(sustainability);
    }

    async loadAvailableCarriers() {
        try {
            const response = await fetch(`${this.apiBase}/available-carriers`);
            const data = await response.json();

            if (data.status === 'success') {
                this.displayAvailableCarriers(data.data);
            }
        } catch (error) {
            console.error('Error loading carriers:', error);
        }
    }

    displayAvailableCarriers(carriersData) {
        const container = document.getElementById('available-carriers-info');
        if (!container) return;

        const html = `
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">🚢 Available Shipping Carriers</h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Total Carriers:</strong> ${carriersData.total_carriers}</p>
                            <p><strong>Continents Covered:</strong> ${carriersData.continents_covered}</p>
                            <p><strong>Service Types:</strong> ${carriersData.service_types.join(', ')}</p>
                        </div>
                        <div class="col-md-6">
                            <div class="list-group">
                                ${carriersData.carriers.slice(0, 5).map(carrier => `
                                    <div class="list-group-item">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <strong>${carrier.name}</strong>
                                                <br><small>${carrier.regions.join(', ')}</small>
                                            </div>
                                            <div class="text-end">
                                                <span class="badge bg-success">${(carrier.reliability_score * 100).toFixed(0)}%</span>
                                                <br><small>${(carrier.sustainability_score * 100).toFixed(0)}% eco</small>
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    async loadGlobalInsights() {
        try {
            const response = await fetch(`${this.apiBase}/global-shipping-insights`);
            const data = await response.json();

            if (data.status === 'success') {
                this.displayGlobalInsights(data.data);
            }
        } catch (error) {
            console.error('Error loading global insights:', error);
        }
    }

    displayGlobalInsights(insights) {
        const container = document.getElementById('global-shipping-insights');
        if (!container) return;

        const html = `
            <div class="card">
                <div class="card-header">
                    <h6 class="mb-0">📊 Global Shipping Market Insights</h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6>📈 Market Overview</h6>
                            <p><strong>Daily Volume:</strong> ${insights.market_overview.total_daily_volume_kg.toLocaleString()} kg</p>
                            <p><strong>Daily Packages:</strong> ${insights.market_overview.total_daily_packages.toLocaleString()}</p>
                            <p><strong>Average Cost:</strong> $${insights.market_overview.average_shipping_cost_usd}</p>
                            <p><strong>Volume Savings:</strong> ${insights.market_overview.volume_savings_percentage}%</p>
                        </div>
                        <div class="col-md-6">
                            <h6>🏆 Carrier Performance</h6>
                            <p><strong>Most Reliable:</strong> ${insights.carrier_performance.most_reliable}</p>
                            <p><strong>Most Sustainable:</strong> ${insights.carrier_performance.most_sustainable}</p>
                            <p><strong>Best Value:</strong> ${insights.carrier_performance.best_value}</p>
                            <p><strong>Most Competitive:</strong> ${insights.carrier_performance.most_competitive}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    createShippingCharts(quote) {
        // Create charts for shipping quote visualization
        this.createTopCarriersChart(quote.top_3_carriers);
        this.createSustainabilityChart(quote.sustainability_ranking);
    }

    createTopCarriersChart(carriers) {
        const ctx = document.getElementById('topCarriersChart');
        if (!ctx) return;

        if (this.charts.topCarriers) {
            this.charts.topCarriers.destroy();
        }

        this.charts.topCarriers = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: carriers.map(c => c.carrier_name),
                datasets: [{
                    label: 'Final Rate (USD)',
                    data: carriers.map(c => c.final_rate_usd),
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Rate (USD)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Top 3 Carriers - Final Rates'
                    }
                }
            }
        });
    }

    createVolumeBiddingChart(bidding) {
        const ctx = document.getElementById('volumeBiddingChart');
        if (!ctx) return;

        if (this.charts.volumeBidding) {
            this.charts.volumeBidding.destroy();
        }

        const carriers = bidding.best_bids.slice(0, 8).map(bid => bid.carrier);
        const discounts = bidding.best_bids.slice(0, 8).map(bid => bid.volume_discount_percentage);

        this.charts.volumeBidding = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: carriers,
                datasets: [{
                    data: discounts,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Volume Discounts by Carrier'
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createCarrierComparisonChart(comparison) {
        const ctx = document.getElementById('carrierComparisonChart');
        if (!ctx) return;

        if (this.charts.carrierComparison) {
            this.charts.carrierComparison.destroy();
        }

        const carriers = comparison.carrier_summary.slice(0, 8).map(c => c.carrier_name);
        const rates = comparison.carrier_summary.slice(0, 8).map(c => c.average_rate_usd);
        const reliability = comparison.carrier_summary.slice(0, 8).map(c => c.average_reliability * 100);

        this.charts.carrierComparison = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: carriers,
                datasets: [{
                    label: 'Average Rate (USD)',
                    data: rates,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)'
                }, {
                    label: 'Reliability (%)',
                    data: reliability,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Carrier Performance Comparison'
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    createSustainabilityChart(sustainability) {
        const ctx = document.getElementById('sustainabilityChart');
        if (!ctx) return;

        if (this.charts.sustainability) {
            this.charts.sustainability.destroy();
        }

        const carriers = sustainability.carrier_sustainability_ranking.slice(0, 8).map(c => c.carrier_name);
        const scores = sustainability.carrier_sustainability_ranking.slice(0, 8).map(c => c.average_sustainability_score * 100);
        const carbon = sustainability.carrier_sustainability_ranking.slice(0, 8).map(c => c.average_carbon_footprint);

        this.charts.sustainability = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: carriers,
                datasets: [{
                    label: 'Sustainability Score (%)',
                    data: scores,
                    backgroundColor: 'rgba(75, 192, 192, 0.8)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                }, {
                    label: 'Carbon Footprint (kg CO₂)',
                    data: carbon,
                    backgroundColor: 'rgba(255, 159, 64, 0.8)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Sustainability Score (%)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Carbon Footprint (kg CO₂)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Sustainability vs Carbon Footprint'
                    }
                }
            }
        });
    }

    async exportShippingData() {
        if (!this.currentQuote && !this.currentBidding) {
            this.showNotification('No shipping data to export', 'warning');
            return;
        }

        const exportData = {
            timestamp: new Date().toISOString(),
            shipping_quote: this.currentQuote,
            volume_bidding: this.currentBidding
        };

        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `seeker-shipping-data-${new Date().toISOString().split('T')[0]}.json`;
        link.click();

        this.showNotification('Shipping data exported successfully!', 'success');
    }

    async refreshShippingData() {
        this.showLoading('Refreshing shipping data...');
        
        try {
            await this.loadAvailableCarriers();
            await this.loadGlobalInsights();
            this.showNotification('Shipping data refreshed!', 'success');
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showNotification('Error refreshing data: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    showLoading(message) {
        const loadingDiv = document.getElementById('loading-overlay');
        const loadingMessage = document.getElementById('loading-message');
        
        if (loadingDiv && loadingMessage) {
            loadingMessage.textContent = message;
            loadingDiv.style.display = 'flex';
        }
    }

    hideLoading() {
        const loadingDiv = document.getElementById('loading-overlay');
        if (loadingDiv) {
            loadingDiv.style.display = 'none';
        }
    }

    showNotification(message, type = 'info') {
        const notificationDiv = document.createElement('div');
        notificationDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notificationDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        notificationDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notificationDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notificationDiv.parentNode) {
                notificationDiv.parentNode.removeChild(notificationDiv);
            }
        }, 5000);
    }
}

// Initialize Global Shipping Marketplace when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.seekerGlobalShipping = new SEEKERGlobalShipping();
}); 